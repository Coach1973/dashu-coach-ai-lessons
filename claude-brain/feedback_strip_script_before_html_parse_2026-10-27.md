# 教訓：解析網頁前先剝掉 `<script>`，髒資料先查「髒在哪一層」

> 記錄日期：2026-10-27（bni_tainan 台南行事曆同步機制）
> 檔案：`~/.openclaw/agents/bni_tainan/scripts/sync_calendar.py` → `knowledge/tainan_calendar.md`

## 情境

台南培訓行事曆同步檔 `tainan_calendar.md` 最後一筆多了一段髒資料：

```
- 1219-1220(六日) M2（09:00-17:00，集思北科大，${time}）
```

`${time}` 明顯是程式碼模板變數，不是活動資訊。

## 根因（不是資料壞掉，是解析器抓錯地方）

來源頁 `https://event.bymyway.com/tainan-calender/` 頁尾有「新增活動」用的 **JavaScript 模板程式碼**，裡面字面寫著：

```js
<div class="meta-row"><span class="icon">🕒</span>${time}</div>
```

解析器用「icon span 後面到下一個 `<` 之前」的字串抓取 meta 欄位。切完**最後一筆**活動的 event-item 區塊後，頁面尾端（含整段 `<script>`）沒被切斷，於是尾端的 `<script>` 被當成該活動的內容掃進去，`${time}` 就被當成「時間」抓走。

**上游資料完全正常**——靜態 HTML 裡的活動資料一個字都沒壞。

## 正確修法（雙層防護）

```python
# 解析前剝掉所有 script 區塊
html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
```

再在清洗 meta 時加一道防呆：

```python
cleaned = text.strip()
if "${" in cleaned:
    cleaned = re.sub(r"\$\{[^}]*\}", "", cleaned).strip("，,、 ").strip()
if cleaned:
    metas.append(cleaned)
```

## 驗收（一定要做逐行 diff，不能只看「跑成功」）

重跑後：**106 筆一筆沒少**，逐行 diff 只有 2 行不同（同步時間戳 + 那筆的 `${time}` 消失），殘留模板變數 0。

commit `8a97aff116fb39b656acc10dbbdb0085b6cfe6fc`（`~/.openclaw` repo 的 **master** 分支）。

## 通則一：髒資料先問「髫在哪一層」

上游資料壞掉 vs 自己的解析器壞掉，處置完全不同。順序：

1. 先 `grep` **原始 HTML**，找到那個怪字串**原本住在誰身上**（是資料欄位？還是頁尾 JS？）。
2. 找到宿主 → 決定改資料還是改程式。
3. 沒搞清楚宿主就改資料，只會把髒東西「洗白」進資料庫，以後每次同步又長回來。

## 通則二：長頁面的 script / style 區塊要先剝掉再解析

事件列表頁常在尾端放「新增／編輯」用的 JS 模板。若不先剝，尾端 JS 會被當成最後一筆內容掃進去。這個通則不只適用行事曆——**任何解析 HTML 清單頁都適用**。

## 通則三：`~/.openclaw` 與 `workspace/` 是兩個獨立 repo

| 目錄 | 分支 | remote |
|---|---|---|
| `~/.openclaw` | **master** | `Coach1973/mac-openclaw-workflows` |
| `~/.openclaw/workspace` | **main** | 同上（另一條線） |

`scripts/git_wrong_branch_guard.py` 就是在擋這個坑（試金石123：10/16 有 AI 在 workspace 打成 `git pull --rebase origin master`，把整個 workspace 換成另一套檔）。

- 改 `agents/bni_tainan/**` → commit 到 `~/.openclaw` → 推 **master**
- 改 `workspace/**` → commit 到 `workspace` → 推 **main**
