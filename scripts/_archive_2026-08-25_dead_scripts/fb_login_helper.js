// 一次性登入助手：開啟 FB 登入頁等教練登入，cookie 自動存到 fb_session_data
const puppeteer = require('/Users/bymyway/.openclaw/node_modules/puppeteer');

(async () => {
  console.log("🚀 開啟 FB 登入頁（fb_session_data profile）...");
  const browser = await puppeteer.launch({
    headless: false,
    userDataDir: "/Users/bymyway/.openclaw/workspace/scripts/fb_session_data",
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: null
  });

  const page = await browser.newPage();
  await page.goto('https://www.facebook.com/login.php', { waitUntil: 'networkidle2' });

  console.log("⏳ 等待教練登入...（偵測 URL 不再含 /login 即視為成功）");
  console.log("   教練登入完成後，此視窗會自動關閉。");

  // 最多等 5 分鐘
  const start = Date.now();
  const TIMEOUT = 5 * 60 * 1000;

  while (Date.now() - start < TIMEOUT) {
    await new Promise(r => setTimeout(r, 2000));
    const url = page.url();
    if (!/\/login|index\.php\?next=/.test(url)) {
      console.log(`✅ 偵測到登入成功（URL: ${url}）`);
      // 等一下讓 cookie 寫入
      await new Promise(r => setTimeout(r, 3000));
      await browser.close();
      console.log("🎉 Cookie 已存到 fb_session_data，可重新跑生日抓取腳本。");
      process.exit(0);
    }
  }

  console.log("⚠️ 5 分鐘未登入成功，自動關閉視窗。");
  await browser.close();
  process.exit(1);
})();
