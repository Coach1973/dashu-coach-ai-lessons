---
name: project-seabiscuit-dashboard-2026-07-26
description: seabiscuit.bymyway.com 監控後台上線，Cloudflare Tunnel ingress設定變更記錄(不在git範圍內的基礎設施狀態)
metadata:
  type: project
---

教練要求為「教練都在想什麼」LINE小幫手建立獨立監控後台，仿照 `bni.bymyway.com` 模式，取名 `seabiscuit.bymyway.com`。

**Why:** 教練要看服務品質和回應狀況，需要跟bni_tainan一樣的獨立監控入口。

**How to apply:**
- Cloudflare Zero Trust網頁後台要求先輸入帳單資訊才能進入管理介面(billing paywall)，未替教練輸入任何付款資料
- 改用 `cloudflared tunnel route dns openclaw-macmini seabiscuit.bymyway.com` (CLI，走本機cert.pem認證，不受網頁付費牆限制)建立DNS CNAME
- 再用臨時建立、範圍限縮為「Cloudflare Tunnel:Edit」、7天有效期的API Token，透過 `PUT /accounts/{account}/cfd_tunnel/{tunnel}/configurations` 把新hostname加進tunnel `openclaw-macmini`(e35d30ec-45cf-4854-8afc-1bf92b163231)的ingress規則，指向`http://localhost:18789`(跟bni.bymyway.com同一個服務)
- 設定版本從 version 11 → version 12
- 完成後立即刪除該臨時API Token(Cloudflare後台+本機檔案皆已清除，不留常駐高權限金鑰)
- 本機openclaw.json同步新增 `gateway.controlUi.allowedOrigins` 加入 `https://seabiscuit.bymyway.com`（此部分已隨commit `8b73bbea` 進git）

**驗證**：`curl https://seabiscuit.bymyway.com/` 回200，`get_page_text`確認顯示OpenClaw Control登入頁，密碼沿用既有`Bymyway7`(gateway.auth.password未變動)。

相關：[[project_vps_self_onboard_hook_2026-07-06]]（bni.bymyway.com同套Cloudflare tunnel模式的前例）
