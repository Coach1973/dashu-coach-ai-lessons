#!/usr/bin/env node
/**
 * 大台南策展中心 — 13 則歷史隱形貼文重貼腳本 v4（event.bymyway.com 正式站）
 * 進 FB 首頁 → 點「建立貼文」 → 寫文案 → 點「繼續」 → 點「發布」
 *
 * 前置：Chrome 已用 --remote-debugging-port=9222 啟動
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';

const POSTS = [
  {
    title: 'EVERYDAY CAFÉ 台南三店',
    desc: '生吐司早午餐．勝利店・海安店・陽光公園店',
    slug: 'everydaycaf-tai-nan-san-dian',
  },
  {
    title: "柚式藝術 Yo's Art（張騰文）",
    desc: '讓每一朵花，留住最好的那一刻。永生花 ｜ 鈔票花禮 ｜ 韓式氣球 ｜ 婚禮派派佈置。台南 · 屏東 ｜ 全省安全宅配。',
    slug: 'flower-site',
  },
  {
    title: '傅恩平｜商務英漢通譯',
    desc: '兩種語言之間，總要有人站著。臺南善化，榮益齋。',
    slug: 'fu-en-ping',
  },
  {
    title: '六淨山房 · 知事官邸古蹟餐廳',
    desc: '百年官邸 · 茶香咖啡 · 光影時光。一日兩時，與自己重逢。',
    slug: 'historic-residence',
  },
  {
    title: '康燕居（燕窩）',
    desc: '一盞燕窩，四百年的講究',
    slug: 'kangyenju',
  },
  {
    title: '中華新媒體影音發展協會（nmda v1）',
    desc: '讓專業被看見，讓合作真正發生',
    slug: 'nmda',
  },
  {
    title: '中華新媒體影音發展協會（nmda v2）',
    desc: '讓專業被看見，讓合作真正發生',
    slug: 'nmda-2',
  },
  {
    title: '陳佩君老師（佩佩老師）',
    desc: '鋼琴家・音樂教育家',
    slug: 'peipei',
  },
  {
    title: '楊仁豪 — 品牌 IP 規劃師',
    desc: '不只申請權利，更為你的品牌打造智慧資產的護城河。懂商業的智財專家，守護你的品牌資產。',
    slug: 'sbip',
  },
  {
    title: '水交社眷村食堂 — 相聚場',
    desc: '在府城南郊的水交社眷村文化園區中，質樸不假裝飾的眷落。手工拉麵、慢燉牛腱、中藥材熬煮的湯頭。',
    slug: 'xiangjuchang',
  },
  {
    title: '邱南寅・小南雕刻',
    desc: '龍益宗教文物 — 一面牌位，一部家族的故事',
    slug: 'xiaonan',
  },
  {
    title: '謝緯翔｜理賠領航員',
    desc: '九年前，他自己的理賠單從 60 萬被砍到 18 萬。從那天起，他決定學會整套規則——不讓同樣的事發生在別人身上。',
    slug: 'xie-wei-xiang',
  },
  {
    title: '張育慈｜順業肥料資材行',
    desc: '從土壤到餐桌。彰化溪州，三十年的肥料家業，第二代的接棒。',
    slug: 'zhang-yu-ci',
  },
];

const HASHTAGS = '#大台南策展中心 #大樹教練產業鍊';

function buildPostBody(p) {
  const url = `https://event.bymyway.com/curated/${p.slug}/`;
  // FB 會自動抓 og:title/og:description/og:image 展開 preview card
  // 文案只放簡短描述 + URL + hashtag
  return `${p.title}\n\n${p.desc}\n\n👉 完整介紹：${url}\n\n${HASHTAGS}`;
}

async function postOne(page, post, idx, logFile) {
  console.log(`\n[${idx + 1}/${POSTS.length}] 開始：${post.title}`);

  // 進 FB 首頁
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 點首頁「建立貼文」（aria-label="建立貼文"）
  const createBtn = page.locator('[aria-label="建立貼文"]').first();
  await createBtn.waitFor({ timeout: 10000 });
  await createBtn.click();
  await page.waitForTimeout(3000);

  // 找貼文編輯器（Draft.js / contenteditable）
  const editor = page.locator('[role="textbox"][contenteditable="true"]').first();
  await editor.waitFor({ timeout: 10000 });
  await editor.click();
  await page.waitForTimeout(500);

  // Draft.js 對合成鍵盤事件沒反應 — 改用 page.evaluate 直接寫 innerText
  const body = buildPostBody(post);
  await editor.evaluate((el, text) => {
    el.focus();
    const sel = window.getSelection();
    sel.removeAllRanges();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    sel.addRange(range);
    document.execCommand('insertText', false, text);
    el.dispatchEvent(new InputEvent('input', { bubbles: true, cancelable: true, inputType: 'insertText', data: text }));
  }, body);
  await page.waitForTimeout(2000);

  const textContent = await editor.textContent();
  if (!textContent.includes(post.title.slice(0, 10))) {
    throw new Error(`編輯器文字未寫入，實際：${textContent.slice(0, 100)}`);
  }
  console.log('   ✅ 文案已寫入');

  // FB 2026+ 兩階段 modal：先點「繼續」進到 stage 2，stage 2 才有「發布」
  const continueBtn = page.locator('[aria-label="繼續"]').first();
  const continueVisible = await continueBtn.isVisible({ timeout: 3000 }).catch(() => false);
  if (continueVisible) {
    console.log('   點「繼續」進 stage 2...');
    await continueBtn.click();
    await page.waitForTimeout(4000);
  }

  // 找發布按鈕（stage 2 才會出現）— 注意：FB 2026+ 是繁體「發佈」不是簡體「發布」
  const submitBtn = page
    .locator('[aria-label="發佈"], [aria-label="Post"], [aria-label="分享"], [aria-label="Share"]')
    .last();
  await submitBtn.waitFor({ timeout: 10000 });
  await submitBtn.click();
  await page.waitForTimeout(6000);

  console.log('   ✅ 已送出');
  fs.appendFileSync(logFile, `[${new Date().toISOString()}] ✅ ${post.title}\n`);
}

(async () => {
  console.log('🔌 連接 CDP:', CDP_URL);
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  if (!context) { console.error('❌ 找不到 context'); process.exit(1); }

  let page = context.pages()[0] || await context.newPage();
  console.log('📄 page:', page.url() || '(空白)');

  // 先驗證登入
  await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  const isLoggedIn = await page.locator('[aria-label="建立貼文"]').first().isVisible({ timeout: 5000 }).catch(() => false);
  if (!isLoggedIn) { console.error('❌ 看起來未登入'); process.exit(1); }
  console.log('✅ 已登入 FB');

  const logFile = path.resolve(__dirname, '../distill/curation_repost_log_2026-09-18.txt');
  fs.appendFileSync(logFile, `\n=== v4 (event.bymyway.com URLs) 開始 ${new Date().toISOString()} ===\n`);

  let success = 0, fail = 0;
  for (let i = 0; i < POSTS.length; i++) {
    try {
      await postOne(page, POSTS[i], i, logFile);
      success++;
    } catch (err) {
      fail++;
      const errMsg = `[${new Date().toISOString()}] ❌ ${POSTS[i].title} — ${err.message}\n`;
      fs.appendFileSync(logFile, errMsg);
      console.error(`❌ ${POSTS[i].title}：${err.message}`);
      try {
        const ss = path.resolve(__dirname, `../distill/repost_fail_${i + 1}_${Date.now()}.png`);
        await page.screenshot({ path: ss });
        fs.appendFileSync(logFile, `   截圖：${ss}\n`);
      } catch {}
    }
  }

  fs.appendFileSync(logFile, `\n=== 完成 ${new Date().toISOString()} — 成功 ${success}/${POSTS.length}，失敗 ${fail} ===\n`);
  console.log(`\n📊 成功 ${success}/${POSTS.length}，失敗 ${fail}`);
  console.log(`📝 log: ${logFile}`);
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
