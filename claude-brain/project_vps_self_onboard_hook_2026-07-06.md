---
name: project-vps-self-onboard-hook-2026-07-06
description: VPS小龍蝦(43.245.60.200)新增vps-onboard-approve機關，讓它自己核准+開通新朋友，不靠Mac/Hermes；含真實bug發現與修復
metadata:
  type: project
  originSessionId: f94a84d7-dc78-4966-9311-844652976917
---

教練要求：VPS 小龍蝦要能自己完成「核准+開通新朋友」，完全不依賴 Mac 或 Hermes VPS。

**架構釐清（查證後才知道，不是原本假設）：**
- OpenClaw 原生就有「pairing」核准機制（`openclaw pairing list/approve`），陌生人第一次傳訊息會先卡在這關，核准後才會流到下一步
- 另有一支 `auto-provision-stranger` hook 專門負責「建立獨立空間」，但它從未真正因為真實陌生人的訊息而觸發過——之前查到的「8位真實朋友」都是走更早的手動流程建立的
- VPS 小龍蝦本人（agent "main"）原本不會操作 pairing 指令，因為 `VPS_CORE_RULES.md` R09/R12 明講「無法執行 bash 指令、無法執行本機操作」——這是體驗版刻意設計的安全限制

**建立的新機關：**
- `/root/openclaw/data/hooks/vps-onboard-approve/handler.js`，註冊在 `openclaw.json` → `hooks.internal.entries.vps-onboard-approve`
- 邏輯：教練對小龍蝦說「核准/開通/放行/批准/通過 + 對象」→ hook（以Node程式碼身分，不受LLM工具權限限制）查待核准清單 → 比對目標 → `openclaw pairing approve` → 直接建立獨立workspace + agents.list + bindings（沿用 auto-provision-stranger 同款邏輯）→ 觸發 Docker 自動重啟套用設定

**🔴 真實 bug（端到端實測才抓到，不是紙上談兵）：**
1. 關鍵字比對只認「核准/開通/放行」三詞，教練實際講「批准」時沒被認出
2. 抓訊息文字的欄位優先序錯了：優先抓到 `c.transcript`（系統包了時間戳/寄件人資訊的組合字串，例如「[Telegram coach id:... 時間] 批准 XXX」），而非 `c.body`（使用者真正輸入的乾淨文字）。錨定式正則 `^(核准|開通|放行)` 因此永遠比對不到

**修復：** 調整候選欄位順序讓 `c.body` 優先，正則改為 `/(核准|開通|放行|批准|通過)\s*(.+)/`（不錨定開頭，含同義詞）。

**驗證方式（不只是「應該會動」，是真人實測）：**
教練用全新 Telegram 號碼（coach wu, ID `8820573555`）實際測試——訊息卡在待核准 → 教練核准 → 用第一版機關發現核准成功但沒建空間（bug 現形）→ 修復機關 → 手動補完這筆漏掉的建空間動作 → 重啟後驗證：agents/bindings 從 9 筆變 10 筆，教練本人 main 綁定完全未受影響，新帳號 workspace 檔案（AGENTS.md/SOUL.md/USER.md等）正確建立。

**Why：** 教練要 VPS 完全自主，不要每次都要問 Mac 或透過 Hermes 中介——這是守則#12「拒絕當資訊搬運工」在系統設計層級的落實。

**How to apply：** 未來若要修改這支 hook 的觸發詞或邏輯，記得欄位優先序這個坑（`c.body` 才是乾淨原文）；且任何「應該會動」的機關，沒有真人實測走過一輪之前，都不能算數——這次如果只做完程式碼就回報「完成」，不會發現這個 bug。相關：[[project_hermes_vps_shutdown_evaluation_2026-07-06]]。
