#!/opt/homebrew/bin/node
/**
 * 教官對話歷史掃描腳本
 * 用途：掃描 history.jsonl 中的教練發言，找出錯誤模式和痛點
 * 輸出：教官對話精華 + 錯誤模式分析
 */

const fs = require('fs');
const path = require('path');

// 讀取 history.jsonl
const historyFile = '/Users/bymyway/.claude/history.jsonl';
const content = fs.readFileSync(historyFile, 'utf-8');
const lines = content.split('\n').filter(l => l.trim());

console.log(`📊 共 ${lines.length} 筆記錄\n`);

// 解析所有教練發言
const messages = [];
for (const line of lines) {
  try {
    const entry = JSON.parse(line);
    if (entry.display && entry.display.trim()) {
      messages.push({
        display: entry.display.trim(),
        timestamp: entry.timestamp,
        sessionId: entry.sessionId,
        pastedContents: entry.pastedContents ? Object.keys(entry.pastedContents).length : 0
      });
    }
  } catch (e) {
    // 跳過無效行
  }
}

console.log(`✅ 成功解析 ${messages.length} 筆記錄\n`);

// 錯誤模式關鍵字搜尋
const errorPatterns = [
  {
    name: '讓教練當搬運工（#11-#12）',
    keywords: ['你自己去', '你自己', '按 Cmd', '按鍵盤', '打開', '輸入路徑', '去 XXX', '複製貼上', '我再教', '你要按'],
    rules: '#11/#12/#E04'
  },
  {
    name: '方向明確卻停住不執行（#13）',
    keywords: ['你怎麼看', '你要不要', '你覺得呢', '我說過', '我之前說', '不是說好', '你搞清楚', '你自己'],
    rules: '#13/#E06'
  },
  {
    name: '資訊小白不懂專業術語（#10）',
    keywords: ['什麼意思', '這是什麼', 'ETA', '不懂', '聽不懂', '我不知道這是', '你要解釋'],
    rules: '#10/#E10'
  },
  {
    name: '守則被違反（被教練指出）',
    keywords: ['不是第', '第 5 條', '第5條', '守則說', '你違反', '你錯了', '你搞混', '你搞錯'],
    rules: '#E08/#21'
  },
  {
    name: '失敗/錯誤/血淚',
    keywords: ['失敗', '錯誤', '問題', '不對', '搞砸', '糟糕', '後悔', '早知道', '不應該'],
    rules: '#7/#E05'
  },
  {
    name: '語音辨識問題',
    keywords: ['語音', '語辨', '輸入法', '聽錯', '說成', '打成', '變成'],
    rules: '#18/#E07'
  },
  {
    name: '情緒強度高的表達',
    keywords: ['無奈', '生氣', '失望', '傷心', '鬱卒', '挫折', '崩潰', '很難過'],
    rules: '情緒指標'
  },
  {
    name: '重複同樣的要求',
    keywords: ['我說過', '我已經', '我再說', '不是第一次', '你又', '每次都', '每次都問'],
    rules: '重複觸發'
  },
  {
    name: '要求記住/記錄',
    keywords: ['你記得', '你要記住', '你應該記', '寫下來', '我要你記'],
    rules: '#13/#E02'
  },
  {
    name: '要求保密/安全',
    keywords: ['不要公開', '不要外傳', '保密', '安全', '不能說'],
    rules: '安全意識'
  }
];

// 搜尋所有模式
const matches = [];
for (const pattern of errorPatterns) {
  for (const msg of messages) {
    for (const kw of pattern.keywords) {
      if (msg.display.includes(kw)) {
        matches.push({
          ...pattern,
          keyword: kw,
          message: msg.display.substring(0, 300),
          timestamp: msg.timestamp,
          sessionId: msg.sessionId,
          length: msg.display.length
        });
        break; // 每則訊息每個模式只算一次
      }
    }
  }
}

// 按模式分組統計
const patternStats = {};
for (const m of matches) {
  if (!patternStats[m.name]) {
    patternStats[m.name] = {
      ...m,
      count: 0,
      examples: []
    };
  }
  patternStats[m.name].count++;
  if (patternStats[m.name].examples.length < 3) {
    patternStats[m.name].examples.push({
      keyword: m.keyword,
      message: m.message.substring(0, 200)
    });
  }
}

// 排序
const sorted = Object.values(patternStats).sort((a, b) => b.count - a.count);

console.log('═══════════════════════════════════════════════════════');
console.log('🔍 教官對話錯誤模式掃描結果');
console.log('═══════════════════════════════════════════════════════\n');

for (const s of sorted) {
  const date = new Date(s.timestamp).toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
  console.log(`\n【${s.name}】${s.count} 筆 │ ${s.rules}`);
  console.log(`最近：${date}`);
  console.log('───────────────────────────');
  for (const ex of s.examples) {
    console.log(`  [${ex.keyword}] ${ex.message.substring(0, 150)}`);
  }
}

// 輸出教練最長的發言（最可能有價值的內容）
console.log('\n═══════════════════════════════════════════════════════');
console.log('📝 教官最長的 20 則發言（最可能有價值的內容）');
console.log('═══════════════════════════════════════════════════════\n');

const longest = [...messages]
  .filter(m => m.length > 100)
  .sort((a, b) => b.length - a.length)
  .slice(0, 20);

for (let i = 0; i < longest.length; i++) {
  const m = longest[i];
  const date = new Date(m.timestamp).toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
  console.log(`[${i + 1}] ${date} (${m.length}字)`);
  console.log(`    ${m.message.substring(0, 200)}${m.message.length > 200 ? '...' : ''}`);
  if (m.pastedContents > 0) console.log(`    📎 含附件/貼圖`);
  console.log();
}

// 統計時段分佈
console.log('═══════════════════════════════════════════════════════');
console.log('📅 對話時段分佈');
console.log('═══════════════════════════════════════════════════════\n');

const hourCount = {};
for (const m of messages) {
  const h = new Date(m.timestamp).getHours();
  const label = `${h}:00-${h}:59`;
  hourCount[label] = (hourCount[label] || 0) + 1;
}

const sortedHours = Object.entries(hourCount).sort((a, b) => b[1] - a[1]);
for (const [h, c] of sortedHours.slice(0, 10)) {
  const bar = '█'.repeat(Math.ceil(c / 5));
  console.log(`  ${h} │ ${bar} (${c})`);
}

// 總結
console.log('\n═══════════════════════════════════════════════════════');
console.log('📊 總結');
console.log('═══════════════════════════════════════════════════════');
console.log(`總發言筆數：${messages.length}`);
console.log(`錯誤模式觸發：${matches.length} 筆`);
console.log(`獨立模式類型：${sorted.length} 種`);
console.log(`最大單則發言：${Math.max(...messages.map(m => m.length))} 字`);
