// 🔴 驗證腳本 v3（2026-11-04）：先摸清 FB 頁面「今日壽星」區塊的 DOM 結構，
// 再用「profile 連結 + h2 文字」兩條路徑交叉比對主腳本結果。
const puppeteer = require('/Users/bymyway/.openclaw/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REAL_CHROME = '/Users/bymyway/Library/Application Support/Google/Chrome';
const WORK_PROFILE = '/Users/bymyway/.openclaw/fb_session_data_local';
const CDP_PORT = 9225;
const COOKIE_FILES = ['Cookies', 'Device Bound Sessions', 'Network Persistent State', 'Preferences', 'Secure Preferences', 'Login Data', 'Login Data For Account', 'Web Data', 'History'];
const DIR_FILES = ['Local Storage', 'Session Storage', 'Sessions', 'Sessions_Encrypted'];

function sh(cmd) {
  try { return execSync(cmd, { stdio: ['ignore', 'pipe', 'pipe'], timeout: 60000 }).toString(); }
  catch (e) { return (e.stdout || '').toString() + (e.stderr || '').toString(); }
}
function resetCookieState() {
  sh(`pkill -f "remote-debugging-port=${CDP_PORT}" 2>/dev/null`); sh(`sleep 1`);
  sh(`rm -f "${WORK_PROFILE}/Default/Cookies"* "${WORK_PROFILE}/Default/Network Persistent State"* 2>/dev/null`);
  sh(`rm -f "${WORK_PROFILE}"/Singleton* "${WORK_PROFILE}/Default"/Singleton* 2>/dev/null`);
}
function syncCookies() {
  const src = path.join(REAL_CHROME, 'Default'), dst = path.join(WORK_PROFILE, 'Default');
  fs.mkdirSync(dst, { recursive: true });
  try { fs.copyFileSync(path.join(REAL_CHROME, 'Local State'), path.join(WORK_PROFILE, 'Local State')); } catch (e) {}
  let copied = 0;
  for (const f of COOKIE_FILES) { const s = path.join(src, f); if (!fs.existsSync(s)) continue; try { fs.copyFileSync(s, path.join(dst, f)); copied++; } catch (e) {} }
  for (const d of DIR_FILES) { const s = path.join(src, d); if (!fs.existsSync(s)) continue; try { sh(`ditto "${s}" "${path.join(dst, d)}" 2>/dev/null`); } catch (e) {} }
  return copied;
}
function countCookies() {
  const db = path.join(WORK_PROFILE, 'Default', 'Cookies');
  if (!fs.existsSync(db)) return -1;
  const out = sh(`sqlite3 "${db}" "select count(*) from cookies where host_key like '%facebook.com' and name in ('c_user','xs');" 2>/dev/null`).trim();
  return parseInt(out, 10) || 0;
}
function launchChrome() {
  sh(`pkill -f "remote-debugging-port=${CDP_PORT}" 2>/dev/null`);
  sh(`rm -f "${WORK_PROFILE}"/Singleton* "${WORK_PROFILE}/Default"/Singleton* 2>/dev/null`);
  sh(`open -na "Google Chrome" --args --user-data-dir="${WORK_PROFILE}" --remote-debugging-port=${CDP_PORT} --headless=new --disable-gpu --no-first-run --no-default-browser-check --disable-session-crashed-bubble about:blank`);
  for (let i = 0; i < 45; i++) { const v = sh(`curl -s --max-time 2 http://localhost:${CDP_PORT}/json/version 2>/dev/null`); if (v && v.includes('Browser')) return true; sh('sleep 1'); }
  return false;
}
function shutdown() { sh(`pkill -f "remote-debugging-port=${CDP_PORT}" 2>/dev/null`); }

(async () => {
  resetCookieState();
  const copied = syncCookies();
  console.log('驗證腳本｜同步 cookie 檔案數：' + copied + '，FB cookie（啟動前）：' + countCookies() + ' 筆');
  if (countCookies() <= 0) process.exit(2);
  if (!launchChrome()) { console.log('⚠️ Chrome 啟動失敗'); process.exit(3); }

  let browser = null;
  try {
    browser = await puppeteer.connect({ browserURL: `http://localhost:${CDP_PORT}` });
    const pages = await browser.pages();
    const page = pages[0] || await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36');
    await page.goto('https://www.facebook.com/friends/birthdays/', { waitUntil: 'networkidle2', timeout: 90000 });
    await new Promise(r => setTimeout(r, 8000));
    const finalUrl = page.url();
    if (/\/login|index\.php\?next=/.test(finalUrl)) { console.log('⚠️ 被導去登入頁：' + finalUrl); await browser.disconnect(); shutdown(); process.exit(2); }

    const dump = await page.evaluate(() => {
      const h2s = Array.from(document.querySelectorAll('h2'));
      const list = h2s.map((h, i) => ({
        i,
        text: (h.innerText || '').trim(),
        tag: h.tagName,
        parentTag: h.parentElement ? h.parentElement.tagName : '',
        linksInH2: h.querySelectorAll('a').length,
        cls: (h.getAttribute('class') || '').slice(0, 60)
      }));
      // 今日壽星 h2 之後，頁面上所有 profile 連結文字（依文件順序）
      const todayIdx = h2s.findIndex(h => (h.innerText || '').trim() === '今日壽星');
      const profileLinks = [];
      if (todayIdx >= 0) {
        const stop = ['剛過生日的壽星', '即將過生日的壽星', '近期過生日的壽星', '朋友', '新朋友'];
        const todayEl = h2s[todayIdx];
        // 找 todayEl 的「區塊容器」：往上找帶 role 或 data-pagelet 的祖先
        let container = todayEl;
        for (let k = 0; k < 8 && container.parentElement; k++) {
          container = container.parentElement;
          if (container.querySelectorAll('a[href*="/profile.php"]').length >= 3) break;
        }
        const links = container.querySelectorAll('a[href*="/profile.php"]');
        links.forEach(a => {
          const t = (a.innerText || '').trim();
          if (t) profileLinks.push({ text: t, href: (a.getAttribute('href') || '').split('?')[0] });
        });
        // 容器內 h2 清單（另一條路徑）
        const containerH2 = Array.from(container.querySelectorAll('h2')).map(h => (h.innerText || '').trim());
        // 容器文字（前 1500 字）
        const containerText = (container.innerText || '').slice(0, 1500);
        // 下一個 h2（用來判斷區塊結束）
        const nextH2 = h2s[todayIdx + 1] ? (h2s[todayIdx + 1].innerText || '').trim() : '(無)';
        return { ok: true, h2List: list, todayIdx, containerH2, profileLinks, containerText, nextH2, stop };
      }
      return { ok: false, h2List: list };
    });

    console.log('\n=== 頁面所有 h2（前 30）===');
    dump.h2List.slice(0, 30).forEach(h => console.log(`   [${h.i}] ${JSON.stringify(h.text)}  (parent=${h.parentTag}, h2內連結=${h.linksInH2})`));
    if (!dump.ok) { console.log('❌ 找不到「今日壽星」'); await browser.disconnect(); shutdown(); process.exit(1); }
    console.log('\n今日壽星 h2 索引：' + dump.todayIdx + '，下一個 h2：' + JSON.stringify(dump.nextH2));
    console.log('\n=== 容器內 h2 ===');
    dump.containerH2.forEach((t, i) => console.log(`   ${i}. ${JSON.stringify(t)}`));
    console.log('\n=== 容器內 profile 連結文字 ===');
    dump.profileLinks.forEach((p, i) => console.log(`   ${i + 1}. ${p.text}  ${p.href}`));
    console.log('\n=== 容器文字（前 1200 字）===\n' + dump.containerText);

    await browser.disconnect(); shutdown(); process.exit(0);
  } catch (e) {
    console.error('❌ 驗證腳本錯誤：', e.message);
    try { if (browser) await browser.disconnect(); } catch (e2) {}
    shutdown(); process.exit(1);
  }
})();
