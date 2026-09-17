const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('Step 1: 進 FB 首頁...');
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);

  console.log('Step 2: 點「建立貼文」...');
  await page.locator('[aria-label="建立貼文"]').first().click();
  await page.waitForTimeout(4000);

  console.log('Step 3: 寫文案...');
  const editor = page.locator('[role="textbox"][contenteditable="true"]').first();
  await editor.click();
  await page.waitForTimeout(500);
  await editor.evaluate(el => {
    el.focus();
    const sel = window.getSelection();
    sel.removeAllRanges();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    sel.addRange(range);
    document.execCommand('insertText', false, '測試文案 debug');
    el.dispatchEvent(new InputEvent('input', { bubbles: true, cancelable: true, inputType: 'insertText', data: '測試文案 debug' }));
  }, '測試文案 debug');
  await page.waitForTimeout(2000);

  console.log('Step 4: 截圖 stage 1 (寫完文案後)...');
  await page.screenshot({ path: '/tmp/fb-stage1.png', fullPage: false });

  console.log('Step 5: 點「繼續」...');
  await page.locator('[aria-label="繼續"]').first().click();
  await page.waitForTimeout(5000);

  console.log('Step 6: 截圖 stage 2 (點繼續後)...');
  await page.screenshot({ path: '/tmp/fb-stage2.png', fullPage: false });

  console.log('Step 7: 列出 stage 2 所有可見 button 文字...');
  const allBtns = await page.evaluate(() => {
    const results = [];
    document.querySelectorAll('div[role="button"], span[role="button"], button').forEach(el => {
      const text = el.innerText?.trim();
      const aria = el.getAttribute('aria-label');
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      if (text && text.length > 0 && text.length < 50) {
        results.push({
          text,
          aria,
          rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width) },
        });
      }
    });
    return results.slice(0, 50);
  });
  console.log('Stage 2 buttons:', JSON.stringify(allBtns, null, 2));

  await browser.close();
})().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
