---
name: project-opencode-ccswitch-moved-to-e-2026-07-25
description: OpenCode桌面版與CC Switch的使用者資料已搬到E槽junction保護，過程中CC Switch的settings.json/log意外遺失（真正的provider資料庫沒事）
metadata:
  type: project
  originSessionId: d268c1f5-61c8-4d8a-b08f-ea791a6ff0a1
  modified: 2026-07-25T06:05:31.947Z
---

2026-07-25，7/24 LINE junction事故善後期間，教練主動問「這些設定會不會也被下次一鍵還原洗掉」，比照LINE/Chrome/Comet既有SOP把兩套App的使用者資料搬到E槽：

- **OpenCode桌面版**：`.config/opencode`、`.local/share/opencode`（對話資料庫）、`AppData/Roaming/ai.opencode.desktop`（視窗狀態）三個資料夾，全部搬到`E:\Claude-Data\AppData\OpenCode-{Config,LocalShare,Roaming}`，C槽原位置改建junction。
- **CC Switch**：`.cc-switch`（含provider網址/API金鑰的`cc-switch.db`）搬到`E:\Claude-Data\AppData\CCSwitch-Config`。

**🔴 過程中的教訓**：CC Switch搬移時App其實還在背景執行（`tasklist`關鍵字搜尋漏看，因為程序名稱`cc-switch.exe`中間有連字號），第一次刪除舊資料夾時檔案被鎖只刪掉一部分（`settings.json`、log檔），事後用`robocopy /MIR`同步這個不完整狀態，把這兩個檔案也從E槽目的地一併清掉了。**真正重要的`cc-switch.db`（所有provider的URL/API金鑰）全程被程式鎖住沒被動到，資料本身沒有遺失**，只有「目前選用哪個provider」這個UI狀態需要教練重開後手動再選一次。

**Why：** 關程式前用`tasklist`確認時，關鍵字搜尋要考慮程序名稱可能帶連字號等變體，不能只用最直覺的字串比對；用`robocopy /MIR`同步前，若來源資料夾的檔案數量跟預期不符（這次從13個掉到1個），要先停下來查為什麼少了，不能照樣同步覆蓋過去。

**How to apply：** 之後搬其他App資料到E槽前，先用更寬的條件（例如WMI查ExecutablePath）確認程式真的完全關閉，不要只信`tasklist`的簡單關鍵字比對；robocopy前後的檔案數量如果有落差，要先解釋清楚落差原因再繼續，不能只看「來源目的地一致」就放行。

- OpenCode程式本體：C槽（7/25當天新裝）
- CC Switch程式本體：D槽（`D:\Users\bymyw\AppData\Local\Programs\CC Switch`，6/14建立，從未被任何C槽還原動到）

Related: [[project-line-moved-to-e]], [[feedback-data-move-du-sh-verify]]
