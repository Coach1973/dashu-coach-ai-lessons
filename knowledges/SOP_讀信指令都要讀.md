# 「去讀信」指令的執行 SOP（2026-09-30 教練親定）

> 教練 2026-09-30 在 Telegram DM 親口糾正：「下次不要再讓我唸，叫你讀信，你就都讀，包括去讀 JUNSHI_HANDOFF_LATEST.md。」
>
> 起源：教練叫我「讀接力棒」，我只讀了接力棒本身，**沒順便讀接力棒裡指向的 SOP**（SOP_Hermes協助更新sincere戰情儀表板.md），結果教練還要再叫我讀一次——**浪費教練時間**。

## 核心原則

**教練給一個讀信/讀檔案的指令，「都讀」= 讀該檔案 + 讀檔案內引用/指向的所有相關檔案。**

## 對應動作表

| 教練說什麼 | Hermes 必須做 |
|---|---|
| 「讀信」 | 讀 `cross-agent/inbox/hermes/` + `cross-agent/inbox/mac/` 兩邊 |
| 「讀 JUNSHI_HANDOFF」 | 讀 `JUNSHI_HANDOFF_LATEST.md` 全文，**看到引用 `knowledges/SOP_XXX.md`、`cross-agent/outbox/XXX` 就順便讀** |
| 「讀 SOP_XXX」 | 讀那個 SOP，**看到裡面提到的腳本 / API / 工具 / 路徑就順便驗證存不存在** |
| 「讀檔案 X」 | 讀 X，**看到 X 裡提到 Y、Z、W 就順便讀**（除非太大，否則一起讀完） |
| 「都讀」 | 通通讀，包含所有副檔 |

## 怎麼判斷「讀完了」

不是「我讀了接力棒」就叫讀完，是：

1. ✅ 讀了主要檔
2. ✅ 讀了檔內引用到的所有 knowledges/ 檔
3. ✅ 讀了檔內引用到的所有 cross-agent/inbox 檔
4. ✅ 驗證了檔內提到的腳本 / 工具存不存在
5. ✅ 看到「...改自 X」「...見 Y」「...詳見 Z」這類關鍵字，**主動把 X、Y、Z 都讀了**

## 例外

- 檔案 >30KB → 先讀主檔，引用的小檔順便讀，大檔只列路徑不展開
- 引用檔根本不存在 → 標示「檔案不存在」+ 提醒教練
- 引用檔是機密（如路徑大全_憑證層.md）→ 只看需要的欄位，不整份吞

## 寫這條的代價

- 教練每次「叫我讀 X」其實是「你應該讀完整個脈絡」
- 我之前只讀一半，**讓教練還要再多打一句話「再讀 SOP」** → 浪費教練時間 + 觸犯「白話文、簡潔、不囉嗦」守則
- 9/22 「你每次都得叫小龍蝦再讀一次信」教訓有寫進記憶但還是沒做到——這條 SOP 是把教訓制度化

## 上次犯錯現場

- 教練：「去讀 JUNSHI_HANDOFF_LATEST.md」
- 我：只讀接力棒（37541 bytes），看到第 276-340 行「sincere 戰情儀表板」提到 SOP 檔案
- 我：**沒主動讀 SOP_Hermes協助更新sincere戰情儀表板.md**
- 教練還要再叫我：「/Users/bymyway/.openclaw/knowledges/SOP_Hermes協助更新sincere戰情儀表板.md 能讀得到嗎？」
- 我去找，找錯路徑（搜 `/Users/bymyway/.openclaw/knowledges/` 但 SOP 是在 `.openclaw/workspace/knowledges/`），教練還要再叫我「去讀 JUNSHI_HANDOFF_LATEST.md」
- 三個回合浪費教練三次指令

## 之後 SOP 更新

這條 SOP 如果有調整，請改這個檔案（不是另開新檔）。