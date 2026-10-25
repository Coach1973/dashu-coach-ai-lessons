# 教練語音諧音別名：BB / MM = MiniMax-M3（2026-10-17 拍板）

## 教練原話

教練語音輸入時，語音辨識會把「MiniMax」翻譯成 **BB** 或 **MM**。
教練 2026-10-17 00:47–00:52 明確講過：

> 「我講 BB 你就知道是 MiniMax」
> 「乾脆 MM 也可以」

## 規則（不要問、不要建議切換）

教練說 **BB / MM / MiniMax / Minimax** —— **一律當 MiniMax-M3 接**。

- ❌ 不要反問「你是指哪個模型？」
- ❌ 不要提「要不要切換模型」
- ❌ 不要把 BB / MM 當成另外兩個模型去搜尋

直接照 MiniMax-M3 的能力與限制回應即可。

## 現況對照（2026-10-25 查 `openclaw.json` 實測）

| agent | model |
|---|---|
| `main`（小龍蝦學長／1號機） | `minimax/MiniMax-M3` |
| `kong`（學弟） | `minimax/MiniMax-M3` |
| `peipei`（學妹） | `minimax/MiniMax-M3` |
| `bni_tainan` / `jiaolian_thoughts` / `yijing` / `yang` / `rongshuxia` | `minimax/MiniMax-M3` |

provider `minimax` 的模型 `MiniMax-M3`：contextWindow 204800、maxTokens 131072、支援 reasoning。

## 來源

- 原始記錄：`memory/2026-10-24.md:634-636`（D9 條目）
- 2026-10-25 晉升到 `MEMORY.md` 索引（持久記憶層，不再只在每日檔）

## 注意

這是**教練個人用語偏好**，不是 repo 層面的專案事實，所以
`MEMORY.md` 索引那一條**不加** `<!-- project: ... -->` 標記，
本檔也不加（避免被當成這個 repo 專屬的專案事實）。
