# team.bymyway.com 程式本體已完成，請軍師接手正式網域部署

> **寄件人**：Mac 終端機（軍師）
> **收件人**：Mac 終端機（軍師，下一棒）
> **時間**：2026-09-01 03:35 台灣時間
> **教練是否在場**：是，教練親口要求軍師直接接手做，不要等 Hermes

## 任務狀態

✅ **程式本體 100% 完成並推上 GitHub**（Hermes 那邊 3.5 小時零進度，軍師直接動手，詳見 v156 接力棒記錄的 ai-art 模式）

## 你（下一棒軍師）要做的事：正式網域部署

跟 bni-chapters 一樣的標準流程（DNS + Cloudflare Tunnel + launchd 背景服務三件套）。

### Repo 位置
- 本機：`/Users/bymyway/github_repos/team-bymyway/`
- GitHub：`https://github.com/Coach1973/team-bymyway`（剛剛推上去，main 分支）
- 公開網站目標：`team.bymyway.com`（教練指定）

### 需要的部署決策（建議先看路徑大全）

1. **DNS**：在 Cloudflare bymyway.com 加一筆 `team` 子網域（A 或 CNAME），指向要部署的位置
2. **Cloudflare Tunnel**：新開一組 tunnel（不要跟 bni-chapters 共用），命名 `team-bymyway`
3. **launchd 看護 plist**：新寫一支 `com.coach.team-webapp.plist`（背景服務，永駐不漏接）
4. **本機服務**：跑在 port 5073（已在 app.py 改好，env 變數 `TEAM_PORT`）
5. **環境變數**：
   - `TEAM_SECRET_KEY`：隨機產 32 字，建議用 `python3 -c "import secrets; print(secrets.token_urlsafe(32))"` 然後寫進 launchd plist 的 EnvironmentVariables
6. **venv 借用**：先用 `/Users/bymyway/github_repos/bni-chapters/venv/`（跟 v152 處理 bigtree-tw 同個模式，避免重複安裝套件），**正式上線前建議遷到自己獨立的 venv**

### 部署步驟（跟 bni-chapters v148 那次大同小異）

1. Cloudflare DNS 加 `team.bymyway.com` → Tunnel endpoint
2. `cloudflared tunnel create team-bymyway`（用教練的 Cloudflare 帳號）
3. 寫 `/etc/cloudflared/team-bymyway.yml`（或放 `~/.cloudflared/`）
4. 到 `/Users/bymyway/github_repos/team-bymyway/` 跑：
   - `git pull`（拿最新程式碼）
   - `cloudflared tunnel route dns team-bymyway team.bymyway.com`
5. 寫 launchd plist（參考 `com.coach.bni-chapters-webapp.plist`，改成 `com.coach.team-webapp`）
6. `launchctl load` 啟動背景服務
7. `curl https://team.bymyway.com/` 驗證 200
8. `https://team.bymyway.com/team-01` 驗證分會頁面可訪問

### 部署前完整檢查清單

- [ ] Cloudflare DNS 設定完成
- [ ] Cloudflare Tunnel 建立完成並 route DNS
- [ ] launchd plist 寫好並 load
- [ ] 本機 port 5073 跑得起來（驗證：`/Users/bymyway/github_repos/bni-chapters/venv/bin/python3 app.py`）
- [ ] 環境變數 `TEAM_SECRET_KEY` 已設定
- [ ] `https://team.bymyway.com/` 回 200
- [ ] `https://team.bymyway.com/team-01` 渲染正確（teal 主題、3 個示範分會可見）
- [ ] `/admin/login` 可以登入（教練會在後台改預設密碼）
- [ ] **首次部署後通知教練實際操作**，因為這個網站的視覺風格（teal vs BNI 紅黑）、示範文案（第一/第二/第三分會佔位）教練可能要在後台大幅修改

### 已知風險（跟 v148 peipei-event 斷線 5 天是同一類）

⚠️ 每次新開一個獨立子網域都是孤兒服務風險。本場已經把「單一服務分散到多個 launchd/Tunnel」的病根寫進記憶（`reference_bymyway_subdomain_530_missing_launchd_2026-08-29`），新網域一定要當天上 launchd，不要拖到隔天。

### Commit hash 跟 commit message

`e9d87dc` — feat: team.bymyway.com 通用分會系統（複製bni-chapters架構，去BNI品牌）

### 如果你（下一棒軍師）要查 v152 大樹小講怎麼脫離 Netlify

看 `JUNSHI_HANDOFF_LATEST.md` v152 那段，**那邊不是這次任務**，不要被誤導。**這次任務是建新網域，不是脫離 Netlify**。

— Mac 軍師
2026-09-01 03:35 台灣時間
