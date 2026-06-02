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


---

## ✅ 任務三補完（2026-06-02 23:17）

教練實測：「**打的很順，一切正常**」

**已完成：**
- 鼠鬚管 + 無蝦米全套部署 ✅
- 註冊到 macOS AppleEnabledInputSources ✅
- Boshiamy 試用版完整卸載（.app + plist + Application Support）✅
- 備份：`~/Library/Rime/_backup_boshiamy_uninstall_20260602_231649/`
- 記憶紅線更新：`reference_coach_input_method.md`

**過程中的失誤 + 復原（守則 #07）：**
- 失誤：Python `plistlib.dump` 簽名搞反 → `com.apple.HIToolbox.plist` 變 0 byte
- 偵測：寫完立刻 `defaults read` 驗證，發現「does not exist」
- 修復：4 秒內重建 plist（含教練原本 8 個輸入源）
- 預防：寫進 `reference_coach_input_method.md` 的「危險操作」段落，下次同類操作必先 `cp` 備份

---

---

# 🔴 下一場軍師待辦（教練 2026-06-02 23:25 親交）

## 任務一：守則故事庫品管重判

**背景：** 過去兩三天（2026-05-29 ~ 2026-06-02）跑出來的「特助 21 守則」場景／故事庫，**有一些不錯的進度**，但教練希望**軍師再做一次品管重判**。

**已知路徑（軍師前棒給 MiniMax 的任務檔，可作起點）：**
- `~/.openclaw/workspace/knowledges/TASK_守則故事庫_品管重判_給MiniMax.md`（2026-05-29 10:08）
- `~/.openclaw/workspace/knowledges/TASK_故事庫_真實性與重複度檢查_給MiniMax.md`（2026-05-29 04:26）
- `~/.openclaw/workspace/knowledges/TASK_守則故事庫_給MiniMax終端機.md`（2026-05-29 04:21）

**新軍師要做：**
1. 先讀上述三份 TASK 檔，理解前一波品管的標準
2. 找到 MiniMax 跑出來的「最新一版」故事庫成品（可能在 `memory/`、`knowledges/`、`distill/` 某處——要 grep + ls -lt 鎖定）
3. 用「真實性 / 重複度 / 守則對映準確度」三維度評審
4. 產出評審報告（哪些通過、哪些要重做、哪些要刪）
5. 跟教練確認後執行
6. ⚠️ 這是**判斷類**任務（不是執行類）→ 用 Opus 軍師模式，不要 Haiku 混用（記憶 `feedback_model_choice_quality_first`）

## 任務二：M3 模型全面同步（Hermes + VPS 小龍蝦）

**背景：** 本場（2026-06-02）軍師已把 Mac 端小龍蝦的 3 個 agent 從 `minimax/MiniMax-M2.7` 升到 `minimax/MiniMax-M3`（commit `1df3b9c`）。**但教練現在要求全面 M3，所以另外兩台也要查、要同步：**

### 2-A：Hermes（VPS `113.29.232.178` 或其他 IP，記憶 `project_hermes_vps`）
- 連線方式：`ssh root@113.29.232.178`（密碼路徑見記憶或 `~/.openclaw/credentials/`）
- 查設定檔位置（過去經驗：可能在 `~/hermes/config.yaml` 或 `auth.json`）
- 看 model 欄位現況
- 如果不是 M3，升級到 `MiniMax-M3` 並重啟服務
- 驗證：發一句訊息看回應正常

### 2-B：VPS 小龍蝦（`43.245.60.200`，記憶 `project_team_structure`）
- 連線：`sshpass -p <密碼> ssh root@43.245.60.200`（密碼放在記憶或 credentials/）
- 進 docker：`docker exec -u root -it openclaw bash`
- 查 `openclaw.json` 的 `agents.list[].model` 欄位
- 不是 M3 就改成 `minimax/MiniMax-M3`
- 重啟 gateway
- 驗證：Telegram 發一句看回應正常

**驗收標準：**
- 三台（Mac / Hermes / VPS 小龍蝦）都跑 M3
- 每台給 commit hash 或 docker exec 輸出截圖作憑證
- 更新接力棒並 commit

**⚠️ 風險提醒：**
- VPS 小龍蝦：M2.7 的 cron 任務、prompt 可能對 M3 行為敏感，升級後先觀察 24 小時
- Hermes：過去有 aiprimetech proxy bug（記憶 `feedback_aiprimetech_proxy_string_bug`），改 model 前先確認 API endpoint 還是走 `api.minimax.io`
- 兩台都升完後，記得回頭更新本接力棒（劃掉這條，標 ✅）

---

## 📊 本場（2026-06-02）軍師 commit 清單

| Commit | 內容 |
|--------|------|
| `1df3b9c` | Mac 小龍蝦 M2.7 → M3（含 /model 補入 M3） |
| `fd8a078` | /model 選單精簡，留 5 家 provider |
| `8d9c0dfe` | 鼠鬚管+無蝦米完整安裝（接力棒首次更新） |
| `3e3c21eb` | Boshiamy 卸載完成、教練實測「打的很順」 |

