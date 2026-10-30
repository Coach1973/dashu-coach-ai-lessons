---
name: feedback-letters-to-junshi-go-to-inbox-not-outbox
description: 寫信給別台軍師一律放 cross-agent/inbox/<收信人>/，不是 outbox（歸檔用）；寫完要從雲端讀回確認；聯想誤放 outbox 被教練罵(2026-10-28)
metadata:
  type: feedback
---

2026-10-28 21:43 聯想把換 NMDA 理監事頁照片的交接信放在 `cross-agent/outbox/2026-10/`，Mac 說「讀信」只讀 `inbox/mac/`，讀不到；教練：「寫信給軍師你又不是第一次寫，怎麼會犯這麼低級的錯誤？」

**Why:** README 鐵律：教練不傳話、路徑永遠不變＝`inbox/{對方機器}/`；outbox 是已讀已處理的歸檔。我寫信時沒對照 SOP，憑印象放。
**How to apply:** 要叫別台做事＝檔名 `{YYYYMMDD-HHMM}_{from}-to-{to}_{topic}.md` 放 `cross-agent/inbox/<收信人>/`，信頭寫寄件人／收件人／口令；聯想 workspace 常落後雲端幾百個版本，要用臨時 worktree 從 origin/main 開、只 commit 那一個檔再 push，推完用 `git ls-tree origin/main` 驗證在對的資料夾。跟教練只說一句「請在 Mac 說讀信」。相關：[[reference-cloud-letters-to-junshi-path-2026-10-06]]。
