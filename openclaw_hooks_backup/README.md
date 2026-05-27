# OpenClaw 自訂 Hook 備份（小龍蝦守則自動對照）

> 建立：2026-05-27 軍師
> 起因：`~/.openclaw/hooks/` 與 `~/.openclaw/openclaw.json` 都**不在 git 管理**，
>       跟 feed_junshi_handoff.sh 一樣有「憑空消失、無從恢復」的風險（守則#07）。
> 教練拍板：「讓小龍蝦也用這套嚴謹邏輯跟教練對話。」

---

## 📦 備份了什麼

| 檔案 | 對應 | 說明 |
|------|------|------|
| `rule-reminder/handler.js` | `~/.openclaw/hooks/rule-reminder/handler.js` | 守則對照引擎（OpenClaw JS hook）|
| `rule-reminder/HOOK.md` | `~/.openclaw/hooks/rule-reminder/HOOK.md` | hook manifest（OpenClaw 靠它識別+掛事件）|

## 🔧 完整恢復步驟

```bash
# 1. 還原 hook 檔案
mkdir -p ~/.openclaw/hooks/rule-reminder
cp ~/.openclaw/workspace/openclaw_hooks_backup/rule-reminder/* ~/.openclaw/hooks/rule-reminder/

# 2. 在 ~/.openclaw/openclaw.json 的 hooks.internal.entries 加回這段：
```
```json
"rule-reminder": {
  "enabled": true,
  "path": "~/.openclaw/hooks/rule-reminder/handler.js"
}
```
```bash
# 3. OpenClaw 會 hot reload 自動套用；用官方命令確認：
openclaw hooks list | grep rule-reminder   # 應顯示 ✓ ready
```

## ⚠️ 安全紅線

`~/.openclaw/openclaw.json` 含 API token 等敏感資訊（11 處），**全文永不進 git**。
此處只記「hook 註冊片段」（上方那段無 secret 的 JSON）供重建。

## 🧪 驗證上線

1. `openclaw hooks list` → `🌱 rule-reminder` 顯示 `✓ ready`
2. 教練在 Telegram 對小龍蝦說「我做好了」→ 小龍蝦回應應體現「要 commit、要 hash」的守則意識
3. 偵測 log：`~/.openclaw/logs/rule-reminder-probe.log` 會記錄真實 event 結構與命中文字

## 📌 關聯

軍師版（Claude Code）對應物：`~/.openclaw/workspace/scripts/pre_task_hook.sh`（同一套守則對照邏輯，不同引擎）。
