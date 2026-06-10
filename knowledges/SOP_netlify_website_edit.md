# 網站修改 SOP（標準作業程序）

> 教練親定 2026-05-30，更新 2026-06-06，所有 AI 助教（終端機/桌面版/小龍蝦/Hermes）強制遵守。

---

## 🔴 站台分流鐵律（教練 2026-06-06 親定）

| 站台 | 平台 | 費用 | 使用時機 |
|------|------|------|---------|
| coach1973 GitHub Pages | GitHub | **免費** | 開發、測試、日常更新 |
| Netlify（超限戰等公開站） | Netlify | **扣點** | 確認完善後才同步 |

**規則：**
- coach1973.github.io 底下的站（如 cool-case）→ **直接 git push 到 gh-pages 分支**，不走 Netlify
- Netlify 站（theunrestrictedwar、jiesheng-leadership 等）→ 走下方七步驟
- **嚴禁未確認就推 Netlify**，扣點不可逆

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
