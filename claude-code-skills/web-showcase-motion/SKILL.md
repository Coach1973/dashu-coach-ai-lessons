---
name: web-showcase-motion
description: 教練要做「品牌展示型網頁」的動態手法時使用——「做像 taroil 那種展示網頁」「滾輪數字」「滿版影片捲動縮成卡片」「跑馬燈客戶牆」「文字升起」「開場動畫」「頁面轉場」「圖片載入不跳版」。拆自 www.taroil.studio（2026-11-03 用 REA 拆解），收錄 7 招：縮框開場、滾輪數字、純 CSS 跑馬燈、文字升起、頁面簾幕轉場、取景器開場、圖片清單防跳版。只學做法，不搬原站的文字、圖片、商標。
---

# 品牌展示網頁動態手法（拆自 taroil.studio）

來源：`https://www.taroil.studio/`（台中設計工作室，Nuxt／Vue＋GSAP）。拆解日期 2026-11-03，用 `bigtree-web-feature-clone` 的流程（REA＋獨立除錯 Chrome）。技法庫另有 7 招（捲軸控制影片、粒子波浪等）在 `https://event.bymyway.com/curated/reverse-skill/`，這裡只放那一頁**沒有**的。

**原則（原站每一招都遵守，做的時候也要）**
1. 先給靜態版，動畫只加分：預設就看得到內容，`prefers-reduced-motion: reduce` 一律直接顯示最終狀態。
2. 進畫面才動：用 IntersectionObserver，離開畫面就暫停或不載入。
3. 重的東西晚點載：GSAP 用動態 import、影片 `preload="none"`＋poster、圖片進畫面前 320px 才載。
4. 無障礙文字另放一份（數字滾輪的 `sr-only` 版）。
5. 手機另一組數字（縮框 inset／圓角在 ≤850px 換）。

---

## 招 A｜捲動縮框開場（滿版影片縮成圓角卡片）
適合：品牌首頁第一屏、讓人從「沉浸」進到「內容」。
**怎麼做**：第一屏是滿版影片＋45% 黑色蓋層＋大標。往下捲時，影片層從滿版縮到比螢幕小一圈（每邊 10px、手機 14px，**最小不低於 0.94 倍**），圓角同時從 0 長到 18px（手機 22px）。捲 **1.55 個螢幕高** 縮完，用 `sine.inOut` 緩動，`scrub .45` 讓動畫慢半拍跟上捲軸（有阻尼感）。
**關鍵數字**：縮到 ≥0.94、圓角 18／22px、捲動距離 1.55×視窗高、scrub 0.45、影片 `muted loop playsinline preload="none"` ＋ webp poster，canplay 後才 play。
**GSAP 版**（原站做法，gsap 用 `await import()` 延後載入）：
```js
gsap.to(media,{scaleX:()=>Math.max((box.clientWidth-inset*2)/box.clientWidth,.94),
  scaleY:()=>Math.max((box.clientHeight-inset*2)/box.clientHeight,.94),
  borderRadius:radius+'px',force3D:true,ease:'sine.inOut',
  scrollTrigger:{trigger:box,start:'top top',end:()=>'+='+Math.round(innerHeight*1.55),scrub:.45,invalidateOnRefresh:true}});
```
**不用套件版**（已在瀏覽器實測：捲到 0.8 屏 scale≈0.969、半徑≈11.5px；捲到 1.6 屏 scale≈0.941、半徑 22px）：`scroll` 事件算進度 `t=clamp(scrollY/(innerHeight*1.55))`，每幀 `cur+=(t-cur)*.18` 做阻尼，`e=-(cos(πt)-1)/2`，`transform:scale(sx,sy)`、`borderRadius=radius*e`。CSS：`.media{transform-origin:50%;will-change:transform,border-radius;contain:paint}`，外層 `overflow:hidden`。
**注意**：蓋層要 `border-radius:inherit`，不然縮小後蓋層的直角會露出來。

## 招 B｜滾輪數字（純 CSS，不用數字動畫程式）
適合：「60+ 完成專案」「30+ 合作品牌」這類成績區；比「從 0 數到目標」更有質感。
**怎麼做**：每一位數字是一條直立的「滾輪」（0–9 重複疊三輪＝30 格，每格高 1em），外框 `overflow:hidden; height:1em`。滾輪初始停在第三輪對應位置 `translateY(calc(var(--end)*-1em))`，其中 `--end = 20 + 該位數字`。進畫面時先把滾輪歸零（`ready`＝停在第一輪 0），一個 frame 後切 `running`，加上 transition，滾輪就從 0 滾到目標（共滾過 20 格以上，看起來像里程表飛轉）。
**關鍵數字**：1 秒、`cubic-bezier(.16,1,.3,1)`（衝快停穩）、延遲＝`--stat`×70ms＋`--pos`×45ms（一個數字接一個、同一數字由左到右）、IntersectionObserver `threshold .25`。
**狀態機**：`data-motion` ＝ `static`（沒動畫、直接顯示終值）→ `ready` → `running` →（最後一個滾輪 `transitionend`）`settled`。reduced-motion 或不支援 IO 就維持 `static`。
```css
.stat-digit{display:inline-block;width:.6em;height:1em;overflow:hidden}
.stat-reel{display:block;transform:translateY(calc(var(--end)*-1em))}
.stat-reel>span{display:block;height:1em}
[data-motion=ready]   .stat-reel{transform:translateY(0)}
[data-motion=running] .stat-reel{transition:transform 1s cubic-bezier(.16,1,.3,1);
  transition-delay:calc(var(--stat)*70ms + var(--pos)*45ms)}
```
產生 DOM：`<span class="sr-only">60+</span><span aria-hidden>…每位數字一個 .stat-digit>.stat-reel(30 個 <span>i%10</span>)…</span>`（螢幕閱讀器念 sr-only 那份）。
**已驗證**：60／30／8／5 四組在瀏覽器實測，滾輪最終停在正確數字。多位數寬度用 `.6em`（等寬字型不需要，比例字型看 tabular-nums）。

## 招 C｜純 CSS 無限跑馬燈（客戶 Logo 牆）
適合：合作品牌、媒體報導、客戶名單。
**怎麼做**：同一組內容**複製兩份**並排放在 `width:max-content` 的軌道裡，動畫從 `translateX(0)` 到 `translateX(-50%)`（正好一份寬，接縫無感），`linear infinite`，**一開始 `paused`**；IntersectionObserver 看到容器進畫面才加 `is-active` 把 `animation-play-state` 改 `running`；滑鼠移上去暫停；reduced-motion 直接 `animation:none`。
**關鍵數字**：一圈 18 秒；複製的第二份加 `aria-hidden`；圖片 `src` 要進畫面前 320px 才給（`rootMargin:'320px 0px'`），之前先留空。
**已驗證**：捲進畫面後 `is-active` 變 true。

## 招 D｜文字升起（clip-path＋位移，依序延遲）
適合：段落、標題進場。
**怎麼做**：初始 `opacity:0; clip-path:inset(0 0 100%); transform:translateY(28px)`（文字被裁光、往下偏），進畫面加 `.in` → `opacity:1; clip-path:inset(0); transform:none`，`.9s cubic-bezier(.16,1,.3,1)`。同一批元素依 DOM 順序給 `--d: i*120ms` 的延遲。原站另有 `data-reveal-skip` 讓第一屏元素不排隊。
**🔴 踩到的坑（我自己測到的）**：IntersectionObserver 會把元素**自己的 clip-path** 算進可見面積——被裁光的元素 `intersectionRatio` 永遠是 0，所以 `threshold:0.3` **永遠不會觸發**，字永遠不出現。解法：`threshold:0`（ratio 0 仍算 `isIntersecting`），搭 `rootMargin:'0px 0px -12% 0px'` 讓它進到畫面下緣上方一點再升起；或改觀察外層容器，把 clip-path 放內層。
`@media (prefers-reduced-motion:reduce){[data-reveal]{opacity:1;clip-path:none;transform:none}}` 一定要加。

## 招 E｜頁面轉場簾幕
適合：多頁網站（Nuxt／Vue Router 這類單頁應用）切頁。
**怎麼做**：切頁時一塊品牌色的簾幕用 Web Animations API 從下往上蓋住（`translateY(100%)→0`，**460ms**），新頁面載好後簾幕往上離開（`0→-100%`，**500ms**），`cubic-bezier(.645,.045,.355,1)`，`fill:'forwards'`。用計數器（每次進場 `++token`）擋掉快速連點造成的動畫打架；偵測到 reduced-motion 或沒有 `element.animate` 就直接換頁。
```js
const ease='cubic-bezier(.645,.045,.355,1)';
const slide=(el,a,b,ms)=>el.animate([{transform:`translateY(${a})`},{transform:`translateY(${b})`}],{duration:ms,easing:ease,fill:'forwards'}).finished;
await slide(curtain,'100%','0%',460);   // 蓋上
/* …換內容… */
await slide(curtain,'0%','-100%',500);  // 離開
```
（這招本場沒做成測試頁，數字來自程式碼，用到時請實測。）

## 招 F｜取景器開場動畫（品牌敘事用）
適合：攝影、影像、設計類品牌，第一次造訪的開場 2～3 秒。
**怎麼做**：全螢幕深色層（`intro-scene`），依序播：取景框淡入（`viewfinder-arrive`）→ 對焦框四個角＋十字準心從 1.1 倍縮到 1 倍並「對焦」（`focus-hunt`，logo 從 blur(22px) 變清楚 `logo-hunt`）→ 鎖定時準心放大淡出像脈衝（`lock-pulse` 0.55→3.8 倍）→ 快門閃一下（`shutter-click`，透明度 0→.16→0）→ 品牌色簾幕升起蓋過（`orange-rise` translateY 100%→0→-100%）→ 整層淡出（`viewfinder-leave`）。全部是純 CSS `@keyframes`，用 `is-boot` 之類的 class 控制，播完移除節點。
**要點**：把它當「每個瀏覽器只看一次」（sessionStorage 記旗標，要 try/catch）；整段 ≤3 秒、點擊或按鍵可跳過；reduced-motion 直接不播。**這一招的意象（相機取景）是 Taroil 的品牌，換成別人的產品要換成自己的隱喻（例如茶：蒸氣升起、水墨暈開），不要照搬取景器造型。**
（本招只讀了 CSS 關鍵影格，沒有逐幀實測。）

## 招 G｜圖片清單防跳版（主色＋尺寸＋多寬度）
適合：圖多的作品集頁（原站一頁 64 張圖）。
**怎麼做**：建置時把每張圖的資料存成一份清單：`{路徑:{c:'#主色', w:寬, h:高, v:[960,1920,2880]}}`。頁面用 `w/h` 預留版面（`aspect-ratio`），圖還沒載入前先顯示主色當底，載入後淡入；`v` 是這張圖有哪幾種寬度的檔，組出 `srcset`。這樣圖慢載也不會「整頁往下跳」，也不會在手機下載 2880 寬。
**我們可以怎麼用**：策展頁圖多時，上架程式順手產生這份清單；`<img>` 一律帶 `width/height`、`loading="lazy"`、`decoding="async"`。
（本招看的是原站資料檔的結構；產生清單的程式它沒公開，要自己寫。）

---

## 用法
1. 教練說「做像 taroil 那樣的展示網頁」「加滾輪數字／跑馬燈／縮框開場」→ 直接從上面挑招，不問要不要。
2. 套進頁面前先跑 `module_kit.py menu` 對照大樹標準模組；全頁最小字 20px；頁尾四連結照 `bigtree-web-edit`。
3. **寫完必須實測**：本機起測試伺服器（不要用 8765、5060，改用 8791 這類埠），用內建瀏覽器切到前景後再量（瀏覽器窗格在背景時 `requestAnimationFrame` 不跑、IntersectionObserver 不回呼，會誤判成「壞了」）。量法：滾到位置後讀 `getComputedStyle` 的 transform／opacity，不靠截圖。
4. 已實測的完整範例（招 A～D）在同資料夾 `demo.html`，直接複製改字即可。
5. 重做用自己的文字、圖片、品牌，不搬 taroil 的內容。

## 這份拆解沒做到的
- 沒有跑真手機測；招 E、F、G 只讀程式／CSS，沒做成可操作的測試頁。
- 沒登入或後台，原站的聯絡表單、作品詳情頁（動態路由）沒拆。
- 原站是 Nuxt 單頁應用，我們的策展頁多為單檔 HTML，招 E 要改成自己的換頁方式才用得上。
