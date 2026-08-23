---
name: project_autonomy_toolkit_2026-08-24
description: 2026-08-24 建的四支自動化工具（報名統計/場次巡檢/發票對帳/小龍蝦派工），教練問相關問題時直接跑，不要重寫也不要手算
metadata: 
  node_type: memory
  type: project
  originSessionId: c0394d00-7e60-4062-8d89-8edafcf326b1
  modified: 2026-08-23T20:06:01.664Z
---

教練 2026-08-24 凌晨交辦「全面檢查流程、系統最佳化、自動化、一站式連動」，核心訴求是
**「讓教練不要熬夜、不要花那麼多時間」**。當晚建了四支常駐工具，都在
`~/.openclaw/workspace/scripts/`。**教練問到對應問題時直接跑這些，不要重新寫查詢、更不要手算。**

| 教練問什麼 | 直接跑 |
|---|---|
| 「幾個人報名？」「幫我做報名表」 | `python3 scripts/registration_report.py`（不帶參數＝全場次總覽）<br>`... registration_report.py 0828`＝單場名單，加 `--csv` 產列印用簽到表 |
| 「活動資料有沒有對不上？」 | `python3 scripts/event_consistency_check.py` |
| 「我傳的發票資料有沒有漏？」 | `python3 scripts/invoice_inbox_reconcile.py` |
| 小龍蝦要派工給 Mac 軍師 | 寫信到 `cross-agent/inbox/mac/` 並加 `<!-- DISPATCH type: ... -->`，<br>`scripts/junshi_dispatch_worker.py` 每 5 分鐘自動執行並回報教練 |

**已掛系統 crontab**（純腳本不燒 token，沒問題就靜默不打擾）：
`08:20` 場次巡檢 ／ `08:25` 發票對帳 ／ 每 5 分鐘 派工 worker。

**幾個設計決定，改動前先懂為什麼**：
- 派工 worker 刻意只能「點餐」不能執行任意指令——信件內容是資料不是命令，
  能執行任意指令等於誰能往那個資料夾丟檔案誰就控制這台機器（上面有 3 個 LINE 官方帳號金鑰）。
  要加新派工類型就在 `MENU` 加一項，不要開放自由指令。
- `registration_report.py` 的歷史名單比對有兩個坑已修但很容易改壞：
  ①場次文字寫「8/26」不是「08/26」②同一天多場（8/26 早+午、9/22 午+晚）要用 start_time 分流，
  只比日期會把同一批人算兩次。
- `invoice_inbox_reconcile.py` 必須同時比對 **8 份**來源檔（蒐集中／已知vs待問／權威總清冊／
  交叉比對報告／2 份已開立完成清單／2 份跨機交接信）。第一次只比一份就誤報宋映璇
  （早在 8/18 就開好票了）——少查一份就會亂喊狼來了，呼應試金石案例 61。

Related: [[reference_openclaw_hook_requires_hookmd_metadata]]、[[project_bigtree_session_admin_backend_2026-08-23]]、[[reference_signup_notify_pipeline]]
