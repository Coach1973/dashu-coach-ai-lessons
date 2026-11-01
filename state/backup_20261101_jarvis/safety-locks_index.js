// ============================================================
// 🔒 Safety Locks 外掛（小龍蝦端三鎖之二，2026-06-11 軍師建立，教練拍板）
//
// 起因：終端機端已有刪檔鎖/截圖鎖（PreToolUse hook），但小龍蝦
//       （OpenClaw gateway）走的是自己的 exec 工具，hook 管不到。
//       本外掛用官方 before_tool_call 把同一套鎖裝到小龍蝦身上。
//
// 通行證跟終端機共用同一個檔案（教練同意一次，兩邊都認）：
//   刪除：~/.openclaw/workspace/state/DELETE_APPROVED（10 分鐘）
//   截圖：~/.openclaw/workspace/state/SCREENSHOT_APPROVED（10 分鐘）
//
// 推送鎖不在此處——git pre-push 是倉庫層的鎖，任何人（含小龍蝦）
// 從那些資料夾 push 都會被攔，天生全覆蓋。
// ============================================================
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const STATE = path.join(os.homedir(), ".openclaw/workspace/state");
const TOKEN_DELETE = path.join(STATE, "DELETE_APPROVED");
const TOKEN_SHOT = path.join(STATE, "SCREENSHOT_APPROVED");
// 📘 FB 鎖（2026-10-30 教練拍板）：上架作品不貼 FB。10/30 凌晨小龍蝦把「hsiuli FB 補發」當成自己的待辦，
// 連開 Chrome 登 FB 失敗又重開，停不下來。教練明說要動 FB 時才 touch 這個通行證（10 分鐘有效）。
const TOKEN_FB = path.join(STATE, "FB_APPROVED");
const FB_RE = /facebook\.com|fb\.com\/|graph\.facebook|business\.facebook|m\.facebook/i;
const FB_ALLOW = /fb_birthday_scraper/;
// 📵 LINE 推播鎖（2026-11-01 案例142）：教練只說「每天提醒我發結繩」，小龍蝦自己寫文案、自己開推播許可，
// 用「大樹教育顧問」官方帳號發了 24 則廣告。分身一律不准開推播許可、不准寫或跑會打 LINE 推播 API 的程式；
// 許可只能由軍師在 Claude 對話裡、教練親口同意後開（line_push_approve.sh 也會再擋一次）。沒有通行證可解。
const LINE_PUSH_RE = /LINE_PUSH_APPROVED|line_push_approve|api\.line\.me\/v2\/bot\/message\/(push|multicast|broadcast|narrowcast)|jiesheng_line_push|jiesheng_daily_push/i;
// 只擋「真的去操作 FB」：開瀏覽器／自動化／打 FB API。網頁裡改某人的 FB 連結只是文字，不擋
const FB_DRIVE = /playwright|puppeteer|chromium|connectOverCDP|remote-debugging|page\.goto|graph\.facebook|business\.facebook|curl[^\n]{0,200}facebook|open\s+-a[^\n]{0,80}facebook/i;
const MAX_AGE_MS = 10 * 60 * 1000;

function tokenValid(p) {
  try {
    const st = fs.statSync(p);
    if (Date.now() - st.mtimeMs <= MAX_AGE_MS) return true;
    fs.unlinkSync(p);
  } catch {}
  return false;
}

// 與終端機 delete_guard.sh 同一套特徵（兩邊必須同步維護）
const DANGER = [
  /\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\b|--recursive)/,
  /\bfind\b.*-delete\b/,
  /\bfind\b.*-exec\s+rm\b/,
  /\bgit\s+clean\b.*-[a-zA-Z]*f/,
  /\brsync\b.*--delete/,
  /\bshred\b/,
];
const SAFE_TARGETS =
  /\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+("|')?(\/tmp\/|\/private\/tmp\/|\$TMPDIR|node_modules\b)/;

// 💸 LK888 收費鎖（試金石案例85，2026-09-26：一句「直接跑下一張」被重跑21次，
// 28張需求出成96張、額度燒光）。花錢的出圖一律要經過 scripts/lk888_guard.py，
// 這裡擋的是「繞過閘門」：直接打 api.lk888.ai 的指令或腳本。
const WORKSPACE = path.join(os.homedir(), ".openclaw/workspace");
const LK888_HOST = /api\.lk888\.ai/i;
const LK888_GUARD = /\blk888_guard\b/;
const SCRIPT_TOKEN = /(?:^|[\s;&|'"(=])((?:~\/|\/|\.{1,2}\/)?[^\s;&|'"()<>]+\.(?:py|mjs|cjs|js|sh))(?=$|[\s;&|'")])/g;

function resolveScripts(cmd, workdir) {
  const cdMatch = cmd.match(/\bcd\s+("([^"]+)"|'([^']+)'|(\S+))\s*(&&|;)/);
  const base = cdMatch ? (cdMatch[2] || cdMatch[3] || cdMatch[4]) : workdir || WORKSPACE;
  const found = new Set();
  for (const m of cmd.matchAll(SCRIPT_TOKEN)) {
    let p = m[1];
    if (p.startsWith("~/")) p = path.join(os.homedir(), p.slice(2));
    const candidates = path.isAbsolute(p) ? [p] : [path.resolve(base, p), path.resolve(WORKSPACE, p)];
    for (const c of candidates) {
      try {
        if (fs.statSync(c).isFile()) { found.add(c); break; }
      } catch {}
    }
  }
  return [...found];
}

// 只擋真的會發出連線的寫法；git commit 訊息、grep、echo 只是提到網址文字，不擋
const NET_CLIENT = /\b(curl|wget|https?ie|http)\b[^|;&\n]*api\.lk888\.ai/i;
const INLINE_CODE = /\b(python3?|node|ruby|perl)\b\s+(-[ce]\b|-\s*<<|<<)/;

function lk888Bypass(cmd, workdir) {
  if (LK888_HOST.test(cmd) && !LK888_GUARD.test(cmd) && (NET_CLIENT.test(cmd) || INLINE_CODE.test(cmd)))
    return "指令本身直接呼叫 api.lk888.ai";
  for (const f of resolveScripts(cmd, workdir)) {
    try {
      if (fs.statSync(f).size > 5 * 1024 * 1024) continue;
      const src = fs.readFileSync(f, "utf8");
      if (LK888_HOST.test(src) && !LK888_GUARD.test(src)) return `腳本 ${path.basename(f)} 直接呼叫 api.lk888.ai`;
    } catch {}
  }
  return null;
}

// 📚 紀錄檔覆寫鎖（案例85：小龍蝦只讀前50行就整份寫回，試金石案例庫3906行變109行；
// 案例83 HEARTBEAT.md 被灌爆是同一類）。工作區裡的大型 .md 紀錄檔只准局部編輯或附加。
const SHRINK_MIN_BYTES = 10 * 1024;
function overwriteShrink(p, content) {
  if (typeof p !== "string" || typeof content !== "string") return null;
  const abs = p.startsWith("~/") ? path.join(os.homedir(), p.slice(2)) : path.resolve(WORKSPACE, p);
  if (!abs.startsWith(WORKSPACE + path.sep) || !abs.endsWith(".md")) return null;
  try {
    const before = fs.statSync(abs).size;
    const after = Buffer.byteLength(content, "utf8");
    if (before >= SHRINK_MIN_BYTES && after < before / 2) return { abs, before, after };
  } catch {}
  return null;
}

// 🧠 長期記憶上限鎖（2026-10-30 教練拍板）：分身開機每個檔只讀 2 萬字，超過中間被截掉。
// 巴哈 MEMORY.md 10/21 整理到 2 萬內，9 天又長到 28,858 字。寫入後會超過上限就擋，叫它把新記錄寫進當天日記。
const MEMORY_CAP = 20000;
const MEMORY_WRITE_RE = /(?:>>?|\btee\b(?:\s+-a)?|\bsed\s+-i)[^|;&]*?MEMORY\.md/;
function memoryFile(p, agentId) {
  if (typeof p !== "string" || !/(^|\/)MEMORY\.md$/.test(p)) return null;
  if (p.startsWith("~/")) return path.join(os.homedir(), p.slice(2));
  if (path.isAbsolute(p)) return p;
  const ws = agentId && agentId !== "main" ? path.join(os.homedir(), ".openclaw/agents", agentId) : WORKSPACE;
  return path.resolve(ws, p);
}
function chars(f) { try { return fs.readFileSync(f, "utf8").length; } catch { return 0; } }
export function memoryCapBlock(event, agentId) {
  const p = event.params ?? {};
  let file = null, after = 0;
  if (event.toolName === "write") {
    file = memoryFile(p.path, agentId); after = String(p.content ?? "").length;
  } else if (event.toolName === "edit") {
    file = memoryFile(p.path ?? p.file_path, agentId);
    if (file) after = chars(file) + JSON.stringify(p).length;  // 粗估：現有字數＋這次參數長度
  } else if (event.toolName === "exec") {
    const cmd = String(p.command ?? "");
    if (!MEMORY_WRITE_RE.test(cmd)) return null;
    const m = cmd.match(/[^\s'"<>|;&]*MEMORY\.md/);
    const base = p.workdir || (cmd.match(/^\s*cd\s+([^\s;&]+)/) || [])[1];
    const rel = m ? m[0] : "MEMORY.md";
    file = rel.startsWith("/") || rel.startsWith("~/") || !base ? memoryFile(rel, agentId)
      : path.resolve(base.replace(/^~(?=\/)/, os.homedir()), rel);
    if (file) after = chars(file) + cmd.length;
  }
  if (!file || after <= MEMORY_CAP) return null;
  const today = new Date(Date.now() + 8 * 3600 * 1000).toISOString().slice(0, 10);
  return `🧠🔒 長期記憶上限鎖：${path.basename(path.dirname(file))}/MEMORY.md 寫完會超過 ${MEMORY_CAP} 字（開機讀不完，中間會被截掉）。` +
    `這次的新記錄改寫進 memory/${today}.md（用 >> 附加），不用問教練；MEMORY.md 要整理過期段落，請軍師處理。`;
}

// 🧑‍💼 怡靜分身白名單鎖（2026-10-01 教練交辦）：怡靜是外部夥伴，教練只開放
// 「五個分會查詢／第一分會出席更新」跟「LK888 產業鏈出圖」，不開整台 Mac。
// yijing 分身只能跑下面這幾支固定工具、只能改自己資料夾裡的檔案，其他一律擋。
const SANDBOXED_AGENTS = new Set(["yijing", "yang"]);
const YANG_HOME = path.join(os.homedir(), ".openclaw/agents/yang");
const YIJING_HOME = path.join(os.homedir(), ".openclaw/agents/yijing");
const YIJING_EXEC_ALLOW =
  /^\s*(?:python3|\/usr\/bin\/python3|\/opt\/homebrew\/bin\/python3)\s+(?:~|\/Users\/bymyway)\/\.openclaw\/workspace\/scripts\/(?:team_tool|generate_industry_chain|check_industry_chain_names)\.py(?:\s|$)/;
// 雙引號裡的 $() 和反引號照樣會被執行，所以這幾個字只有單引號裡可以出現
const SHELL_EXPAND = /[`$\\\n\r]/;
const SHELL_CHAIN = /[;&|<>]/;
function unsafeShell(cmd) {
  const noSingle = cmd.replace(/'[^']*'/g, "");
  if (/'/.test(noSingle) || /"/.test(noSingle.replace(/"[^"]*"/g, ""))) return true;
  return SHELL_EXPAND.test(noSingle) || SHELL_CHAIN.test(noSingle.replace(/"[^"]*"/g, ""));
}
const WRITE_TOOLS = new Set(["write", "edit", "apply_patch", "multi_edit"]);

function sandboxBlock(event, agentId) {
  if (agentId === "yang") {
    if (event.toolName === "exec" || event.toolName === "process") return "楊尚儒老師專屬特助目前不開放執行指令（分會資料庫、LK888 都還沒開），這個動作不在允許範圍內。";
    if (WRITE_TOOLS.has(event.toolName)) {
      const target = path.resolve(String(event.params?.path ?? event.params?.file_path ?? "").replace(/^~(?=\/)/, os.homedir()));
      return target.startsWith(YANG_HOME + path.sep) ? null : "楊尚儒老師專屬特助只能修改自己資料夾裡的記憶檔。";
    }
    return null;
  }
  if (event.toolName === "exec") {
    const cmd = String(event.params?.command ?? "");
    const parts = cmd.split(/\s*(?:&&|;|\n)\s*/).filter((x) => x.trim());
    if (parts.length && parts.every((x) => YIJING_EXEC_ALLOW.test(x) && !unsafeShell(x))) return null;
    return "怡靜專屬特助只能使用分會查詢工具（team_tool.py）和產業鏈出圖工具，這個動作不在允許範圍內。";
  }
  if (WRITE_TOOLS.has(event.toolName)) {
    const target = path.resolve(String(event.params?.path ?? event.params?.file_path ?? "").replace(/^~(?=\/)/, os.homedir()));
    if (target.startsWith(YIJING_HOME + path.sep)) return null;
    return "怡靜專屬特助只能修改自己資料夾裡的記憶檔。";
  }
  if (event.toolName === "process") return "怡靜專屬特助不能控制背景程式。";
  return null;
}

// 案例 F 教訓：剝掉 heredoc 與引號內的字面文字再判斷
function stripLiterals(cmd) {
  let s = cmd.replace(
    /<<-?\s*['"]?([A-Za-z_][A-Za-z0-9_]*)['"]?[\s\S]*?\n\1(?=\s|$)/g,
    " HEREDOC ",
  );
  return s.replace(/"[^"]*"/g, '""').replace(/'[^']*'/g, "''");
}


// 🔁 重複防呆鎖（2026-10-12 小龍蝦約瑟布圖事件：同一則訊息＋同一個長指令每 14 秒重複一次、65 次以上）
// 起因：exec 一送出就回「Command still running」，模型下一輪又覺得老闆的問題沒回答，重發訊息、重跑腳本，自己撐起迴圈。
// 做法：機械式擋「短時間內完全相同」的訊息與長工作指令，不靠模型自己記得；重啟閘道後記憶清空是可接受的。
const recent = new Map(); // key -> 最近一次放行的時間（毫秒）
const MSG_WINDOW_MS = 3 * 60 * 1000;     // 完全相同的訊息 3 分鐘內不重發
const EXEC_WINDOW_MS = 10 * 60 * 1000;   // 完全相同的長工作指令 10 分鐘內不重跑
const LONG_EXEC_SECONDS = 120;           // 只管預計跑 2 分鐘以上的指令，查進度用的短指令不受影響

// v1.4（2026-10-12 03:00 第二次迴圈）：模型每輪把指令改幾個字（echo 文字、sleep 秒數），v1.3 的「完全相同」擋不到，
// 10 秒一輪重跑同一支推 GitHub 腳本。改成：200 字以上的指令，跟 5 分鐘內跑過的某一支「行」重疊八成以上就擋。
const SIMILAR_WINDOW_MS = 5 * 60 * 1000;
const SIMILAR_MIN_CHARS = 200;
const SIMILAR_RATIO = 0.8;
const recentExecs = []; // { agentId, lines:Set, t }

function cmdLines(cmd) {
  return new Set(cmd.split("\n").map((l) => l.trim().replace(/\d+/g, "#")).filter((l) => l && !/^echo\b/.test(l)));
}

function similarExecWithin(agentId, cmd) {
  if (cmd.length < SIMILAR_MIN_CHARS) return 0;
  const now = Date.now();
  while (recentExecs.length && now - recentExecs[0].t > SIMILAR_WINDOW_MS) recentExecs.shift();
  const lines = cmdLines(cmd);
  for (const r of recentExecs) {
    if (r.agentId !== agentId || !lines.size || !r.lines.size) continue;
    let common = 0;
    for (const l of lines) if (r.lines.has(l)) common++;
    if (common / Math.max(lines.size, r.lines.size) >= SIMILAR_RATIO) return Math.max(1, Math.round((now - r.t) / 1000));
  }
  recentExecs.push({ agentId, lines, t: now });
  return 0;
}

// ⏱️ 一輪工作上限鎖（v1.7，2026-10-30 巴哈事件：一輪跑 70 分鐘、149 支各不相同的查詢指令，每次都說「現在收尾寫入」卻沒停，
// 中間的話也沒送到群組，教練以為它沒反應）。前面的重複鎖只擋「一樣／八成像」的指令，擋不到這種「一直換題目查」的迴圈。
// 門檻是量過的：小龍蝦正常工作一輪最多 184 次工具（10/30 量 801 輪），所以不限死次數，改成：
//   悶頭鎖：連續 SILENT_LIMIT 次工具都沒對外講話 → 擋一次，要它先送一句進度，送完照常做；
//   收尾鎖：同一輪滿 HARD_MINUTES 分鐘或 HARD_CALLS 次 → 除了送訊息全部擋，逼它直接把結論講出來，這輪就結束。
const SILENT_LIMIT = 30;
const HARD_MINUTES = 30;
const HARD_CALLS = 200;
const turns = new Map(); // runKey -> { start, last, total, silent }

function turnBudgetBlock(event, ctx) {
  const key = ctx?.runId || ctx?.sessionKey || ctx?.agentId;
  if (!key) return null;
  const now = Date.now();
  for (const [k, t] of turns) if (now - t.last > 2 * 60 * 60 * 1000) turns.delete(k);
  let t = turns.get(key);
  if (t && now - t.last > 10 * 60 * 1000) t = null; // 閒置 10 分鐘＝新的一輪（沒有 runId 時靠這條重算）
  if (!t) {
    t = { start: now, last: now, total: 0, silent: 0 };
    turns.set(key, t);
    console.log("[safety-locks] 一輪工作計數開始:", key, "ctx欄位:", Object.keys(ctx ?? {}).join(","));
  }
  t.last = now;
  if (event.toolName === "message" && String(event.params?.action ?? "") === "send") {
    t.silent = 0; // 有對外講話就重新算悶頭次數
    return null;
  }
  t.total++;
  t.silent++;
  const mins = Math.round((now - t.start) / 60000);
  if (mins >= HARD_MINUTES || t.total >= HARD_CALLS) {
    console.log("[safety-locks] ⏱️ 收尾鎖觸發:", key, `${mins}分鐘 ${t.total}次`);
    return (
      `⏱️🔒 收尾鎖：這一輪已經做了 ${mins} 分鐘、用了 ${t.total} 次工具，對方一直在等。` +
      "現在不要再查、不要再呼叫任何工具，直接用文字回覆對方：①已經查到／做好的結論 ②還沒做完的事 ③你預設的下一步（自己選一個合理的，不要叫對方決定）。" +
      "回覆完這一輪就結束，對方下一則訊息會重新開始計算。"
    );
  }
  if (t.silent >= SILENT_LIMIT) {
    t.silent = 0;
    console.log("[safety-locks] ⏱️ 悶頭鎖觸發:", key, `${mins}分鐘 ${t.total}次`);
    return (
      `⏱️🔒 悶頭鎖：你已經連續 ${SILENT_LIMIT} 次工具沒跟對方講話，對方看不到你在做事，會以為你當機。` +
      "這一次的工具沒有執行。請先用 message 工具（action=send）送一句白話進度給對方：做到哪、還差什麼、大約還要多久。" +
      "送完就可以繼續做；如果其實已經查夠了，就直接用文字回覆結論，不要再查。"
    );
  }
  return null;
}

function repeatKey(kind, agentId, ...parts) {
  return `${kind}|${agentId ?? "?"}|${parts.join("|")}`.replace(/\s+/g, " ").slice(0, 600);
}

function repeatedWithin(key, windowMs) {
  const now = Date.now();
  for (const [k, t] of recent) if (now - t > 10 * 60 * 1000) recent.delete(k); // 順手清舊的
  const last = recent.get(key);
  if (last && now - last <= windowMs) return Math.max(1, Math.round((now - last) / 1000));
  recent.set(key, now);
  return 0;
}

export default {
  id: "safety-locks",
  name: "Safety Locks",
  register(api) {
    console.log("[safety-locks] 外掛已註冊 before_tool_call 攔截（v1.7 含LK888收費鎖＋紀錄檔覆寫鎖＋重複防呆鎖＋相似指令鎖＋FB鎖＋LINE推播鎖＋長期記憶上限鎖＋一輪工作上限鎖）");
    api.on(
      "before_tool_call",
      (event, ctx) => {
        console.log("[safety-locks] 偵測工具呼叫:", event.toolName, "agent:", ctx?.agentId ?? "?");
        try {  // 壞了就放行（hook 一律 fail-open）
          const reason = turnBudgetBlock(event, ctx);
          if (reason) return { block: true, blockReason: reason };
        } catch (e) { console.log("[safety-locks] 一輪上限鎖出錯，放行:", e?.message); }
        if (["exec", "browser", "process", "write", "edit", "apply_patch"].includes(event.toolName)) {  // write/edit：10/30 它先把網址寫進 /tmp/*.js 再執行，繞過只看 exec 的版本
          let raw = JSON.stringify(event.params ?? {});
          if (event.toolName === "exec") {  // 已存在的腳本（node /tmp/x.js）也看內容
            for (const f of resolveScripts(String(event.params?.command ?? ""), event.params?.workdir)) {
              try { if (fs.statSync(f).size < 2 * 1024 * 1024) raw += fs.readFileSync(f, "utf8"); } catch {}
            }
          }
          if (LINE_PUSH_RE.test(raw)) {
            return {
              block: true,
              blockReason:
                "📵🔒 LINE 推播鎖（2026-11-01 教練拍板）：分身不能用 LINE 官方帳號主動發訊息給任何人，也不能開推播許可或寫推播程式。" +
                "教練說「提醒我發」＝提醒教練本人，不是替他發。這件不用做也不用問教練，直接用一句話提醒教練本人就好。",
            };
          }
          if (FB_RE.test(raw) && (event.toolName === "browser" || FB_DRIVE.test(raw)) && !FB_ALLOW.test(raw) && !tokenValid(TOKEN_FB)) {
            return {
              block: true,
              blockReason:
                "📘🔒 FB 鎖（2026-10-30 教練拍板）：上架作品一律不貼 FB，也不要去補貼、查貼文、登入臉書。" +
                "這件事不用做，也不用問教練，直接當作已完成，把結果回報給教練就好。",
            };
          }
        }
        if (["write", "edit", "exec"].includes(event.toolName)) {
          const reason = memoryCapBlock(event, ctx?.agentId);
          if (reason) return { block: true, blockReason: reason };
        }
        if (SANDBOXED_AGENTS.has(ctx?.agentId)) {
          const reason = sandboxBlock(event, ctx?.agentId);
          if (reason) return { block: true, blockReason: `🧑‍💼🔒 ${reason}` };
        }
        if (event.toolName === "write") {
          const hit = overwriteShrink(event.params?.path, event.params?.content);
          if (hit && !tokenValid(TOKEN_DELETE)) {
            return {
              block: true,
              blockReason:
                `📚🔒 紀錄檔覆寫鎖（案例85：試金石案例庫被整份覆寫，3906行變109行）：${path.basename(hit.abs)} 現在 ${hit.before} bytes，` +
                `這次寫入只有 ${hit.after} bytes，會把原本一半以上的內容清掉。紀錄檔只能用 edit 局部修改，或用 exec 加 >> 附加在最後面；` +
                "真的要大幅刪減，必須先問教練，教練同意後 touch ~/.openclaw/workspace/state/DELETE_APPROVED（10 分鐘有效）。",
            };
          }
          return;
        }
        if (event.toolName === "message" && String(event.params?.action ?? "") === "send") {
          const text = String(event.params?.message ?? "").trim();
          if (text.length >= 20) {
            const att = JSON.stringify(event.params?.attachments ?? "");
            const secs = repeatedWithin(repeatKey("msg", ctx?.agentId, event.params?.target, text, att), MSG_WINDOW_MS);
            if (secs) {
              return {
                block: true,
                blockReason:
                  `🔁🔒 重複訊息鎖：這則一模一樣的訊息 ${secs} 秒前已經送給同一個人了，沒有再送。` +
                  "不要重發同樣的話；如果是在等工作跑完，就安靜等、用 process poll 看進度，有新結果或新進度再講。",
              };
            }
          }
          return;
        }
        if (event.toolName !== "exec") return;
        const cmd = String(event.params?.command ?? "");
        if (!cmd) return;
        const stripped = stripLiterals(cmd);

        // 🔁 長工作指令重複鎖
        if (Number(event.params?.timeoutSeconds ?? 0) >= LONG_EXEC_SECONDS) {
          const secs = repeatedWithin(repeatKey("exec", ctx?.agentId, cmd), EXEC_WINDOW_MS);
          if (secs) {
            return {
              block: true,
              blockReason:
                `🔁🔒 重複指令鎖：這個一模一樣的長工作 ${secs} 秒前才啟動過，可能還在背景執行，沒有再跑一次。` +
                "請用 process（list / poll / log）看它跑到哪裡，等它自己跑完；不要重新啟動，也不要重發同樣的訊息。",
            };
          }
        }

        // 🔁 相似指令重複鎖（v1.4）
        {
          const secs = similarExecWithin(ctx?.agentId, cmd);
          if (secs) {
            return {
              block: true,
              blockReason:
                `🔁🔒 相似指令鎖：這支指令跟 ${secs} 秒前跑過的那支內容八成相同，沒有再跑。` +
                "回「Command still running」代表它還在背景跑，不是失敗：用 process poll 等它跑完、讀完整結果再決定下一步；" +
                "不要改幾個字重跑，也不要重發同樣的道歉或說明。5 分鐘內真的要換做法，就換一支明顯不同的指令。",
            };
          }
        }

        // 💸 LK888 收費鎖（案例85）
        const bypass = lk888Bypass(cmd, event.params?.workdir);
        if (bypass) {
          return {
            block: true,
            blockReason:
              `💸🔒 LK888收費鎖（案例85：9/26一句話被重跑21次，28張出成96張、額度燒光）：${bypass}，沒有經過收費閘門。` +
              "請改用現成的 scripts/generate_comic_panel.py（漫畫/鎖臉）或 scripts/generate_industry_chain.py（產業鏈）；" +
              "若一定要自己寫腳本，把打 LK888 的 urllib.request.urlopen 換成 lk888_guard.urlopen（import lk888_guard）。" +
              "教練明說重畫才可在指令前加 LK888_REDO=1。",
          };
        }

        // 📷 截圖鎖（案例 4：未經同意截圖）
        if (/\bscreencapture\b/.test(stripped) && !tokenValid(TOKEN_SHOT)) {
          return {
            block: true,
            blockReason:
              "📷🔒 截圖鎖：教練明令未經同意不可截圖。請先問教練；教練同意後執行 touch ~/.openclaw/workspace/state/SCREENSHOT_APPROVED 再重試（10 分鐘有效）。",
          };
        }

        // 🗑️ 刪檔鎖（案例 23：21GB 蒸發）
        if (DANGER.some((re) => re.test(stripped)) && !SAFE_TARGETS.test(cmd)) {
          if (tokenValid(TOKEN_DELETE)) return;
          return {
            block: true,
            blockReason:
              "🗑️🔒 刪檔鎖（案例23，21GB血淚）：珍貴資料只搬不刪；搬移後必須 du -sh 比對一致才能刪源頭。請改用搬到存檔區，或先取得教練同意後執行 touch ~/.openclaw/workspace/state/DELETE_APPROVED 再重試（10 分鐘有效）。",
          };
        }
      },
      { priority: 100 },
    );
  },
};
