// 增量蒸餾腳本：每2小時自動執行，蒸餾今日對話精華進 CLIENT_PROFILE.md
// 用途：從 memory/*.md 蒸餾教練關鍵發言，追加到 CLIENT_PROFILE.md
// 觸發：cron job 9c3fc55d，頻率：每2小時

const fs = require('fs');
const path = require('path');

const BASE = '/Users/bymyway/.openclaw/workspace';
const MEMORY_DIR = path.join(BASE, 'memory');
const PROFILE = path.join(BASE, 'CLIENT_PROFILE.md');
const TOP10 = path.join(BASE, 'distill/top10_errors_2026-05-23.md');

// 今天日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
const memoryPath = path.join(MEMORY_DIR, `${dateStr}.md`);

console.log(`[增量蒸餾 ${dateStr}] 檢查 ${memoryPath}`);

// 檢查 memory 檔案是否存在
if (!fs.existsSync(memoryPath)) {
  console.log('NO_NEW_ENTRIES');
  process.exit(0);
}

// 讀取今日 memory
const content = fs.readFileSync(memoryPath, 'utf8');

// 提取教練關鍵發言（跳過 system prompt / third-person note-taker）
const coachPattern = /👤 教練：(.{20,500})/g;
const matches = [...content.matchAll(coachPattern)];
const realMessages = matches.filter(m => 
  !m[1].startsWith('You are a third') && 
  !m[1].startsWith('Recent memories') &&
  !m[1].startsWith('[') &&
  !m[1].startsWith('System') &&
  !m[1].startsWith('Conversation')
);

// 如果有新發現就更新 CLIENT_PROFILE.md
if (realMessages.length > 0) {
  const latest = realMessages[realMessages.length - 1][1].trim();
  const timestamp = today.toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
  
  const entry = `\n## 蒸餾 ${dateStr} ${realMessages.length} 則教練發言\n- 時間：${timestamp}\n- 最新：${latest.slice(0, 300)}\n`;
  
  if (fs.existsSync(PROFILE)) {
    const current = fs.readFileSync(PROFILE, 'utf8');
    fs.writeFileSync(PROFILE, current + entry);
  } else {
    fs.writeFileSync(PROFILE, `# CLIENT_PROFILE.md — 教練對話蒸餾\n## 起源：特助心法守則#14（提煉是一種美德）\n${entry}`);
  }
  
  console.log(`✅ 蒸餾完成：${realMessages.length} 則新發言`);
  process.exit(0);
} else {
  console.log('NO_NEW_ENTRIES');
  process.exit(0);
}
