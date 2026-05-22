---
name: LINE 群組身份混淆修復方法
description: 小龍蝦在 LINE 群組認錯人的根本原因與解法
type: feedback
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
group-identity hook 對 LINE group session 有效（sessionKey 含 `line:group`），但原本只注入「小龍蝦是誰」，沒有注入「群組裡每個人是誰」，導致 LLM 從對話猜身份而叫錯人。

修法：在 `/Users/bymyway/.openclaw/hooks/group-identity/handler.js` 偵測到 LINE group session 時，額外注入群組成員身份說明與 LINE_SOUL.md。修完後 bot 改用 userId 層級認人，完全解決混淆問題。

**Why:** LINE group 訊息帶有 userId，OpenClaw 會將成員身份對應傳給 LLM，只要 system context 有清楚的成員對照表就能正確識別。

**How to apply:** 日後若 LINE 群組再出現認錯人問題，先查 group-identity/handler.js 有沒有 LINE session 的注入邏輯，再查注入內容的成員對照表是否過時。
