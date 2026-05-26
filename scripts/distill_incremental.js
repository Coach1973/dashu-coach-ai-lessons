// 增量蒸餾腳本 v2（2026-05-26 修訂）
// 修訂說明：
//   1. 改讀 🦞小龍蝦 bullet points（第三人稱摘要），原讀 👤教練 prompt 永遠空
//   2. 修正時區：改用台灣時間（UTC+8），原用 UTC 凌晨日期差一天
//   3. 加入 memory 大小警示：超 80KB 自動寫入 HEARTBEAT.md
// 觸發：cron job 9c3fc55d，頻率：每2小時

const fs = require('fs');
const path = require('path');

const BASE = '/Users/bymyway/.openclaw/workspace';
const MEMORY_DIR = path.join(BASE, 'memory');
const PROFILE = path.join(BASE, 'CLIENT_PROFILE.md');
const HEARTBEAT = path.join(BASE, 'HEARTBEAT.md');

// 台灣時間（UTC+8），避免凌晨跑到前一天的日期
const twnDate = new Date(Date.now() + 8 * 3600 * 1000);
const dateStr = twnDate.toISOString().split('T')[0];
const memoryPath = path.join(MEMORY_DIR, `${dateStr}.md`);

console.log(`[增量蒸餾 ${dateStr}] 檢查 ${memoryPath}`);

if (!fs.existsSync(memoryPath)) {
  console.log('NO_MEMORY_FILE');
  process.exit(0);
}

// ⚠️ Memory 大小警示（超 80KB 寫入 HEARTBEAT.md，提醒心跳去分割）
const fileSizeKB = Math.round(fs.statSync(memoryPath).size / 1024);
if (fileSizeKB > 80) {
  try {
    const hb = fs.existsSync(HEARTBEAT) ? fs.readFileSync(HEARTBEAT, 'utf8') : '';
    const warningKey = `memory/${dateStr}.md 已達`;
    if (!hb.includes(warningKey)) {
      fs.appendFileSync(HEARTBEAT, `\n⚠️ [${dateStr}] ${warningKey} ${fileSizeKB}KB（超過 80KB），下次心跳應執行分割`);
      console.log(`⚠️ memory 大小警示已寫入 HEARTBEAT.md（${fileSizeKB}KB）`);
    }
  } catch (e) {
    console.log(`警示寫入失敗: ${e.message}`);
  }
}

// 如果今天已蒸餾，直接結束
if (fs.existsSync(PROFILE)) {
  const existing = fs.readFileSync(PROFILE, 'utf8');
  if (existing.includes(`蒸餾 ${dateStr}`)) {
    console.log(`${dateStr} 已蒸餾，結束`);
    process.exit(0);
  }
}

const content = fs.readFileSync(memoryPath, 'utf8');

// 提取 🦞小龍蝦 的 bullet points（第三人稱摘要，才是真實蒸餾資料）
// 跳過純系統通知，保留有意義的行為描述
const SKIP_PATTERNS = [
  /HEARTBEAT_OK/,
  /replied with.*HEARTBEAT/i,
  /cron job status output/i,
  /async exec.*completed/i,
  /heartbeat poll/i,
  /processed the completion result internally/i,
  /^系統回報.*行事曆每週同步 cron/i,
  /^用戶觸發定時心跳任務.*1-HB\.md/i,
  /^OpenClaw 執行心跳檢查，回報結果：cron 正常/i,
  /^OpenClaw 分析.*並識別.*已處理/i,
  /context overflow/i,
  /session restart/i,
];

const entries = [];
const lobsterPat = /🦞 小龍蝦：([\s\S]*?)(?=👤 教練：|---|$)/g;
let m;
while ((m = lobsterPat.exec(content)) !== null) {
  const section = m[1];
  for (const line of section.split('\n')) {
    if (!line.trimStart().startsWith('- ')) continue;
    const text = line.replace(/^\s*- /, '').trim();
    if (text.length < 30) continue;
    if (SKIP_PATTERNS.some(p => p.test(text))) continue;
    entries.push(text.slice(0, 300));
  }
}

console.log(`提取到 ${entries.length} 個有效紀錄`);

if (entries.length === 0) {
  console.log('NO_NEW_ENTRIES');
  process.exit(0);
}

// 寫入 CLIENT_PROFILE.md（今日記錄放在最前面）
const todaySection = `## 蒸餾 ${dateStr}（共 ${entries.length} 則）\n${entries.map((e, i) => `${i + 1}. ${e}`).join('\n')}\n`;

let profile = '';
if (fs.existsSync(PROFILE)) {
  profile = fs.readFileSync(PROFILE, 'utf8');
} else {
  profile = '# CLIENT_PROFILE.md — 教練對話蒸餾（守則 #14：提煉是一種美德）\n';
}

const firstNewline = profile.indexOf('\n') + 1;
const newProfile = profile.slice(0, firstNewline) + '\n' + todaySection + '\n---\n\n' + profile.slice(firstNewline);
fs.writeFileSync(PROFILE, newProfile);

console.log(`✅ 蒸餾完成：${entries.length} 則有效紀錄 → CLIENT_PROFILE.md`);
