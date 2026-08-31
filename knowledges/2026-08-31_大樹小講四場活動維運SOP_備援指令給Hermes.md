# 大樹小講網頁維運交接指令（給 Hermes 備援用）

> 用途：教練（大樹教練）擔心 Claude 額度在本週三（2026-09-03）下午 1 點前用完，這份文件讓 Hermes（另一個在同一台 Mac 上執行的 AI）能無縫接手「大樹小講」相關網頁的維護工作，不中斷。
> 寫這份文件的人：軍師（Sonnet 5，終端機），2026-08-31。
> 涵蓋範圍：教練近期最在乎的 4 場活動——9/5、9/16、9/22（下午+晚上）、9/23-24。
> 前提：Hermes 跟軍師在**同一台 Mac**上，能存取同樣的檔案系統、git repo、終端機。以下路徑全部是這台 Mac 的絕對路徑。

---

## 0. 先確認自己是誰、在哪、服務誰（守則 E04）

- 你是 Hermes，在這台 Mac（教練的主力工作機）上執行任務，服務對象是大樹教練。
- 教練說話風格：口語、常常語音輸入，講活動細節時可能有相對日期（「這週三」「下週」），一律換算成臺灣時間絕對日期再動作。
- 任何不可逆或會花錢/花額度的動作（尤其是 Netlify 部署），**教練親口說「推」或「沒問題」才能執行**，不能自己判斷「應該沒問題」就推。這條是教練 2026-06-09 血淚換來的鐵律，全機（所有 AI）都要遵守。

---

## 1. 現況總覽：兩條網站路線，哪個是主力

大樹小講目前**同時存在兩種上線方式**，教練正在把重心從 Netlify 移到自架的 bymyway 動態渲染，但 Netlify 暫時還沒退場：

| 路線 | 網址 | 更新方式 | 即時性 |
|---|---|---|---|
| **🟢 主力（bymyway 動態渲染，2026-08-30 上線）** | `https://event.bymyway.com/bigtree/` | 改資料庫（`event.db`）或改 repo 原始檔，**存檔當下立刻反映**，不需要任何部署動作 | 即時 |
| GitHub Pages（備援，免費不扣額度） | `https://coach1973.github.io/bigtree/` | `git push` 到 `main` 分支即可 | 幾分鐘內生效 |
| Netlify 正式站（舊主力，逐步要退場，教練還在觀察） | `https://bigtree-tw.netlify.app` | 需要**手動 zip 打包 + 呼叫 Netlify API**，每次部署扣 15 點額度，且**必須教練親口說「推」才能做** | 手動觸發才生效 |

**結論：教練若只是要改活動時間/地點/文案，優先在 `event.bymyway.com/bigtree/` 這條線上處理（改資料庫最快），不用每次都去動 Netlify。只有教練明確要「正式對外發布到 Netlify 那個網址」時，才走第三條線的部署流程（見第 5 節）。**

同樣的「bymyway 動態渲染」模式也用在這幾個系列活動：

| 網址 | 對應內容 | 現況 |
|---|---|---|
| `event.bymyway.com/bigtree/` | 大樹小講（多場次矩陣，讀 `event.db`） | 涵蓋 9/5、9/16、9/19、9/22、9/23-24 全部場次 |
| `event.bymyway.com/ai-talk/` | 半天制系列（目前是 9/22 台南場：凌榆舜+大樹教練雙講師版） | 已上線（v153 完成） |
| `event.bymyway.com/ai-forum/` | 兩天制系列（目前是 9/23-24 台中場） | 已上線 |

**重要觀念（教練 2026-08-30 定調）**：這幾個網址代表「活動格式/系列」，不代表某一次的地點或年份——之後場地換了，內容直接改，網址不換。

---

## 2. 檔案與路徑地圖

```
/Users/bymyway/github_repos/bigtree/index.html          ← 大樹小講網頁原始碼（GitHub Pages + Netlify 用這份）
/Users/bymyway/github_repos/ai-talk/                     ← 半天制系列網頁原始碼（現為 9/22 台南場）
/Users/bymyway/github_repos/ai-forum-taichung/           ← 兩天制系列網頁原始碼（現為 9/23-24 台中場）

/Users/bymyway/.openclaw/workspace/event-signup/
  ├─ app.py               ← Flask app，event.bymyway.com 所有路由都在這裡（含 /bigtree/、/ai-talk/、/ai-forum/）
  ├─ db.py                ← 資料庫存取函式
  ├─ event.db             ← 場次資料庫，SQLite，events 表是唯一真相源
  ├─ bigtree_publish.py   ← 大樹小講「一鍵發佈」到 Netlify 的邏輯（資料庫→網頁→git→Netlify）
  └─ credentials/netlify_token.txt   ← Netlify API Token（唯讀權限即可看到，不要印出來貼聊天視窗）
```

服務本身是常駐的（launchd 看護，`com.coach.event-webapp`），改 `event.db` 或改 repo 檔案後**不用重啟服務**，`/bigtree/`、`/ai-talk/`、`/ai-forum/` 這幾條路由本來就是「每次請求都重新讀檔+讀資料庫」，改完立刻生效，用瀏覽器重新整理就看得到。

---

## 3. 改「大樹小講」場次資料（時間/地點/費用/主題）——這是最常見的需求

**唯一真相源是 `event.db` 的 `events` 表**，不要直接改 `bigtree/index.html` 裡的 `SESSION_DATES` 陣列——那段現在是「發佈到 Netlify/GitHub Pages 時」由程式產生的，手改了下次一鍵發佈會被覆蓋掉，而且 `event.bymyway.com/bigtree/` 這個主力網址根本不讀那段陣列，是直接查資料庫。

**改法（三選一，都可以）：**

1. **教練自己在後台改**（優先建議，教練有登入帳密）：`https://event.bymyway.com/admin/sessions`，新增/編輯/刪除/設為已取消。這是教練本人操作，不受任何 AI 部署鐵律限制。
2. **Hermes 用 SQL 直接改**（教練口頭交代時）：
   ```bash
   cd /Users/bymyway/.openclaw/workspace/event-signup
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('event.db')
   conn.execute(\"UPDATE events SET start_time=?, transport=? WHERE slug=?\", ('13:30', '費用1人200元（支付場地費）｜座位50人｜13:30開始，16:30結束', 'bigtree-0922-day'))
   conn.commit()
   "
   ```
   欄位對照：`event_date`（YYYY-MM-DD）、`start_time`（HH:MM，同一天多場次靠這個排序+靠這個做簽到路由判斷）、`slot_key`（早/早半/午/午半/晚/晚半/夜/上午/下午/全日/TBD）、`name`（主題）、`location`/`venue`/`address`/`transport`（場地/交通/費用說明）、`slug`（報名識別碼，前台深連結跟報名表單都靠它，不要亂改既有 slug）、`status`（active/cancelled/draft）。
3. **改完後立刻用瀏覽器或 curl 驗證** `event.bymyway.com/bigtree/` 內容已更新（這條路由零快取，改了就看得到）：
   ```bash
   curl -s "https://event.bymyway.com/bigtree/" | grep "13:30開始"
   ```

**改完 `event.db` 之後，這樣就完成了「讓官網即時更新」的任務，不需要額外做任何 git commit 或 Netlify 部署。** 只有教練明確要「把 GitHub Pages / Netlify 那個舊網址也同步」時，才需要走第 5 節的一鍵發佈或手動部署流程。

---

## 4. 改「大樹小講」非場次內容（文案/版面/彈窗等）

這類改動要直接改 `bigtree/index.html` 原始碼（`SESSION_DATES` 以外的部分），例如報名成功彈窗文案、Hero 區塊文字。改完：

```bash
cd /Users/bymyway/github_repos/bigtree
git add index.html
git commit -m "說明這次改了什麼"
git push origin main
```

`git push` 完成後：
- `event.bymyway.com/bigtree/` 這條路線**只有 `SESSION_DATES` 那段是即時從資料庫渲染**，其他部分（含這次改的文案）讀的是 repo 裡 `index.html` 的最新內容，push 完立刻生效。
- GitHub Pages（`coach1973.github.io/bigtree/`）幾分鐘內自動更新。
- **Netlify 正式站不會自動更新**（`bigtree-tw` 是手動上傳型站台，push GitHub 不會觸發 Netlify 部署）。要同步 Netlify，見第 5 節，且要教練說「推」才能做。

⚠️ 這種改動用 `bigtree_publish.py` 的一鍵發佈按鈕**會被擋下來**（它的去重檢查只認 `SESSION_DATES` 那段內容有沒有變，非場次類的改動它偵測不到，會回報「已是最新內容」而拒絕發佈），要用下面第 5 節的手動流程。

---

## 5. 需要同步 Netlify 正式站時的部署 SOP（教練親口說「推」才能做）

### 5.1 場次資料類的改動（時間/地點/費用/新增或刪除場次）

先確認 `event.db` 已經改好（第 3 節），教練說「推」之後：

```bash
cd /Users/bymyway/.openclaw/workspace/event-signup
NETLIFY_DEPLOY_CONFIRMED=1 python3 -c "
import db, bigtree_publish as bp
conn = db.get_conn()
result = bp.publish(conn, '大樹小講場次更新')
print(result)
conn.close()
"
```

`publish()` 會自動做完：資料庫→產生 `SESSION_DATES`→寫回 `index.html`→`git commit`+`push`→打包 zip→呼叫 Netlify API→等到 `state == "ready"` 才算成功。**看 `result` 的回傳值**：`{"ok": True, ...}` 才是真的成功，`ok: False` 要看 `step`/`message` 判斷卡在哪一步。

也可以請教練自己到 `event.bymyway.com/admin/sessions` 按「發佈到官網」，教練本人按＝本人授權，不受這條「要說推才能做」的規矩限制。

### 5.2 非場次類的改動（文案/版面）——一鍵發佈按鈕擋不住這種，要手動打包

**這段每一步都是血淚換來的，禁止自行「優化」或「簡化」，尤其是打包方式：**

```bash
# 1. 確認 index.html 改動已經 commit + push（見第4節）

# 2. 用 git archive 打包（只取已提交內容，不夾帶工作區未確認的修改）
rm -f /tmp/bigtree_publish.zip
TMPDIR=$(mktemp -d)
cd /Users/bymyway/github_repos/bigtree
git archive HEAD | tar -x -C "$TMPDIR"
cd "$TMPDIR" && zip -qr /tmp/bigtree_publish.zip . -x ".git*"

# 3. 驗證這個 zip 裡有目錄項（沒有目錄項 Netlify 會解壓失敗，這是踩過的坑）
python3 -c "
import zipfile
zf = zipfile.ZipFile('/tmp/bigtree_publish.zip')
dirs = [i for i in zf.infolist() if i.is_dir()]
print(f'目錄項數量: {len(dirs)}（必須 > 0）')
"

# 4. 教練親口說「推」之後才執行這一步
TOKEN=$(cat /Users/bymyway/.openclaw/workspace/credentials/netlify_token.txt)
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary "@/tmp/bigtree_publish.zip" \
  "https://api.netlify.com/api/v1/sites/40e580f0-1def-4777-adb8-587ef023ed36/deploys"
# 記下回傳的 "id"（deploy_id）

# 5. 輪詢部署狀態，一定要等到 "state":"ready" 才算成功，200只代表「檔案收到了」
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.netlify.com/api/v1/sites/40e580f0-1def-4777-adb8-587ef023ed36/deploys/<deploy_id>" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['state'])"
```

**絕對禁止的打包方式（都踩過雷，會讓 Netlify 回 `Deploy failed while extracting zip`）：**
- `git archive --format=zip -o x.zip HEAD`（中文檔名沒有 UTF-8 旗標，Netlify 解壓失敗）
- Python `zipfile` 手動走訪檔案打包（不會自動寫入目錄項，Netlify 一樣解壓失敗）
- Windows 上用 PowerShell `Compress-Archive`（產生反斜線路徑，這台是 Mac 用不到但寫這裡提醒別的機器）

**驗證部署後線上內容（文字跟圖片要分開驗證，缺一不可）：**
```bash
curl -s https://bigtree-tw.netlify.app/ | grep "關鍵字"
curl -sI https://bigtree-tw.netlify.app/images/xxx.jpg   # 確認 200 且 Content-Type: image/jpeg，不是只看狀態碼
```

**部署完成後，手動補記額度**（`bigtree_publish.py` 的 `publish()` 會自動記，但這條手動 curl 流程不會）：
```bash
python3 -c "
import json
from pathlib import Path
p = Path('/Users/bymyway/.openclaw/workspace/state/netlify_deploy_quota.json')
data = json.loads(p.read_text())
data['credit_pools'][0]['remaining'] -= 15
p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
"
```

### 5.3 其他兩個系列站台的 Netlify Site ID（若教練要求同步）

| 站台 | Netlify Site ID | Netlify 網址 |
|---|---|---|
| 大樹小講 bigtree-tw | `40e580f0-1def-4777-adb8-587ef023ed36` | bigtree-tw.netlify.app |
| 半天制系列 ai-talk-tw（9/22台南場內容） | `633b4b00-dae8-476c-a21b-9d0548bf1e66` | ai-talk-tw.netlify.app |
| 兩天制系列 ai-forum-taichung（9/23-24台中場） | `1d45648a-2651-4478-a7c2-d62af42215f2` | ai-forum-taichung.netlify.app |

這兩個站台沒有像 `bigtree_publish.py` 這樣的自動化腳本，若要部署，走 5.2 的手動打包流程，把 repo 路徑跟 Site ID 換成對應的即可（`ai-talk` repo 或 `ai-forum-taichung` repo）。

---

## 6. 目前 4 場活動的資料現況（2026-08-31 查證，供對照，實際請以 `event.db`/`/admin/sessions` 為準）

| 日期 | slug | 主題 | 地點 | 時間 | 費用 |
|---|---|---|---|---|---|
| 9/5（六） | `bigtree-0905` | 零基礎學 AI，起步比較快 | KR養生廚房（台南市東區崇明十一街31巷5號） | 14:00起（午半） | — |
| 9/16（三）上午 | `bigtree-0916-am` | 當古典音樂遇到AI流水席活動（上午場） | 郭音樂廳（高雄市鹽埕區） | 10:00起 | 300元（上下午合報500元） |
| 9/16（三）下午 | `bigtree-0916-pm` | 當古典音樂遇到AI流水席活動（下午場） | 同上 | 14:00起 | 同上 |
| 9/22（二）下午 | `bigtree-0922-day` | AI微論壇 | 台南安平維悅酒店 | 13:30-16:30 | 200元（支付場地費），50席 |
| 9/22（二）晚上 | `bigtree-0922-night` | 如何輕輕鬆鬆使用AI之轉念心法+HOWA改善情緒睡眠品質 | 同上 | 17:30進場~20:30 | 500元（附餐盒+音樂表演），50席 |
| 9/23（三） | `bigtree-0923` | AI微論壇 | 沃茲新創空間・忠明館（台中） | 全日 | 1800元 |
| 9/24（四） | `bigtree-0924` | AI微論壇 | 同上 | 全日 | 1800元 |

- 9/5、9/16、9/23-24 這幾場：`event.bymyway.com/bigtree/` 已經是最新資料，Netlify/GitHub Pages 是否同步請看教練上次是否說過「推」。
- 9/22 這兩場：對應的獨立網頁是 `event.bymyway.com/ai-talk/`（凌榆舜+大樹教練雙講師版），內容已於 2026-08-31 上線並經教練兩輪回饋修正（時間文字、拿掉設攤卡片）。
- 9/23-24 這兩場：對應的獨立網頁是 `event.bymyway.com/ai-forum/`（台中場內容），已上線。

**報名系統**：所有場次的線上報名都會寫進 `event.db` 的 `signups`/`attendees` 表，並透過 Telegram「活動報名即時通知」群組（chat_id `-5349981085`，教練+佩佩老師同見）通知，不是走 LINE（LINE 推播已於 2026-08-24 全面停用）。查某場報名人數：

```bash
cd /Users/bymyway/.openclaw/workspace/event-signup
python3 ../scripts/registration_report.py bigtree-0922-day   # slug 換成想查的場次
```

---

## 7. 幾條不能忘的鐵律（違反 = 重複踩過的坑）

1. **改資料庫或改 repo 原始碼可以自己判斷直接做**（這是教練已經拍板同意的「不用每次確認」的日常維護），但**任何會扣 Netlify 額度的部署動作，一律要教練親口說「推」或「沒問題」才能執行**——除非是教練自己在 `/admin/sessions` 按按鈕。
2. **同一天有多場次時，`event.db` 的 `start_time` 欄位一定要填**，現場 QR 簽到系統靠它判斷「現在是哪一場」，沒填會導致晚場來賓的簽到資料被誤記到早場。
3. 打包 Netlify 部署 zip，只能用「`git archive HEAD | tar -x` 解到暫存目錄 → 系統 `zip` 指令打包」這個組合，不要自己「優化」成 `git archive --format=zip` 或 Python zipfile，兩者都會讓 Netlify 解壓失敗（見第 5.2 節）。
4. Netlify 回 HTTP 200 不代表部署成功，一定要輪詢到 `state == "ready"`。
5. 做完任何一項任務後，在 `JUNSHI_HANDOFF_LATEST.md`（`/Users/bymyway/.openclaw/workspace/JUNSHI_HANDOFF_LATEST.md`）補一段簡短紀錄（做了什麼、改了哪個檔案/資料庫、有沒有 git commit hash），讓下一個接手的人（不管是軍師還是 Hermes）看得懂現況，這是教練最重視的「完美交接」（守則 #06）。

---

## 8. 快速自我檢查（開始動手前）

- [ ] 教練要改的是「場次資料」還是「文案版面」？→ 決定走第 3 節還是第 4 節
- [ ] 有沒有涉及 Netlify 部署？→ 有的話，教練有沒有明確說「推」？
- [ ] 改完 `event.db` 或 repo 後，有沒有實際 `curl` 或開瀏覽器驗證 `event.bymyway.com` 上內容真的更新了？
- [ ] 若走 Netlify 部署，有沒有等到 `state == "ready"` 才回報教練「已上線」？
- [ ] 做完後有沒有在接力棒或至少回覆教練時附上 commit hash / 具體憑證？
