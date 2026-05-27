"use strict";

// OpenClaw Hook：rule-reminder
// 用途：小龍蝦跟教練對話時，每則訊息自動偵測關鍵字、注入相關「特助守則」提醒。
//       軍師版（Claude Code）pre_task_hook.sh 的 OpenClaw 對應版本，讓守則對照
//       「不靠模型記得、靠系統強制」。
// 事件：message:preprocessed（照 context-overflow-guard / bot-relay-inbound 模板）
// 注入：event.context.inject.push({ role:'system', content })
// 軍師建立 2026-05-27（教練拍板「讓小龍蝦也用這套嚴謹邏輯」）

const fs = require('fs');
const path = require('path');

const PROBE_LOG = path.join(process.env.HOME, '.openclaw', 'logs', 'rule-reminder-probe.log');

// === 防禦性多路徑抽取教練訊息文字 ===
// OpenClaw minified 源碼未明確暴露當前訊息欄位，故嘗試所有常見路徑；
// 抓不到時 dump 結構到 probe log，供事後精準化。
function extractText(event) {
  const c = (event && event.context) || {};
  const cands = [
    event.text,
    c.text, c.content, c.prompt, c.input, c.transcript, c.userText, c.body, c.userMessage,
    (c.message && (typeof c.message === 'string' ? c.message : (c.message.text || c.message.content))),
  ];
  const pickLast = (arr) => {
    if (Array.isArray(arr) && arr.length) {
      const last = arr[arr.length - 1];
      if (typeof last === 'string') return last;
      if (last && typeof last === 'object') return last.text || last.content || '';
    }
    return '';
  };
  cands.push(pickLast(event.messages));
  cands.push(pickLast(c.messages));
  for (const v of cands) if (typeof v === 'string' && v.trim()) return v;
  return '';
}

// === 偵測：記錄 event 結構（只記 keys + 短樣本，不存完整隱私）===
function probeDump(event, matchedText) {
  try {
    const c = (event && event.context) || {};
    const info = {
      ts: new Date().toISOString(),
      type: event.type,
      action: event.action,
      topKeys: Object.keys(event || {}),
      ctxKeys: Object.keys(c),
      messagesLen: Array.isArray(event.messages) ? event.messages.length : null,
      textPreview: matchedText ? String(matchedText).slice(0, 50) : '(抓不到文字)',
    };
    fs.appendFileSync(PROBE_LOG, JSON.stringify(info) + '\n');
  } catch (e) { /* silent */ }
}

// === 關鍵字 → 守則對照（翻譯自 pre_task_hook.sh，依 trigger_index.md）===
const RULES = [
  { re: /就這樣|按這樣|照這樣|算了|不做了|你決定|你看著辦|你覺得呢/, msg: '守則#08（花時間討論就是為了執行）：教練已給方向，直接執行，不再問「要做嗎」。' },
  { re: /做好了|完成了|做完|搞定|弄好了|處理好/, msg: '守則#05（凡走過必留痕跡）：口頭完成不算數，當場 commit + 給 hash 才算。' },
  { re: /對不起|抱歉|有問題|壞了|不行|出錯|錯誤|失敗|沒反應|當機/, msg: '守則#04（解決問題比解釋問題更重要）：先修好，再說原因，別只道歉。' },
  { re: /找不到|搜尋不到|找不著|沒看到|不見了/, msg: '守則#02（錯誤的地圖找不到正確位置）：先問「我是不是找錯方向了？」' },
  { re: /你又問|你又忘|怎麼又|記不住|說過了|講過了|提醒過/, msg: '守則#01（在乎=記住用戶說的話）：馬上記住並寫入 memory，下次不再犯。' },
  { re: /終端機|桌面版|手機|電報|Telegram|VPS|哪台|哪個環境|哪個介面/, msg: '守則#17（用戶環境確認）：先確認哪個介面/設備，終端機≠手機≠VPS。' },
  { re: /就像|好比|比喻|故事|小說|電影|連續劇|武俠|掌門|師兄|師弟|師妹/, msg: '守則#13（顧客的聲音=存在價值）：教練的比喻是線索，記錄並分析背後含義。' },
  { re: /為什麼|為何|原因|目的|意義何在/, msg: '守則#09（知道為什麼才有判斷力）：先確認目的，回到使命/願景/信念判斷。' },
  { re: /上傳|部署|deploy|github|上線|發布/i, msg: '守則#04（交付前驗證）：上線/部署後先用 curl 檢測 HTTP 200，再說「完成」。' },
  { re: /複製|貼上|回傳|幫我貼|拿給我/, msg: '守則#12（拒絕當資訊搬運工）：自己處理，不叫教練複製貼上回傳。' },
  { re: /太複雜|搞不懂|不要那麼麻煩|簡單一點/, msg: '守則#16（複雜的解法不一定正確）：先問「您想要什麼結果？」用最簡單的路徑。' },
];

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'message' || event.action !== 'preprocessed') return;
  if (!event.context || typeof event.context !== 'object') return;

  const text = extractText(event);

  // 抓不到文字：dump 結構供精準化，靜默退出（不壞事）
  if (!text) { probeDump(event, ''); return; }

  const hits = [];
  for (const r of RULES) if (r.re.test(text)) hits.push('• ' + r.msg);

  if (hits.length === 0) return;

  // 命中時記錄一筆，確認 hook 真的有在運作 + 抓到文字
  probeDump(event, text);

  const injection = [
    '🌱 守則提醒（系統自動對照 trigger_index）：',
    ...hits,
    '（對照後再回應教練；引用守則前先查 特助心法.md 原文確認一字不差。）',
  ].join('\n');

  if (!event.context.inject) event.context.inject = [];
  if (Array.isArray(event.context.inject)) {
    event.context.inject.push({ role: 'system', content: injection });
  }
};

module.exports = handler;
module.exports.default = handler;
