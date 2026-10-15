---
name: reference_lenovo_memory_ntfs_nonpaged_pool_leak_2026-10-15
description: 聯想記憶體從50%飆到77%＝核心非分頁集區 NtFC(ntfs.sys) 漏 15GB，不是程式在吃；工作管理員看不到；怎麼查、重開機才釋放；同場移除 ChatGPT(套件名 OpenAI.Codex)
metadata:
  node_type: memory
  type: reference
  originSessionId: 4aac7f25-d657-43c8-a422-e28fd94a634d
  modified: 2026-10-15T07:10:34.308Z
---

2026-10-15 教練問「記憶體本來50%以下現在70~80%，誰佔的」。查證結果：
- 所有程式合計只約 15GB（claude 2.8、comet 2.2、svchost 2.0…），**核心「非分頁集區」16GB**（正常 0.5~1GB）。
- 用 NtQuerySystemInformation(class 22, SystemPoolTagInformation) 列 pool tag（不需管理員，腳本在 `%TEMP%\mem_check_20261015\pooltags.ps1`）：**NtFC＝15,005MB、1.2 億筆未釋放**，`grep -a NtFC drivers/*.sys` → **ntfs.sys**。
- 取樣 25 秒 NtFC 完全沒漲＝過去某段時間累積、現在沒在漏。已開機 300 小時（10/3 起）。**只有重開機會釋放**。
- 🔴 NordVPN 已排除（教練 10/15 糾正「我沒開它、它也沒在跑，為什麼是嫌疑犯」）：mshield.sys 登錄有、但 **State=Stopped**；正在跑的硬碟過濾驅動全是微軟的。教訓：**列嫌疑前先查它有沒有在執行**（Win32_SystemDriver State），「有登記」不等於「有在跑」。注意 nordsec-threatprotection-service 服務本身是 Running（自動啟動），但驅動沒掛。重開後若再漲，要用 Windows 內建 `wpr -start Pool` 抓是哪個程式觸發（需管理員同意）。
- 🔴 **快速啟動開著（HiberbootEnabled=1）：按「關機」再開不會清核心記憶體，要按「重新啟動」**。10/3 01:03 那次開機前沒有正常關機紀錄（疑當機/斷電）。14:14 再量 15,008MB，16 分鐘只漲 2.6MB（慢漏，過去曾爆量）。
- 追蹤機制：`scripts/ntfc_leak_watch.py` 掛 UserPromptSubmit（教練說話才量，0.1 秒，不輪詢），狀態檔 `E:/Claude-Data/.claude/state/ntfc_watch.json`；偵測重啟記新起點、跨 1/2/4/8GB 各提醒一次、沒放掉會提醒要按重新啟動（commit 6cc2286eb）。教練 10/15「重開之後，幫我查查」＝提醒跳出時就追查並回報。
- 🔴 **聯想 UAC 設成「不詢問直接給管理員」（ConsentPromptBehaviorAdmin=0、PromptOnSecureDesktop=0）**：Start-Process -Verb RunAs 不會跳任何視窗。10/15 我叫教練「按是」三次，教練根本沒看到東西被問「是跳在你看得到我看不到的地方嗎」。這也可能是 Gemini/ChatGPT 能不問就裝上的原因。**10/15 14:27 教練自己調成 ConsentPromptBehaviorAdmin=5（通知、不調暗桌面）**，之後 RunAs 會跳視窗，要先告訴教練「會跳出視窗請按是」，並確認真的有跳。
- 用管理員跑的 PowerShell 腳本要**全英文**（Windows PowerShell 5 讀無 BOM 中文會壞掉）；Start-Transcript 不會記下 wpr 的輸出，要確認錄製狀態請用管理員身份跑 `wpr -status` 並寫進檔案再讀。
- 10/15 14:23:18 開始用 WPR 只錄 NtFC（設定檔 `%TEMP%\ntfc_trace_20261015\ntfc.wprp`）1 小時 → ntfc.etl，用 tracerpt 轉 CSV 看是哪個 PID 在要。
- ✅ 10/15 14:50 教練重新啟動：NtFC 歸 0、核心非分頁集區 0.90GB、整體使用率 40%（重開前 77%）；追蹤 hook 開新對話第一句就自動跳出，實測有效。WPR 錄製因重開中斷（那段時間本來就沒漏），兇手仍未知，等 hook 跨 1GB 提醒時再錄。
- 分頁檔仍固定 4GB、committed 33.4GB → 跟 [[reference_lenovo_freeze_virtual_memory_exhausted_2026-10-08]] 同一種當機風險。

同場：ChatGPT 桌面版在 Windows 套件名是 **OpenAI.Codex**（開始選單叫 ChatGPT，所以「找不到解除安裝」），9/27 前後裝、10/11 被商店自動更新；我們的 git 紀錄查無 AI 安裝過。用 `Remove-AppxPackage OpenAI.Codex_…` 移除（不需管理員），已驗證開始選單消失。`%LOCALAPPDATA%\OpenAI`（設定檔）沒刪，刪檔鎖規則。
