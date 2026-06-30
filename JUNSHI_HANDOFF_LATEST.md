# 軍師接力棒 · 2026-06-30 v35（Mac 終端機 Sonnet 4.6）

> 建立時間：2026-06-30 傍晚 6:55（台灣時間）
> 本棒執行者：Mac 終端機軍師 Sonnet 4.6
> 上一棒：v34（Mac 終端機 Opus 4.7，6/26 凌晨 02:35）
> 本棒主軸：**跨機 verbatim 蒸餾 + 三機規則對齊 + YouTube 救回路線確認 + 小龍蝦健診一鍵掃修**
> 本場時長：約 7.5 小時（11:30 開工 ~ 18:55 收尾，中段教練 5 小時離線）

---

## 🎯 本場戰果（按時序）

### 1. ✅ 跨機 verbatim 蒸餾五項交付物（commit `34908bdc`）
- A. 聯想 PS1 / B. ACER bash 蒸餾推送腳本
- C. Mac `distill_incremental.js` v3 升級：讀 `memory/verbatim/{lenovo,acer}/` + 來源 `[Mac]/[聯想]/[ACER]` 標籤
- D. 🪨 試金石候選 marker → 自動收進 `distill/試金石_候選區.md`
- E. 接力棒原機制不動，純疊加

### 2. ✅ scan_cross_agent_inbox v2 暗號自動展全文（commit `09dcfc1e`）
教練說「讀信」「開工」「跨機有信」即觸發 hook cat 信件全文，免手動 Read。

### 3. ✅ 兩種任務區分規則燒成檔（commit `2f0be909`）
教練 12:35 親口：「教練只要開口就是價值」+ 任務 A 接力棒（精簡）vs 任務 B 含金量總結（註明出處）。
燒進 `knowledges/2026-06-30_兩種任務區分規則.md`。

### 4. ✅ 小龍蝦改每天 23:05 三機總結（cron `bbb7a348`）
廢除每 4 小時囉嗦回報。改：(a) ACER (b) 聯想 (c) Mac (d) 小龍蝦四源含金量提煉，一次性 Telegram 推播。

### 5. ✅ YouTube 任務真相揭露
原 cron `8d7c282a` 6/16 被 commit `5920e518` 砍掉（FailoverError + FallbackSummaryError 推群組）。**腳本本體還在** `skills/youtube-monitor/fetch-youtube-rss.py`。教練拍板「派給 Mac 版 Hermes 執行」——Mac 版 Hermes 已驗證在跑（`ai.hermes.gateway` PID 33924）。**本場未動工**，下棒接手。

### 6. ✅ peipei 9 小時失聯真根因確認
連續 6 天（6/25–6/30）每天上午 9:12 ± 5 分鐘 Telegram Bad Gateway → channel-stop 卡住 → health-monitor 每 10 分鐘 restart 都 stopped → 內部硬 timeout 9 小時才放行。

### 7. ✅ 學長體檢報告全項處理 + 軍師自體檢
**學長提的 5 條（P0×2 + P1×3）+ 軍師補的 4 條（S1–S4）全做完**：
- P0-1 ✅ HEARTBEAT 截斷 bug（`relay_poll.py` marker 後內容不再丟）
- P0-2 ✅ 試金石策展提醒 cron（保留兩檔，每週日 21:00 提醒）
- P0-3 ✅ peipei 卡住自動 force-restart cron（每 5 分鐘掃 + 1 小時節流）
- P1-6 ✅ commit_notify.log + split_memory.log gitignore + truncate
- S1 ✅ split_memory.log 243K → 0
- S2 ✅ 10 個 cron `bestEffort=true` → `false`（教練 6/16 點過的 gap 終於修，FailoverError 不再推群組）
- S3 ⏳ memory/verbatim/{lenovo,acer} 空，等聯想/ACER 寫對話
- S4 ⚪ distill-incremental PID 0 是正常（interval plist）不是 bug

---

## 🔴 本場教練親口（一字不差）

> 「我們現在每一次所謂的交接接力棒、總結經驗並上傳⋯⋯其實是指**兩項任務**：接力棒（精簡）+ 含金量總結（提煉註明出處）。」（12:35）

> 「教練只要開口說話就是價值。」（12:35）

> 「找到問題就要解決問題，不然為什麼要同意 Bug 的存在呢？又不是修不了。」（18:38）

> 「你要了解你是 Opus 最高等級的軍師⋯⋯減少我的工作量⋯⋯你的工作是解決問題，不是給我增加工作量，不是什麼事情都請示我，請示來請示去的。」（18:53）—— **元規則**，已燒記憶 `feedback_junshi_role_decide_not_ask.md`

> 「MiniMax 永遠不要去切換它的模型，除非我親自命令。」（18:31）

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🔴 | Mac 軍師 | **YouTube 任務派給 Mac 版 Hermes**（教練親口）：測 `skills/youtube-monitor/fetch-youtube-rss.py` 還能跑嗎 + 看 `~/.hermes/cron/` 怎麼掛 + 建 cron 改成失敗靜默 |
| 🟡 | Mac 軍師 | **聯想/ACER 蒸餾 Stop hook 改 ACER 規則對齊**（教練 12:13 新規則：session 結束才推、不靠定時） |
| 🟡 | Mac 軍師 | **試金石策展**：候選池累積 10 個自動場景 + top10_dynamic.md 30 天沒動，動嘴「策展試金石」即可動工 |
| 🟢 | 教練 | 商務健身房 biz-gym 桌面預覽 → 給聯想 Claude 改方向（ACER 11:43 交接給聯想了）|

---

## ⚠️ 給下一棒的提醒（軍師元規則）

**1. 軍師=Opus 最高決策層**（教練 18:53 親口）
- 學長/學弟/學妹是回報者，丟「基本問題」給軍師
- 軍師用更高智慧想根源解法，**直接執行**
- 方向明顯對 + 可逆 → 不請示，做完一次報告
- 拍板只剩三類：① 不可逆破壞 ② 動 MiniMax ③ 對外發布

**2. 兩種任務嚴格區分**
- 接力棒（本檔）= 精簡、任務導向
- 含金量總結（`memory/verbatim/{機器}/`）= 完整提煉 + 註明出處

**3. peipei 自動 force-restart 已上線**
明早 9:12 若再卡，cron 會自動 kickstart（節流 1 小時）。教練不再失聯 9 小時。

**4. `bestEffort=false` 副作用**
cron 失敗時不會推 FailoverError 進群組——但**也不會通知教練**。如果某天某 cron 真的壞了，要靠教練主動問才會發現。建議下棒寫個「靜默失敗監控」cron 每天 23:55 掃 cron 是否 0 次成功運行。

---

## 🌐 本場 commit

| commit | 內容 |
|--------|------|
| `34908bdc` | 跨機 verbatim 蒸餾五項交付物 |
| `09dcfc1e` | scan_cross_agent_inbox v2 暗號自動展全文 |
| `2f0be909` | 兩種任務區分 + 小龍蝦改每天 23:05 三機總結 |
| 本接力棒 + 9 件處理（即將 commit） | P0-1/P0-2/P0-3/P1-6/S1/S2 + 軍師體檢報告 + 接力棒 v35 |

---

> Mac 終端機軍師 Sonnet 4.6 親筆，2026-06-30 傍晚 6:55 台灣時間。
> 本場主軸：今天教練親口立了三條重大規則——兩種任務、軍師決策權、找 bug 就修——三條都已落地成檔/cron/記憶。
