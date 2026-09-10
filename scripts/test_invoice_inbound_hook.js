#!/usr/bin/env node
"use strict";
// invoice-inbound hook 驗證腳本（教練 2026-08-24 交辦「全面檢查」時建立）
// 用教練 2026-08-18~08-24 的真實訊息當測資，確認不會漏抓、也不會亂抓。
// 執行：INVOICE_HOOK_TEST=1 node scripts/test_invoice_inbound_hook.js
// 設 INVOICE_HOOK_TEST=1 時 hook 不會真的發 Telegram，不會騷擾教練。

process.env.INVOICE_HOOK_TEST = '1';

const fs = require('fs');
const path = require('path');
const os = require('os');

const INBOX_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'state', 'invoice_inbox');
const handler = require(path.join(os.homedir(), '.openclaw', 'hooks', 'invoice-inbound', 'handler.js'));

// [訊息, 應該落地嗎, 期待撈到的姓名（子集比對）]
const CASES = [
  ['杜亞洛 要給您開培訓發票\n三聯式發票資訊：公司抬頭：宿易智能有限公司 / 統一編號：89163511\n\n劉彥彬 /VPGYN9U',
    true, ['杜亞洛', '劉彥彬']],
  ['玫萱  /1.IXOIR\n陳新典 /92HFLDY\n\n只要是給手機條碼的一律是二聯，以後都不用再問',
    true, ['玫萱', '陳新典']],
  ['這是發票的手機載具\n/.70FYL2 林佳慧', true, ['林佳慧']],
  // 🔴 這則是 2026-08-20 真正掉掉的那筆：全文零個發票關鍵字，只有姓名+載具
  ['連皓宇 /88ZMR73\n陳新典 /92HFLDY\n玫萱 /1.IXOIR\n吳三貴 /2J9BX2D',
    true, ['連皓宇', '陳新典', '玫萱', '吳三貴']],
  ['伍芬群 三聯 朽木室內裝修有限公司 統編94312414', true, ['伍芬群']],
  ['今天天氣真好，我們來聊聊發票制度', false, []],
  ['請幫我訂高鐵票 0912345678 12345678', false, []],
  ['幫我看一下報名人數', false, []],
];

async function main() {
  const before = new Set(fs.existsSync(INBOX_DIR) ? fs.readdirSync(INBOX_DIR) : []);
  const marker = Date.now();
  let pass = 0, fail = 0;

  for (const [i, [text, shouldLand, expectNames]] of CASES.entries()) {
    const countBefore = countEntries();
    await handler({
      type: 'message', action: 'preprocessed',
      context: { body: text, senderId: 'telegram:6124913915', channelId: 'telegram' },
      sessionKey: 'agent:main:telegram:6124913915',
    });
    const entries = readEntries();
    const landed = entries.length > countBefore;
    const latest = landed ? entries[entries.length - 1] : null;

    let ok = landed === shouldLand;
    let detail = '';
    if (ok && shouldLand) {
      const missing = expectNames.filter((n) => !latest.names.includes(n));
      const junk = latest.names.filter((n) => !expectNames.includes(n));
      if (missing.length) { ok = false; detail += ` 漏抓姓名=${missing.join(',')}`; }
      if (junk.length) { detail += ` ⚠️多抓=${junk.join(',')}`; }
      detail += ` 載具=${latest.carriers.join(' ') || '-'} 統編=${latest.taxIds.join(' ') || '-'} 類型=${latest.type || '-'}`;
    }
    console.log(`${ok ? '✅' : '❌'} case ${i}: 落地=${landed}(期待${shouldLand})${detail}`);
    ok ? pass++ : fail++;
  }

  // 🔴 2026-09-06教練回報連兩則誤報後新增：心跳健檢(channel/chatId='heartbeat')
  // 把HEARTBEAT.md全文當context灌進來，其中「timeout/INVALID_API_KEY/網路類錯誤
  // 需自動調參」這句系統狀態說明文字，恰好符合手機發票條碼格式(斜線+7碼英數)，
  // 之前會被誤判成真的發票資訊寫進log+發Telegram騷擾教練。
  {
    const countBefore = countEntries();
    await handler({
      type: 'message', action: 'preprocessed',
      context: {
        body: 'Read HEARTBEAT.md if it exists (workspace context). Follow it strictly.\n自動修復動作： 無（無 timeout/INVALID_API_KEY/網路類錯誤需自動調參）',
        senderId: 'heartbeat', channelId: 'heartbeat',
      },
      sessionKey: 'agent:main:main',
    });
    const landed = countEntries() > countBefore;
    console.log(`${landed ? '❌' : '✅'} case heartbeat: 落地=${landed}(期待false，心跳訊息不該被當發票)`);
    landed ? fail++ : pass++;
  }

  // 🔴🔴 2026-09-10第二次發作：心跳事件從9/9晚上起不再標示channel/chatId='heartbeat'，
  // 改成偽裝成channel='telegram'/chatId=教練本人真實ID(6124913915)，讓9/6那次靠channel
  // 字串比對的排除邏輯完全失效——連續14次(9/9 23:07~9/10 03:36)把HEARTBEAT.md內文
  // 誤存成假發票+發靜音通知，教練半夜收到亂碼訊息才發現。修復改成直接偵測心跳prompt
  // 文字本身的固定開頭，不依賴容易被系統版本改變格式的channel/chatId間接欄位。
  {
    const countBefore = countEntries();
    await handler({
      type: 'message', action: 'preprocessed',
      context: {
        body: 'Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.\n自動修復動作： 無（無 timeout/INVALID_API_KEY/網路類錯誤需自動調參）',
        senderId: '6124913915', channelId: undefined,
      },
      sessionKey: 'agent:main:main',
    });
    const landed = countEntries() > countBefore;
    console.log(`${landed ? '❌' : '✅'} case heartbeat-disguised-as-telegram: 落地=${landed}(期待false，即使channel偽裝成telegram+教練真實ID也不該被當發票)`);
    landed ? fail++ : pass++;
  }

  console.log(`\n結果：${pass} 通過 / ${fail} 失敗（共 ${CASES.length + 2}）`);
  process.exit(fail === 0 ? 0 : 1);
}

function monthFilePath() {
  const d = new Date();
  const local = new Date(d.getTime() + (8 * 60 + d.getTimezoneOffset()) * 60000);
  return path.join(INBOX_DIR, `${local.getFullYear()}-${String(local.getMonth() + 1).padStart(2, '0')}.jsonl`);
}
function readEntries() {
  const f = monthFilePath();
  if (!fs.existsSync(f)) return [];
  return fs.readFileSync(f, 'utf-8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));
}
function countEntries() { return readEntries().length; }

main();
