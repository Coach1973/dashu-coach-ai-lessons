# SOP：Coze LINE 官方帳號搬遷到小龍蝦本機（OpenClaw + MiniMax-M3）

> 定稿日：2026-07-26，來源：「教練都在想什麼」帳號搬遷實戰記錄（bni_tainan v75 是第一個案例，這次是第二個，教練要求寫成 SOP 供後續帳號複用）。
> 教練原話：「請嚴謹地把這個流程寫出一個 SOP，因為我還有其他類似的帳號也要這麼做。」
> 適用情境：教練有一個 Coze 平台上串接 LINE 官方帳號的機器人，要搬到小龍蝦（Mac 本機 OpenClaw）+ MiniMax-M3。

---

## 第 0 步：開工前確認方向

- 確認這是哪一個 LINE 官方帳號（Bot Basic ID、帳號名稱）
- 確認教練是否已登入該帳號的 `manager.line.biz` 後台（若沒有，先請教練登入）
- **不要假設「這個帳號一定有/一定沒有既有 Coze 串接」——查證前不要下結論**（試金石教訓：曾經因為只查 manager.line.biz 就誤判「完全沒有機器人」，其實 LINE Developers Console 才是真相源）

---

## 第 1 步：查證帳號現況（真相源查證，不可省略）

### 1a. manager.line.biz 後台（初步了解）
- 進 `manager.line.biz/account/@xxx` 看好友數、群發歷史、聊天功能開關狀態
- ⚠️ **這裡顯示的 Webhook 網址欄位可能是空的/過期的假象，不可當作最終結論**

### 1b. LINE Developers Console（真相源，必查）
- 進 `developers.line.biz/console/channel/<Channel ID>/messaging-api`
- 記下：Channel ID、Channel Secret、**Webhook URL**、**Use webhook 開關狀態**
- 若 Webhook URL 顯示 `https://api.coze.com/adapter/line/webhook/<數字ID>`，代表**真的有 Coze 機器人在服務這個帳號**，那個數字 ID 就是 Coze 的 bot ID，記下來

### 1c. 若確認有 Coze 串接，去 Coze 後台找到對應的 Bot
- 進 `coze.com/space/<space_id>/develop`，注意：**這個列表頁面常常需要等幾秒才會渲染完成**，第一次讀取內容是空的不代表真的沒有 bot，重新整理或稍等再讀一次
- 用步驟 1b 記下的 bot ID 比對 URL（`coze.com/space/<space_id>/bot/<bot_id>`），確認是同一個 bot，不要只看名稱相似就當作同一個
- **同一個 Coze 帳號底下常常有多個不相關的 bot**（教練這次的空間裡還有 BNI 小幫手、AI實驗小學、大法經書等其他用途的 bot）——只處理跟這個 LINE 帳號真正對應的那一個，其他的一律不要碰、不要引用其知識庫

---

## 第 2 步：逐字擷取 Coze 人設（Persona & Prompt）

- Coze 的 Persona 編輯框是**虛擬化渲染**（virtualized），不會把全部文字一次放進畫面 DOM，用一般讀取工具會抓不全
- 正確做法：**逐段捲動 + 逐段讀取**，用 accessibility tree（`read_page` 之類的工具，filter=all）讀取當前畫面內容，一段一段記錄，捲到底為止
- 教練的 prompt 常常是「多次疊代」寫成的，可能同一份文件裡有兩三層不同版本的「Role」開頭（同一份 prompt 裡重複出現多次 `# Role:` 標題），**這是正常的，不要自作主張刪減/去重**——原封不動全部照抄過去，一字不差搬遷（跟 bni_tainan 的原則一致）。如果教練後續要精簡，再另外討論
- 特別注意「絕對不可修改」「100%準確」這類標記的區塊（通常是團隊使命/信念/守則等核心教條），這些是逐字複製的最高優先，不可意譯改寫

---

## 第 3 步：查證這個 Bot 掛的知識庫

- 在 Coze bot 編輯頁的 Skills/Knowledge 區塊，記下實際掛載的知識庫名稱清單（**不是**整個 Coze 空間裡的所有知識庫，只看這個 bot 實際掛的那幾個）
- **逐一點進每個知識庫**，檢查右側是否顯示「0 segments」+ 錯誤圖示（滑鼠移過去會顯示如「系統內部異常」）——這代表這份知識庫從未真正處理成功，Coze 版機器人實際上讀不到內容
- 若確認損壞：請教練提供對應的原始檔案（通常是 .docx），教練電腦裡多半還留著原始檔
- 若知識庫是正常的（有 segments 數字）：可以視情況決定是否要花時間逐段擷取內容，或直接請教練提供原始檔案更快

---

## 第 4 步：建立本機 agent 骨架

```bash
mkdir -p ~/.openclaw/agents/<account_id>/knowledge
mkdir -p ~/.openclaw/agents/<account_id>/scripts
```

- `AGENTS.md`：把第 2 步擷取的 Persona 原封不動整理進去，開頭加註搬遷來源（Coze bot ID、搬遷日期、擷取方式說明）
- 知識庫檔案（教練提供的 .docx）用 python 擷取純文字存進 `knowledge/*.md`：

```python
import zipfile, re, html
with zipfile.ZipFile(path) as z:
    xml = z.read('word/document.xml').decode('utf-8')
texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml, flags=re.S)
full = html.unescape(''.join(texts))
```

- **不分段沒關係**，教練原話：「反正基本上對你而言，有沒有分段應該都不是重點，能讀取到內容最重要」——重點是內容完整，格式細節不用強求

---

## 第 5 步：知識庫太大時的效能處理（教練指示，46 萬字以上務必套用）

若知識庫總字數偏大（經驗值：超過 10 萬字建議套用），**不要**指望把全部內容塞進 agent 的 bootstrap 系統提示詞（會拖慢回覆速度、大幅增加 token 成本，且每次對話都要重複付出這個成本）。

改用 SQLite FTS5 全文檢索（Python 內建 `sqlite3` 模組自帶，零新依賴）：

1. `scripts/build_search_index.py`：把 `knowledge/*.md` 依段落/句尾標點切成幾百字一段的語意段落，寫進 `scripts/knowledge_index.sqlite` 的 FTS5 虛擬表
   - **注意**：docx 擷取出來的原始文字常常沒有換行/段落標記（因為 `<w:t>` 直接串接），若只用 `\n\n` 切段會切不細（可能整份文件只切成 1-2 段），要加一層 fallback：段落本身超長時改用中文句尾標點（。！？；）再切一次
2. `scripts/search_knowledge.py`：CLI 查詢工具，用法 `search_knowledge.py "關鍵字1 關鍵字2" --top 3`，OR 邏輯關鍵字比對，回傳最相關的幾段原文
3. `AGENTS.md` 裡明確指示 agent：需要具體案例/教條原文時，用 `exec` 呼叫這支搜尋腳本，不要假設知識庫已經在自己的記憶裡
4. 用**真實測試**驗證：問一個只有在知識庫深處才有答案的具體問題，確認 agent 真的呼叫了搜尋腳本、答案內容跟品質正確（可查 session 的 trajectory log 或直接看有沒有呼叫到 `search_knowledge`）
5. 之後教練再補充知識庫內容，跑一次 `build_search_index.py` 重建索引即可（幾秒完成）

---

## 第 6 步：註冊 LINE 通道 + 建立 agent 綁定

```bash
# 6a. 存憑證（不進git明文，權限600）
umask 077
printf '%s' '<Channel Access Token>' > ~/.openclaw/credentials/line-<account_id>-token.txt
printf '%s' '<Channel Secret>' > ~/.openclaw/credentials/line-<account_id>-secret.txt

# 6b. 註冊LINE帳號
openclaw channels add --channel line --account <account_id> \
  --token-file ~/.openclaw/credentials/line-<account_id>-token.txt \
  --secret-file ~/.openclaw/credentials/line-<account_id>-secret.txt \
  --name "<顯示名稱>"

# 6c. 建立agent綁定
openclaw agents add <account_id> \
  --workspace ~/.openclaw/agents/<account_id> \
  --model minimax/MiniMax-M3 \
  --bind line:<account_id> \
  --non-interactive
```

**Channel Access Token 取得方式**：`developers.line.biz/console/channel/<Channel ID>/messaging-api` 頁面最下方「Channel access token (long-lived)」區塊，沒有的話按「Issue」產生。

---

## 第 7 步：🔴 陌生人配對關卡 + 獨立對話記錄（血淚教訓，必做，不可跳過）

**這一步 bni_tainan 跟「教練都在想什麼」都各犯過一次，第三次不能再犯：**

編輯 `openclaw.json`，在該帳號的 `channels.line.accounts.<account_id>` 底下加：
```json
"dmPolicy": "open",
"allowFrom": ["*"],
"groupAllowFrom": ["*"]
```

在對應的 route（`bindings` 陣列裡 `agentId: "<account_id>"` 那條）加：
```json
"session": { "dmScope": "per-channel-peer" }
```

**為什麼這兩個缺一不可**：
- 沒有 `dmPolicy: open` → 任何好友第一次傳訊息都會卡在「陌生人配對」關卡，收不到回覆，教練要一個一個手動核准，體驗極差
- 沒有 `dmScope: per-channel-peer` → 所有好友共用同一個對話記錄，會互相看到彼此的對話內容，是資安問題

改完 `openclaw gateway restart`，用 `openclaw channels status` 確認該帳號顯示 `running`。

---

## 第 8 步：本機測試（webhook 切換前，必做）

```bash
openclaw agent --agent <account_id> --message "<測試問題1，問核心教條>"
openclaw agent --agent <account_id> --message "<測試問題2，問具體案例>"
```

檢查：
- 語氣/格式是否符合人設（LINE 平台通常要求：禁止 `**粗體**`、用【】強調、段落間留空行、連結直接貼網址）
- 核心教條類問題是否逐字正確
- 案例類問題：若知識庫還沒補齊，是否誠實說不確定，而不是自己編案例

---

## 第 9 步：Webhook 正式切換（會影響真實好友，教練確認後才做）

- 進 `developers.line.biz/console/channel/<Channel ID>/messaging-api`
- Webhook URL 改成 `https://openclaw.bymyway.com/line/webhook`（跟其他帳號共用同一個 tunnel/webhook 路徑，OpenClaw 用 request 裡的 channel signature 分辨帳號，不需要每個帳號用不同路徑）
- 按「Verify」，確認回傳 Success（可用 `read_network_requests` 確認實際 API 呼叫 `statusCode: 200`）
- `openclaw channels status` 再次確認 `running`

**切換是有真實影響的動作（會讓 Coze 版本停止回應好友），確認教練說「現在就切」才動手，不要自己判斷時機。**

---

## 第 10 步：陌生人真人測試 + 修復（若卡住）

若有真實好友回報「收不到回覆」或系統跳出 pairing code，代表第 7 步的 `dmPolicy` 設定沒生效或漏做，回頭檢查、補上，`gateway restart` 後請對方**直接再傳一次訊息**即可，不需要手動核准 pairing code（open policy 下 pairing 機制已被繞過）。

---

## 第 11 步：User ID → 真實姓名 對照（已泛化，通常不用額外設定）

`hooks/bni-member-directory-map/` 這支 hook（2026-07-26 已泛化為全帳號通用）會自動對**任何**新 LINE 帳號的每個新 user ID 生效，不需要重新設定，前提是：
- 第 6 步的 credentials 檔案命名遵守 `line-<account_id>-token.txt` 慣例
- 若想要「猜測真實姓名」功能（不只是記顯示暱稱），額外準備 `agents/<account_id>/knowledge/member_directory.md`，格式比照 bni_tainan：
  ```
  | 姓名 | 專業 | 電話 | 合作對象 |
  ```
  沒有這份檔案也沒關係，會自動降級為只記 LINE 顯示名稱，不做姓名猜測，不會報錯。

查詢方式：`state/<account_id>_line_id_map.json`。

---

## 第 12 步：監控後台（可選，教練要看服務品質時才做）

若教練要一個獨立網址即時看這個帳號的完整對話記錄，仿照 `bni.bymyway.com` 模式：

1. `openclaw.json` 的 `gateway.controlUi.allowedOrigins` 加入新網址
2. 用 CLI（不要用網頁 Zero Trust 後台，該後台可能卡在要求輸入帳單資訊）：
   ```bash
   cloudflared tunnel route dns openclaw-macmini <新網址>
   ```
3. 建一個範圍限縮為「Cloudflare Tunnel:Edit」、短效期（如 7 天）的臨時 API Token（`dash.cloudflare.com/<account>/api-tokens/create`，這個頁面本身不受 Zero Trust 付費牆限制），用來透過 API 更新 tunnel 的 ingress 規則：
   ```bash
   curl -X GET/PUT "https://api.cloudflare.com/client/v4/accounts/<account_id>/cfd_tunnel/<tunnel_id>/configurations" \
     -H "Authorization: Bearer <臨時token>" ...
   ```
   在既有 ingress 陣列裡（保留其他帳號的規則）新增一條指向 `http://localhost:18789` 的新 hostname，**必須放在 `http_status:404` 的 catch-all 規則之前**
4. **用完立刻刪除這個臨時 API Token**（Cloudflare 後台 + 本機都要清除），不留常駐高權限金鑰
5. 驗證：`curl -o /dev/null -w "%{http_code}" https://<新網址>/` 應回 200

第一次有新裝置/新瀏覽器打開會卡在「需要裝置配對」，把畫面顯示的 device ID 給軍師，`openclaw devices approve <ID>` 一次就好，之後同一台裝置不會再卡。

---

## 檢查清單（每次搬遷結束前對照）

- [ ] Coze 原始 bot 人設已逐字搬進 `AGENTS.md`（含所有版本/層級，未刪減）
- [ ] Coze 知識庫健康狀況已查證，損壞的已跟教練要原始檔案補齊
- [ ] 知識庫超過約 10 萬字已套用 FTS5 全文檢索，AGENTS.md 有寫檢索指令
- [ ] `dmPolicy: open` + `allowFrom: ["*"]` + `dmScope: per-channel-peer` 三項都已設定（第 7 步）
- [ ] 本機測試至少 2 題（教條類 + 案例類）都正確
- [ ] Webhook 切換前有教練明確「現在就切」的確認
- [ ] Webhook Verify 回 Success
- [ ] User ID 對照 hook 自動生效（不用額外處理，除非要姓名猜測功能才補 member_directory.md）
- [ ] 全部改動都有對應 git commit + hash
