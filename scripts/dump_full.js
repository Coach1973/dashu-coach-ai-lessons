const { chromium } = require('playwright');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  await page.goto('https://www.facebook.com/professional_dashboard/content/content_library/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(10000);

  // 滾動 15 次
  for (let i = 0; i < 15; i++) {
    await page.mouse.wheel(0, 2000);
    await page.waitForTimeout(2000);
  }

  // 抓所有 permalinks（過濾掉 FB 內部 chrome 連結）
  const data = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href*="/posts/"]'));
    const permalinks = [...new Set(links.map((a) => a.href.split('?')[0]))];
    // 抓時間範圍指示
    const range = (document.body.innerText.match(/過去\s*\d+\s*天[^\n]*/) || [''])[0];
    // 找「已選擇 X 則貼文」
    const selected = (document.body.innerText.match(/已選擇[^\n]*/) || [''])[0];
    return { permalinks, range, selected, fullLen: document.body.innerText.length };
  });

  console.log('時間範圍:', data.range);
  console.log('選擇計數:', data.selected);
  console.log('permalinks 數:', data.permalinks.length);
  console.log('全文長度:', data.fullLen);
  console.log('\n前 20 個 permalinks:');
  data.permalinks.slice(0, 20).forEach((p) => console.log('  ', p));

  // dump 完整文字存檔
  const fullText = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync('/tmp/fb_content_library_full.txt', fullText);
  console.log(`\n完整文字已存 /tmp/fb_content_library_full.txt (${fullText.length} 字)`);

  // 計算「已發佈」字串出現次數
  const matchCount = (fullText.match(/已發佈/g) || []).length;
  console.log(`"已發佈" 出現次數: ${matchCount}`);

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
