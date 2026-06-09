# 軍師接力棒 · 2026-06-09 下午 v6（Opus 4.7 終端機 session，圓桌完工+進入 7 天試煉）

> 建立時間：2026-06-09 下午 5:05 台灣時間
> 本棒執行者：Opus 4.7（接續上午 v5，Opus 4.7 同人）
> 上一棒：Opus 4.7 上午 v5（圓桌 v2.0→v2.4 連修五輪）

---

## 🎯 教練本場最重要決策

**「接下來就是做一週的測試，有遇到什麼問題再來完善。」**——下午 5:03 親令

→ **2026-06-09（週二）下午 5:05 起進入 7 天試煉期，至 2026-06-16（下週二）期末驗收**

下一棒進來時若還在 7 天內：**這是觀察期，非開發期**。除非教練明確指派新任務或試煉中發現 bug，否則不主動改架構。

---

## 🏆 本場成果（共 8 task + 9 commit hash 憑證）

### 系統治本類（6 task，下午 12:55 完成）
1. **bot-relay v2.5** 補三層 fallback 解 botId=unknown bug（commit `63a6017`，dry-run 四案全綠）
2. **sent event lag** 根因 = botId=unknown，v2.5 已解
3. **SOUL/RTO 直連為主** 實質落地——三隻 SOUL 純直連、shared-relay 自 05-26 起無新檔
4. **Netlify 部署守護** PreToolUse hook 攔截未授權部署（commit `0321abef`）
5. **Mac H Phase 1 驗收 4/4 全綠** FB cron 下午 2:33（06:33 UTC）準時跑、status=ok、含「【Mac H 試營運】」前綴（hermes repo commit `3072d11`）
6. **cron 首跑驗證** fb-birthday/dreaming 跑通；vps-healthcheck 0 bytes 待查

### 時間鐵律寫死系統（下午 2:31 教練親罵第 N 次）
7. **inject_taiwan_time.sh** UserPromptSubmit hook 教練每次說話自動注入當下台灣時間（commit `2a3447b9`）
8. **bot-relay-inbound timeZone='Asia/Taipei'** 鎖死時區顯示（commit `7a72cb1`）
9. **HEARTBEAT 首段紅標 + memory 補課** 教訓「寫文字 ≠ 系統行為，要寫 hook」

### 圓桌會議架構完工（下午 2:46，教練親令 A+B 雙保險）
10. **方案 A：council_orchestrator.sh + launchctl 每 120 秒巡邏**（commit `873a1b13`）
    - 條件：學長派議程後 >60 秒 + 學弟學妹都發過 OR 派發後 >5 分鐘 + 學長沒收尾
    - 動作：minimax anthropic-compat API 生 Council 三段 → main bot Telegram sendMessage
    - 防呆：lockfile 5 分鐘 TTL + 發後手動寫 BOT_MESSAGES 防重觸
11. **方案 B：bot-relay/handler.js 學弟學妹 sent 即時觸發**（commit `b550eb5`）
    - 把 Council 延遲從 2 分鐘壓到秒級
    - 只對 kong/peipei 觸發避免 main 自循環

### 實測下午 2:43 & 2:45 兩次 Council 已成功發到分工群
- launchctl cron 跑 53 次後**完全沒重複觸發**（防呆 100% 有效）

---

## 🔑 本場 9 個 commit hash

| Commit | Repo | 內容 |
|--------|------|------|
| `63a6017` | root | bot-relay v2.5 補 fallback |
| `0321abef` | root | Netlify PreToolUse 守護 |
| `7a72cb1` | root | bot-relay-inbound timeZone |
| `b550eb5` | root | 方案 B hook 觸發 |
| `2a3447b9` | workspace | 時間鐵律 inject hook |
| `1596e3af` | workspace | HEARTBEAT 12:55 紀錄 |
| `873a1b13` | workspace | 方案 A council orchestrator |
| `96bfa86e` | workspace | HEARTBEAT 下午 2:46 紀錄 |
| `3072d11` | hermes | Mac H Phase 1 驗收 |

---

## 📋 7 天試煉期觀察清單（給下一棒/教練）

### 每天必看（下次開工第一件事）
1. **trigger log**：`tail -20 /Users/bymyway/.openclaw/workspace/logs/council_orchestrator.log`
   - 看有沒有「✅ council sent successfully」
   - 看有沒有「llm failed」「tg send failed」錯誤
2. **BOT_MESSAGES.md botId 分布**：`grep '"2026-06-09\|"2026-06-10' BOT_MESSAGES.md | jq -r .botId | sort | uniq -c`
   - 應該看到 main/kong/peipei 真實出現，不再是 unknown/1号機
3. **launchctl cron 健康**：`launchctl list | grep -E "council|fb-birthday|gateway"`
4. **gateway PID 是否還活**：`ps aux | grep "openclaw.*gateway"`

### 期末驗收（2026-06-16 下午）
- [ ] 每天至少 1 次成功 Council 觸發（共 7 次以上）
- [ ] 沒有重複 Council 訊息（防呆 100% 有效）
- [ ] 沒有 LLM call timeout 或 Telegram API 失敗
- [ ] gateway 沒被 auto-fix-session-lock 誤殺
- [ ] Mac H FB cron 下午 2:30 每天準時跑

---

## ⏳ 留給下一棒（試煉期間若教練明確要做）

### 中優先
- **vps-healthcheck stdout 0 bytes 要查**——cron 觸發了但無輸出，可能 sshpass 失敗 silent
- **Mac H Phase 2/3** 7 天試煉期同時進行：接其他 SOP（Netlify 案例網站）、補 Hook 對照機制、補 BOT_MESSAGES 收錄到 Mac H

### 低優先（試煉中遇到再修）
- council_orchestrator LLM 改用 fallback template（minimax 失敗時不要靜默）
- bot-relay/handler.js text substring(0,200) 太短導致 Council 在 BOT_MESSAGES 截斷顯示不全

---

## 🪞 本場軍師三大教訓

1. **架構限制要寫程式碼解，不要寫文字鐵律自己騙自己**——圓桌會議 v2.x 文件寫了一堆「學長要收尾」「學弟學妹發完學長就收尾」，但 OpenClaw 設計上 bot 訊息根本不觸發其他 bot 的 hook，文件再多也沒用。最後 A+B 144 行 shell + 11 行 Node.js 解決 3 個月架構問題。
2. **時間 N 次跌倒同個地方 = 機制問題不是健忘**——教練第 N 次親罵時間錯亂，光寫記憶+HEARTBEAT 沒用，要 UserPromptSubmit hook 自動注入到 context 開頭，AI 才「沒機會忘」。
3. **dry-run 通過就 commit + 重啟 gateway 載入新 hook**——OpenClaw hook 修改後 gateway 不會自動 reload，今天兩次 kickstart（下午 12:47 / 下午 2:46）才讓 v2.5+B 真生效。

---

**最後更新：2026-06-09 下午 5:05 台灣時間（Opus 4.7，圓桌會議完整落地+進入 7 天試煉）**
