const puppeteer = require('/Users/bymyway/.openclaw/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');

// 🔴 profile 路徑：2026-10-03 搬去 953-SSD 外接碟後，launchd 背景執行時
//    Chrome 建不了 SingletonLock（Operation not permitted），整支腳本連續 19 天失敗。
//    Chrome profile 必須放本機碟，外部磁碟在 launchd 權限下不能寫。
//    優先用本機副本；沒有就退回舊路徑（手動在終端機跑時仍可用）。
const LOCAL_PROFILE = '/Users/bymyway/.openclaw/fb_session_data_local';
const SSD_PROFILE = '/Users/bymyway/.openclaw/workspace/scripts/fb_session_data';

function pickProfile() {
  const candidates = [LOCAL_PROFILE, SSD_PROFILE];
  for (const p of candidates) {
    try {
      if (fs.existsSync(path.join(p, 'Default'))) return p;
    } catch (e) {}
  }
  return SSD_PROFILE;
}

(async () => {
  const profile = pickProfile();
  console.log('使用 profile：' + profile);
  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    userDataDir: profile
  });
  
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

  try {
    await page.goto('https://www.facebook.com/friends/birthdays/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 4000));

    // 🔴 抓登入狀態：被導去 index.php 代表 session 過期
    const finalUrl = page.url();
    const isLoginRedirect = /\/login|index\.php\?next=/.test(finalUrl);
    if (isLoginRedirect) {
      console.log("⚠️ FB session 已過期，被導去登入頁，無法抓壽星。");
      console.log("   終網址：" + finalUrl);
      console.log("   請教練登入後再跑一次。");
      console.log("   （修復方式：先在本地 Chrome 登入 FB，cookie 會同步到 fb_session_data）");
      await browser.close();
      process.exit(2);
    }

    const birthdays = await page.evaluate(() => {
      const h2s = Array.from(document.querySelectorAll('h2')).map(h => h.innerText.trim());
      let todayList = [];
      let isTodaySection = false;

      for (let text of h2s) {
        if (text === '今日壽星') {
          isTodaySection = true;
          continue;
        }
        if (text === '剛過生日的壽星' || text === '即將過生日的壽星' || text === '近期過生日的壽星' || text === '朋友') {
          break;
        }
        if (isTodaySection && text.length > 0) {
          todayList.push(text);
        }
      }
      return todayList;
    });

    if (birthdays.length === 0) {
      // 🔴 多一道確認：真的沒壽星 vs 抓不到（DOM 改版）
      const sanity = await page.evaluate(() => {
        const allH2 = Array.from(document.querySelectorAll('h2')).map(h => h.innerText.trim());
        const bodyText = document.body.innerText.slice(0, 500);
        return { allH2, bodyText };
      });
      if (sanity.allH2.length === 0) {
        console.log("⚠️ 找不到任何 <h2>，FB 頁面可能改版。");
        console.log("   頁面前 500 字：" + sanity.bodyText);
      } else {
        console.log("✅ 今天沒有 FB 壽星。");
      }
    } else {
      console.log(`\n🎉 今天共有 ${birthdays.length} 位 FB 壽星！\n名單如下：\n`);
      birthdays.forEach((b, i) => console.log(`${i+1}. ${b}`));
      console.log(`\n💡 請教練直接複製名單進行半自動發送。`);
    }

  } catch (error) {
    console.error("❌ 腳本執行發生錯誤，可能是 FB 尚未登入或 DOM 改變：", error.message);
  } finally {
    await browser.close();
  }
})();
