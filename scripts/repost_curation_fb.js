#!/usr/bin/env node
/**
 * 大台南策展中心 — 21 則歷史隱形貼文重貼腳本
 * 透過 Chrome DevTools Protocol 接管已登入 FB 的 Chrome 實例
 *
 * 前置條件：
 * 1. 教練 Chrome 已關閉
 * 2. 用 `open -a "Google Chrome" --args --remote-debugging-port=9222` 啟動帶 port
 * 3. 等 3 秒讓 Chrome 開 DevTools server
 * 4. 跑這個腳本
 *
 * 用法：node scripts/repost_curation_fb.js
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FB_PAGE_URL = 'https://www.facebook.com/大台南策展中心/';
const CDP_URL = 'http://localhost:9222';

const POSTS = [
  {
    title: 'EVERYDAY CAFÉ 台南三店',
    desc: '生吐司早午餐．勝利店・海安店・陽光公園店',
    url: 'https://coach1973.github.io/everydaycaf-tai-nan-san-dian/',
    img: 'https://coach1973.github.io/everydaycaf-tai-nan-san-dian/img/hero-toast.jpg',
  },
  {
    title: '柚式藝術 Yo's Art（張騰文）',
    desc: '讓每一朵花，留住最好的那一刻。永生花 ｜ 鈔票花禮 ｜ 韓式氣球 ｜ 婚禮派派佈置。台南 · 屏東 ｜ 全省安全宅配。',
    url: 'https://coach1973.github.io/flower-site/',
    img: 'https://coach1973.github.io/flower-site/img/hero.jpg',
  },
  {
    title: '傅恩平｜商務英漢通譯',
    desc: '兩種語言之間，總要有人站著。臺南善化，榮益齋。',
    url: 'https://coach1973.github.io/fu-en-ping/',
    img: 'https://coach1973.github.io/fu-en-ping/assets/hero-fields.jpg',
  },
  {
    title: '六淨山房 · 知事官邸古蹟餐廳',
    desc: '百年官邸 · 茶香咖啡 · 光影時光。一日兩時，與自己重逢。',
    url: 'https://coach1973.github.io/historic-residence/',
    img: 'https://coach1973.github.io/historic-residence/assets/hero-front.jpg',
  },
  {
    title: '康燕居（燕窩）',
    desc: '一盞燕窩，四百年的講究',
    url: 'https://coach1973.github.io/kangyenju/',
    img: 'https://coach1973.github.io/kangyenju/assets/cliff_wide.jpg',
  },
  {
    title: '中華新媒體影音發展協會（nmda v1）',
    desc: '讓專業被看見，讓合作真正發生',
    url: 'https://coach1973.github.io/nmda/',
    img: 'https://coach1973.github.io/nmda/assets/gallery/activity-01.jpg',
  },
  {
    title: '中華新媒體影音發展協會（nmda v2）',
    desc: '讓專業被看見，讓合作真正發生',
    url: 'https://coach1973.github.io/nmda-2/',
    img: 'https://coach1973.github.io/nmda-2/assets/gallery/activity-01.jpg',
  },
  {
    title: '陳佩君老師（佩佩老師）',
    desc: '鋼琴家・音樂教育家',
    url: 'https://coach1973.github.io/peipei/',
    img: 'https://coach1973.github.io/peipei/images/image2.jpg',
  },
  {
    title: '楊仁豪 — 品牌 IP 規劃師',
    desc: '不只申請權利，更為你的品牌打造智慧資產的護城河。懂商業的智財專家，守護你的品牌資產。',
    url: 'https://coach1973.github.io/sbip/',
    img: 'https://coach1973.github.io/sbip/assets/og-card.jpg',
  },
  {
    title: '水交社眷村食堂 — 相聚場',
    desc: '在府城南郊的水交社眷村文化園區中，質樸不假裝飾的眷落。手工拉麵、慢燉牛腱、中藥材熬煮的湯頭。',
    url: 'https://coach1973.github.io/xiangjuchang/',
    img: 'https://coach1973.github.io/xiangjuchang/assets/img/env-hall.jpg',
  },
  {
    title: '邱南寅・小南雕刻',
    desc: '龍益宗教文物 — 一面牌位，一部家族的故事',
    url: 'https://coach1973.github.io/xiaonan/',
    img: 'https://coach1973.github.io/xiaonan/assets/nan-portrait.jpg',
  },
  {
    title: '謝緯翔｜理賠領航員',
    desc: '九年前，他自己的理賠單從 60 萬被砍到 18 萬。從那天起，他決定學會整套規則——不讓同樣的事發生在別人身上。',
    url: 'https://coach1973.github.io/xie-wei-xiang/',
    img: 'https://coach1973.github.io/xie-wei-xiang/assets/og-card.jpg',
  },
  {
    title: '張育慈｜順業肥料資材行',
    desc: '從土壤到餐桌。彰化溪州，三十年的肥料家業，第二代的接棒。',
    url: 'https://coach1973.github.io/zhang-yu-ci/',
    img: 'https://coach1973.github.io/zhang-yu-ci/assets/og-card.jpg',
  },
];

const HASHTAGS = '#大台南策展中心 #大樹教練產業鍊';

function buildPostBody(p) {
  return `${p.desc}\n\n👉 完整介紹：${p.url}\n\n${HASHTAGS}`;
}

async function postOne(page, post, idx) {
  console.log(`\n[${idx + 1}/${POSTS.length}] 開始貼：${post.title}`);

  // 進粉專首頁（每次都重新進，避免留在上一則的 modal 裡）
  await page.goto(FB_PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(2000);

  // 找「寫貼文」入口 — FB 的 selector 在 2026 改成多個入口
  // 常見入口：a[aria-label*="建立貼文"]、div[aria-label*="建立貼文"]、button 內含「建立貼文」
  const composer = await page
    .locator('[aria-label*="建立貼文"], [aria-label*="Create a post"], [aria-label*="Write something"]')
    .first();
  await composer.waitFor({ timeout: 15000 });
  await composer.click();
  await page.waitForTimeout(2000);

  // 等待貼文編輯器出現（Draft.js / contenteditable）
  const editor = page.locator('[role="textbox"][contenteditable="true"]').first();
  await editor.waitFor({ timeout: 15000 });
  await editor.click();
  await page.waitForTimeout(500);

  // Draft.js 對合成鍵盤事件沒反應 — 改用 page.evaluate 直接寫 innerText
  await editor.evaluate((el, text) => {
    // 模擬真實輸入：focus + execCommand + 觸發 input event
    el.focus();
    const sel = window.getSelection();
    sel.removeAllRanges();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    sel.addRange(range);
    document.execCommand('insertText', false, text);
    // 確保觸發 React 監聽的 input event
    el.dispatchEvent(new InputEvent('input', { bubbles: true, cancelable: true, inputType: 'insertText', data: text }));
  }, buildPostBody(post));
  await page.waitForTimeout(2000);

  // 截圖確認文字已寫入（避免 Draft.js 假成功）
  const textContent = await editor.textContent();
  if (!textContent.includes(post.desc.slice(0, 20))) {
    throw new Error(`貼文編輯器文字未正確寫入，實際：${textContent.slice(0, 100)}`);
  }
  console.log(`   ✅ 文案已寫入編輯器`);

  // 找「貼文 / Post」按鈕發布
  // 注意：FB 的「發布」按鈕 selector 經常變動，2026 通常是 div[aria-label*="發布"] 或 div[aria-label*="Post"]
  const submitBtn = page
    .locator('[aria-label="發布"], [aria-label="Post"], div[role="button"]:has-text("發布"), div[role="button"]:has-text("Post")')
    .last();
  await submitBtn.waitFor({ timeout: 10000 });
  await submitBtn.click();
  await page.waitForTimeout(5000); // 等 FB 處理

  console.log(`   ✅ 已送出（等待 FB 處理）`);
}

(async () => {
  console.log('🔌 連接到 Chrome DevTools Protocol:', CDP_URL);
  let browser;
  try {
    browser = await chromium.connectOverCDP(CDP_URL);
  } catch (err) {
    console.error('❌ 連接失敗：請確認 Chrome 已用 --remote-debugging-port=9222 啟動');
    console.error('   啟動指令：open -a "Google Chrome" --args --remote-debugging-port=9222');
    console.error('   錯誤訊息：', err.message);
    process.exit(1);
  }

  console.log('✅ 連線成功，找到 contexts:', browser.contexts().length);
  const context = browser.contexts()[0];
  if (!context) {
    console.error('❌ 找不到 context，請確認 Chrome 已登入 FB');
    process.exit(1);
  }

  // 找現有 page 或開新 page
  let page = context.pages()[0];
  if (!page) {
    page = await context.newPage();
  }
  console.log('📄 使用 page:', page.url() || '(空白)');

  // 先驗證是否已登入
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  const isLoggedIn = await page
    .locator('[aria-label="你的個人檔案"], [aria-label="Your profile"], [aria-label*="帳號"]')
    .first()
    .isVisible()
    .catch(() => false);
  if (!isLoggedIn) {
    console.error('❌ 看起來未登入 FB，請先確認 Chrome 已登入');
    process.exit(1);
  }
  console.log('✅ 已登入 FB');

  const logFile = path.resolve(__dirname, '../distill/curation_repost_log_2026-09-18.txt');
  fs.appendFileSync(logFile, `\n=== 開始 ${new Date().toISOString()} ===\n`);

  let successCount = 0;
  let failCount = 0;
  for (let i = 0; i < POSTS.length; i++) {
    try {
      await postOne(page, POSTS[i], i);
      successCount++;
      fs.appendFileSync(logFile, `[${new Date().toISOString()}] ✅ ${POSTS[i].title}\n`);
    } catch (err) {
      failCount++;
      const errMsg = `[${new Date().toISOString()}] ❌ ${POSTS[i].title} — ${err.message}\n`;
      fs.appendFileSync(logFile, errMsg);
      console.error(`❌ ${POSTS[i].title} 失敗：${err.message}`);
      // 不中斷，繼續下一則
      // 把錯誤截圖存起來
      try {
        const ssPath = path.resolve(__dirname, `../distill/repost_fail_${i + 1}_${Date.now()}.png`);
        await page.screenshot({ path: ssPath, fullPage: false });
        fs.appendFileSync(logFile, `   截圖：${ssPath}\n`);
      } catch {}
    }
  }

  fs.appendFileSync(logFile, `\n=== 完成 ${new Date().toISOString()} — 成功 ${successCount}/${POSTS.length}，失敗 ${failCount} ===\n`);

  console.log(`\n📊 結果：成功 ${successCount}/${POSTS.length}，失敗 ${failCount}`);
  console.log(`📝 記錄檔：${logFile}`);

  // 不關 browser，教練可以繼續用 Chrome
})();
