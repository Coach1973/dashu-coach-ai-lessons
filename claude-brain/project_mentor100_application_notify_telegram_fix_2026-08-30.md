---
name: project_mentor100_application_notify_telegram_fix_2026-08-30
description: mentor100(百人導師)申請通知從LINE(sme-register-fn)改走Telegram，修復8/27靜默漏接事故
metadata: 
  node_type: memory
  type: project
  originSessionId: 90ed8b02-52bf-4620-8c47-59ea26a8ef70
  modified: 2026-08-30T13:34:21.329Z
---

教練回報：2026-08-27有人提交AI百人導師團隊申請，但教練Telegram完全沒收到通知，還誤以為對方沒提交而重複去提醒，結果發現重複。查證`/Users/bymyway/github_repos/mentor100/app.py`的`apply_submit()`，根因是通知函式`_notify_coach_line()`打的是舊版Netlify function `https://sme-register-fn.netlify.app/.netlify/functions/register`（LINE通道），且用`except requests.RequestException: pass`吞掉錯誤——跟event-signup試金石案例62（報名通知LINE月配額用完靜默失敗一整週）是完全同一種坑，只是這次發生在另一個獨立專案（mentor100）身上，因為當初event-signup修復時沒有連帶盤點其他也在用sme-register-fn的專案。

已改用event-signup已驗證過的Telegram Bot API直送方案（讀`~/.openclaw/openclaw.json`的`channels.telegram.accounts.bot_main.botToken`，直送教練個人chat_id`6124913915`），失敗一律寫進`notify_failures.log`不再靜默吞掉。已用真實`/apply`端點提交測試驗證（無失敗log產生，webapp.error.log顯示302成功），測試資料已從`mentors.db`的applications表清除。commit`1b9b816`（mentor100 repo）。

已順手全機掃描`sme-register-fn`/`_notify_coach_line`/`COACH_LINE_USER_ID`，確認mentor100是唯一還沒遷移的專案，event-signup裡的殘留只是註解提及歷史，非活著的呼叫路徑。

**Why**：這類「靜默失敗的第三方通知呼叫」屬於同一種病根會在不同專案各自復發的類型——每次修好一個不代表全部都好，因為每個Flask小專案是各自獨立的程式碼庫，沒有共用的通知函式庫。
**How to apply**：往後任何新開的、需要通知教練的小專案，直接複製event-signup的`_notify_xiaolongxia()`/`_log_notify_failure()`寫法（讀openclaw.json bot_main token直送chat_id，失敗必寫log），不要各自發明或沿用舊的LINE/Netlify function路徑。若之後又聽到教練說「我都沒收到通知」，第一步就是grep全機`sme-register-fn`/`netlify.*notify`/`LINE.*notify`類字串抓還沒遷移的專案，不用重新排查。

Related: [[reference_telegram_registration_notify_group]]（event-signup同款修復的原始案例）
