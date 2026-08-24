#!/usr/bin/env node
"use strict";
// group-activity-memory hook 驗證腳本（教練 2026-08-24 交辦「活動討論群要記住每件事」時建立）
// 執行：node scripts/test_group_activity_memory_hook.js
// 用真實群組訊息格式測試：①一般發言會落地 ②非追蹤群組不會落地 ③彙整關鍵字會觸發完整注入

const fs = require('fs');
const path = require('path');
const os = require('os');

const MEMORY_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'group_memory');
const TEST_FILE = path.join(MEMORY_DIR, '活動討論群.md');
const handler = require(path.join(os.homedir(), '.openclaw', 'hooks', 'group-activity-memory', 'handler.js'));

function makeEvent(rawText, chatId) {
  const ctx = { body: rawText, senderId: `telegram:group:${chatId}`, channelId: 'telegram' };
  return { type: 'message', action: 'preprocessed', context: ctx, sessionKey: 'agent:main:telegram:group' + chatId };
}

async function main() {
  // 乾淨開始：備份既有檔案（如果有）再測試，測完會還原，不動教練真實記憶
  const hadExisting = fs.existsSync(TEST_FILE);
  const backup = hadExisting ? fs.readFileSync(TEST_FILE, 'utf8') : null;
  if (hadExisting) fs.unlinkSync(TEST_FILE);

  let pass = 0, fail = 0;
  const check = (label, cond) => { console.log(`${cond ? '✅' : '❌'} ${label}`); cond ? pass++ : fail++; };

  // ① 一般發言會落地
  await handler(makeEvent(
    '[Telegram 活動討論群 id:-1003537129853 Mon 2026-08-24 13:06:47 GMT+8] coach (6124913915): 這次活動要找的攤販：手工皂、咖啡、乾燥花',
    '-1003537129853'
  ));
  let content = fs.existsSync(TEST_FILE) ? fs.readFileSync(TEST_FILE, 'utf8') : '';
  check('第一則發言已落地', content.includes('手工皂、咖啡、乾燥花'));
  check('寄件人有記錄', content.includes('coach'));

  // ② 非追蹤群組不會落地（用另一個chat_id）
  const before = content;
  await handler(makeEvent(
    '[Telegram 隨便一個別的群 id:-9999999 Mon 2026-08-24 13:07:00 GMT+8] someone (111): 這句不該被記錄',
    '-9999999'
  ));
  content = fs.readFileSync(TEST_FILE, 'utf8');
  check('非追蹤群組不會寫入活動討論群檔案', content === before && !content.includes('這句不該被記錄'));

  // ③ 再加一則，累積內容
  await handler(makeEvent(
    '[Telegram 活動討論群 id:-1003537129853 +1m Mon 2026-08-24 13:08:05 GMT+8] 佩君 老師 (8786886419): 好點子：現場加一個AI體驗攤位',
    '-1003537129853'
  ));
  content = fs.readFileSync(TEST_FILE, 'utf8');
  check('第二則發言也落地', content.includes('好點子：現場加一個AI體驗攤位'));

  // ④ 彙整關鍵字觸發注入，且注入內容包含前面兩則的完整歷史
  const event = makeEvent(
    '[Telegram 活動討論群 id:-1003537129853 +2m Mon 2026-08-24 13:10:00 GMT+8] coach (6124913915): 幫我彙整一下目前討論的內容',
    '-1003537129853'
  );
  await handler(event);
  const injected = (event.context.inject || []).map(i => i.content).join('\n');
  check('彙整關鍵字有觸發注入', event.context.inject && event.context.inject.length > 0);
  check('注入內容包含第一則(攤販)', injected.includes('手工皂、咖啡、乾燥花'));
  check('注入內容包含第二則(AI體驗攤位idea)', injected.includes('好點子：現場加一個AI體驗攤位'));
  check('注入內容包含這次彙整請求本身', injected.includes('彙整'));

  // ⑤ 沒有彙整關鍵字的一般發言不會觸發注入
  const event2 = makeEvent(
    '[Telegram 活動討論群 id:-1003537129853 +3m Mon 2026-08-24 13:11:00 GMT+8] coach (6124913915): 好，那明天再討論',
    '-1003537129853'
  );
  await handler(event2);
  check('一般發言不觸發注入', !event2.context.inject);

  console.log(`\n結果：${pass} 通過 / ${fail} 失敗（共 ${pass + fail}）`);

  // 還原：把測試寫的內容清掉，恢復教練原本的檔案狀態（若原本沒有就整個刪掉，不留測試殘留）
  if (hadExisting) fs.writeFileSync(TEST_FILE, backup);
  else if (fs.existsSync(TEST_FILE)) fs.unlinkSync(TEST_FILE);
  console.log(hadExisting ? '🧹 已還原原本的記憶檔內容' : '🧹 測試檔已清除，未留殘留');

  process.exit(fail === 0 ? 0 : 1);
}

main();
