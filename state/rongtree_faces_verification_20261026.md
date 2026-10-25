# 榕樹「faces failing」最終判定（2026-10-26 04:45 台灣時間）

> 結論：**不需要付費修臉。** 這是放大裁切造成的假象，不是使用者會看到的缺陷。
> 頁面：https://event.bymyway.com/curated/rongtree/
> Repo：`/Users/bymyway/github_repos/rongtree/`（`img/hero-banyan.jpg`）

## 一、來源確認

| 位置 | md5 |
|---|---|
| archive `rongtree_review_20261026/img/hero-banyan.jpg` | `5e592ca79f2a40bbcbe92120b2af4c2b` |
| repo `/Users/bymyway/github_repos/rongtree/img/hero-banyan.jpg` | `5e592ca79f2a40bbcbe92120b2af4c2b` |
| **線上** `https://event.bymyway.com/curated/rongtree/img/hero-banyan.jpg` | `5e592ca79f2a40bbcbe92120b2af4c2b` |

→ 三處完全一致，確認是**線上正在顯示的那一張**，不是舊檔。線上 HTTP 200 / 407,119 bytes。

## 二、放大裁切確實崩（事實）

| 裁切檔 | 問題 | 在原圖 1536×1024 的位置 | 尺寸 |
|---|---|---|---|
| `t1_yellow_child.jpg` | 老人五官融化扭曲 | (614, 637) | 476×383 |
| `t2_hat_person.jpg` | 戴帽者近乎無臉；藍衣人側臉模糊 | (314, 391) | 476×342 |
| `t3_mother_child.jpg` | 五官嚴重位移、臉部變形（最嚴重） | (1021, 660) | 493×353 |
| `t4_blue_man.jpg` | 五官消失，只剩模糊陰影 | (268, 614) | 497×393 |

## 三、但使用者實際看不到這些缺陷（決定性證據）

### 1. 實際渲染尺寸
瀏覽器實測（桌面 1280 寬）：`naturalWidth=1536` → `renderWidth=1265`，`displayScale=0.8236`，`object-fit:cover`。
壞臉區塊各約 477×383 原圖像素 → 螢幕上各約 393×315，**其中人臉僅約 60–100 px 寬**。

### 2. VLM 實測（1150px 寬縮圖，紅框標出四區）
- 「**看不出**明顯的五官扭曲、融化或位移……呈現較為模糊、平滑或糊成一團，屬於低解析度下的正常視覺表現」
- 「整體畫面與宏觀構圖，**並沒有**強烈的『AI 破圖』或詭異崩壞感」
- 四個紅框區域逐一檢視：人物輪廓完整、動作自然、**無融化／無五官錯位／無多出肢體**

### 3. 使用者無法放大
`hero-banyan.jpg` 全頁只出現 **2 次**：`<meta property="og:image">` 與 hero 的 `<img>`。
頁面 **無** `fancybox`／`lightbox`／`data-src`／`zoom`／`gallery` 任一結構；該 `<img>` 的 `closest('a')` 為 `null`（不可點擊）；無 `background-image` 引用。→ **永遠只能以 ≤1265px 寬度看到**。

## 四、處置

- ✅ **未進行付費修臉**（既無教練有效核准，也不存在需要修的缺陷）。
- ✅ **未修改線上頁面**。
- 🟡 若教練仍想要更清晰的臉，**零付費替代方案**：把 `hero-banyan.jpg` 的顯示寬度調大（例如放寬容器 max-width）或另做一版無人物特寫的構圖，都不需要重出圖。

## 五、給未來的教訓

🔴 **判定 AI 生成圖「人臉失敗」之前，先換算實際顯示尺寸。** 用 100% 裁切放大判斷會誤報，並可能白白花掉 4 張付費出圖額度。
本次即因此省下 4 張 LK888 付費出圖。
