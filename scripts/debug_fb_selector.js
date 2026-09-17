const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('Navigating to 大台南策展中心 粉專...');
  await page.goto('https://www.facebook.com/大台南策展中心/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);

  console.log('URL:', page.url());
  console.log('Title:', await page.title());

  // 截圖存起來
  await page.screenshot({ path: '/tmp/fb-debug-screenshot.png', fullPage: false });
  console.log('Screenshot saved: /tmp/fb-debug-screenshot.png');

  // 找所有可能的「建立貼文」元素
  const candidates = await page.evaluate(() => {
    const results = [];
    // 收集所有 aria-label 含「建立」「發布」「貼文」「Create」「Post」「Write」的元素
    document.querySelectorAll('[aria-label]').forEach(el => {
      const label = el.getAttribute('aria-label');
      if (label && /(建立|發布|貼文|Create|Post|Write|寫貼文)/i.test(label)) {
        results.push({
          tag: el.tagName,
          label,
          role: el.getAttribute('role'),
          text: el.innerText?.slice(0, 30),
        });
      }
    });
    return results.slice(0, 30);
  });
  console.log('Aria-label candidates:', JSON.stringify(candidates, null, 2));

  // 找包含「寫貼文」「建立貼文」「What\'s on your mind」「Create post」的可見按鈕/連結/div
  const visibleCandidates = await page.evaluate(() => {
    const results = [];
    const allEls = document.querySelectorAll('div, button, a, span');
    allEls.forEach(el => {
      const text = el.innerText?.trim();
      if (!text || text.length > 50) return;
      if (/(建立貼文|寫貼文|Create a post|What.{0,3}s on your mind|Write something|發佈貼文|開始發佈)/i.test(text)) {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          results.push({
            tag: el.tagName,
            role: el.getAttribute('role'),
            text,
            aria: el.getAttribute('aria-label'),
            visible: rect.width > 50 && rect.height > 20,
            rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
          });
        }
      }
    });
    return results.slice(0, 20);
  });
  console.log('Visible text candidates:', JSON.stringify(visibleCandidates, null, 2));

  await browser.close();
})().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
