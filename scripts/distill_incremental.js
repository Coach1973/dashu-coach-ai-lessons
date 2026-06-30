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

// ℹ️ Memory 大小提早通知（超 130KB 寫入 HEARTBEAT.md，純資訊）
// 注意：真正的分割已由 scripts/split_memory.sh 自動處理（門檻 150KB，Mac cron 每30分鐘）。
//       這裡只是提早讓教練知道「快滿了」，無需任何人手動分割。
const fileSizeKB = Math.round(fs.statSync(memoryPath).size / 1024);
if (fileSizeKB > 130) {
  try {
    const hb = fs.existsSync(HEARTBEAT) ? fs.readFileSync(HEARTBEAT, 'utf8') : '';
    const warningKey = `memory/${dateStr}.md 已達`;
    if (!hb.includes(warningKey)) {
      fs.appendFileSync(HEARTBEAT, `\nℹ️ [${dateStr}] ${warningKey} ${fileSizeKB}KB（接近門檻），split_memory.sh 會在 150KB 自動分割，無需手動`);
      console.log(`ℹ️ memory 大小提早通知已寫入 HEARTBEAT.md（${fileSizeKB}KB）`);
    }
  } catch (e) {
    console.log(`通知寫入失敗: ${e.message}`);
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

// 主源：Mac 本機 memory（加 [Mac] 標籤）
let content = '[__SOURCE__:Mac]\n' + fs.readFileSync(memoryPath, 'utf8');

// 跨機 verbatim 來源（v3 2026-06-30 新增，對應 knowledges/2026-06-30_跨機verbatim蒸餾備忘.md）
// 從 memory/verbatim/{lenovo,acer}/YYYY-MM-DD.md 補上跨機紀錄
const CROSS_SOURCES = [
  { tag: 'lenovo', label: '聯想' },
  { tag: 'acer',   label: 'ACER' },
];
for (const src of CROSS_SOURCES) {
  const p = path.join(MEMORY_DIR, 'verbatim', src.tag, `${dateStr}.md`);
  if (fs.existsSync(p)) {
    content += `\n\n[__SOURCE__:${src.label}]\n` + fs.readFileSync(p, 'utf8');
    console.log(`✅ 讀取跨機 verbatim：${src.label}（${p}）`);
  }
}

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
const touchstoneCandidates = [];  // 🪨 試金石候選收集
// 依 [__SOURCE__:XXX] 分段，預設 Mac
const sections = content.split(/\[__SOURCE__:([^\]]+)\]\n/);
// sections = ['', 'Mac', '<body>', '聯想', '<body>', 'ACER', '<body>']
for (let i = 1; i < sections.length; i += 2) {
  const source = sections[i];
  const body = sections[i + 1] || '';
  const prefix = source === 'Mac' ? '' : `[${source}] `;
  const lobsterPat = /🦞 小龍蝦：([\s\S]*?)(?=👤 教練：|---|$)/g;
  let m;
  while ((m = lobsterPat.exec(body)) !== null) {
    for (const line of m[1].split('\n')) {
      if (!line.trimStart().startsWith('- ')) continue;
      const text = line.replace(/^\s*- /, '').trim();
      if (text.length < 30) continue;
      if (SKIP_PATTERNS.some(p => p.test(text))) continue;
      const tagged = (prefix + text).slice(0, 300 + prefix.length);
      entries.push(tagged);
      if (/🪨\s*試金石候選[:：]/.test(text)) touchstoneCandidates.push(tagged);
    }
  }
  // 跨機 verbatim 檔（body 直接是 `- [tag] xxx` 形式，非 🦞/👤 對話格式）也收
  if (source !== 'Mac') {
    for (const line of body.split('\n')) {
      if (!line.trimStart().startsWith('- ')) continue;
      const text = line.replace(/^\s*- /, '').trim();
      if (text.length < 30) continue;
      if (SKIP_PATTERNS.some(p => p.test(text))) continue;
      const sliced = text.slice(0, 300);
      // 跨機檔本身已內含 [聯想]/[ACER] tag，無需重貼
      entries.push(sliced);
      if (/🪨\s*試金石候選[:：]/.test(text)) touchstoneCandidates.push(sliced);
    }
  }
}
// 去重（跨機 verbatim 區段可能跟主源段重疊）
const seen = new Set();
const uniqEntries = entries.filter(e => { if (seen.has(e)) return false; seen.add(e); return true; });
entries.length = 0; entries.push(...uniqEntries);

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

// 🪨 試金石候選彙整（交付物 D）
if (touchstoneCandidates.length > 0) {
  const TOUCHSTONE = path.join(BASE, 'distill', '試金石_候選區.md');
  const stamp = `## ${dateStr}（${touchstoneCandidates.length} 則跨機候選）\n`;
  const block = stamp + touchstoneCandidates.map(t => `- ${t}`).join('\n') + '\n\n---\n\n';
  let prev = fs.existsSync(TOUCHSTONE) ? fs.readFileSync(TOUCHSTONE, 'utf8')
    : '# 🪨 試金石候選區（自動收集，教練決定收不收）\n\n> 來源：跨機 verbatim 蒸餾標記。對應 `knowledges/2026-06-30_跨機verbatim蒸餾備忘.md` 交付物 D。\n\n';
  if (!prev.includes(stamp)) {
    const head = prev.indexOf('\n\n') + 2;
    fs.writeFileSync(TOUCHSTONE, prev.slice(0, head) + block + prev.slice(head));
    console.log(`🪨 寫入試金石候選 ${touchstoneCandidates.length} 則 → ${TOUCHSTONE}`);
  }
}
