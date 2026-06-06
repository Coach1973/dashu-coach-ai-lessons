# 軍師接力棒 · 2026-06-06 16:20（Opus 4.6 終端機 session 結案）

> 建立時間：2026-06-06 16:20
> 上一棒：Opus 4.6 2026-06-05 23:00
> 本棒執行者：Opus 4.6 軍師（Claude Code CLI 終端機）

---

## ✅ 本場完成

### 任務一：Karpathy 技能評估與整合 ✅
- 比較 `multica-ai/andrej-karpathy-skills` 與特助心法
- 新增 E10~E12 三條執行細則到 `~/.claude/CLAUDE.md`
- E10：編碼前說出假設（Karpathy 原則一）
- E11：只碰必要的，只清自己的亂（原則二+三）
- E12：把任務轉成可驗證目標（原則四）
- 結論：不適合寫到小龍蝦系統（僅適用於寫程式的 AI）

### 任務二：jiesheng-leadership 書封修復 ✅
- 書封 book.png 和 teacher.jpg 404
- 根因：上一棒軍師 6/5 22:42 用手動 API 推送改字，zip 漏帶圖片
- 修復：空 commit `6d3faa2` → git push 觸發 GitHub 自動部署
- Netlify deploy ID：`6a23ce25ec2d`

### 任務三：「流量」指令——Telegram 查 AI 用量 ✅
- 教練在 Telegram 說「流量」→ 小龍蝦回報 Claude/OpenCode Go/MiniMax 用量
- **方案一（hook inject）失敗**：OpenClaw `message:preprocessed` 是 fire-and-forget，inject 不被消費
- **方案二（SOUL.md 指令）成功**：在 SOUL.md 加鐵律四，小龍蝦讀 `state/usage_cache.json` 回報
- 教練實測確認功能正常
- 快取數據來源：軍師用 Chrome MCP 讀取三家平台頁面後寫入

---

## 🪞 本場教訓

1. **OpenClaw 內部 hook 的 `message:preprocessed` 是 fire-and-forget**——不能用來注入 prompt 內容。花了大量時間 debug 才找到這個架構限制。下次遇到 hook 無效，先確認事件類型是否被 await。
2. **重複回答浪費流量**——教練已回答過的問題，不要因為 context 壓縮後重複輸出。
3. **手動 API 推送漏圖片是反覆型錯誤**——jiesheng-leadership 和 theunrestrictedwar 連續兩次同樣問題。有 GitHub 連結的站一律用 git push。

---

## 📊 Commit 清單

| Commit | Repo | 內容 |
|--------|------|------|
| `204888bf` | openclaw | CLAUDE.md 變更記錄（E10-E12） |
| `6d3faa2` | jiesheng-leadership | 空 commit 觸發自動部署修復圖片 |
| `7c2c2ae` | openclaw | hooks/usage-query 程式碼 |
| `fa1f1f02` | workspace | SOUL.md 鐵律四 + usage_cache.json |

---

## 📝 給下一棒

- **流量指令已上線**：教練說「流量」小龍蝦會回報。快取在 `workspace/state/usage_cache.json`，需要軍師定期用 Chrome MCP 更新
- **快取更新方式**：用 Chrome MCP 讀 claude.ai/settings/usage、opencode.ai、platform.minimax.io 三個頁面，把數據寫入 usage_cache.json
- **hook 程式碼保留**：`~/.openclaw/hooks/usage-query/` 完整可用，等 OpenClaw 未來支援 awaited hook 事件後可啟用
- **YouTube 頻道重新利用**：教練有 bot token `8570992742:AAGR_swFNzjopUuaAkWYZa-h8U9oHn5jlZk`（@CoachWuYouTubeDailyBot），待規劃用途
- CLAUDE.md 已新增 E10-E12（Karpathy 工程執行紀律）

---

**最後更新：2026-06-06 16:20（Opus 4.6 終端機 session 結案）**
