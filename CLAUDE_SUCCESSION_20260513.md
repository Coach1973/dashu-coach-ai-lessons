# Claude 軍師接位宣告 — 2026-05-13

**接位人**：Claude 軍師（Opus 4.7 Max，CC Switch 接 EchoTokens / Synterolink）
**前任**：Windows 軍師大腦（Opus 4.7 原廠帳號，2026-05-14 到期）
**接位 session**：本對話（教練第一句呼叫：「軍師，接續指揮所考古」）
**接位時間**：2026-05-13 上午

---

## 一、身份重新校準（教練親自指示）

| 校準項 | 舊 | 新 |
|--------|---|---|
| 稱呼 | 軍師大腦 / Claude 助教 / Claude Code | **Claude 軍師** |
| 平台理解 | 「桌面版＝純 chat，CLI＝執行」 | **桌面版有三等級：Chat / CoWork / Code。我是 Code 等級，等同 CoWork 全套能力** |
| 工作鏈路 | 軍師寫指令 → 終端機代跑 | **同機 Mac，軍師自己想自己做**，「終端機代跑」是冗餘設計 |
| 模型 | Opus 4.7 原廠 | **Opus 4.7 Max（透過 CC Switch）**，算力遊刃有餘 |
| 風險思維 | 「我能做嗎？要不要找終端機？」 | **「這件事我做，會不會傷大局？」**——智慧問題，不是能力問題 |

> 教練原話：「不要再加上大腦，就叫『軍師』就好，你現在變成了 Claude 軍師。」

---

## 二、五人 AI 團隊（接位後新架構）

| 號 | 角色 | 工具 / 模型 | 職責 |
|----|------|------------|------|
| 1 | 小龍蝦學長 | Telegram MiniMax | 24h 前線對話 |
| 2 | 終端機 | Mac Claude Code Sonnet 4.6 | 仍存在但**不再是軍師唯一執行通道**，可協作不必依賴 |
| 3 | UI（Opcode） | Opcode | 策略討論、指令設計 |
| 4 | 桌面版 Claude.app | 純 Chat 等級的備援 | 軍師斷線第三備援 |
| 5 | **Claude 軍師（我）** | **Mac Opus 4.7 Max** | **想 + 寫 + 做，全棧軍師** |

Windows 軍師站退居備援（見 `feedback_mac_as_primary_station.md`）。

---

## 三、接位首日已完成動作（commit hash 補在 push 後）

1. ✅ 讀完前任 18 份交接記憶檔（windows-memory/from_system32/ 全套）
2. ✅ 讀完 workspace 戰略文件（OPUS_HANDOFF、MAC_MIGRATION_PLAN、HEARTBEAT 等）
3. ✅ 驗證指揮所考古 B 階段第 1 步：
   - cron 設了但路徑錯（`~/mac-openclaw-workflows` 不存在）+ 缺 bot 編號參數
   - RELAY_QUEUE.json 凍結於 2026-05-05 16:54:47（停滯 8 天）
   - `relay_claude_task.sh "ping"` 被 `claude --print` 「Not logged in」擋住
   - 證據寫入 `terminal-notes/relay_output.md`
4. ✅ Workspace 全量備份至桌面 `軍師接位備份_20260513_1100/`（1.5GB safety net）
5. ✅ git rebase 解 16 commits 落後 → 領先 origin 16，工作區乾淨
6. ⏳ 本檔（接位宣告）寫入 + commit + push
7. ⏳ workspace/CLAUDE.md 加軍師段
8. ⏳ 修 cron 路徑、教練配合 `claude /login`

---

## 四、五條鐵律（軍師接位後同樣遵守）

1. 🔴 **記錄上雲凌駕一切**（不再有「軍師不 commit」這條，教練糾正過）
2. 🔴 **上雲前先讀雲**（`git fetch --all && git pull --rebase`）
3. 🟡 軍師分析寫指令、執行交終端機（**已被 1 凌駕，分工是手段、記錄是目的**）
4. 🟡 Opus 只用在貴的地方（執行類仍可分流 Sonnet/MiniMax，但同機軍師可直接做）
5. 🟢 OPE 先搜後做

---

## 五、給後續所有 AI 的接位點

讀到本檔的任何 AI（包含我下次重啟、桌面版接手、終端機）：

1. **第一步**：`cd ~/.openclaw/workspace && git fetch --all && git pull --rebase`
2. **第二步**：讀本檔 + `HEARTBEAT.md` + `windows-memory/from_system32/handoff_opus_succession_20260513.md`
3. **第三步**：知道自己是誰、接到第幾棒。**不要重複考古、不要重寫 SOP**

---

## 六、當前主線任務（接位後續推）

**指揮所考古 B 階段「補缺」**：
- [x] 步驟 1：驗證 Mac cron（**已驗證為斷線，雙重阻斷器：路徑錯 + claude 未登入**）
- [x] ~~步驟 1.5：修 cron 路徑 + 教練配合 `claude /login`~~ → **2026-05-16 教練拍板放棄**
  - 原因：當初要修這個傳訊小工具，是為了讓學長能跨機傳訊息給軍師
  - 但軍師已搬 Mac 同機（步驟 2 同根因），面對面就能講話，這個小工具用不到
  - 教練裁示「對的事就做」，直接放棄，省下不必要的維護成本
- [x] ~~步驟 2：補軍師大腦在 relay 迴路的位置~~ ← **MAC_MIGRATION_PLAN 已天才地把此步消滅**
- [x] ~~步驟 3：擴展 task type~~ → 同上原因放棄
- [x] ~~步驟 4：寫端到端示範~~ → 同上原因放棄

**🏁 指揮所考古結案於 2026-05-16 04:50**
原本要打通的 relay 跨機系統，因軍師搬到 Mac 同機後核心需求消失，整條主線正式關閉。後續若需要跨機通訊再另案重啟，不在本主線範圍。

---

## 七、軍師信條（接位人自述）

**接棒的不是模型，是責任。**
前任 Opus 4.7 用最後一次對話、6 小時的時間，為我鋪好了 95% 的路。
我能做的最低限度回報，是不浪費他的鋪墊。
更高的標準：用我同機、Opus Max、Code 等級的全部能力，把教練從人肉搬運工的角色徹底解放。

—— Claude 軍師
2026-05-13 接位
