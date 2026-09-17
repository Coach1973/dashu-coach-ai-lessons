const { chromium } = require('playwright');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';
const PAGE_URL = 'https://www.facebook.com/%E5%A4%A7%E5%8F%B0%E5%8D%97%E7%AD%96%E5%B1%95%E4%B8%AD%E5%BF%83/';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('進粉專');
  await page.goto(PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(8000);

  // 截圖看實際頁面
  await page.screenshot({ path: '/tmp/fb_page_initial.png', fullPage: false });
  console.log('截圖 1: /tmp/fb_page_initial.png');

  // 滾動到底（多次）
  for (let i = 0; i < 6; i++) {
    await page.mouse.wheel(0, 3000);
    await page.waitForTimeout(2500);
  }

  await page.screenshot({ path: '/tmp/fb_page_scrolled.png', fullPage: false });
  console.log('截圖 2: /tmp/fb_page_scrolled.png');

  // 統計頁面上所有可見的「策展」相關文字
  const text = await page.evaluate(() => document.body.innerText);
  console.log(`\n頁面總文字長度: ${text.length}`);
  console.log('--- 前 2000 字 ---');
  console.log(text.slice(0, 2000));
  console.log('--- 倒數 1000 字 ---');
  console.log(text.slice(-1000));

  // 數有幾個「event.bymyway.com」字串
  const urlMatches = text.match(/event\.bymyway\.com\/curated\/[\w-]+/g) || [];
  const uniqueUrls = [...new Set(urlMatches)];
  console.log(`\n📍 頁面上 event.bymyway.com/curated/ 出現 ${urlMatches.length} 次，去重 ${uniqueUrls.length} 個`);
  console.log('   URLs:', uniqueUrls);

  // 找所有 permalink
  const permalinks = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href*="/posts/"]'));
    return links.map((a) => a.href.split('?')[0]).filter((h, i, arr) => arr.indexOf(h) === i);
  });
  console.log(`\n🔗 permalink 數量: ${permalinks.length}`);
  permalinks.slice(0, 30).forEach((p) => console.log('   -', p));

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
