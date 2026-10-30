const puppeteer = require('/Users/bymyway/.openclaw/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 🔴 2026-10-31 修法（Puppeteer 直接 launch 會被 macOS 判定為「無 responsible app」，
//    導致鑰匙圈 ACL 拒絕、cookie 解不出來 → 被導去登入頁）：
//    1) cookie 來源改成教練自己的 Chrome（真實 profile 的 cookie 一定是新的）
//    2) Chrome 改用 `open -na`（LaunchServices）啟動 → macOS 會正確歸屬
//       responsible app，鑰匙圈才會放行；再掛 CDP port 用 puppeteer.connect
//    3) --headless=new → 教練螢幕不會跳出任何視窗
const REAL_CHROME = '/Users/bymyway/Library/Application Support/Google/Chrome';
const WORK_PROFILE = '/Users/bymyway/.openclaw/fb_session_data_local';
const CDP_PORT = 9225;

const COOKIE_FILES = [
  'Cookies', 'Device Bound Sessions', 'Network Persistent State',
  'Preferences', 'Secure Preferences', 'Login Data', 'Login Data For Account',
  'Web Data', 'History'
];
const DIR_FILES = ['Local Storage', 'Session Storage', 'Sessions', 'Sessions_Encrypted'];

function sh(cmd) {
  try { return execSync(cmd, { stdio: ['ignore', 'pipe', 'pipe'], timeout: 60000 }).toString(); }
  catch (e) { return (e.stdout || '').toString() + (e.stderr || '').toString(); }
}

// 1) 同步 cookie：從教練真實 Chrome 複製到工作 profile（保留加密格式，不用解密）
function syncCookies() {
  const srcDefault = path.join(REAL_CHROME, 'Default');
  const dstDefault = path.join(WORK_PROFILE, 'Default');
  fs.mkdirSync(dstDefault, { recursive: true });

  // Local State（os_crypt 用同一把鑰匙）
  try { fs.copyFileSync(path.join(REAL_CHROME, 'Local State'), path.join(WORK_PROFILE, 'Local State')); } catch (e) {}

  let copied = 0;
  for (const f of COOKIE_FILES) {
    const s = path.join(srcDefault, f);
    if (!fs.existsSync(s)) continue;
    try { fs.copyFileSync(s, path.join(dstDefault, f)); copied++; } catch (e) {}
  }
  for (const d of DIR_FILES) {
    const s = path.join(srcDefault, d);
    if (!fs.existsSync(s)) continue;
    try {
      sh(`ditto "${s}" "${path.join(dstDefault, d)}" 2>/dev/null`);
    } catch (e) {}
  }
  return copied;
}

// 2) 檢查工作 profile 是否還有 FB 登入 cookie
function hasSessionCookie() {
  const db = path.join(WORK_PROFILE, 'Default', 'Cookies');
  if (!fs.existsSync(db)) return false;
  try {
    const out = sh(`sqlite3 "${db}" "select count(*) from cookies where host_key like '%facebook.com' and name in ('c_user','xs');"`).trim();
    return parseInt(out, 10) > 0;
  } catch (e) { return false; }
}

// 3) 經 LaunchServices 啟動 Chrome（關鍵：讓 macOS 歸屬 responsible app）
function launchChrome() {
  sh(`pkill -f "remote-debugging-port=${CDP_PORT}" 2>/dev/null`);
  sh(`pkill -9 -f SecurityAgent 2>/dev/null`);
  sh(`rm -f "${WORK_PROFILE}"/Singleton* "${WORK_PROFILE}/Default"/Singleton* 2>/dev/null`);

  sh(`open -na "Google Chrome" --args --user-data-dir="${WORK_PROFILE}" --remote-debugging-port=${CDP_PORT} --headless=new --disable-gpu --no-first-run --no-default-browser-check --disable-session-crashed-bubble about:blank`);

  for (let i = 0; i < 45; i++) {
    const v = sh(`curl -s --max-time 2 http://localhost:${CDP_PORT}/json/version 2>/dev/null`);
    if (v && v.includes('Browser')) return true;
    sh('sleep 1');
  }
  return false;
}

function shutdown() {
  sh(`pkill -f "remote-debugging-port=${CDP_PORT}" 2>/dev/null`);
}

(async () => {
  const copied = syncCookies();
  const hasCookie = hasSessionCookie();
  console.log('同步 cookie 檔案數：' + copied + '，FB 登入 cookie：' + (hasCookie ? '有' : '無'));

  if (!hasCookie) {
    console.log('⚠️ 教練 Chrome 裡也沒有 FB 登入 cookie 了，需要教練在瀏覽器重新登入 Facebook。');
    process.exit(2);
  }

  if (!launchChrome()) {
    console.log('⚠️ Chrome 啟動失敗（CDP port 未就緒）。');
    process.exit(3);
  }

  let browser = null;
  try {
    browser = await puppeteer.connect({ browserURL: `http://localhost:${CDP_PORT}` });
    const pages = await browser.pages();
    const page = pages[0] || await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36');

    await page.goto('https://www.facebook.com/friends/birthdays/', { waitUntil: 'networkidle2', timeout: 90000 });
    await new Promise(r => setTimeout(r, 6000));

    const finalUrl = page.url();
    if (/\/login|index\.php\?next=/.test(finalUrl)) {
      console.log('⚠️ FB session 已過期，被導去登入頁，無法抓壽星。');
      console.log('   終網址：' + finalUrl);
      console.log('   請教練登入後再跑一次。');
      await browser.disconnect();
      shutdown();
      process.exit(2);
    }

    const birthdays = await page.evaluate(() => {
      const h2s = Array.from(document.querySelectorAll('h2')).map(h => h.innerText.trim());
      let todayList = [];
      let isTodaySection = false;
      for (const text of h2s) {
        if (text === '今日壽星') { isTodaySection = true; continue; }
        // 🔴 區段結束標記只有在「已經進入今日壽星」之後才算數：
        //    「新朋友」這個 h2 會出現在「今日壽星」之前，先 break 會抓到 0 人。
        if (isTodaySection && (text === '剛過生日的壽星' || text === '即將過生日的壽星' || text === '近期過生日的壽星' || text === '朋友')) break;
        if (isTodaySection && text.length > 0) todayList.push(text);
      }
      return { todayList, allH2: h2s };
    });

    if (birthdays.todayList.length === 0) {
      console.log('✅ 今天沒有 FB 壽星。');
      console.log('   （檢查到的 h2：' + JSON.stringify(birthdays.allH2.slice(0, 12)) + '）');
    } else {
      console.log(`\n🎉 今天共有 ${birthdays.todayList.length} 位 FB 壽星！\n名單如下：\n`);
      birthdays.todayList.forEach((b, i) => console.log(`${i+1}. ${b}`));
      console.log(`\n💡 請教練直接複製名單進行半自動發送。`);
    }

    await browser.disconnect();
    shutdown();
    process.exit(0);
  } catch (error) {
    console.error('❌ 腳本執行發生錯誤：', error.message);
    try { if (browser) await browser.disconnect(); } catch (e) {}
    shutdown();
    process.exit(1);
  }
})();
