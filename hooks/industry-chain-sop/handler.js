"use strict";

// OpenClaw Hook：industry-chain-sop
// 用途：孔大哥（kong）/佩佩老師（peipei）的專屬Telegram群組裡有人說「XX的產業鍊SOP」時，
//       伺服器端代勞整個「MiniMax組prompt → lk888生圖 → 推Telegram」流程，不需要開放
//       exec/runtime工具給kong/peipei的帳號。詳見 HOOK.md。
// 事件：message:preprocessed（跟 bni-reminder-schedule 同一個事件）
// 軍師建立 2026-09-16（教練交辦BNI組隊計畫產業鏈自動生圖，權限鎖死後的伺服器端方案）
//
// 🔴 2026-09-18教練當場糾正：舊版鎖「只認孔大哥/佩佩老師本人Telegram ID」，但兩人的
// AI助理其實是跑在各自專屬Telegram群組裡(kong群組-5083547625/peipei群組-5115910257)，
// 教練本人直接在群組裡下指令時sender是教練的ID不是孔大哥/佩佩老師本人的ID，舊規則悄悄
// 擋掉、hook從未真正觸發過（hook.log從未產生過任何一行）。改成「這個群組本身就是受控
// 私人群組，裡面任何人講都算數」，不再卡死只認本人ID。

const { execFile } = require("child_process");
const fs = require("fs");
const path = require("path");
const https = require("https");

const HOME = process.env.HOME;
const WORKSPACE = path.join(HOME, ".openclaw", "workspace");
const SCRIPT_PATH = path.join(WORKSPACE, "scripts", "generate_industry_chain.py");
const AUTH_PROFILES_PATH = path.join(WORKSPACE, "agent", "auth-profiles.json");
const LOG_PATH = path.join(HOME, ".openclaw", "hooks", "industry-chain-sop", "hook.log");

const ACCOUNT_CONFIG = {
  kong: { allowedGroupId: "-5083547625", telegramAccount: "bot_kong" },
  peipei: { allowedGroupId: "-5115910257", telegramAccount: "bot_peipei" },
};

// 🔴 2026-09-17教練實測發現：舊版只認死板句型「XX的產業鍊SOP」，教練實際說「請執行
// 產業服務鏈SOP對象是企業教練」(用「服務鏈」+主題放在SOP後面)完全對不上，hook沒觸發，
// 訊息被當一般聊天，AI瞎猜著去搜資料夾。改成「寬鬆判斷是否要觸發」+「主題交給MiniMax
// 從整句話判斷」，不要用regex死板抓字，教練想怎麼講都行。
const LOOSE_TRIGGER_RE = /產業(?:服務)?[鍊鏈]\s*SOP/;

function log(line) {
  try {
    fs.appendFileSync(LOG_PATH, `[${new Date().toISOString()}] ${line}\n`);
  } catch (_) {
    // logging must never crash the hook
  }
}

function extractText(event) {
  const c = (event && event.context) || {};
  const cands = [c.bodyForAgent, event.text, c.text, c.content];
  for (const v of cands) if (typeof v === "string" && v.trim()) return v.trim();
  return "";
}

function parseSession(event) {
  const sessionKey = String(event.sessionKey ?? (event.context && event.context.sessionKey) ?? "");
  const parts = sessionKey.split(":");
  const agentIdx = parts.indexOf("agent");
  const accountId = agentIdx >= 0 && parts[agentIdx + 1] ? parts[agentIdx + 1] : null;

  let senderId = String(event.from ?? (event.context && event.context.from) ?? "");
  senderId = senderId.replace(/^telegram:/, "");

  // 群組session的sessionKey長相：agent:kong:telegram:group:-5083547625
  const groupIdx = parts.indexOf("group");
  const groupId = groupIdx >= 0 && parts[groupIdx + 1] ? parts[groupIdx + 1] : null;

  let chatId = String((event.context && event.context.chatId) ?? "");
  chatId = chatId.replace(/^telegram:/, "");

  return { accountId, senderId, groupId, chatId, sessionKey };
}

function getMinimaxKey() {
  const data = JSON.parse(fs.readFileSync(AUTH_PROFILES_PATH, "utf-8"));
  return data.profiles["minimax:default"].key;
}

// 🔴 2026-09-17改版：舊版要求呼叫端自己用regex從句子裡精準抓出topic再傳進來，句型一變就抓空。
// 改成把使用者「原始整句話」直接交給MiniMax，主題判斷跟prompt生成一次做完——LLM本來就比regex
// 更擅長處理「主題放前面/放後面/换句話說」這類自然語言變化，不用再窮舉句型规则。
function askMinimaxForPrompt(rawText) {
  return new Promise((resolve, reject) => {
    const apiKey = getMinimaxKey();
    const instruction = `使用者傳來這句話：「${rawText}」，他想做一張「產業服務鏈」的圖片生成prompt。

請照以下格式回答，不要有其他文字、不要markdown：
第一行：TOPIC: <這句話裡真正要做產業服務鏈圖的對象/主題，通常是一個職業、店家名稱或身份，例如「企業教練」「鴻達醬油行」——忽略「請執行」「產業服務鏈SOP」「對象是」這類指令性文字本身，只抓出真正的主題>
第二行開始：完整的中文圖片生成prompt，格式必須完全照這個模板填空：

我需要做一張產業服務鏈，要用手繪可愛風格做出來。中心是「<第一行判斷出的主題>」的插畫。標題：<你想一個貼切的四到八字標題>。為<這個主題的目標客群>提供從<第一項服務>到<最後一項服務>的一條龍支援。周邊環繞以下專業類別節點，每個節點配精緻手繪icon：<列出15~20個跟這個主題異業合作最相關的服務類別，用頓號分隔，不要跟中心主體重複>。所有文字必須完全正確、清晰可讀，不能有亂碼或錯字。`;

    const payload = JSON.stringify({
      model: "MiniMax-M3",
      max_tokens: 1500,
      messages: [{ role: "user", content: instruction }],
    });

    const req = https.request(
      {
        hostname: "api.minimax.io",
        path: "/anthropic/v1/messages",
        method: "POST",
        headers: {
          "x-api-key": apiKey,
          "anthropic-version": "2023-06-01",
          "content-type": "application/json",
          "content-length": Buffer.byteLength(payload),
        },
        timeout: 60000,
      },
      (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          try {
            const parsed = JSON.parse(body);
            const text = parsed?.content?.[0]?.text;
            if (!text) return reject(new Error(`MiniMax回應無文字內容: ${body.slice(0, 300)}`));
            const lines = text.trim().split("\n");
            const topicLineIdx = lines.findIndex((l) => /^TOPIC:/i.test(l.trim()));
            if (topicLineIdx === -1) {
              // MiniMax沒照格式回，退而求其次：整段當prompt，主題用原始話術兜底
              return resolve({ topic: rawText.slice(0, 20), prompt: text.trim() });
            }
            const topic = lines[topicLineIdx].replace(/^TOPIC:\s*/i, "").trim() || rawText.slice(0, 20);
            const prompt = lines.slice(topicLineIdx + 1).join("\n").trim();
            if (!prompt) return reject(new Error(`MiniMax只回了TOPIC沒有prompt本體: ${body.slice(0, 300)}`));
            resolve({ topic, prompt });
          } catch (e) {
            reject(new Error(`MiniMax回應解析失敗: ${e.message}, body=${body.slice(0, 300)}`));
          }
        });
      },
    );
    req.on("error", reject);
    req.on("timeout", () => req.destroy(new Error("MiniMax請求逾時")));
    req.write(payload);
    req.end();
  });
}

function runGenerateScript({ prompt, chatId, telegramAccount, topic }) {
  const args = [
    SCRIPT_PATH,
    "--prompt",
    prompt,
    "--telegram-chat-id",
    chatId,
    "--telegram-account",
    telegramAccount,
    "--caption",
    `${topic}的產業鍊圖`,
  ];
  execFile("python3", args, { timeout: 150000 }, (err, stdout, stderr) => {
    if (err) {
      log(`FAIL generate script topic="${topic}" chatId=${chatId} err=${err.message} stderr=${stderr}`);
    } else {
      log(`OK generate script topic="${topic}" chatId=${chatId} stdout=${stdout.trim()}`);
    }
  });
}

const handler = async (event) => {
  try {
    if (!event || event.type !== "message" || event.action !== "preprocessed") return;

    const parsed = parseSession(event);
    const cfg = parsed.accountId && ACCOUNT_CONFIG[parsed.accountId];
    if (!cfg) return;
    // 群組本身就是受控私人群組（教練+孔大哥/佩佩老師），裡面任何人講都算數，
    // 不再卡死只認孔大哥/佩佩老師本人ID（那個舊規則曾讓教練本人在群組下指令時被悄悄擋掉）。
    if (parsed.groupId !== cfg.allowedGroupId) return;

    const text = extractText(event);
    if (!LOOSE_TRIGGER_RE.test(text)) return;

    log(`TRIGGER accountId=${parsed.accountId} groupId=${parsed.groupId} senderId=${parsed.senderId} rawText="${text.slice(0, 80)}"`);

    let topic, prompt;
    try {
      ({ topic, prompt } = await askMinimaxForPrompt(text));
    } catch (e) {
      log(`FAIL minimax prompt rawText="${text.slice(0, 80)}" err=${e.message}`);
      return;
    }

    log(`PROMPT topic="${topic}" prompt="${prompt.slice(0, 200)}..."`);
    const targetChatId = parsed.chatId || parsed.groupId;
    runGenerateScript({ prompt, chatId: targetChatId, telegramAccount: cfg.telegramAccount, topic });
  } catch (e) {
    log(`ERROR ${e && e.stack ? e.stack : e}`);
  }
};

module.exports = handler;
