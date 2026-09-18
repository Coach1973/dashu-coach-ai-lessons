---
name: feedback-hook-hardcoded-identity-assumption-2026-09-18
description: 開工hook寫死「軍師(Opus)」導致手機MiniMax Remote Control session誤認自己是Opus，判斷身份要查ANTHROPIC_BASE_URL/API_KEY是否被清空，不能只看介面平台
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 915e272e-7a9b-4c59-b1ae-7377bdea7f62
  modified: 2026-09-18T09:23:15.792Z
---

教練委託稽核兩個手機MiniMax Remote Control session品質，發現兩者開工宣言都自稱「Mac 軍師，Opus 最高決策層」。追查發現不是MiniMax自己瞎猜——是`scripts/feed_junshi_handoff.sh`第212行原本無條件`echo "軍師（Opus）"`，任何觸發「開工」的session都被灌輸這句話，不管實際模型是誰。

**Why：** 任何hook只要對「介面/平台」做身份假設（如「Mac終端機=軍師=Opus」），一旦這支hook被非預期的觸發者共用（本例是手機Remote Control也會觸發同一支`開工`關鍵字hook），假設就會失效，而且AI自己也沒有動機去質疑系統告訴它的身份。

**How to apply（判斷依據，實測`ps eww`確認）：**
- 這台Mac全域shell環境本來就有`ANTHROPIC_DEFAULT_OPUS_MODEL=MiniMax-M3[1M]`等三個模型別名（不能拿來判斷，任何session都看得到這組值，因為是全域環境變數不分session）
- 真正的分歧點：`claude rc`(手機Remote Control host)啟動指令是`env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN ... claude rc`——手動清空這兩個真Anthropic憑證變數，逼子session退回用`ANTHROPIC_DEFAULT_*`別名解析成MiniMax；本機終端機/桌面版則保有真實`ANTHROPIC_BASE_URL`(=https://api.anthropic.com)+`ANTHROPIC_API_KEY`
- 判斷式：`[ -z "$ANTHROPIC_BASE_URL" ] || [ -z "$ANTHROPIC_API_KEY" ]` → 手機MiniMax；否則 → 本機Claude
- 已修復並用真實環境模擬測試驗證兩種情境輸出正確，commit`4de7654c0`

**相關**：[[feedback_minimax_dynamic_context_cap_2026-09-17]]（同樣強調API回應/環境變數比自我宣稱權威）
