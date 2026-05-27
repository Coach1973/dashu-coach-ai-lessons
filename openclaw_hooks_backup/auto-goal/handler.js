"use strict";

// OpenClaw Hook：auto-goal
// 用途：偵測教練下任務的訊號，自動注入「執行合約」到 context。
//       讓小龍蝦每次接到任務就知道「什麼叫完成」——不靠模型記得，靠系統強制。
// 事件：message:preprocessed
// 注入：event.context.inject.push({ role:'system', content })
// 依據：特助場景庫117個場景TOP5痛點
// 軍師建立 2026-05-28（對應軍師版 auto_goal_hook.sh）

const fs = require('fs');
const path = require('path');

const PROBE_LOG = path.join(process.env.HOME, '.openclaw', 'logs', 'auto-goal-probe.log');

// === 防禦性多路徑抽取教練訊息文字（與 rule-reminder 相同策略）===
function extractText(event) {
  const c = (event && event.context) || {};
  const cands = [
    event.text,
    c.text, c.content, c.prompt, c.input, c.body, c.userText, c.userMessage, c.transcript,
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

// === 任務關鍵詞偵測 ===
const TASK_PATTERNS = [
  /幫我|請你|幫忙|麻煩你/,
  /你去|去讀|去寫|去建|去修|去查|去跑|去搜|去設|去確認|去測|去執行|去處理|去上傳|去部署|去更新|去刪/,
  /做一個|建一個|寫一個|設一個|建立|新增|產生|輸出|生成/,
  /修改|更新|修正|修復|檢查|確認|驗證|測試一下|跑一下|執行一下/,
  /開始做|繼續做|繼續執行|把.{1,20}做完|把.{1,20}完成|完成.{1,10}任務/,
];

// 排除純閒聊（問答類不注入）
const CHAT_PATTERNS = [
  /^你覺得|^你怎麼|^你認為|^什麼是|^解釋|^告訴我|^說說|^介紹/,
];

// === 執行合約文字 ===
const CONTRACT = `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 執行合約（系統自動注入，任務啟動）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

根據117個場景TOP5痛點，以下是本次任務的完成標準：

✅ 什麼叫「完成」（缺一不算）
  1. 任務實際執行完畢——不只是說「好的」「收到」
  2. 有具體憑證：commit hash / 檔案路徑 / 指令輸出結果
  3. 主動回報：做了什麼＋憑證在哪

⚡ 執行鐵律（對應最高頻失敗模式）
  • 方向清楚→直接執行，不問「要不要做」（#08，最高頻26次）
  • 先確認清楚再行動，不瞎猜（#09，21次）
  • 自問自答驗證後再回答（#03，19次）
  • 解決問題，不只解釋原因（#04，16次）
  • 口頭說完成=零，要有憑證（#05，16次）

🚫 以下行為視為任務失敗
  • 說「完成了」但沒有任何憑證
  • 叫教練自己複製貼上任何東西
  • 遇到障礙只道歉，沒有提出解法
  • 找不到檔案就假裝找到
  • 承諾了沒做到

📋 Session 結束前必做
  更新交接紀錄：做了什麼、憑證、下一步
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;

module.exports = async function handler(event) {
  try {
    const text = extractText(event);

    // probe log：記錄 event 結構（供精準化）
    try {
      const c = (event && event.context) || {};
      fs.appendFileSync(PROBE_LOG, JSON.stringify({
        ts: new Date().toISOString(),
        topKeys: Object.keys(event || {}),
        ctxKeys: Object.keys(c),
        textPreview: text ? text.slice(0, 60) : '(抓不到)'
      }) + '\n');
    } catch (_) {}

    if (!text) return;

    // 排除閒聊
    for (const re of CHAT_PATTERNS) {
      if (re.test(text)) return;
    }

    // 偵測任務訊號
    const isTask = TASK_PATTERNS.some(re => re.test(text));
    if (!isTask) return;

    // 注入執行合約
    if (!event.context) event.context = {};
    if (!Array.isArray(event.context.inject)) event.context.inject = [];
    event.context.inject.push({ role: 'system', content: CONTRACT });

  } catch (e) {
    try { fs.appendFileSync(PROBE_LOG, `[ERROR] ${e.message}\n`); } catch (_) {}
  }
};
