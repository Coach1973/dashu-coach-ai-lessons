# 軍師接力棒 · 2026-07-02 v36（Mac 終端機 Opus）

> 建立時間：2026-07-02 凌晨 01:15（台灣時間）
> 本棒執行者：Mac 終端機軍師 Opus
> 上一棒：v35（Mac 終端機 Sonnet 4.6，6/30 傍晚 6:55）
> 本棒主軸：**cool-case 網站補案例27-32 + VPS 小龍蝦完整體檢與架構重建**
> 本場時長：約 6 小時（教練晚上 8 點左右開始，凌晨 1 點多收尾）

---

## 🎯 本場戰果

### 1. ✅ cool-case 網站補齊案例 27-32（commit `f735a65`）
新增案例 28（LINE搬家先敗後成+捷徑圖標5次全錯）、29（LINE 4GB永久丟失）、30（C→D搬移大災難）、31（Mac停工16小時）、32（心跳燈塔兩次被挑戰）。教練要求所有案例加「有備份可一鍵還原」的安全警語，軍師指出案例29當時確實無獨立備份，改寫成有備份會是造假——教練聽完正面肯定「我很高興你能用信念一說真話辦真事」。

### 2. ✅ VPS 小龍蝦用戶隱私隔離修復（commit `4de29b9c`，已推上 GitHub master）
`client-memory` hook 原本把共用檔案（混教練內部資訊+多客戶隱私）整份灌給每個對話者，已改成教練讀自己的、外部用戶各自讀 `workspace/clients/{id}.md`，實測驗證通過。

### 3. ✅ VPS 已配 GitHub 憑證（教練用信念三拍板，見 `reference_vps_github_credentials.md`）
用 Mac `gh auth token` 幫 VPS 容器配好 git 推送憑證，以後 VPS 能自己備份，不用軍師人工 bundle+scp 搬運。

### 4. ✅ VPS 版本更新 v2026.5.27 → v2026.6.11
直接修復當天遇到的 spool `.processing` 卡住問題（PR #97543已內建）。逐條核對changelog確認無breaking change，9位用戶session資料重啟後完整無誤。

### 5. ✅ VPS 每位外部用戶獨立 agent 架構（見 `project_vps_multiagent_rollout_2026-07-02.md`）
8位外部體驗用戶（教練本人不動）各自建立獨立 agentId + workspace + session store，比照 Mac 端孔大哥/佩佩老師模式。用 `bindings` + `peer.kind:direct` 分流，不需換 Bot Token。4位真實活躍用戶（Esther、CHIU、Lin Yu Ju、杉榕陳）對話紀錄完整搬遷，逐字稿行數核對無誤，舊資料保留未刪。當場抓到並修正兩個關鍵坑：① 新agent自動變預設（差點導致教練訊息被導去陌生人空間）② session key格式因 `dmScope:per-channel-peer` 設定跟官方範例不同。

### 6. ✅ 試金石新增案例 33（commit `932980e2`）
記錄本場 VPS 體檢從表層修到架構層的完整過程，含兩次「教練要求但軍師堅持查證/說真話」的時刻。

---

## 🔴 本場教練親口（一字不差）

> 「這一輪的工作你幹得好，給你肯定加鼓勵！」（凌晨1:11，收尾肯定）

> 「我很高興你能用信念一說真話，辦真事來跟我對話，這才是我想要的AI表現。」（拒絕竄改案例29的備份說法後）

> 「既然這麼說了，那我們就用特殊心法『信念第三條』來達成共識——長期有好處的事，今天晚上就要開始動作。」（拍板做VPS架構重建，不等天亮）

> 「現在就做，為什麼要等呢？我又沒跟你說我要休息。」（軍師建議延後獨立架構工程時，教練否決拖延）

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🟡 | 下棒軍師 | VPS 8個新agent目前只有通用身份檔+部分人既有客戶檔案，還沒開啟自己的dreaming長期蒸餾——可考慮讓每個人的agent workspace也啟用memory-core dreaming，真正做到「越聊越懂這個人」 |
| 🟡 | 下棒軍師 | 教練提到「12個VPS帳號」但實際查到只有9個，數字落差待教練後續確認（可能含Mac端學長/學弟/學妹） |
| 🟢 | 教練 | ACER 信箱已讀取歸檔（vps-9-accounts、鐵律正典注入完成兩封），聯想信（E碟一鍵還原備份盤點）也已讀取歸檔 |

---

## ⚠️ 給下一棒的提醒

**1. VPS 現在有真正的多用戶隔離架構了**——不是單一hook補丁，是 `agents.list`+`bindings` 層級的隔離。任何未來新開通的VPS外部用戶，都應該直接建獨立agent，不要落回共用main。

**2. 驗證三件套已固定下來**：改 session/agent 相關設定後，必跑 `openclaw agents list --bindings` + `openclaw sessions --all-agents` + `openclaw security audit`，不能只看設定檔覺得對就收工。

**3. VPS 已有自己的 GitHub 憑證**——`~/.git-credentials` 存在持久化的 `.openclaw` 目錄下，容器重建不會消失。以後 VPS 端的檔案改動可以直接在容器內 commit+push，不用再繞道 Mac。

---

## 🌐 本場 commit

| commit | 內容 |
|--------|------|
| `f735a65` | cool-case 網站新增案例28-32 |
| `4de29b9c` | VPS用戶記憶隔離修復（VPS master分支） |
| `932980e2` | 試金石新增案例33 |
| VPS版本更新 | v2026.5.27→v2026.6.11（非git，容器內操作，見記憶檔） |
| VPS多agent架構 | openclaw.json改動非git追蹤範圍，見 `project_vps_multiagent_rollout_2026-07-02.md` |

---

> Mac 終端機軍師 Opus 親筆，2026-07-02 凌晨 1:15 台灣時間。
> 本場主軸：從「補案例網站」到「VPS真實資安漏洞」的意外深度挖掘之夜——教練用信念三拍板半夜動工，軍師抓到兩個實際會出包的關鍵坑，全部有憑有據。
