const { chromium } = require('playwright');

const CDP_URL = 'http://localhost:9222';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  // 開 FB 首頁看登入身份
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);

  // 找帳號頭像 / 名稱
  const profileInfo = await page.evaluate(() => {
    // 找個人 profile link
    const meLink = document.querySelector('a[aria-label="你的個人檔案"], a[href*="/me/"], a[href*="/profile.php"]');
    const profileName = document.querySelector('[aria-label="你的個人檔案"]')?.getAttribute('aria-label');
    // 找導覽列的所有用戶名稱
    const allLinks = Array.from(document.querySelectorAll('a[href*="facebook.com/"]')).slice(0, 30).map((a) => ({
      href: a.href,
      text: (a.innerText || '').slice(0, 50),
      aria: a.getAttribute('aria-label') || '',
    }));
    return { profileName, allLinks: allLinks.filter((l) => l.text || l.aria) };
  });

  console.log('📋 Profile name:', profileInfo.profileName);
  console.log('🔗 相關連結（前 20）:');
  profileInfo.allLinks.slice(0, 20).forEach((l) => {
    console.log(`   - [${l.aria || l.text}] ${l.href}`);
  });

  // 用 Graph API me 查 user id
  // 但需要 access token，從 cookie 撈
  const cookies = await context.cookies('https://www.facebook.com/');
  const cUser = cookies.find((c) => c.name === 'c_user');
  const xs = cookies.find((c) => c.name === 'xs');
  console.log('\n🍪 c_user:', cUser?.value);
  console.log('🍪 xs:', xs?.value?.slice(0, 20) + '...');

  if (cUser) {
    // 用 Graph API 查 user id
    const url = `https://graph.facebook.com/v18.0/me?access_token=${xs?.value}&method=get&fields=id,name`;
    const res = await page.evaluate(async (u) => {
      try {
        const r = await fetch(u);
        return await r.text();
      } catch (e) {
        return `ERR: ${e.message}`;
      }
    }, url);
    console.log('\n📡 Graph /me:', res.slice(0, 300));
  }

  // 截圖看頁面
  await page.screenshot({ path: '/tmp/fb_home.png', fullPage: false });

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
