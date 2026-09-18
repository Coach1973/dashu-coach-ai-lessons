# 軍師接力棒 · 2026-09-19 v220（封存）

> 來源：`JUNSHI_HANDOFF_LATEST.md`（v224 棒新增時依 E16 接力棒瘦身鐵律搬入 archive）
> 封存時間：2026-09-19 04:45
> 上一棒：v219
> 下一棒：v221（仍在主檔 `JUNSHI_HANDOFF_LATEST.md`）

---

# 軍師接力棒 · 2026-09-19 v220（Mac桌面版 Sonnet 5，接力棒狀態表失真教訓+CLAUDE.md開機瘦身236KB→78KB+手機Remote Control重啟卡死未解）

> 建立時間：2026-09-18 22:54 ~ 2026-09-19 00:03（台灣時間，約1.2小時）
> 上一棒：v219
> 本棒主軸：**開工時照唸接力棒舊狀態表，把v219已經解決並驗證上線的「10/3 Netlify部署」問題當成新問題重新丟給教練選A/B/C，教練當場動怒（「你一個不小心，我就在那邊跟你講半天」）。查明根因後修好單一實例+建立機械式防呆機制。順勢查教練追問的另兩件事：MiniMax context window被鎖200K的真正機制、CLAUDE.md開機注入佔掉84%context的根因，兩件都查到底並動手修復。最後嘗試重啟手機Remote Control host，卡在一個排除10種來源仍查不到的謎樣阻擋，教練裁示先總結收工。**

## 🎯 本場戰果

### 1. 接力棒狀態表失真教訓：單一實例修復+機械防呆機制上線
根因：v219把「10/3 Netlify部署失敗」解決並verified live後，只在文末新增敘述，沒回頭把開頭狀態表那一列的🔒改成✅。v220開工照唸舊狀態表，把已解決的問題重新端給教練選，教練當場動怒糾正。已重新curl驗證現況（published deploy `6aad2282`、`archive/lecture-history.html`200、舊中文路徑404）確認真的已上線，更正狀態表為✅。新建`scripts/handoff_sync_guard.sh`（PreToolUse Bash matcher，比照`netlify_deploy_guard.sh`同款模式）：git commit涉及`JUNSHI_HANDOFF_LATEST.md`時，偵測「新增完成敘述卻沒同步更新狀態表對應列」的落差並提醒（非硬擋），3種情境測試通過，已註冊生效。commit`425e877`+`552232f2`。

### 2. CLAUDE.md開機注入236KB→78KB：教練「開機就佔84%」投訴的真根因+修復
教練追問「MiniMax context明明改了1M，為什麼開機讀完就佔84%」。查證：`CLAUDE.md`（每次開工自動注入）236KB，幾乎全是`JUNSHI_HANDOFF_LATEST.md`鏡像全文；後者「現在真正待辦」狀態表累積195列，其中**162列狀態早已是✅（已完成）**，佔175KB（78%），從未被移出主檔。已封存162筆✅列（`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`，git history+試金石完整保留不遺失，只是不再每次開工重灌）+封存v217完整戰果敘述，只留32筆真正需要追蹤的活躍列。`JUNSHI_HANDOFF_LATEST.md`223KB→65KB，`CLAUDE.md`鏡像後236KB→78KB（已由既有auto-sync cron自動commit+push，本場補commit源頭檔案），commit`552232f2`。

### 3. MiniMax 1M context window機制查證（部分完成，卡在無法實測驗證）
用`claude-code-guide`agent+官方docs(`code.claude.com/docs/en/model-config`)查證確認：`CLAUDE_CODE_AUTO_COMPACT_WINDOW`只設auto-compact**門檻**，不會擴大實際context window；自訂/gateway model ID只要含`[1m]`字尾（不分大小寫）Claude Code理論上會自動假設1M window，這是官方文件明載、且對應GitHub issue #68522已於2026-08-17正式修復關閉的功能。這台Mac `claude --version`是2.1.273，版本夠新理論上該生效。追查手機端為何還是200K，發現`claude rc` host process（PID 97294）**從2026-09-17 03:47就沒重啟過**，比當晚的MiniMax設定修復早了一天多，手機開新session只是透過tmux重連同一個process，從沒機會吃到新設定——這才是200K問題的真正根因（不是1M機制本身失效）。

### 4. 手機Remote Control重啟卡死：耗時排查未解，教練裁示收工
教練同意關閉舊process後，新的`claude rc`（含`.zshrc`裡9/17就建好的專用別名`claude-remote`）**完全起不來**，堅持報錯「偵測到API金鑰/自訂BASE_URL存在」，即使該次呼叫已用`env -u`清空相關變數。逐一排除10處已知設定來源（settings.json三層、shell rc檔、Keychain兩組憑證、launchd全域環境、背景daemon、`~/.claude.json`）**全部排除仍查不到真正來源**。過程中`claude auth logout`+`claude auth login`重新走過一次真OAuth登入，**這部分確認乾淨成功**（帳號正確、本對話視窗全程未受影響），但`claude rc`症狀完全沒變。教練考量對話框已到48% context，裁示先總結收工，這題留到下一個對話框繼續查。完整排除清單+3個下一步建議方向見[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_stale_handoff_row_represented_as_unsolved_2026-09-18`：接力棒「文字敘述」跟「狀態表」是兩個要手動同步的地方，只寫敘述不改表格狀態，下一棒會把已解決的問題當新問題重新端出來。已建機械防呆`handoff_sync_guard.sh`。
2. `reference_remote_control_relaunch_blocked_mystery_2026-09-19`：手機Remote Control重啟卡死的完整排除清單，下一場直接從這份清單的「懷疑方向」（`tengu_ccr_bridge`旗標）接續查，不用重新排查已確認排除的10處。

## 📋 下一場開工先做
1. **最優先**：手機Remote Control (`claude rc`) 重啟卡死——教練決定要繼續查/砍掉重練/先擱置，三選一，見上方狀態表🔒列+[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]完整排除清單。
2. 沿用v218/v219既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測(教練不催)、peipei-ai-backup舊commit金鑰歷史(教練已表態不處理)、`stop_rules_master.py`規則#07誤判regex(教練示意MiniMax有空自行補丁)。
3. 💬試金石案例庫商業化討論——教練指定的軍師專屬討論題目，本場再度沒空展開（連續第二場被其他緊急事項擠掉），下一場優先主動提起。
4. E16接力棒瘦身：本場v217已封存，主檔現為v218~v220共3棒，下次開工建議把v218搬進archive維持2棒上限。

## 🔑 本場commit
`workspace`：`425e87794`(接力棒10/3狀態表更正+教訓記憶)、`552232f24`(接力棒瘦身236KB→78KB+handoff_sync_guard.sh新建)。本次收工commit另計，含v220接力棒本身+Remote Control排除清單記憶檔。
