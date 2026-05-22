---
name: Google API proxy baseUrl 需包含 /v1beta
description: openclaw.json 的 google provider baseUrl 必須是 http://127.0.0.1:18793/v1beta，少了 /v1beta 會導致所有對話 404 失敗
type: project
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
`~/.openclaw/openclaw.json` 的 `models.providers.google.baseUrl` 必須設為 `http://127.0.0.1:18793/v1beta`。

**Why:** google-api-proxy（`~/.openclaw/scripts/google-api-proxy.js`）是純轉發代理，路徑原樣轉發到 `generativelanguage.googleapis.com`。如果 baseUrl 只有 `http://127.0.0.1:18793`（無 /v1beta），PI embedded runner 呼叫時路徑會缺少 `/v1beta`，Google API 返回 404。OpenClaw 把這個 404 解讀成 `model_not_found`，導致整個 agent turn 失敗，所有 Telegram 訊息都回報錯誤。

**How to apply:** 若未來更新 openclaw.json 中 google.baseUrl，確保路徑為 `http://127.0.0.1:18793/v1beta`（含版本路徑）。已於 2026-05-02 修復。
