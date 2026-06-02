# 軍師接力棒 · 2026-06-02

**上一棒軍師：** Deepseek v4 pro max
**交接時間：** 2026-06-02 23:00
**本棒軍師：** Claude Sonnet 4.6（終端機 Claude Code）

---

## ✅ 今日完成（2026-06-02）

### 任務一：升級小龍蝦模型 M2.7 → M3
- 修 `~/.openclaw/openclaw.json` 三個 agent 模型欄位
- 補上 M3 進 minimax provider models 清單（讓 /model 看得到）
- **Commit：** `1df3b9c`

### 任務二：精簡 /model 選單，只留 5 家
- Disabled 12 個 LLM provider plugin（amazon-bedrock, github-copilot, groq,
  huggingface, kimi-coding, mistral, openai, opencode, openrouter,
  vercel-ai-gateway, xai, zai）
- 從 models.providers 移除 kimi（教練未列入保留）
- Gateway 重啟 pid 11207 → 11509
- 保留：minimax / anthropic / codex / opencode-go / google
- **Commit：** `fd8a078`
- **附註：** `codex` ≠ `openai`，codex 走 ChatGPT 訂閱通道（gpt-5.2/5.4/5.4-mini）；
  openai 走 API key 通道（已關），教練確認維持現狀

### 任務三：鼠鬚管 + 無蝦米輸入法完整安裝
- **問題：** Deepseek 上棒卡在「無蝦米字根對照表是專有資料、要教練給連結」
- **軍師解：** GitHub 找到 `hsuanyi-chou/rime-liur`（全功能、自包含、49 萬行字根）
- **執行：**
  1. clone repo → /tmp/rime-liur
  2. 備份 ~/Library/Rime/ 原本錯的骨架到 _backup_scaffold_*
  3. 複製 rime-liur/Rime/* 全部 12 個 yaml + opencc/
  4. Squirrel --install 註冊輸入源
  5. open Squirrel.app 觸發部署
  6. 驗證 build/liur.extended.table.bin 已生成
- **狀態：** 鼠鬚管已註冊、liur schema 為預設、字典已編譯
- **教練只剩動：** Ctrl+Space 切到鼠鬚管即可開始打字（不必登出登入）

---

## 📂 關鍵路徑

| 用途 | 路徑 |
|------|------|
| Rime 設定 | `~/Library/Rime/` |
| Rime 編譯產出 | `~/Library/Rime/build/` |
| 原骨架備份 | `~/Library/Rime/_backup_scaffold_20260602_225813/` |
| OpenClaw 設定 | `~/.openclaw/openclaw.json` |

---

## 🎯 給下一棒軍師的提醒

1. **守則#12 落實：** 上棒卡關是因為叫教練給「下載連結」——其實 GitHub 上現成有方案。
   下次遇到「教練要給我什麼檔案」先 WebSearch / gh search，自己找。
2. **OpenClaw 模型現況：** 已是 MiniMax-M3，5 家 provider 精簡完，
   不要再亂動 openclaw.json（守則 #04 寫死規則）
3. **接力棒未完成：** 封存檔整合（`_archive_2026-05-20/workspace_duplicates/` 41 個）
   仍待整合進 memory/

---

