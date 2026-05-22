---
name: coach-rustdesk-remote-env
description: 教練平常是從 Windows 桌機透過 RustDesk 遠端連線操作這台 Mac，鍵盤滑鼠都是 Windows 端的
metadata: 
  node_type: memory
  type: project
  originSessionId: ddc5e99b-ea0c-43f0-8898-5b61266824c4
---

教練操作這台 Mac 的方式：**從 Windows 桌機透過 RustDesk 遠端連線**，鍵盤、滑鼠用的都是 Windows 端的硬體，畫面也是遠端投過來的。

**Why:** 2026-05-22 排查「打 E/F/I/M 觸發快捷鍵」問題時才揭露這個環境。跨平台（Windows→Mac）遠端連線會引入一整層本機看不到的變因（按鍵映射、修飾鍵卡住、傳輸丟包、畫面延遲）。

**How to apply:**
- 教練回報「鍵盤怪怪的、按鍵變快捷鍵、滑鼠飄」這類問題，**先把 RustDesk 跨平台這層列入嫌疑**，不要一頭栽進 Mac 本機設定。
- 已確診案例：打字母變快捷鍵（F→全螢幕、E→表情、I→搜尋）是 RustDesk 把 Command+Control 修飾鍵「卡在按住狀態」造成的，時好時壞、跨所有 App 與輸入法。即時解＝Windows 端各修飾鍵(Ctrl/Alt/Shift/Win)按一下放開／斷線重連。對應 RustDesk issue #5707。
- **RustDesk 鍵盤模式（教練 2026-05-22 親測）：要用「1:1 傳輸模式」(Map mode)，嘸蝦米才正常可用；「傳統模式」(Legacy) 會讓嘸蝦米輸入法消失/不能用。翻譯模式(Translate) 尚未測。→ 教練電腦預設請固定用 1:1 傳輸模式。**
- 截圖成本考量：畫面是遠端的，截圖更貴更慢，能用指令查就別截圖（呼應截圖鐵律）。
- 相關：[[feedback_voice_typo_shixing_shouze]]（香草/小草輸入法的語音對映）。
