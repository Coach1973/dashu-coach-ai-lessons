#!/usr/bin/env node
/**
 * 刪除大台南策展中心粉專上「錯誤」的策展貼文
 * 識別規則（只看對錯，不分新舊）：
 *   - 抓粉專上所有 13 個 slug 標題的貼文
 *   - 對每則計算「event.bymyway.com/curated/<slug>」出現次數
 *   - 出現 2 次以上 = 重複網址 = 錯的 → 刪
 *   - 出現 1 次（單一網址）= 對的 → 留
 */

const { chromium } = require('playwright');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';
const PAGE_URL = 'https://www.facebook.com/GT.Curation/';

const SLUG_TITLES = {
  'everydaycaf-tai-nan-san-dian': ['EVERYDAY CAFÉ'],
  'flower-site': ["柚式藝術"],
  'fu-en-ping': ['傅恩平'],
  'historic-residence': ['六淨山房', '知事官邸'],
  'kangyenju': ['康燕居'],
  'nmda': ['中華新媒體影音發展協會', 'nmda'],
  'nmda-2': ['中華新媒體影音發展協會', 'nmda'],
  'peipei': ['陳佩君老師', '佩佩老師'],
  'sbip': ['楊仁豪'],
  'xiangjuchang': ['水交社眷村食堂', '相聚場'],
  'xiaonan': ['邱南寅'],
  'xie-wei-xiang': ['謝緯翔'],
  'zhang-yu-ci': ['張育慈', '順業肥料'],
};

function isSlugInText(slug, text) {
  const url = `event.bymyway.com/curated/${slug}`;
  const matches = text.match(new RegExp(url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || [];
  return matches.length;
}

async function deletePost(page, postPermalink, slug, reason) {
  console.log(`\n🗑️  [${slug}] 準備刪除 - 原因: ${reason}`);
  console.log(`   連結: ${postPermalink}`);

  const tab = await page.context().newPage();
  try {
    await tab.goto(postPermalink, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await tab.waitForTimeout(4000);

    // 找「⋯」按鈕（貼文右上角）
    let menuBtn = null;
    for (const sel of ['[aria-label="更多動作"]', '[aria-label="更多"]', '[aria-label="更多選項"]', '[aria-label="動作"]', '[aria-label="More"]']) {
      const el = tab.locator(sel).first();
      if (await el.isVisible({ timeout: 2000 }).catch(() => false)) {
        menuBtn = el;
        break;
      }
    }
    if (!menuBtn) {
      console.log('   ⚠️  找不到「⋯」按鈕，跳過');
      return false;
    }
    await menuBtn.click();
    await tab.waitForTimeout(2000);

    // 找「刪除」選單項
    let deleteItem = null;
    for (const sel of ['[role="menuitem"]:has-text("刪除")', 'span:has-text("刪除貼文")', 'span:has-text("刪除")', '[role="menuitem"]:has-text("Delete")']) {
      const el = tab.locator(sel).first();
      if (await el.isVisible({ timeout: 1500 }).catch(() => false)) {
        deleteItem = el;
        break;
      }
    }
    if (!deleteItem) {
      console.log('   ⚠️  找不到「刪除」選單項，跳過');
      await tab.keyboard.press('Escape');
      return false;
    }
    await deleteItem.click();
    await tab.waitForTimeout(2000);

    // 確認對話框的「刪除」按鈕
    let confirmBtn = null;
    for (const sel of ['div[role="dialog"] [aria-label="刪除"]', '[aria-label="刪除"]', 'div[role="dialog"] span:has-text("刪除")']) {
      const el = tab.locator(sel).last();
      if (await el.isVisible({ timeout: 2500 }).catch(() => false)) {
        confirmBtn = el;
        break;
      }
    }
    if (!confirmBtn) {
      console.log('   ⚠️  找不到確認對話框，按 ESC 中止');
      await tab.keyboard.press('Escape');
      return false;
    }
    await confirmBtn.click();
    await tab.waitForTimeout(3000);

    console.log(`   ✅ 已送出刪除指令`);
    return true;
  } catch (err) {
    console.log(`   ❌ 錯誤: ${err.message}`);
    return false;
  } finally {
    await tab.close();
  }
}

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('🔌 進粉專:', PAGE_URL);
  await page.goto(PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);

  // 滾動多次確保所有策展貼文都載入
  for (let i = 0; i < 8; i++) {
    await page.mouse.wheel(0, 1500);
    await page.waitForTimeout(1500);
  }

  // 抓所有貼文 article
  const posts = await page.evaluate(() => {
    const out = [];
    const articles = document.querySelectorAll('div[role="article"]');
    const seen = new Set();
    articles.forEach((el) => {
      if (seen.has(el)) return;
      seen.add(el);
      const txt = (el.innerText || '').replace(/\s+/g, ' ').trim();
      // 抓 permalink
      const linkEl = el.querySelector('a[href*="/posts/"], a[href*="/permalink/"]');
      const permalink = linkEl ? linkEl.href.split('?')[0] : '';
      if (txt.length > 20) {
        out.push({ permalink, text: txt });
      }
    });
    return out;
  });

  console.log(`\n📋 抓到 ${posts.length} 篇貼文（article 區塊）`);

  // 對每個 slug，找所有相關貼文並檢查 URL 計數
  const toDelete = [];
  const kept = [];

  for (const [slug, sigs] of Object.entries(SLUG_TITLES)) {
    const matched = posts.filter((p) => sigs.some((s) => p.text.includes(s)));
    matched.forEach((p) => {
      const count = isSlugInText(slug, p.text);
      const slugUrl = `event.bymyway.com/curated/${slug}`;
      const allUrls = (p.text.match(/event\.bymyway\.com\/curated\/[\w-]+/g) || []);
      const uniqUrls = [...new Set(allUrls)];

      if (count >= 2 || (count === 1 && uniqUrls.length > 1)) {
        toDelete.push({ slug, permalink: p.permalink, count, text: p.text.slice(0, 100) });
      } else if (count === 1) {
        kept.push({ slug, permalink: p.permalink, count, text: p.text.slice(0, 100) });
      } else {
        // 找不到 slug 對應 URL（可能是用其他 slug 但標題對）
        console.log(`   ⚠️  [${slug}] 標題對但找不到 ${slugUrl}`);
      }
    });
  }

  // 去重：同 permalink 多次計入只算一次
  const seenPerm = new Set();
  const toDeleteUnique = toDelete.filter((p) => {
    if (seenPerm.has(p.permalink)) return false;
    seenPerm.add(p.permalink);
    return true;
  });
  const keptPerm = new Set();
  const keptUnique = kept.filter((p) => {
    if (keptPerm.has(p.permalink)) return false;
    keptPerm.add(p.permalink);
    return true;
  });

  console.log(`\n🗑️  應刪除（重複網址/錯誤）: ${toDeleteUnique.length} 則`);
  toDeleteUnique.forEach((p) => console.log(`   - [${p.slug}] ${p.text}`));

  console.log(`\n✅ 保留（單一網址/正確）: ${keptUnique.length} 則`);
  keptUnique.forEach((p) => console.log(`   - [${p.slug}] ${p.text}`));

  // 儲存清單
  const logFile = '/Users/bymyway/.openclaw/workspace/distill/fb_wrong_posts_to_delete_2026-09-18.txt';
  const lines = [
    `=== 對錯判定清單 ${new Date().toISOString()} ===`,
    `總策展貼文: ${toDeleteUnique.length + keptUnique.length}`,
    `應刪除: ${toDeleteUnique.length}`,
    `保留: ${keptUnique.length}`,
    '',
    '--- 應刪除 ---',
    ...toDeleteUnique.map((p, i) => `[${i + 1}] slug=${p.slug} count=${p.count}\n    ${p.permalink}\n    ${p.text}`),
    '',
    '--- 保留 ---',
    ...keptUnique.map((p, i) => `[${i + 1}] slug=${p.slug} count=${p.count}\n    ${p.permalink}\n    ${p.text}`),
  ];
  fs.writeFileSync(logFile, lines.join('\n'));
  console.log(`\n📝 判定清單: ${logFile}`);

  // 開始刪除
  console.log('\n' + '='.repeat(80));
  console.log(`開始刪除 ${toDeleteUnique.length} 則錯誤貼文...`);
  console.log('='.repeat(80));

  let deleted = 0;
  for (let i = 0; i < toDeleteUnique.length; i++) {
    const p = toDeleteUnique[i];
    console.log(`\n[${i + 1}/${toDeleteUnique.length}]`);
    const ok = await deletePost(page, p.permalink, p.slug, `重複網址 (count=${p.count})`);
    if (ok) deleted++;
    await page.waitForTimeout(3500);  // 慢一點避免 FB rate limit
  }

  console.log(`\n📊 完成：應刪 ${toDeleteUnique.length} 則，成功 ${deleted} 則`);
  console.log(`📝 log: ${logFile}`);

  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
