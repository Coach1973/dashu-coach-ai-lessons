#!/usr/bin/env node
/**
 * 從 FB 內容資料庫（管理員視角）抓所有策展貼文
 * 規則：找出 13 個 slug 中「重複網址」的（錯的），刪除
 */

const { chromium } = require('playwright');
const fs = require('fs');

const CDP_URL = 'http://localhost:9222';
const MANAGE_URL = 'https://www.facebook.com/professional_dashboard/content/content_library/';

const SLUG_SIGNATURES = {
  'everydaycaf-tai-nan-san-dian': ['EVERYDAY CAFÉ'],
  'flower-site': ['柚式藝術'],
  'fu-en-ping': ['傅恩平'],
  'historic-residence': ['六淨山房', '知事官邸'],
  'kangyenju': ['康燕居'],
  'nmda': ['中華新媒體影音發展協會'],
  'nmda-2': ['中華新媒體影音發展協會'],
  'peipei': ['陳佩君老師', '佩佩老師'],
  'sbip': ['楊仁豪'],
  'xiangjuchang': ['水交社眷村食堂', '相聚場'],
  'xiaonan': ['邱南寅'],
  'xie-wei-xiang': ['謝緯翔'],
  'zhang-yu-ci': ['張育慈', '順業肥料'],
};

async function deletePost(page, postPermalink, slug, reason) {
  console.log(`\n🗑️  [${slug}] 原因: ${reason}`);
  const tab = await page.context().newPage();
  try {
    await tab.goto(postPermalink, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await tab.waitForTimeout(4000);

    let menuBtn = null;
    for (const sel of ['[aria-label="更多動作"]', '[aria-label="更多"]', '[aria-label="更多選項"]', '[aria-label="動作"]', '[aria-label="More"]']) {
      const el = tab.locator(sel).first();
      if (await el.isVisible({ timeout: 2000 }).catch(() => false)) {
        menuBtn = el;
        break;
      }
    }
    if (!menuBtn) {
      console.log('   ⚠️  找不到「⋯」');
      return false;
    }
    await menuBtn.click();
    await tab.waitForTimeout(2000);

    let deleteItem = null;
    for (const sel of ['[role="menuitem"]:has-text("刪除")', 'span:has-text("刪除貼文")', 'span:has-text("刪除")']) {
      const el = tab.locator(sel).first();
      if (await el.isVisible({ timeout: 1500 }).catch(() => false)) {
        deleteItem = el;
        break;
      }
    }
    if (!deleteItem) {
      console.log('   ⚠️  找不到「刪除」選單');
      await tab.keyboard.press('Escape');
      return false;
    }
    await deleteItem.click();
    await tab.waitForTimeout(2000);

    let confirmBtn = null;
    for (const sel of ['div[role="dialog"] [aria-label="刪除"]', '[aria-label="刪除"]', 'div[role="dialog"] span:has-text("刪除")']) {
      const el = tab.locator(sel).last();
      if (await el.isVisible({ timeout: 2500 }).catch(() => false)) {
        confirmBtn = el;
        break;
      }
    }
    if (!confirmBtn) {
      console.log('   ⚠️  找不到確認對話框');
      await tab.keyboard.press('Escape');
      return false;
    }
    await confirmBtn.click();
    await tab.waitForTimeout(3000);
    console.log('   ✅ 已送出刪除');
    return true;
  } catch (err) {
    console.log('   ❌ 錯誤:', err.message.slice(0, 100));
    return false;
  } finally {
    await tab.close();
  }
}

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  console.log('🔌 進內容資料庫');
  await page.goto(MANAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(6000);

  // 滾動多次觸發 lazy load
  for (let i = 0; i < 10; i++) {
    await page.mouse.wheel(0, 2000);
    await page.waitForTimeout(1500);
  }

  // 抓所有貼文區塊
  const posts = await page.evaluate(() => {
    const out = [];
    // 內容資料庫每則貼文是 article 或 div 內含時間戳
    const articles = document.querySelectorAll('div[role="article"]');
    articles.forEach((el) => {
      const txt = (el.innerText || '').replace(/\s+/g, ' ').trim();
      const linkEl = el.querySelector('a[href*="/posts/"]');
      const permalink = linkEl ? linkEl.href.split('?')[0] : '';
      // 抓「已發佈 • 時間」標籤
      const timeMatch = txt.match(/(今天上午|今天下午|\d+\s*小時前|\d+\s*分鐘前|\d+\s*天前|\d+\/\d+)/);
      const time = timeMatch ? timeMatch[1] : '';
      if (txt.length > 30) {
        out.push({ permalink, time, text: txt.slice(0, 400) });
      }
    });
    return out;
  });

  console.log(`\n📋 抓到 ${posts.length} 篇貼文`);

  // 過濾策展 + 計算 URL 重複
  const toDelete = [];
  const kept = [];
  const seen = new Set();

  for (const p of posts) {
    if (!p.permalink || seen.has(p.permalink)) continue;
    let matchedSlug = null;
    for (const [slug, sigs] of Object.entries(SLUG_SIGNATURES)) {
      if (sigs.some((s) => p.text.includes(s))) {
        matchedSlug = slug;
        break;
      }
    }
    if (!matchedSlug) continue;
    seen.add(p.permalink);

    const slugUrl = `event.bymyway.com/curated/${matchedSlug}`;
    const allUrls = (p.text.match(/event\.bymyway\.com\/curated\/[\w-]+/g) || []);
    const uniqUrls = [...new Set(allUrls)];
    const slugUrlCount = allUrls.filter((u) => u === slugUrl).length;

    const entry = { slug: matchedSlug, permalink: p.permalink, time: p.time, slugCount: slugUrlCount, uniqCount: uniqUrls.length, text: p.text.slice(0, 80) };

    if (slugUrlCount >= 2 || uniqUrls.length > 1) {
      toDelete.push(entry);
    } else if (slugUrlCount === 1) {
      kept.push(entry);
    } else {
      // 找不到自己 slug 的 URL，但標題對 — 可能被截斷或格式不同
      console.log(`   ⚠️  [${matchedSlug}] 標題對但找不到 ${slugUrl}，text 開頭: ${p.text.slice(0, 100)}`);
    }
  }

  console.log(`\n🗑️  應刪除（重複網址）: ${toDelete.length} 則`);
  toDelete.forEach((p) => console.log(`   - [${p.slug}] slugCount=${p.slugCount} uniq=${p.uniqCount} ${p.time} | ${p.text}`));
  console.log(`\n✅ 保留（單一網址）: ${kept.length} 則`);
  kept.forEach((p) => console.log(`   - [${p.slug}] ${p.time} | ${p.text}`));

  // 寫清單
  const logFile = '/Users/bymyway/.openclaw/workspace/distill/fb_delete_v2_log_2026-09-18.txt';
  fs.writeFileSync(logFile, [
    `=== 內容資料庫掃描 ${new Date().toISOString()} ===`,
    `總策展貼文: ${toDelete.length + kept.length}`,
    `應刪: ${toDelete.length}, 保留: ${kept.length}`,
    '',
    '--- 應刪 ---',
    ...toDelete.map((p) => `[${p.slug}] ${p.time} ${p.permalink} (slug×${p.slugCount}, uniq=${p.uniqCount})`),
    '',
    '--- 保留 ---',
    ...kept.map((p) => `[${p.slug}] ${p.time} ${p.permalink} (slug×${p.slugCount})`),
  ].join('\n'));
  console.log(`\n📝 log: ${logFile}`);

  // 開始刪除
  console.log('\n開始刪除...');
  let deleted = 0;
  for (let i = 0; i < toDelete.length; i++) {
    const p = toDelete[i];
    console.log(`\n[${i + 1}/${toDelete.length}]`);
    const ok = await deletePost(page, p.permalink, p.slug, `slug×${p.slugCount} uniq=${p.uniqCount}`);
    if (ok) deleted++;
    await page.waitForTimeout(4000);
  }

  console.log(`\n📊 應刪 ${toDelete.length} 則，成功 ${deleted} 則`);
  await browser.close();
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
