# 輪播/滑動元件 SOP（標準作業程序）

> 教練親定 2026-06-05，所有 AI 助教強制遵守。
> 本 SOP 源自 theunrestrictedwar.netlify.app 號外輪播的慘痛教訓（案例 R），一次就做對。
> 核心理念：瀏覽器原生 API > 自己寫的 transform 動畫（守則#16）

---

## 🎯 設計鐵律（一行話記住）

> **所有輪播/滑動切換元件，一律用「原生水平滾動 + scrollTo」組合，禁用 transform + flex 自製動畫。**

---

## 📦 HTML 標準結構

```html
<!-- 三層：外層容器 / track（滾動區） / 卡片 -->
<div class="overflow-x-auto overflow-y-hidden w-full snap-x snap-mandatory"
     id="track"
     style="scroll-behavior: smooth; -webkit-overflow-scrolling: touch;">

    <div class="item flex-shrink-0 snap-start" 
         style="width: 100%; min-width: 100%;">
        卡片 1 內容
    </div>
    <div class="item flex-shrink-0 snap-start" 
         style="width: 100%; min-width: 100%;">
        卡片 2 內容
    </div>
    <!-- 更多卡片... -->
</div>
```

### 關鍵 class 與 style 對照

| 元素 | 設定 | 作用 |
|------|------|------|
| **track** | `overflow-x-auto` | 原生水平滾動條 |
| | `overflow-y-hidden` | 防止垂直滾動干擾 |
| | `snap-x snap-mandatory` | 滾動自動對齊到卡邊界 |
| | `scroll-behavior: smooth` | 按鈕點擊平滑滾動 |
| | `-webkit-overflow-scrolling: touch` | iOS Safari 慣性滾動 |
| **item（卡片）** | `flex-shrink-0` | 不被 flex 壓縮 |
| | `snap-start` | 滾動停止時對齊到卡左緣 |
| | `width: 100%; min-width: 100%` | 每張卡占滿 track 寬度 |

---

## 🎛️ JavaScript 標準邏輯

### 取得 DOM 元素
```javascript
const track = document.getElementById('track');
const items = track ? track.querySelectorAll('.item') : [];
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageCounter = document.getElementById('pageCounter');
let currentIndex = 0;
const totalItems = items.length;
```

### 每頁顯示幾張（perView）
```javascript
function getPerView() {
    // 卡片少時（≤ 2 張）永遠 1 張，確保按鈕可切換（maxIndex > 0）
    // 卡片多時（≥ 3 張）保留原本設計：桌面 2 張、手機 1 張
    if (totalItems <= 2) return 1;
    return window.innerWidth >= 768 ? 2 : 1;
}
```

### 更新畫面（核心）
```javascript
function updateCarousel() {
    const perView = getPerView();
    const maxIndex = Math.max(0, totalItems - perView);
    currentIndex = Math.max(0, Math.min(currentIndex, maxIndex));

    // 🔑 核心：scrollTo 控制頁面切換，瀏覽器原生處理所有複雜度
    const trackWidth = track.clientWidth;
    if (track.clientWidth > 0) {
        track.scrollTo({ 
            left: currentIndex * trackWidth, 
            behavior: 'smooth' 
        });
    }

    // 頁數計數
    pageCounter.textContent = 
        String(currentIndex + 1).padStart(2, '0') + ' / ' + 
        String(maxIndex + 1).padStart(2, '0');

    // 邊界按鈕的視覺反饋（在邊界時半透明 + 不可點）
    const atStart = currentIndex === 0;
    const atEnd = currentIndex >= maxIndex;
    [prevBtn].forEach(btn => {
        if (btn) {
            btn.style.opacity = atStart ? '0.3' : '1';
            btn.style.cursor = atStart ? 'default' : 'pointer';
            btn.disabled = atStart;
        }
    });
    [nextBtn].forEach(btn => {
        if (btn) {
            btn.style.opacity = atEnd ? '0.3' : '1';
            btn.style.cursor = atEnd ? 'default' : 'pointer';
            btn.disabled = atEnd;
        }
    });
}
```

### 按鈕事件
```javascript
prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
    }
});
nextBtn.addEventListener('click', () => {
    const perView = getPerView();
    if (currentIndex < totalItems - perView) {
        currentIndex++;
        updateCarousel();
    }
});
```

### 🔑 監聽滾動事件（同步頁數計數）

**這是「三種並存」的核心** — 當用戶拖動滾動條或觸控滑動時，自動同步頁數計數和按鈕狀態：

```javascript
let scrollTimeout;
track.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        const trackWidth = track.clientWidth;
        if (trackWidth > 0) {
            const newIndex = Math.round(track.scrollLeft / trackWidth);
            if (newIndex !== currentIndex) {
                currentIndex = newIndex;
                // 只更新 UI（不重新觸發 scrollTo，避免無限循環）
                const perView = getPerView();
                const maxIndex = Math.max(0, totalItems - perView);
                pageCounter.textContent = 
                    String(currentIndex + 1).padStart(2, '0') + ' / ' + 
                    String(maxIndex + 1).padStart(2, '0');
                // 更新按鈕狀態（同上）
            }
        }
    }, 100);  // 100ms debounce 避免動畫過程中誤判
}, { passive: true });

// 視窗大小改變時重新計算
window.addEventListener('resize', updateCarousel);

// 初始化
updateCarousel();
```

---

## 🎮 三種互動方式並存

| 方式 | 實作 | 觸發什麼 |
|------|------|---------|
| **按鈕上一頁/下一頁** | click 事件 → `scrollTo` | 平滑滾動到指定頁 |
| **觸控滑動** | 瀏覽器原生 | snap-x 自動對齊到卡邊界 |
| **滾動條拖動** | 瀏覽器原生 + scroll 監聽 | scroll 事件同步頁數計數 |

**這就是教練說的「上一頁、下一頁與滑動桿同時並存」**。零計算誤差，零白屏風險。

---

## ⛔ 禁止事項（過去 AI 全部踩雷的地方）

1. ⛔ **用 `transform: translateX(-X%)` 切換頁面** — flex + transform 寬度計算有太多變數（flex-shrink、min-width、transform 百分比基準、overflow 行為...）
2. ⛔ **JS 計算卡片的寬度百分比** — 讓瀏覽器原生處理，不要自己算
3. ⛔ **用 `display: none / block` 切換** — 失去滑動動畫
4. ⛔ **不監聽 scroll 事件** — 用戶拖滾動條時頁數計數不會更新
5. ⛔ **忘記 `scroll-behavior: smooth`** — 按鈕點下去會「跳」而不是「滑」

---

## ✅ 自我驗證 Checklist（部署前必過）

部署到正式站前，在本機預覽確認：

- [ ] 上一頁/下一頁按鈕能切換
- [ ] 按鈕切換時是**平滑滾動**不是跳
- [ ] 觸控滑動（手機模擬）能切換
- [ ] 滾動條拖動能切換，**且頁數計數會同步更新**
- [ ] 滾動到邊界時，按鈕變半透明 + 不可點
- [ ] 視窗大小改變時（縮放瀏覽器），輪播正常
- [ ] 每張卡都 100% 寬度，內容完整顯示（不被切）

---

## 📚 相關失敗案例

- **案例 R**（distill/failure-case-handbook.md）：輪播第二頁空白，四次改版都沒修好 → 教訓：複雜解法不如原生 API

---

## 🛠️ 完整可複製貼上範本

```html
<!-- HTML -->
<div class="relative">
    <!-- 左右按鈕（裝飾用） -->
    <button id="prevBtn" 
            class="absolute left-0 top-1/2 -translate-y-1/2 z-10 ...">
        <i class="fa-solid fa-chevron-left"></i>
    </button>
    
    <!-- 滾動 track -->
    <div class="overflow-x-auto overflow-y-hidden w-full" 
         id="track" 
         style="scroll-behavior: smooth; -webkit-overflow-scrolling: touch;">
        <div class="item" style="width: 100%; min-width: 100%;">卡 1</div>
        <div class="item" style="width: 100%; min-width: 100%;">卡 2</div>
    </div>
    
    <button id="nextBtn" 
            class="absolute right-0 top-1/2 -translate-y-1/2 z-10 ...">
        <i class="fa-solid fa-chevron-right"></i>
    </button>
    
    <!-- 頁數計數 -->
    <div id="pageCounter" class="text-center mt-4">01 / 02</div>
</div>

<script>
const track = document.getElementById('track');
const items = track.querySelectorAll('.item');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageCounter = document.getElementById('pageCounter');
let currentIndex = 0;
const total = items.length;

function getPerView() {
    if (total <= 2) return 1;
    return window.innerWidth >= 768 ? 2 : 1;
}

function updateUI() {
    const perView = getPerView();
    const maxIndex = Math.max(0, total - perView);
    currentIndex = Math.max(0, Math.min(currentIndex, maxIndex));
    
    const tw = track.clientWidth;
    if (tw > 0) track.scrollTo({ left: currentIndex * tw, behavior: 'smooth' });
    
    pageCounter.textContent = 
        String(currentIndex + 1).padStart(2, '0') + ' / ' + 
        String(maxIndex + 1).padStart(2, '0');
    
    const atStart = currentIndex === 0;
    const atEnd = currentIndex >= maxIndex;
    if (prevBtn) {
        prevBtn.style.opacity = atStart ? '0.3' : '1';
        prevBtn.style.cursor = atStart ? 'default' : 'pointer';
        prevBtn.disabled = atStart;
    }
    if (nextBtn) {
        nextBtn.style.opacity = atEnd ? '0.3' : '1';
        nextBtn.style.cursor = atEnd ? 'default' : 'pointer';
        nextBtn.disabled = atEnd;
    }
}

prevBtn?.addEventListener('click', () => {
    if (currentIndex > 0) { currentIndex--; updateUI(); }
});
nextBtn?.addEventListener('click', () => {
    if (currentIndex < total - getPerView()) { currentIndex++; updateUI(); }
});

let scrollTimeout;
track.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        const tw = track.clientWidth;
        if (tw > 0) {
            const newIndex = Math.round(track.scrollLeft / tw);
            if (newIndex !== currentIndex) {
                currentIndex = newIndex;
                updateUI();
            }
        }
    }, 100);
}, { passive: true });

window.addEventListener('resize', updateUI);
updateUI();
</script>
```

---

> 本 SOP 由軍師（終端機 Claude）於 2026-06-05 建立，教練親定「三種並用法」為標準模式。
> 違反 = 案例 R 重演。
