const { chromium } = require('playwright');

const CDP_URL = 'http://localhost:9222';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  for (const url of [
    'https://www.facebook.com/GT.Curation/',
    'https://www.facebook.com/GT.Curation/timeline',
    'https://www.facebook.com/612941615239114/',
  ]) {
    console.log(`\n========== ${url} ==========`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(6000);
    // 滾動
    for (let i = 0; i < 4; i++) {
      await page.mouse.wheel(0, 2000);
      await page.waitForTimeout(2000);
    }
    const text = (await page.evaluate(() => document.body.innerText)).slice(0, 800);
    console.log('頁面前 800 字:');
    console.log(text);
    const articles = await page.locator('div[role="article"]').count();
    console.log(`\n找到 ${articles} 個 article 區塊`);
    const urls = await page.evaluate(() => {
      const t = document.body.innerText;
      const m = t.match(/event\.bymyway\.com\/curated\/[\w-]+/g) || [];
      return [...new Set(m)];
    });
    console.log(`event.bymyway.com URLs: ${urls.length}`);
    if (urls.length > 0) console.log('   ', urls.slice(0, 20).join('\n    '));
  }

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
