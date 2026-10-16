---
name: sop-delegation-routing
description: "When user @s me with a SOP / 服務鏈 / trigger-pattern command, run a routing+permission precheck before executing. Avoids wasted round trips on SOPs designed for the main-agent exec path or for server-side hooks whose sender condition I don't match."
---

# SOP Delegation Routing

## Trigger

教練或其他 user 直接 @ 我，下了引用 SOP / 服務鏈 / trigger 句型的指令。常見 trigger：
- 「XX的產業鍊 SOP」「XX的產業鏈 SOP」
- 「執行 XX SOP」「跑 XX 流程」
- 任何指名特定 SOP 名稱的訊息

## 預檢三步（一次跑完，不要分多輪）

### Step 1：找 SOP 來源檔（一次 grep）

SOP 通常落在三處（並行找）：

| 位置 | 角色 |
|------|------|
| `~/.openclaw/workspace/SOUL.md` 對應段落 | main agent 的標準路徑（教練自己走） |
| `~/.openclaw/hooks/<sop-name>/HOOK.md` 或 `~/.openclaw/workspace/hooks/<sop-name>/HOOK.md` | server-side hook，可能自動觸發 |
| `~/.openclaw/workspace/knowledges/SOP_*.md`、`~/.openclaw/workspace/.lessons_upload/` 內 SOP | 雜項 SOP |

```bash
grep -rl "<SOP關鍵字>" \
  ~/.openclaw/workspace/SOUL.md \
  ~/.openclaw/workspace/knowledges/ \
  ~/.openclaw/workspace/hooks/ \
  ~/.openclaw/hooks/ 2>/dev/null
```

> 不要直接 `grep -r ~/.openclaw/workspace/` —— 那會掃到 `.lessons_upload/` 596 個歸檔檔案，全是無關雜訊。

### Step 2：讀 SOP，列「執行路徑」

每個 SOP 通常有 1~N 條路徑。逐條列出：

- **main-agent path**：通常寫「main agent 走 exec 跑 scripts/...」
- **server-side hook path**：寫在 HOOK.md，會自動觸發但有 sender / accountId 條件
- **其他 agent path**：少見，看到時補上

### Step 3：對每條路徑做「我能不能跑」檢查

三個問題：

1. **觸發 sender 是誰？**（HOOK.md 會寫「孔大哥本人 8689825759 或佩佩老師本人 8786886419」之類）
2. **我符不符合？**（比對當前訊息的 sender_id 與 accountId）
3. **需要什麼工具權限？**（exec / image_generate / fs / 其它）

## 完成檢核

- [ ] 至少讀過一份 SOP 來源檔（HOOK.md 或 SOUL.md 對應段落）
- [ ] SOP 內所有執行路徑都列出
- [ ] 每條路徑都檢查過 sender 條件 + 工具權限
- [ ] 結論回報給 user（能跑 / 不能跑 / 部分能跑 + 替代方案）
- [ ] 不能跑時，主動準備好交接素材（例如組好 prompt 給 main agent 用）

## 結論回報模板（給 user 看）

```
教練，「<SOP 名稱>」我讀過了，狀況回報：

執行路徑（從 SOP 來源檔列出）：
- 路徑 1：<說明 + 為什麼我跑不了>
- 路徑 2：<說明 + 為什麼我跑不了>

替代方案請您選：
- (A) 我用 <替代工具> 直接跑（注意：扣額度 / 品質不保證）
- (B) 我把任務轉發給 main agent（推薦）
- (C) 您直接 @ <能跑的 agent>

「<對象>」的 <prompt / 素材> 我先組好備用：
<內容>
```

## 常見坑

- **server-side hook 的 sender 條件常誤導**：HOOK.md 寫「孔大哥本人或佩佩老師本人」就只觸發那兩人；教練 @ 你 hook 不會自動跑。
- **`tools.toolsBySender` 鎖的是 `group:runtime`（exec）**：孔大哥/佩佩老師的 agent 沒 exec，但通常有 `image_generate` 子集。
- **不要為了「自動自發」硬跑 image_generate**：SOP 沒設計走 image_generate 時硬跑會扣教練 lk888 額度且品質不保。SOP 內寫「走 exec 跑 scripts/」就照 SOP 設計走，別自創替代路徑。
- **不要假裝執行**：走不通就老實說，不要組個 prompt 假裝已生圖成功。
- **「方向模糊才問」不適用於 SOP 路由**：SOP 設計與我權限的衝突本身就是事實，必須先報告再請示。

## 不適用

- 純問答、知識查詢、訊息回應（無 SOP 引用）
- 一次性個案任務（不需要建路由預檢的成本）
- SOP 文件內已明確指定「此 SOP 由 X agent 執行」的情境（直接看 SOP 就夠，不必三步全跑）
