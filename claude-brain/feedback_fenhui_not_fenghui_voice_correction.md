---
name: feedback_fenhui_not_fenghui_voice_correction
description: "語音糾偏(守則#18)通用規則——「真XX鋒會/峰會」一律理解成「真XX分會」，適用所有BNI分會，不用逐一確認"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d05983a9-16e3-4186-97eb-bc33e4614732
  modified: 2026-08-09T11:11:05.463Z
---

**通用規則（2026-08-09教練親口擴充）**：語音輸入聽到「真XX鋒會」或「真XX峰會」，
一律直接理解成「真XX分會」——這是BNI所有分會共通的語音辨識模式，不限於特定幾個分會
名稱，之後聽到就直接判斷，不用每次都問教練確認。

起源案例：教練預告的工作願景文件，正確名稱是**真誠分會、真愛分會、真AI分會**（「分
會」不是「峰會」）。之前接力棒/CLAUDE.md/部分蒸餾記錄誤寫成「真誠峰會、真愛峰會、
真實AI峰會」，是語音輸入辨識錯誤（2026-07-17 教練親口糾正：「語音輸入的問題，都是
分會」）。**⚠️名稱另一處更正**：「真實AI分會」是誤記，教練2026-07-31親口澄清正式
名稱是**真AI分會**（少一個「實」字），該分會尚未在BNI Connect登記。

**Why**：守則#18「語音糾偏必問不猜」——中文語音辨識常出現同音异字，「分會」跟「鋒會
/峰會」發音相近，容易被系統誤判成聽起來更「隆重」的詞（峰會=summit，分會=chapter/
branch meeting，意思完全不同）。教練2026-08-09明確要求把這條規則從「三個特定名稱」
升級為「所有真XX鋒會都是真XX分會」的通用判斷邏輯，不用每次不同分會名稱都再問一次。

**How to apply**：以後聽到「真OO鋒會/峰會」（OO代入任何分會名，如富/愛/誠/鑫/鑽/AI
等），直接寫成「真OO分會」，不用再問「這是分會還是峰會」。已修正 `JUNSHI_HANDOFF_
LATEST.md`、`CLAUDE.md` 兩份現行接力棒文件；歷史蒸餾逐字稿（`distill/terminal_
2026-07-14.md`、`distill/terminal_2026-07-16.md`）維持原樣不動，因為那是逐字紀錄語音
辨識當下的實際輸出，改了會失真，不是本次任務範圍。

Related: [[feedback_voice_typo_shixing_shouze]]（同類語音糾偏對映表案例）、
[[project_bni_three_chapters_vision_pending]]（真AI分會正式名稱更正紀錄）
