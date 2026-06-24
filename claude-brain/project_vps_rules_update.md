---
name: VPS 規則體系更新（2026-05-01）
description: VPS 新增20條操作細則、刪除舊HB.md、關閉TTS
type: project
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
2026-05-01 完成三項 VPS 更新：

1. **刪除 HB.md** — 舊架構殘留（學弟妹心跳驅動），與 VPS 定位不符，已清除
2. **新增 VPS_WORK_RULES.md** — 20條操作細則，與原有 VPS_CORE_RULES.md（12條原則）配合使用。Rule 24的「禁讀大型記憶檔」改為「用 CLIENT_PROFILE.md 代替」
3. **關閉 TTS** — `/home/node/.openclaw/settings/tts.json` 從 `always` 改為 `never`

**Why:** VPS 版原本只有12條核心原則，缺少操作細則；HB.md 是 Mac 三機架構的產物；TTS 不需要在 VPS 開啟。

**How to apply:** VPS 規則體系現在是兩層：VPS_CORE_RULES.md（精神）+ VPS_WORK_RULES.md（方法）。
