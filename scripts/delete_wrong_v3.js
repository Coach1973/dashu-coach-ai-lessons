#!/usr/bin/env node
/**
 * 從內容資料庫抓所有策展貼文（從 body.innerText 解析，不用 article selector）
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

async function scrapeAllPosts(page) {
  await page.goto(MANAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(6000);

  // 從「過去 28 天」改抓「過去 90 天」看更多
  // 找時間範圍選擇器
  const rangeBtn = page.locator('text=/過去\\s*\\d+\\s*天/').first();
  if (await rangeBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await rangeBtn.click();
    await page.waitForTimeout(1500);
    // 試著選 90 天
    const opt90 = page.locator('text=/過去\\s*90\\s*天/').first();
    if (await opt90.isVisible({ timeout: 1500 }).catch(() => false)) {
      await opt90.click();
      await page.waitForTimeout(3000);
    } else {
      await page.keyboard.press('Escape');
    }
  }

  // 滾動到底（多次）
  for (let i = 0; i < 12; i++) {
    await page.mouse.wheel(0, 2000);
    await page.waitForTimeout(1500);
  }

  // 抓 body.innerText 全文 + 所有 permalink
  const result = await page.evaluate(() => {
    const allText = document.body.innerText || '';
    const links = Array.from(document.querySelectorAll('a[href*="/posts/"]'));
    const permalinks = [...new Set(links.map((a) => a.href.split('?')[0]))];
    return { allText, permalinks };
  });

  // 用「已發佈 • 時間」當分隔符切
  const segments = result.allText.split(/已發佈\s*[•·]\s*/).filter(Boolean);
  const posts = [];
  for (const seg of segments) {
    const firstLine = seg.slice(0, 30);
    // 時間戳：抓開頭到第一個 \n 或 30 字
    let time = '';
    const timeMatch = seg.match(/^(今天上午[\d:]+|今天下午[\d:]+|昨天上午[\d:]+|\d+\s*小時前|\d+\s*分鐘前|\d+\/\d+|\d+月\d+日)/);
    if (timeMatch) time = timeMatch[1];
    posts.push({ text: seg.slice(0, 600), time });
  }

  console.log(`全文 ${result.allText.length} 字，permalinks ${result.permalinks.length} 個，分段 ${posts.length} 段`);
  return { posts, permalinks: result.permalinks, fullText: result.allText };
}

async function deletePost(page, postPermalink, slug, reason) {
  console.log(`\n🗑️  [${slug}] 原因: ${reason}`);
  console.log(`   ${postPermalink}`);
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
    if (!menuBtn) { console.log('   ⚠️  找不到「⋯」'); return false; }
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
    if (!deleteItem) { console.log('   ⚠️  找不到「刪除」'); await tab.keyboard.press('Escape'); return false; }
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
    if (!confirmBtn) { console.log('   ⚠️  找不到確認'); await tab.keyboard.press('Escape'); return false; }
    await confirmBtn.click();
    await tab.waitForTimeout(3000);
    console.log('   ✅ 已送出');
    return true;
  } catch (err) {
    console.log('   ❌', err.message.slice(0, 80));
    return false;
  } finally {
    await tab.close();
  }
}

(async () => {
  const browser = await chromium.connectOverCDP(CDP_URL);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  const { posts, permalinks, fullText } = await scrapeAllPosts(page);

  // 把 permalink 跟貼文區段對齊（啟發式：每段的「已發佈」前的時間，跟 permalink 順序對應）
  console.log(`\n📊 共 ${posts.length} 則分段，${permalinks.length} 個 permalinks`);
  // 簡化：直接把 permalink 按出現順序分配給分段（假設順序一致）
  const postsWithPermalink = posts.map((p, i) => ({
    ...p,
    permalink: permalinks[i] || '',
  }));

  // 過濾策展 + 判定對錯
  const toDelete = [];
  const kept = [];
  const seen = new Set();

  for (const p of postsWithPermalink) {
    if (!p.permalink || seen.has(p.permalink)) continue;
    let matchedSlug = null;
    for (const [slug, sigs] of Object.entries(SLUG_SIGNATURES)) {
      if (sigs.some((s) => p.text.includes(s))) { matchedSlug = slug; break; }
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
      console.log(`   ⚠️  [${matchedSlug}] 沒找到 URL`);
    }
  }

  console.log(`\n🗑️  應刪: ${toDelete.length}`);
  toDelete.forEach((p) => console.log(`   - [${p.slug}] slug×${p.slugCount} uniq=${p.uniqCount} ${p.time} | ${p.text}`));
  console.log(`\n✅ 保留: ${kept.length}`);
  kept.forEach((p) => console.log(`   - [${p.slug}] ${p.time} | ${p.text}`));

  const logFile = '/Users/bymyway/.openclaw/workspace/distill/fb_delete_v3_log_2026-09-18.txt';
  fs.writeFileSync(logFile, [
    `=== v3 掃描 ${new Date().toISOString()} ===`,
    `應刪: ${toDelete.length}, 保留: ${kept.length}`,
    '',
    '--- 應刪 ---',
    ...toDelete.map((p) => `[${p.slug}] ${p.time} ${p.permalink} (slug×${p.slugCount}, uniq=${p.uniqCount})`),
    '',
    '--- 保留 ---',
    ...kept.map((p) => `[${p.slug}] ${p.time} ${p.permalink}`),
  ].join('\n'));
  console.log(`\n📝 log: ${logFile}`);

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
