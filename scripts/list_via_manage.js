const { chromium } = require('playwright');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  // 直接點「管理貼文」入口
  await page.goto('https://www.facebook.com/GT.Curation/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);

  // 找「管理貼文」連結
  const manageLink = page.locator('a:has-text("管理貼文")').first();
  let entered = false;
  if (await manageLink.isVisible({ timeout: 3000 }).catch(() => false)) {
    const href = await manageLink.getAttribute('href');
    console.log('找到「管理貼文」連結:', href);
    await manageLink.click();
    await page.waitForTimeout(6000);
    entered = true;
  }

  if (!entered) {
    // 試其他 URL
    for (const url of [
      'https://www.facebook.com/GT.Curation/manage',
      'https://www.facebook.com/page_content_listing/GT.Curation/posts',
      'https://business.facebook.com/latest/posts/?asset_id=612941615239114',
    ]) {
      console.log(`\n試 ${url}`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(6000);
      console.log(`目前 URL: ${page.url()}`);
    }
  }

  console.log('\n--- 最終頁面 URL:', page.url());
  console.log('--- 頁面前 1500 字 ---');
  const text = (await page.evaluate(() => document.body.innerText)).slice(0, 1500);
  console.log(text);

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
