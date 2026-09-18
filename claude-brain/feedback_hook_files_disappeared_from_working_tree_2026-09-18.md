---
name: feedback-hook-files-disappeared-from-working-tree-2026-09-18
description: 教hooks目錄在git tree存在但working tree消失時的標準恢復SOP+開工先驗證路徑完整性
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5876ed8b-e8aa-57aa-a324-b2e2e2d54d6f
  modified: 2026-09-18T08:26:24.162Z
---

# hook 整個目錄從 working tree 消失但 git tree 還在

2026-09-18 開工時發現：`hooks/industry-chain-sop/`（含handler.js+HOOK.md，整個v214 groupId修復版）整個目錄從 working tree 不見，但 `git ls-files` 仍輸出完整檔案、`git show <sha> -- hooks/industry-chain-sop/handler.js` 內容也完整。懷疑根因：9/16 commit `054148ab2` 同次 `doctor --fix` 副作用（commit message 明確寫「doctor --fix意外清空的TOOLS.md」）。

**Why：** working tree 消失但 git tree 還在時，最容易誤判成「從未存在過」，但其實是 git 救的回來的（不用重建）。
**How to apply：**

1. **開工第一步先 `git ls-files hooks/`** — 若 git 有追蹤但 `ls hooks/` 說 No such file，代表被某次操作清掉了，可以救
2. **不重建** — 直接 `git checkout <sha> -- hooks/<hook-name>/` 從目標 commit（不一定 HEAD，找 groupId 修復那次的 SHA，例如 v214 = `0228987df`）救回整個目錄
3. **救回後必跑合成事件驗證** — `require()` hook handler 寫個 mock event runner 跑 6~8 個 case（含「對的群組+對的句型」「錯的群組」「一般對話」「空字串」「非白名單 agent」），確認邏輯正確而不是只有檔案回來
4. **真正的觸發 log 才是試金石** — `~/.openclaw/hooks/<name>/hook.log`（不在 repo 在 HOME）才是 runtime 行為真相，git 救回的 handler 跑一次會在 log 裡看到 TRIGGER/PROMPT/OK 這幾行，這才算數
5. **記憶這次事故 → 下一場的 hook 復原 SOP 就是這條**
