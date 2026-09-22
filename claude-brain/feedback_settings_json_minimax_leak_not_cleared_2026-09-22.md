---
name: feedback-settings-json-minimax-leak-not-cleared-2026-09-22
description: 先前「22:34已清空~/.claude/settings.json的MiniMax金鑰」的說法是錯的，實際上API_KEY/AUTH_TOKEN/BASE_URL/DEFAULT_HAIKU_MODEL/DEFAULT_OPUS_MODEL全部還活著指向MiniMax，教練用「Claude帳單88%不動+MiniMax呼叫數0%→4%」的雙帳單交叉比對邏輯當場抓到，比Mac本機nettop測封包更權威
metadata:
  type: feedback
---

# settings.json的MiniMax殘留：帳單交叉比對邏輯 > 本機網路封包測量

## 事件

2026-09-22 23:07~23:33，教練用手機版Claude Code Remote Control連續下指令（含一張「膠囊咖啡機產業服務鏈」圖），同時盯著兩個帳單頁面：
- Anthropic自己的Usage Limits頁面：週用量卡在88%，教練下指令期間**完全沒有跳動**
- MiniMax後台的「5小時4500次呼叫」頁面：**剛歸零，教練下完指令後從0%跳到4%**

教練的邏輯：兩邊帳單都是各自第一方伺服器端的真實計費紀錄，如果任務讓MiniMax跳、Claude不跳，就直接證明手機那個對話框的呼叫真的算在MiniMax頭上——這個推論本身無從辯駁。

而上一棒軍師（v235/v236）用`lsof`+`nettop`測這台Mac上3個活著的Remote Control process，得出「三個對話框流量100%是真Anthropic，MiniMax 0 bytes」的結論，兩者表面互相矛盾。

## 查證過程

1. `ps aux`找出目前活著的Remote Control session，發現有4個而不是3個：PID 13576/83555/95179/95665，全部都帶`--sdk-url https://api.anthropic.com/v1/code/sessions/cse_xxx`
2. `lsof -p <pid> -a -i TCP`複查，確認這4個process的本機網路連線**真的**只連到160.79.104.10（Anthropic relay），TLS憑證`CN=api.anthropic.com`驗證為真——本機網路封包測量的結果本身沒有錯
3. **關鍵發現**：`~/.claude.json`的`lastModelUsage`欄位裡，`/Users/bymyway/.openclaw`專案路徑下`MiniMax-M3[1m]`有真實`costUSD: 0.4881815`的計費紀錄，`/Users/bymyway`專案路徑下`MiniMax-M3`有`costUSD: 0.963788`——**這是Claude Code CLI自己本機記錄的真實花費，不是教練帳單頁面的間接推論，是第一手證據**，證實MiniMax真的被呼叫過且真的花了錢
4. **找到殘留根因**：`~/.claude/settings.json`的`env`區塊，`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`仍是MiniMax的真實金鑰（`sk-cp-0_`開頭）、`ANTHROPIC_BASE_URL`仍是`https://api.minimax.io/anthropic`、`ANTHROPIC_DEFAULT_HAIKU_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL`仍是`MiniMax-M3[1m]`——**跟接力棒v236記載的「22:34教練清MiniMax金鑰之後」完全對不上，這幾個key從頭到尾沒被清乾淨**

## 根因結論（兩層，不是單一原因）

1. **背景Haiku/Opus子任務層**：`ANTHROPIC_DEFAULT_HAIKU_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL`還設成MiniMax-M3[1m]，任何請求Haiku/Opus tier而未指定完整model id的子任務，會被轉譯成非Anthropic原生model字串，退回用`ANTHROPIC_BASE_URL`+`ANTHROPIC_API_KEY`打MiniMax——這部分**本場已修復**（見下方修復段落）
2. **Remote Control主線model層**：PID 83555這個對話框啟動時argv直接是`--model MiniMax-M3[1m]`（不是子任務，是整個session的主模型），這**不是**由settings.json的Haiku/Opus預設決定的，settings.json的`ANTHROPIC_MODEL`實際上早就是`claude-sonnet-5[1m]`。合理推測：這個特定對話串的model選擇是在**手機端Claude App自己的介面**上選定並黏著在該對話串上（可能是教練或之前某次操作在手機上選了「MiniMax-M3」這個模型選項），跟這台Mac的任何設定檔無關，**這部分尚未解決，需要教練在手機上確認/切換**

## 為什麼「本機nettop測封包」跟「帳單頁面」兩種方法都沒說謊，卻算出不同答案

Remote Control session（帶`--sdk-url .../v1/code/sessions/cse_xxx`）本質上是「本機process只跟Anthropic的session託管relay對話，實際model後端呼叫在Anthropic雲端側完成」的橋接架構，不是本機process直接打model供應商API。這跟案例78/v227驗證過的「一般本機/桌面版session」完全不同——那種session才是本機process自己直接决定要不要用`ANTHROPIC_BASE_URL`打MiniMax，nettop測本機封包才抓得到。**Remote Control這種session，本機nettop天生就測不到真正的model後端流量**，因為那筆流量從頭到尾沒有離開Anthropic的伺服器側。這個架構差異本場才第一次被指出，之前的`identity_model_verify.sh`hook沒有區分這兩種session類型，對Remote Control類型的判定會系統性失真。

## 修復（本場已執行）

`~/.claude/settings.json`移除`ANTHROPIC_DEFAULT_HAIKU_MODEL`/`ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME`/`ANTHROPIC_DEFAULT_OPUS_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`四個key，**刻意保留**`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_BASE_URL`不動——因為[[feedback_claude_rc_never_unset_base_url_2026-09-19]]已經驗證過明確去動`ANTHROPIC_BASE_URL`（尤其是unset）會觸發`claude rc`自己的硬性檢查噴錯，這次改用「讓它們變成沒有model字串會去用的死路徑」而非「直接拔掉」來規避同一個坑。編輯前已備份原檔到`~/.claude/settings.json.bak_20260922_2333`。

## 尚未解決

PID 83555這條Remote Control主線的model選擇（`MiniMax-M3[1m]`）根因不在這台Mac的設定檔裡，下一步需要教練協助：①手機上點開那個對話串，確認介面上有沒有「切換模型」的選項，如果有直接切成Claude系列 ②如果沒有這種UI，可能要結束那個對話串重開一個新的，讓它重新走現在已經修好的settings.json預設值

## How to apply

- 判斷「這個session到底是不是用X模型」，先看它的啟動argv有沒有`--sdk-url .../v1/code/sessions/...`——**有這個參數的是Remote Control/雲端橋接session，本機nettop/lsof測不出真正的model後端，只能信argv宣告值+帳單頁面的account-level數字**；沒有這個參數的才是[[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]那套本機nettop方法論適用的對象
- 教練用「兩個第一方帳單頁面同時比對（一邊跳、一邊不跳）」的方法，比任何本機端技術測量都更直接、更難反駁，這類爭議下次優先建議教練直接用這招，而不是又回頭去測本機封包
- 任何「已經清除金鑰/設定」的說法，下次要附上「剛剛cat過這個檔案，目前內容是⋯」的實際驗證片段，不能只憑操作當下「應該有做」的印象回報

## 相關

- [[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]（本機nettop方法論的原始建立，適用範圍需要用本篇補上「僅限非Remote Control session」的限縮）
- [[feedback_claude_rc_never_unset_base_url_2026-09-19]]（為什麼這次修復刻意不動BASE_URL/API_KEY）
- [[feedback_assert_before_verify_pattern_2026-09-17]]（同類型「先斷言後查證」教訓，本次是先斷言「已清除」沒有真的查證檔案內容）
