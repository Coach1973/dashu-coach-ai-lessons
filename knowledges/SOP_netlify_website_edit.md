# 網站修改 SOP（標準作業程序）

> 教練親定 2026-05-30，更新 2026-06-06，2026-06-13 增補 Cowork 分工，2026-06-17 補上「Chrome 唯一預覽鐵律」放最頂，所有 AI 助教（終端機/桌面版/小龍蝦/Hermes）強制遵守。

---

## 🔴🔴🔴 預覽鐵律（2026-06-17 教練第二次親口提醒後寫死，違反 = 守則 #07 同處跌倒）

**本機 HTML 預覽唯一指定瀏覽器 = Google Chrome。**

| 場景 | 唯一正確指令 |
|------|------------|
| 開本機 file:// | `open -a "Google Chrome" /absolute/path/to/index.html` |
| 開本機 server | `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window http://localhost:8899/` |
| 開線上 URL 給教練看 | `open -a "Google Chrome" "https://theunrestrictedwar.netlify.app/"` |

### 禁止做的事

- ❌ `open <path>` 不指定 -a（會走系統預設，可能跳 Safari）
- ❌ `open -a Safari ...`（教練不用 Safari）
- ❌ **觸發 Claude Code 內建 Launch preview panel（教練 2026-06-17 三度強調）**——這個面板展不開、看不到整體，教練每次都要手動關閉造成困擾，AI 每次開啟也浪費資源
- ❌ 用 Write 工具寫到 /tmp/ 期待 Launch 面板顯示

### 🔴 AI 端怎麼避免觸發 Launch 預覽面板

Claude Code 的 `Edit` / `Write` 工具動 HTML 檔會**自動**觸發 PostToolUse hook 把檔案推進 Launch 預覽面板（無 settings.json 開關可關）。所以 AI 端要主動避開：

| 改 HTML 的方式 | 會觸發 Launch 預覽？ |
|---------------|------------------|
| `Edit` 工具 | ✅ 會觸發（教練不要） |
| `Write` 工具 | ✅ 會觸發（教練不要） |
| `Bash` + `python3` / `sed` / `awk` 改檔 | ❌ 不會觸發 ✅ 採用 |

**標準作法**：HTML 改動寫成 Python 腳本透過 Bash 跑（精準替換 + 不觸發預覽）：

```bash
python3 << 'PY'
import re
with open("index.html","r",encoding="utf-8") as f: s = f.read()
s = s.replace("舊字串", "新字串")
with open("index.html","w",encoding="utf-8") as f: f.write(s)
PY
```

改完直接 `open -a "Google Chrome"`，省去教練關預覽面板的麻煩。

### Why
教練 2026-06-17 第二次親口提醒：「之前打開都是用 chrome 為何這次是使用 safari？唯一指定開啟的 html 就是 chrome」。
這條 SOP 本來在 L141 就寫過，但軍師沒落實——這次升為**全 SOP 第一條**，每場讀 SOP 第一眼就看到。

---

## 🤝 Cowork ＋ 軍師分工（特別優惠流量期間，有效至 2026-07-05）

> 詳細 SOP 見 `workspace/SOP_cowork_plus_code_workflow.md`（軍師 commit 25d84ae9）

**簡要：** Cowork 修改＋commit → 教練說「推」→ 軍師 30 秒 push。
**到期後：** 回本 SOP 原本流程（教練自行在終端機 push）。

---

## 🔴 站台分流鐵律（教練 2026-06-06 親定，2026-06-13 H 血淚增補）

| 類型 | 站台 | 更新路徑 | 費用 |
|------|------|---------|------|
| GitHub Pages | cool-case, teamwork/rpl | git push gh-pages → 自動 | 免費 |
| Netlify（GitHub 自動部署型）| **jiesheng-leadership** | git push main → Netlify 自動 hook | **扣點** |
| Netlify（手動上傳型）| theunrestrictedwar 等 22 站 | zip + Netlify API 推送 | **扣點** |

**⚠️ 2026-06-13 H 踩雷紀錄（必讀）：**
- jiesheng-leadership 的 Netlify 站台設定 `repo_url: github.com/Coach1973/jiesheng-leadership` → 它走的是 GitHub 自動部署，不是手動 zip 上傳
- H 的 Netlify token 可 GET 但 POST deploys 被拒（Access Denied）——因為這個站根本不走 API 推
- **jiesheng-leadership 唯一更新路徑：git push main → Netlify 自動部署**
- H 沒有 GitHub token → 改由軍師（Mac 終端機，gh CLI 有效）來 push

**規則：**
- coach1973.github.io 底下的站（cool-case, teamwork 等）→ **git push gh-pages 分支**
- jiesheng-leadership → **git push main**（GitHub 自動觸發 Netlify 部署）
- theunrestrictedwar 等其他 Netlify 站 → **走下方七步驟（zip + API）**
- **全部站台：推之前等教練確認，教練說「推」才動**
- **嚴禁未確認就推，扣點不可逆**

**如何判斷一個 Netlify 站是哪種類型：**
```bash
curl -s -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" \
  "https://api.netlify.com/api/v1/sites/{site_id}" | python3 -c "
import json, sys; d = json.load(sys.stdin)
print('repo_url:', d.get('build_settings', {}).get('repo_url', '無 → 手動上傳型'))"
# 有 repo_url → GitHub 自動部署型（走 git push）
# 無 repo_url → 手動上傳型（走 zip + API）
```

### coach1973 GitHub 站台修改流程

> 🔴 **GitHub 自動部署站也要等教練確認才 push（2026-06-11 血淚）**
> jiesheng-leadership 就是 GitHub 自動部署站，push 等於部署，每次都扣點。
> **所有修改全部做完 → 讓教練確認 → 才 push 一次**，不要分批 push。

```bash
# 本機 clone 路徑
cd /Users/bymyway/github_repos/cool-case   # cool-case 範例

# 1. 先 pull 確保最新
git pull

# 2. 做完所有修改（先別 push）
# 用 Edit / sed 工具修改，所有改動都做完

# 3. 本機預覽讓教練確認
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window http://localhost:8899/

# 4. 教練說「推」才 commit + push（只推一次）
git add .
git commit -m "說明修改內容"
git push origin gh-pages
```

確認上線：`https://coach1973.github.io/cool-case/`

---

---

## 第一步：下載現有版本

```bash
# 1. 找到站台 Site ID
curl -s -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" \
  "https://api.netlify.com/api/v1/sites" | python3 -c "
import json, sys
for s in json.load(sys.stdin):
    if '關鍵字' in s.get('name',''):
        print(f'{s[\"name\"]}  ID: {s[\"id\"]}  URL: {s.get(\"ssl_url\",\"\")}')"

# 2. 列出最新部署的檔案清單
curl -s -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" \
  "https://api.netlify.com/api/v1/sites/{site_id}/deploys?per_page=5" | python3 -c "
import json, sys
for d in json.load(sys.stdin):
    print(f'Deploy: {d[\"id\"]}  {d[\"created_at\"]}  {d[\"state\"]}')"

# 3. 列出該部署的所有檔案
curl -s -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" \
  "https://api.netlify.com/api/v1/deploys/{deploy_id}/files" | python3 -c "
import json, sys
for f in json.load(sys.stdin):
    print(f'{f[\"path\"]}  ({f.get(\"size\",\"?\")} bytes)')"

# 4. 用 deploy URL 下載所有檔案（不是 API，是直接 URL）
mkdir -p /tmp/站台名稱
curl -sL "https://{deploy_id}--站台名稱.netlify.app/index.html" -o /tmp/站台名稱/index.html
curl -sL "https://{deploy_id}--站台名稱.netlify.app/圖片.png" -o /tmp/站台名稱/圖片.png
# 逐一下載所有檔案
```

⚠️ 注意：用 `file` 指令確認下載的是真正的圖片，不是 JSON metadata。

---

## 第二步：建立 _headers 檔

```bash
cat > /tmp/站台名稱/_headers << 'EOF'
/*
  Content-Type: text/html; charset=UTF-8
EOF
```

不帶 _headers 會變成 text/plain 顯示原始碼。

---

## 第三步：修改 HTML

- 直接修改 `/tmp/站台名稱/index.html`
- 如果要隱藏某區塊，做備份：`cp index.html index_備份名稱.html`
- 所有修改在本機完成，不碰線上

---

## 第四步：本機預覽（必做）

```bash
# 啟動本機伺服器
python3 -m http.server 8899 --directory /tmp/站台名稱 &

# 開瀏覽器讓教練查看（🔴 不用 open，Chrome 可能沒在跑）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window http://localhost:8899/
```

> ⚠️ 教練透過 RustDesk 遠端看 Mac，localhost 是可以看到的。
> ⚠️ 禁止用 Claude Code 的 Write 工具把預覽 HTML 寫到 /tmp/，那只會觸發右側 Launch 面板，教練透過 RustDesk 看不到。必須開 Mac 桌面瀏覽器。

---

## 第五步：等教練確認

🔴 **教練說「推」或「沒問題」之前，絕對不推。**

---

## 第六步：一次性推送

```bash
cd /tmp/站台名稱
zip -r /tmp/deploy.zip .
curl -s \
  -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" \
  -H "Content-Type: application/zip" \
  --data-binary "@/tmp/deploy.zip" \
  "https://api.netlify.com/api/v1/sites/{site_id}/deploys" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Deploy ID: {d[\"id\"]}')
print(f'State: {d[\"state\"]}')
print(f'URL: {d.get(\"ssl_url\",\"\")}')"
```

---

## 第七步：線上驗證

```bash
curl -sL https://站台名稱.netlify.app/ | grep "關鍵文字"
```

確認新內容真的上線了。

---

## 常見站台 Site ID 速查

| 站台 | Site ID |
|------|---------|
| jiesheng-leadership | d31aec07-5153-4daa-a2d7-d6fb24083319 |
| northern-tw | f1f3ed15-79b6-4bed-b4d1-0199a185a181 |
| northern-tw-test | 56d3fa7e-41bd-40d9-8000-2e9b779b0461 |
| theunrestrictedwar | 查 reference_netlify_token.md |
| cool-case | 查 reference_netlify_token.md |

---

## 禁止事項

- ❌ 禁止用 git push 部署
- ❌ 禁止未經教練確認就推送
- ❌ 禁止「推完再看」
- ❌ 禁止連續推修小問題——一次改完、一次驗完、一次推
- ❌ 禁止不帶 _headers 檔
- ❌ 禁止不包圖片（上次漏圖封面消失的血淚教訓）

---

> 本 SOP 由軍師建立（2026-05-30），教練親定。
> 違反 = 守則 #03（自我驗證）+ #08（花時間討論就是為了執行）雙重違規。
