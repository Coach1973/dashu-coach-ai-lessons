const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    userDataDir: "/Users/bymyway/.openclaw/workspace/scripts/fb_session_data"
  });
  
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

  try {
    await page.goto('https://www.facebook.com/friends/birthdays/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 4000)); 

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
      console.log("✅ 今天沒有 FB 壽星。");
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
