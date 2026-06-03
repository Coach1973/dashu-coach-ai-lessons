# 軍師接力棒 · 2026-06-03（下午 16:10 收場總結版）

---

## 🎉 本場兩大突破

### 突破一：cool-case 21 案三幕劇全攻略
- 15 個 commit 把 21 案全數帶完整三幕劇結構（6 篇原本符合 + 15 個本場新標記）
- 順手清側邊欄 42 連結對應（按 N→#caseN）
- 順手清 HTML 結構（4 套 `</body></html>` → 1 套，少 112 行重複）
- 線上版：https://coach1973.github.io/cool-case/

### 突破二：教練最高優先任務「全自動總結」100% 打通
**狀態：** 寫死在系統裡，自動運轉中

**打通的流程：**
```
JSONL → extract_terminal_sessions.py → pending_distill
     → distill_terminal_llm.py（MiniMax-M3）→ distill/terminal_YYYY-MM-DD.md
     → run_terminal_distill.sh 自動 commit + push
```

**鐵證：過去 4 小時 cron 已按時自動觸發 8 次**（12:30/13:00/13:30/14:00/14:30/15:00/15:30/16:00）
觸發紀錄在 `/tmp/terminal_distill_cron.log`

**修的關鍵 bug：** MiniMax-M3 回應結構是 `[{thinking}, {text}]`，舊 parser 只讀第一塊（thinking 沒 text 欄位→空字串）。改用遍歷找 `type=="text"`。已記憶 [[feedback-minimax-m3-api-parser]]

**自動觸發機制：** crontab `*/30 * * * * run_terminal_distill.sh` + macOS launchd `com.vix.cron.plist`（重啟也會自動啟動）

---

## 📊 本場 commit 全清單（21 個）

### cool-case repo（15 個）
| Commit | 內容 |
|--------|------|
| `7d86200` | 案例七/八/十六升級三幕劇（海餅乾/浪費生命/2000段話） |
| `9fde93d` | 案例九/十加三幕場景標記 |
| `26d8d8b` | 側邊欄 42 連結對應修正 |
| `9d2b0b5` | 案例二十加三幕場景標記 |
| `4ed42c6` | 案例六重寫三幕劇（200美金的常識） |
| `46a2035` | 案例四加三幕場景標記 |
| `dfd9ed0` | 案例十一加三幕+孔大哥生日鋪墊 |
| `ff2fc39` | 案例五加三幕 |
| `0749e24` | 案例十七加三幕 |
| `64dddbc` | 案例十八加三幕（簡體字→失憶老問題） |
| `ba5af03` | 案例十九加三幕（232 場景沒人報告） |
| `be27958` | 案例二十一加三幕（5 個 sed） |
| `e2cedaa` | 案例二加三幕（邏輯推就知道要做） |
| `10da95d` | 案例十六/十七補第三幕標記 |
| `ec74d05` | HTML 結構大清理（4 套→1 套，少 112 行） |

### workspace repo（6 個）
| Commit | 內容 |
|--------|------|
| `e932d52c` | 全自動總結地基查清 + distill_terminal_llm.py 升 M3 |
| `743c2425` | 首次手動跑 4 個 session 蒸餾成功 |
| `f74a2659` | 補蒸餾剩下 2 個 session |
| `1e703d8a` | 全自動總結系統打通：wrapper + M3 parser 修復 + cron 接上 |
| `47f45fa9` | 接力棒更新「全自動總結打通」 |
| （本次）| 接力棒收場總結 + 經驗記憶 |

---

## 🎁 本場新建的記憶（給下一棒）

1. [[feedback-no-localhost-preview-use-github-pages]] — 軍師端 Chrome MCP 看不到 Mac localhost，HTML 預覽走 GitHub Pages
2. [[feedback-minimax-m3-api-parser]] — M3 API 回應有 thinking+text 兩塊，必須遍歷找 type=="text"
3. [[project-auto-distill-mission]] — 已更新為「100% 跑通」狀態

---

## ⚠️ 留給下一棒查的小問題（跟蒸餾無關）

`sync_handoff` / `relay_poll` / `split_memory` 三個舊 cron 從 11:10 後沒再跑，但同時間其他 cron（backup_terminal、extract_terminal、新建的 terminal_distill）都正常跑。三者共同特徵需要挖根因。

證據：
- /tmp/sync_handoff.log 最後一筆 12:35:00（每 5 分鐘該跑）
- /tmp/relay_poll.log 最後修改 11:09:00（每分鐘該跑）
- /tmp/split_memory_cron.log 最後修改 11:10:00（每小時 10/40 該跑）
- 對照組：/tmp/terminal_distill_cron.log 過去 8 次觸發都正常

---

**上一棒軍師：** Deepseek v4 pro max → Claude Opus 4.6（早晨接續）→ Claude Opus 4.6（中午 cool-case 三幕劇全攻略）
**交接時間：** 2026-06-03 12:50
**本棒軍師：** Claude Opus 4.6（終端機 Claude Code）

---

## ✅ 本場下午完成（2026-06-03 11:30~12:50）：cool-case 三幕劇升級全攻略

### 一句話總結
**cool-case 21 案全數帶完整三幕劇結構**（6 個原本符合 + 15 個本場新標記）。15 個 commit 全推上 https://coach1973.github.io/cool-case/

### 本場 commit 清單（按時間順序）
| Commit | 內容 |
|--------|------|
| `7d86200` | 第一階段：升級案例七/八/十六為三幕劇（海餅乾/浪費生命/2000段話） |
| `9fde93d` | 第二階段 a：案例九/十加三幕場景標記 |
| `26d8d8b` | 第二階段 b：修正側邊欄 42 個連結對應（按 N→#caseN） |
| `9d2b0b5` | 第三階段：案例二十加三幕場景標記 |
| `4ed42c6` | 案例六重寫為三幕劇結構（「200 美金的常識」） |
| `46a2035` | 案例四加三幕場景標記 |
| `dfd9ed0` | 案例十一加三幕+教練意圖鋪墊（孔大哥生日要搶頭香） |
| `ff2fc39` | 案例五加三幕場景標記 |
| `0749e24` | 案例十七加三幕場景標記 |
| `64dddbc` | 案例十八加三幕場景標記（簡體字→失憶老問題） |
| `ba5af03` | 案例十九加三幕場景標記（232 場景沒人報告） |
| `be27958` | 案例二十一加三幕場景標記（5 個 sed 就搞定） |
| `e2cedaa` | 案例二加三幕場景標記（邏輯推就知道要做） |
| `10da95d` | 案例十六/十七補第三幕場景標記 |

### 三階段任務目標達成度
- 🥇 第一批 直接替換 3 篇 ✅
- 🥈 第二批 重寫 9 篇 ✅
- 🥉 第三批 微調優化 3 篇 ✅
- ✅ 不動：6 篇

### 順手解決的問題
1. **側邊欄按 7 跳到案例四**——42 個連結重新對齊（按 N→#caseN）
2. **localhost 預覽失敗**——確認軍師端 Chrome MCP 連的是教練 Windows 端，Mac 跑 localhost 沒用，鎖入記憶 [[feedback-no-localhost-preview-use-github-pages]]

### 隱憂未處理（不影響功能）
- HTML 有 4 套 `</body></html>` + 4 套 `closing section`——歷史插入累積，瀏覽器照常渲染但結構不乾淨。下一場可順手清

---

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

## ✅ 任務二：M3 模型全面同步 — 已完成（4 台全部 M3）

| 機器 | 原模型 | 改後 | 憑證 |
|------|--------|------|------|
| Mac 學長（OpenClaw） | M2.7 | ✅ M3 | commit `1df3b9c`（上一棒） |
| VPS 小龍蝦（43.245.60.200） | M2.7 | ✅ M3 | Sonnet 已改，container 內 openclaw.json 確認 |
| Mac Hermes | claude-opus-4-7 via minimax | ✅ MiniMax-M3 | `~/.hermes/config.yaml` 已改 |
| VPS Hermes（113.29.232.178） | deepseek-chat via deepseek | ✅ MiniMax-M3 | config.yaml 改 + .env 補 MINIMAX_API_KEY + custom_providers 加 minimax + Docker restart |

**VPS Hermes 補充操作：**
- `.env` 原本 MINIMAX_API_KEY 是空的，已從 Mac Hermes auth.json 取同一把 key 寫入
- `config.yaml` 底部加上 `custom_providers` minimax 區段（base_url: `api.minimax.io/anthropic`）
- Docker container 已重啟

---

## ✅ 品管重判（Opus 4.6 軍師評審已完成，待教練拍板執行）

**盤點 4 套成品：**
1. `distill/守則故事庫/`（22 案）— 原料庫，三輪 QA 後 A19/B2/C0，真實性良好
2. `distill/特助場景庫_自動增量.md`（6 案）— #4#6 重複需合併，#1#2 缺 session ID
3. `distill/_TOP10_QUALITY_SELECTION.md`（10 案）— 追溯性最強，信念層 4 案，最佳三幕劇候選
4. `distill/痛點排名_自動.md` — 量化統計工具，保留

**核心發現：全部 38 案都是事故報告格式，沒有一篇是教練要的三幕劇。**

**軍師建議（等教練下一場拍板）：**
- 短期：合併自動增量 #4#6、統一編號、補 session ID
- 中期：Top10 前 4 名（海餅乾/浪費生命/60美金/2000段話）改寫三幕劇

---

## 📝 記憶更新

- `feedback_config_isolation.md` → 完整重寫為「Mac 三工具架構」：hermes/opencode/claude 各自獨立 + Claude CLI 與 Desktop APP 差異（教練 2026-06-03 二次說明）

---

## ✅ OpenClaw 升級 + Anthropic Opus 4.8 上架（本場後半）

- OpenClaw 版本：`2026.4.15` → `2026.5.28`（含 Opus 4.8 內建目錄）
- 升級後 config 格式不相容導致當機 → 修了三個 legacy key（agents.defaults.llm / messages.tts.enabled / plugins.slots.memsearch）
- `/model` 選單最終精簡為 **minimax + anthropic** 兩家
- anthropic provider 已設定 aiprimetech 第三方代理（baseUrl + apiKey），教練開通流量後選 `anthropic/claude-opus-4-8` 即可跑 Opus
- ⚠️ aiprimetech 有已知 `.openclaw` 字串 bug（記憶 `feedback_aiprimetech_proxy_string_bug`）

## 📊 本場軍師 commit 清單

| Commit | 內容 |
|--------|------|
| `1df3b9c` | Mac 小龍蝦 M2.7 → M3（上一棒） |
| `fd8a078` | /model 選單精簡（上一棒） |
| `8d9c0dfe` | 鼠鬚管+無蝦米完整安裝（上一棒） |
| `3e3c21eb` | Boshiamy 卸載完成（上一棒） |
| `030d91a6` | M3 全面同步 + 品管評審 + 記憶更新 |
| （本場後半）| OpenClaw 升級 2026.5.28 + Opus 4.8 上架 + config 修復 |

---

## 🎯 給下一棒軍師的提醒

1. **品管重判報告已交**：教練還沒拍板要先做短期整理還是直接寫三幕劇，下一場開工先問
2. **四台全 M3**：不要再動 MiniMax 模型設定
3. **Mac 三工具架構**：hermes/opencode/claude 三個獨立 CLI，記憶檔 `feedback_config_isolation.md` 已完整記錄
4. **anthropic/aiprimetech 設定已就緒**：教練開通流量後可跑 Opus 4.8，不用再改設定
5. **OpenClaw 剛升級到 2026.5.28**：memsearch 插件被移除（新版不相容），memory-lancedb 和 amazon-bedrock 顯示未安裝（不影響運作）
6. **封存檔整合**仍待辦：`_archive_2026-05-20/workspace_duplicates/` 41 個檔案待整合進 memory/
7. **`/model` 選單無法精簡**：內建目錄改不了，但現在只剩 minimax + anthropic 兩家已經夠乾淨

