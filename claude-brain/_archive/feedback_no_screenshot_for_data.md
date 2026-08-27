---
name: 禁止用截圖讀取系統資訊
description: 查進程、記憶體、系統狀態一律用終端指令，不用截圖
type: feedback
originSessionId: fc769ef4-d5d8-4036-a479-2b86be5d88b8
---
## 規則一：系統資訊查詢不用截圖

優先用 ps、top、vm_stat、launchctl、lsof 等指令直接讀取系統資訊，不要用截圖去看 Activity Monitor 或其他 UI。

## 規則二：能用指令或 API 完成的操作，不用截圖點擊

凡是能透過終端指令、系統指令、API 呼叫完成的任務，一律走指令路線。截圖 + 滑鼠點擊只用在「非得看畫面才能操作」的情境（例如：UI 畫面無指令可達、需要確認視覺呈現是否正確）。

**Why:** 每張截圖消耗大量 token（約 1,000–2,000），且速度慢。教練 2026-05-08 明確指出：助教守則裡應有「盡可能不要用截圖」這條規則。以「關閉 iPhone 來電轉接」為例，macOS defaults 指令可直接完成，不需要開 FaceTime → 截圖 → 點按鈕的流程。

**How to apply:**
- 改系統設定 → 先查有無 `defaults write` 或 `osascript` 指令可達
- 查程序/記憶體/網路 → 終端指令
- 操作 App 設定 → 先查有無 CLI / API
- 截圖只用於：確認視覺結果、純 UI 操作無其他路徑、教練要求看畫面
