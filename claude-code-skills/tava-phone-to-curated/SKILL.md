---
name: tava-phone-to-curated
description: 教練人不在電腦前、用手機走「TAVA 做網頁 → Claude 出圖、組合、打包 → 上架策展中心 → 公開連結」時使用。觸發：教練貼 tava-ai.com/<代碼>/README-for-AI.txt、women-...-pack.zip、image-prompts.txt 網址，或說「手機做網頁」「TAVA 做好了幫我出圖上架」「照交接說明做圖」。一個對話框從頭做到給網址，中間只在出圖前不用問、上架網址自己取。
---

# 手機版：TAVA 網頁 → 出圖 → 上架 → 公開連結

> 來源：2026-11-11 教練第一次全程用手機走完「女人的幸福學」（tava-ai.com/03olehi18o → event.bymyway.com/curated/women-happiness/）。
> 教練端只要兩步：在 TAVA 最後貼 https://coach1973.github.io/tava-to-claude/ 的那一句 → 把 TAVA 回的 README-for-AI.txt 網址貼給 Claude。README 第一行會點名本技能。
> 那次因為分兩個對話框做，第二個不知道圖已出好、差點重出，又找不到圖。**這支技能＝一個對話框從頭做到尾。**

## 教練那端（手機）在做什麼
1. 在手機版 TAVA 說明要做什麼網頁 → TAVA 做好網頁、首屏主圖、出圖指令。
2. 請 TAVA 給「給 AI 的下載說明」→ 拿到 `https://www.tava-ai.com/<代碼>/README-for-AI.txt` 和整包 zip。
3. 把網址貼給 Claude（手機 Remote Control），說要上傳策展中心、設一個網址。
4. 等 Telegram「活動報名即時通知」群跳出上架通知 → 用手機點開檢閱。

**教練在手機上：不要叫他看 Mac 畫面、不要叫他複製貼上、不要問他圖在哪。**

## AI 這端步驟（一次做完）

### 1. 下載整包、讀交接說明
```bash
C=<代碼>   # 例 03olehi18o
mkdir -p /private/tmp/tava-$C && cd /private/tmp/tava-$C
curl -s https://www.tava-ai.com/$C/README-for-AI.txt          # 先讀：檔案清單、出圖規則、換圖方式、EDM 要疊的字
curl -sfLO https://www.tava-ai.com/$C/<pack>.zip && unzip -oq <pack>.zip   # zip 檔名寫在 README 或教練貼的訊息裡
```
README 沒寫 zip 名稱 → 列出網頁、`image-prompts.json`／`.txt`、`image-style.md`、`img/IMG-001-*.webp` 個別抓。

### 2. 先查有沒有人出過圖（防重出扣點）
```bash
ls ~/.openclaw/workspace/handoff_img*/ /private/tmp/*$C* 2>/dev/null; git -C ~/.openclaw log --oneline -20 | grep -i "$C\|出圖"
```
有就直接用，不重出。

### 3. 出圖（LK888，不問點數——教練 11/09 已授權出圖清單一律直接出）
**照新版說明書（https://coach1973.github.io/tava-to-claude/tava.txt）做的交接包**：`image-prompts.json` 已是 run_img_list 格式（id／type／ratio／file／prompt），直接 `run_img_list.py image-prompts.json out`；`type` 是「本人照片」的會被跳過，列進「還沒做的事」。
舊版交接包才需要下面的轉換：
`run_img_list.py` 讀不了 TAVA 的 `.txt`（`===== IMG-00X｜…｜尺寸 WxH｜存檔 … =====` 格式），也不認 JSON 的 `size` 欄位，所以先轉成它要的 JSON：
```bash
python3 - <<'E'
import json,re
items=[]
for h,body in re.findall(r'^===== (.*?) =====\s*$\n(.*?)(?=^=====|\Z)', open('image-prompts.txt',encoding='utf-8').read(), re.S|re.M):
    i=h.split('｜')[0]
    r='4:5' if '1024x1536' in h else ('16:9' if '1536x1024' in h else '1:1')
    items.append({"id":i,"type":"概念","ratio":r,"prompt":body.strip(),"file":i+".png"})
json.dump(items,open('list.json','w'),ensure_ascii=False,indent=1); print(len(items),'張')
E
python3 ~/.openclaw/workspace/scripts/run_img_list.py list.json out --dry-run   # 看張數、比例
python3 ~/.openclaw/workspace/scripts/run_img_list.py list.json out              # 真出圖（一次最多 12 張），會自動傳一覽圖到教練 Telegram
```
- 出完**自己看 `out/contact-sheet.jpg`**：沒有字、人物和首屏 IMG-001 是同一人、人種性別對。OCR 報錯就以眼看為準。
- 講師／本人照片位置：TAVA 只會出空場景，標成「待換本人照片」，不要自己找相似的人頂替。

### 4. 組網頁（照 README「換圖方式」）
- 網頁改名 `index.html`，圖放 `img/`，檔名照 README（例 `IMG-002-v1.web.webp`，用 `out/<編號>.web.webp` 改名）。
- `<div class="slot" data-img="IMG-00X">` 裡的 `<div class="ph">…</div>` 換成 `<img src="img/IMG-00X-v1.web.webp" alt="具體描述">`。
- **EDM 兩張是底圖**：用 Playwright（`chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'})`，`NODE_PATH=/opt/homebrew/lib/node_modules`）把 README 列的標題、日期、地點、費用、聯絡人、主辦疊上去輸出 PNG，接到下載鈕（例 `#dl-v`／`#dl-h`）並移除 `off`。**疊完自己看：字不壓臉。**
- 本機預覽＋檢查：`python3 -m http.server 8741` → `node ~/.openclaw/workspace/scripts/page_preflight.js http://127.0.0.1:8741/`（1280／390 寬、字 ≥20px、沒有左右捲動）。
  - 已知坑：body `overflow-x:hidden` 會讓 sticky 導覽失效 → 改 `clip`；手機左右捲動紅燈要實測 scrollX 確認是不是誤報。
- 打包：`cd <網站資料夾> && zip -qr ../site.zip index.html img -x "*.DS_Store"`

### 5. 上架策展中心（走 bigtree-publish-site，但這兩點不問）
- **短網址 AI 自己取**（教練 11/11：「你自己要取一個名字」）：照主標題取 10 字內小寫英文，先查 `event-signup/curated_sites_registry.json` 不撞名。**不列選項等教練選**——他在手機上，只等 Telegram 通知。
- kind：客戶／夥伴的頁 `shop`；教練自己的作品 `creation`。
```bash
KEY=$(grep '^CURATION_UPLOAD_KEY=' ~/.openclaw/workspace/event-signup/.env | cut -d= -f2)
curl -s -F "kind=shop" -F "package=@site.zip" -F "custom_slug=<短網址>" "https://event.bymyway.com/curation/upload?key=$KEY" -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
python3 ~/.openclaw/workspace/scripts/curation_check_result.py <短網址>   # found:false ≠ 失敗，等一下再查
```

### 6. 驗證（自己查完，不叫教練看）
- `curl -sI https://event.bymyway.com/curated/<短網址>/` → 200＋`text/html`；每張圖 200＋`image/webp`（或 png）。
- Telegram 上架通知有沒有送出：`grep -n "<短網址>" ~/.openclaw/workspace/event-signup/curation_uploads/watch.log | tail`，看得到送出時間和 message_id 就算確認，**不要問教練收到沒**。

### 7. 交付（教練在手機）
- 網址**單獨一行、前後不加任何符號**，手機點了就開。`deliver_open.sh` 只會開 Mac 的 Chrome，教練在手機看不到，可跑但不能當交付。
- 回報：網址、上架通知送出時間、還沒做的事（例：報名表 ENDPOINT 未設、講師照待換），最後「您要做什麼：檢閱頁面」。

## 不要做
- 不要分兩個對話框做（一個出圖、一個上架）；真的分了，出圖那邊要寫交接檔並 commit，給另一邊一句「讀 <路徑>」。
- 不要重出已經出好的圖；不要問點數；不要問短網址；不要叫教練看 Mac 畫面或貼檔案。
- 不用 Netlify。
