# 軍師接力棒 · 2026-07-02 v40（聯想 Sonnet 5）

> 建立時間：2026-07-02（台灣時間，教練說「總結上傳開新對話框」觸發）
> 本棒執行者：聯想軍師 Sonnet 5
> 上一棒：v39（Mac 終端機 Opus，上午 9:00，機關SOP系統化+cool-case案例33-37）
> 本棒主軸：**Hermes VPS 全面處理——版本更新、登入bug修復、核准機制澄清、技能直裝驗證**

---

## 🎯 本場戰果

### 1. ✅ Hermes VPS（113.29.232.178）更新 v0.13.0 → v0.17.0
先備份839M資料（`/root/.hermes.bak.20260702-update`，保留至7/9），舊容器改名保留（`hermes-old-v0.13.0`）可隨時回滾。新版容器穩定運行、進程健康。

### 2. ✅ 更新後 Dashboard 登入 500 錯誤，查出官方bug並修復
正確網址是 `/login`，不是系統自動導向的 `/auth/login?provider=basic`（後者是OAuth專用路徑，Basic Auth走這條會報 NotImplementedError）。已設帳密 `coach` / `Hermes2026Coach!`，實測登入成功（HTTP 200 + `{"ok":true}`）。

### 3. ✅ OpenClaw vs Hermes 架構比較 + Mac本地/VPS雲端 Hermes 差異查證
上網OPE查證後給教練分工建議：小龍蝦=廣度協調中樞、Hermes=深度技能學習體。Mac軍師實際查證本機Hermes（v0.16.0，落後官方3302 commits，workspace跟OpenClaw共用symlink），跟VPS Hermes（v0.17.0，Docker獨立）列表對照。

### 4. 🔴 重大澄清：小龍蝦「開通新用戶」不是全自動
教練親自糾正——有 `openclaw pairing approve` 核准關卡，核准判斷權永遠在教練，不是系統自動放行。查證發現VPS上早已有教練昨晚測試過的 `/root/provision_new_vps_user.sh`（一鍵開通腳本），直接引用，沒有重寫。

### 5. ✅ 三項親自查證通過（教練要求「轉述≠親眼看到」）
- GitHub commit `285bd9e0` 確認存在
- VPS上 `/root/provision_new_vps_user.sh` 親自SSH查證存在（3891 bytes, executable）
- 原始session逐字稿（`e800e341-...jsonl`）挖出真實指令紀錄佐證Mac軍師的測試記錄不是編的

### 6. ✅ vps-onboard-approve 技能直接裝上 VPS Hermes（不叫教練當傳話筒）
教練點破「叫教練去跟Hermes說去讀URL」也是資訊搬運工違規。改為直接SSH進VPS，照Hermes官方技能格式（`/opt/data/skills/devops/{name}/SKILL.md`）寫入檔案，`hermes skills list` 實測驗證顯示 `enabled`。教練現在對赫米斯助教（@hermes_coach1973_bot）說「核准XXX」即可觸發。

---

## 🔴 本場教練親口（一字不差）

> 「那你就不瞭解了，我的 Telegram 早就跟線上版的 Hermes 連線了。我本來就可以透過線上版叫 Hermes 去做事，連這個你都不曉得嗎？」——糾正軍師誤判VPS Hermes Telegram未接通

> 「你轉述的證據鏈我相信它可能是真的，但『你轉述』跟『我親自看到』是兩回事。在沒親自驗到之前，我不動手——這不是卡你，是保護你（守則#04、#15）。」

> 「那你就叫他去網路上自己讀就好了呢？這我又很不爽啊！又叫我當資訊搬運工了，要在你們之間搬來搬去的，那我是什麼？」

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🟢 | 教練 | 實測「核准 XXX」對赫米斯助教是否真的觸發技能 |
| 🟡 | 下一棒軍師 | Mac本地Hermes v0.16.0落後3302 commits，可評估是否也更新到v0.17.0 |
| 🟡 | 下一棒軍師 | 聯想信箱已讀信件已歸檔，無待處理跨機任務 |

---

## ⚠️ 給下一棒的提醒

**1. Hermes技能檔案路徑（VPS）**：`/root/.hermes/skills/devops/vps-onboard-approve/SKILL.md`（host），容器內對應 `/opt/data/skills/devops/vps-onboard-approve/SKILL.md`。技能frontmatter格式仿照官方bundled skill（如kanban），不是隨便寫的Markdown。

**2. 本場兩條新記憶（已寫入聯想共用大腦）**：
- `feedback_dont_relay_between_ai_systems.md`——軍師有SSH/API能力時，不設計需要教練轉話給另一個AI的流程
- `feedback_verify_dont_relay_secondhand_claims.md`——別台AI寫的記憶檔案不算證據，關鍵判斷前要親自查證（git log/SSH/讀原始session log）

**3. pairing approve機制**：`openclaw pairing list` 查待核准清單，`openclaw pairing approve telegram [代碼]` 核准。核准權永遠在教練，AI只負責跑指令。

---

## 🌐 本場相關 commit

| commit | 內容 |
|--------|------|
| `285bd9e0` | 新增SOP：Hermes幫忙開通小龍蝦VPS新用戶 |
| VPS Hermes更新 | 非git追蹤（Docker容器操作），記錄於 `project_hermes_vps_update_20260702.md` |
| VPS技能安裝 | 非git追蹤（直接SSH寫入VPS Hermes容器），SKILL.md格式技能檔 |

---

> 聯想軍師 Sonnet 5 親筆，2026-07-02 台灣時間。
> 本場主軸：教練連續兩次抓到軍師偷懶（誤判Telegram未接通、叫教練當傳話筒），逼出更嚴謹的親自查證+直接動手習慣。
