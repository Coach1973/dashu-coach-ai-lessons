const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('Step 1: 進 FB 首頁...');
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);

  console.log('Step 2: 點「建立貼文」...');
  const createBtn = page.locator('[aria-label="建立貼文"]').first();
  await createBtn.click();
  await page.waitForTimeout(4000);

  console.log('Step 3: 截圖 + 找發布按鈕...');
  await page.screenshot({ path: '/tmp/fb-modal-debug.png', fullPage: false });
  console.log('   截圖: /tmp/fb-modal-debug.png');

  // 找所有可見的「發布」「Post」「送出」按鈕
  const candidates = await page.evaluate(() => {
    const results = [];
    document.querySelectorAll('div[role="button"], button, span[role="button"], a[role="button"]').forEach(el => {
      const text = el.innerText?.trim();
      const aria = el.getAttribute('aria-label');
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      // 只關注「發布」「Post」「分享」「Share」「送出」「Submit」相關
      if ((aria && /(發布|Post|Share|送出|Submit)/i.test(aria)) ||
          (text && /^(發布|Post|Share|送出|Submit)$/i.test(text))) {
        results.push({
          tag: el.tagName,
          role: el.getAttribute('role'),
          text: text?.slice(0, 40),
          aria,
          visible: rect.width > 0 && rect.height > 0,
          rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
        });
      }
    });
    return results.slice(0, 30);
  });
  console.log('發布按鈕候選:', JSON.stringify(candidates, null, 2));

  // 找 modal 內所有可見 button/div role=button，列出文字（找哪個是「發布」）
  const allBtns = await page.evaluate(() => {
    const results = [];
    document.querySelectorAll('div[role="button"], span[role="button"], button').forEach(el => {
      const text = el.innerText?.trim();
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      if (text && text.length > 0 && text.length < 30) {
        results.push({
          text,
          aria: el.getAttribute('aria-label'),
          rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width) },
        });
      }
    });
    return results.slice(0, 40);
  });
  console.log('Modal 內所有按鈕:', JSON.stringify(allBtns, null, 2));

  await browser.close();
})().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
