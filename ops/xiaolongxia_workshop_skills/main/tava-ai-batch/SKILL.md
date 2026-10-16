---
name: tava-ai-batch
description: 教練丟 TAVA / Tooo / Lovart 等第三方 AI 工具 URL（含 N 條 prompt）→ 寫 mixed-mode 腳本一次跑完（"Retouch" 走 edits 帶 reference；"Concept" 走純文字）。LINE 截圖 reference 檔名一個底線 input-S_<num>_0---UUID.jpg。Telegram 8 張拆 4+4 推。
---

# 觸發判斷

教練訊息包含以下任一特徵：

- 丟 TAVA AI URL（`https://www.tava-ai.com/chat/.../image-prompts.html`）
- 丟 Tooo / Lovart 等第三方 AI 工具的 prompt 列表頁面
- 「依照指令把圖片給弄回來要到 LK888 的模式」+ 提供 URL

- 教練丟「出圖指令表一鍵注入」做出來的出圖清單（2026-10-12 新增，`coach1973.github.io/ai-go/biz-web-inject.html`）：每條有 `IMG-001` 起的 ID、類型（實景修飾／概念／圖解背景）、比例、參考照片、英文 Prompt，最後附 JSON。對應：實景修飾→edits（帶參考照片）、概念／圖解背景→generations；比例 16:9、4:3→1536x1024，4:5→1024x1536，1:1→1024x1024；輸出檔名用 ID（IMG-001.png），跑完全部打包成一個 zip 交回教練。有 JSON 就直接讀 JSON，不要從網頁文字猜。

**核心特徵**：URL 內含 N 條結構化 prompt，**部分 prompt 帶 reference 圖**（教練會另外傳照片到對話）。

**不是這個 skill**：

- 教練只丟單張 prompt 文字（走 `infographic-lk888`）
- 教練本人鎖臉漫畫（走 `character-illustration-batch` 鎖臉版）
- 教練本人不出現的 narrative 漫畫（走 `character-illustration-batch` narrative 版）
- 教練丟「產業鏈 SOP」或「夥伴圖」（走 `industry-chain-prompt`）
- 教練口頭/打字描述圖片需求，沒附 URL（走 `infographic-lk888` 或 `character-illustration-batch`）

# 程序

## 1. 抓 URL

```bash
web_fetch(url="<URL>", maxChars=50000)
```

讀下來後手動解析 prompt 區段（通常以 `PROMPT 01 / XX:XX` 或 `### 標題` 開頭）。

## 2. 解析 prompt 列表 + 判斷 mode

- 把每條 prompt 編號 01~N
- **判斷每條 prompt 的 mode**：
  - 有 `參考：S__XXXX_NNNN_0.jpg` / `Retouch S__...` / `preserve the real installation` / `photographic retouch` 字眼 → **edits**
  - 有 `Concept visualization` / `概念` / `not a completed project` / `not a scientific` 字眼 → **generations**
  - 兩種都沒有 → 預設 **generations**，但要 log 出來標註待確認

## 3. 收集 reference 照片

教練會傳 reference 照片到 Telegram，OpenClaw 存到 `~/.openclaw/workspace/media/inbound/openclaw-staged-<UUID>/`。

**檔名規律**：LINE 截圖檔名是 `input-S_XXXX_NNNN_0---<UUID>.jpg`（**一個底線**在 S 後面），不是 prompt 裡寫的 `S__XXXX_NNNN_0.jpg`（兩個底線）。用 `input-S_XXXX_NNNN_0` 過濾。

```bash
ls -la ~/.openclaw/workspace/media/inbound/openclaw-staged-*/input-S_*.jpg
```

找不到的話跟教練確認（不要瞎猜 → 會扣錯點數）。

## 4. 寫 mixed-mode 腳本

存到 `/tmp/<task>_batch.py`，**用 `write` 工具**（避免 heredoc mask 沒被替換）。

完整腳本範本見 `mixed-mode-script.md`。

**關鍵設計**：
- 一個 `PROMPTS` list，每個元素有 `id` / `ref` / `size` / `mode` / `prompt` 五個欄位
- 用迴圈根據 `mode` 自動決定走 `edits`（multipart）或 `generations`（JSON）
- `edits` 模式：boundary 隨機產生、image 欄位帶 reference bytes、prompt/model/size/n 欄位分開
- `generations` 模式：JSON body 一發
- 都用 `lk888_guard.urlopen` 走收費閘門
- 跑完 `time.sleep(3)` 避免打太快

## 5. 執行

```bash
# 8 張約 5-8 分鐘
python3 /tmp/<task>_batch.py
```

用 `exec` 工具：
- `background: true` + `timeoutSeconds: 600`
- 用 `process(poll)` 監看

## 6. view_image 自檢

每張圖都 `view_image` 看，確認：
- 修飾版（edits）：保留原建築/植物/家具比例、沒新增多餘物件
- 概念版（generations）：沒亂加文字/數字/浮水印
- 共通：沒扭曲的手指/變形的臉/醫院病床

## 7. 推 Telegram（拆 4+4 避免 sendMediaGroup 失敗）

**不要一次推 8 張**：2026-10-12 約瑟布 8 張同推 sendMediaGroup 撞 network error 失敗（總 27MB 過 sendMediaGroup 上限），分 4+4 推成功。

- 前 4 張（01-04）：caption 包含 prompt 標題
- 後 4 張（05-08）：caption 包含 prompt 標題 + view_image 發現的問題

## 8. 簡短回報

「✅ 兩批全推（messageId XXX + XXX），N 張完成。任務結束。」一行就好。

# 已知陷阱

| 陷阱 | 解法 |
|------|------|
| 教練丟 URL 後沒傳 reference 照片就說「跑」 | 先檢查 staging dir，缺哪幾張就停、回報缺哪些 |
| 8 張同推 Telegram sendMediaGroup 失敗 | 拆 4+4（2026-10-12 約瑟布案例，總 27MB 過上限）|
| 8 張 reference 沒給齊，教練又說「全跑」 | 缺 reference 的 prompt 自動降級為 generate 模式，**必須在腳本 log + Telegram caption 明確標出降級的編號**，避免教練誤會是 retouch 版 |
| `S_XXXX_NNNN_0` 對應不到 `input-S_XXXX_NNNN_0---UUID.jpg` | LINE 截圖檔名只有 `S_XXXX_NNNN_0`（一個底線），用 `input-S_XXXX_NNNN_0` 過濾 |
| `urllib.request.urlopen` 直接打 LK888 → 收費閘門擋下 | 改用 `lk888_guard.urlopen` |
| heredoc 帶 `API_KEY = ***` → SyntaxError | 用 `write` 工具寫 /tmp/ 腳本 |
| `yieldMs=600000+` 背景化 → OpenClaw exec wrapper 中途殺 process | 用 `background: true` + `timeoutSeconds: 600` + `process(poll)` |
| 教練丟 URL 但 prompt 編號亂跳（例如 01-08 但 03 寫在 07 位置）| 按 URL 內的編號順序照排，不要按 prompt 文字長度排序 |
| retouch 4+4 拆散 → 教練以為「6 張 retouch」集中在第 1 推、第 1 推卻只有 4 張（教練原話：「第一推也只有 4 張圖而已，沒有 6 張圖啊」，2026-10-12 v1=6 retouch+2 text 案例）| Telegram caption 主動標明「第 1 推：4 張 retouch / 第 2 推：2 張 retouch + 2 張文字概念」讓教練能精確點算 retouch 張數；或乾脆 6 張 retouch 一次推、2 張文字概念另推一批 |
| 出圖完成後教練說「下載」「打包」「一次性」 | 走 `image-archive-github` skill（建 GitHub 私庫 + MANIFEST.md + Download ZIP），不要 Telegram 一張一張推或重複推 |

# 參考

- 來源案例：2026-10-12 約瑟布 8 張（6 張實景修飾 + 2 張概念圖，5 分鐘跑完，messageId 12194 + 12198）
- API：`https://api.lk888.ai/v1/images/edits`（multipart）、`https://api.lk888.ai/v1/images/generations`（JSON）
- model：`gpt-image-2`
- size 對應：TAVA 給 16:9 → 1536x1024、4:5 → 1024x1536、4:3 → 1536x1024
- 教練 Telegram chat_id：6124913915
- 既有 skills：`infographic-lk888`（單張純文字）、`character-illustration-batch`（教練鎖臉/narrative）、`industry-chain-prompt`（產業鏈）
- 完整腳本範本：`mixed-mode-script.md`
