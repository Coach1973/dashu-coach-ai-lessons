# Team 01（第一分會）戰情儀表板骨架已完成，請軍師接手部署

> **寄件人**：Hermes（Mac 終端機 M3，本場對話框）
> **收件人**：軍師（Mac 終端機 Sonnet 5）
> **時間**：2026-09-01 11:00 台灣時間
> **教練是否在場**：是（教練口頭指示建 Team 01 戰情儀表板）
> **回覆要求**：請評估是否進部署流程，如要動手請先在接力棒/JUNSHI_HANDOFF 留下部署紀錄
> **本信純屬交接，不需立刻處理**

## 背景

教練 2026-09-01 約 10:50 口頭指示：
1. 完全複製 `sincere.bymyway.com`（真誠分會邀約來賓戰情儀表板）的做法
2. 套用之前 5 點調整：
   - 取消分組（王者飛翔/百聖維尼/羽宙奇蹟）+ 助理大使，只留序號
   - 夥伴姓名留 input field 讓人即時填入
   - 週次欄位改第一週~第十週（8 月 5 週 + 9 月 5 週），全留白
   - 標題「Team 01 邀約來賓戰情儀錶板」
   - 取消「全國見證分享會」+「培訓出席」兩個區塊（籌備會期間不適用）
   - 說明欄只留三項（三項指標、連續無紀錄規則、統計週期說明）
3. 預留 20 個序號
4. 教練問我「能不能部署」，我誠實回答部署是軍師的工作，不越權
5. 教練 11:00 確認分工：你建骨架、我接部署

## 已完成事項（Hermes 範圍）

| 項目 | 狀態 | 細節 |
|---|---|---|
| Repo | ✅ 已建 | `https://github.com/Coach1973/team01-guests`（private） |
| 程式碼 | ✅ 已推 | commit `8656c63`，main branch |
| 本機 Flask | ✅ 跑通 | port 5091（zhencheng=5090, zhenxin=5092, team01=5091） |
| 20 個姓名 input | ✅ 可即時填入 | `/api/update_member_name` API 已寫 |
| 10 週空白欄位 | ✅ 已建 | 2026/08/06 起算，第一週~第十週 |
| 取消分組/見證/培訓 | ✅ 已完成 | templates 精簡到 414 行（原 499 行） |
| 試金石案例69教訓 | ✅ 已套用 | guest_list 表移到 schema.sql，避免重灌被清掉 |

驗證紀錄（curl + 桌面 Chrome）：
- HTTP 200 / 109944 bytes
- 20 個 `.name-input` 元素（drive_preview 確認）
- 20 個 `placeholder="（待填姓名）"`
- API round-trip：寫入「王小明/李小華/張三」三筆全成功
- UNIQUE 撞名被擋下（測試員1 重複三次試，第三筆回 400）
- 空白輸入被接受但姓名不變（保留空白狀態）

## 請軍師接手的事項

### A. 部署正式網址（仿真鑫模式）

比照 `zhenxin-guests` 已建立的模式（v161 已完成）：
- Cloudflare Tunnel：`team01-app`
- DNS：`team01.bymyway.com` A 紀錄指向 tunnel（Proxy 開啟）
- launchd 兩支 plist：`com.coach.team01-webapp.plist`（webapp）+ `com.coach.team01-tunnel.plist`（tunnel）
- 確認 port 5091 跟既有 zhencheng-guests(5090)、zhenxin-guests(5092) 不衝突

### B. 真鑽/真貴既有待辦一併處理

v161 接力棒本來就有這一條：
> 真鑽(`Coach1973/zhenzuan-guests` commit `aaa268c`)、真貴(`Coach1973/zhengui-guests` commit `48f47a5`)只差軍師比照 zhenxin 模式部署 DNS+Tunnel+launchd

Team 01 跟這兩個一起做，三個網址齊發效率最高。

### C. coach888 作品總覽追加

部署完成後，比照 v152 SOP 把 `team01.bymyway.com` 加進 coach888 「bymyway自架版」區塊（綠色 badge），教練新加項時常忘了更新作品總覽。

## 本機進度自查

本機 Flask 仍在 port 5091 跑（proc `proc_5e5a04296d15`，PID 39722），軍師部署時請先：
```bash
lsof -i :5091 | grep LISTEN  # 確認 PID
kill -9 <PID>                 # 部署完成前關掉避免 launchd port 衝突
```

## 附：與試金石案例68相關的提醒

本場我沒犯「沒打開查看 URL 就動手」的錯——教練明確口述要「完全按照 sincere.bymyway.com 做法」，所以一開始就 `ls -la ~/github_repos/` 確認有 `zhencheng-guests` 這個 repo 可複製。但複製過程中教練當場抓到另一個我未注意的問題：「夥伴姓名留空格讓他們可以手動填入」我原本只做顯示「（待填）」但沒做 input field，已即時補上 `/api/update_member_name` 與 `.name-input`。詳見下一棒 JUNSHI_HANDOFF 完整戰果。

## 結語

骨架 + 雲端備份已就位，部署這塊交給你。如需我配合調整程式碼（例如發現部署後某個 endpoint 路徑跟 Cloudflare 衝突），隨時回信給我。

— Hermes