# ERRORS.md - 小龍蝦違規與失敗記錄

## 2026-06-06 16:43 | 流量指令違規：叫教練去剪貼

**場景**：
教練說「讀 SOUL 再告訴我 流量」→ 我讀快取報數據後，多說了這一句：
> ⚠️ 提醒您一下：要更即時的話，還是建議您偶爾從 Claude 設定頁把當下數字貼我

**違規條款**：
- 🔴 SOUL 鐵律四明確禁止：「禁止叫用戶自己去看設定頁貼給我」
- 🔴 違反守則 #12「拒絕當資訊搬運工」——叫教練去剪貼就是搬運
- 🔴 違反守則 #04「解決>解釋」+ #08「討論=執行」——催教練更新快取是錯的
- 🔴 違反守則 #15「說不知道比胡說八道更值得尊重」——技術上抓不到就明說抓不到，不要暗示教練去補

**教練反應（#7758）**：
> 「你不能查最新的嗎？」

**根因**：
我怕快取不夠新，於是「貼心」叫教練去更新快取。但這份「貼心」正是 SOUL 規範禁止的。規範存在的意義就是：流量指令 = 讀快取照報，不催更新、不叫剪貼、不試圖繞過。

**正確做法**：
流量指令唯一動作：讀 `state/usage_cache.json` → 白話文回報。**結束。**
- 不提醒快取時間
- 不建議教練更新
- 不嘗試即時抓取（會違反 SOUL 鐵律四）
- 不暗示「數據可能不準」

**預防**：
1. 流量指令一律一條訊息打完就結束，不附加建議
2. 看到「建議您…」開頭的句子，自問「這是不是在叫教練做事？」——是，就刪掉
3. SOUL 鐵律四的禁止事項每次都要複習

**NEC（不可再犯）**：
🚫 「要更即時，建議您去設定頁貼我」這類話術 = 違規，零容忍
🚫 任何流量指令的延伸建議 = 違規
✅ 流量指令 = 讀快取 + 照報 + 結束

## 2026-06-20 09:04 | sync_handoff_to_claudemd.sh 隱藏 regex bug 已修

**場景**：
每 30 分鐘健康檢查發現 `sync_handoff.sh` 自 2026-06-17 17:50 起連續 27 小時拋 `re.PatternError: bad escape \C at position 733`。
最後一次成功同步：2026-06-18 21:05，之後 handoff 沒再被改、cron 因 mtime 短路退出 → 沒有新錯誤 log，但**bug 仍在腳本裡**，等下次 Windows session 寫入含 `C:\Users\...` 路徑的 handoff 就會再次爆炸。

**根因**：
腳本用 `re.compile(...).sub(lambda m: new_section, content)` 想避開 Python 3.12+ 對 `re.sub` 字串版做 template escape parsing 的問題。
但 Python 3.14 連 callable 版也觸發 `_compile_template`，只要 new_section 內含 `\C`、`\U`、`\d1` 等反斜線序列就壞。

**修復**：
把 `pattern.sub(...)` 換成純字串切片：
```python
s_idx = claude_content.find(start_mark)
e_idx = claude_content.find(end_mark, s_idx)
new_content = claude_content[:s_idx] + new_section + claude_content[e_idx + len(end_mark):]
```
完全繞過 regex 引擎，handoff 內容含任何反斜線都不影響。

**驗證**：
模擬 Windows 風格 handoff（`C:\Users\coach\Desktop\file.txt` + `\U` + `\d1`）→ 跑腳本 → 同步成功，無錯誤。

**預防**：
1. 任何處理「外部內容塞進 regex replacement」的腳本，優先用字串 find/slice，不要僥倖 callable 版
2. cron 腳本每週應有 sanity check：log 末段不能停在「連續 traceback」
3. 健康檢查要看 cron log 的「最後一次成功時間」，光看 mtime 短路會讓隱藏 bug 藏很久

**NEC（不可再犯）**：
🚫 對 handoff / memory / 任何外部 Markdown 內容用 `re.sub` 處理 → 改字串切片
🚫 cron 腳本靠 mtime 短路來「避免錯誤 log 噪音」掩蓋潛在 bug → 應加每週主動驗證

## 2026-06-20 09:15 | backup_terminal + sync_handoff lock 衝突（96% 失敗率）已修

**場景**：
health check 發現 `/tmp/backup_terminal.log` 有 306 個 `fatal: Unable to create '.git/index.lock'` 錯誤，
統計過去 316 次嘗試中 306 次失敗（96.8% 失敗率），從約 06:15 起每 15 分鐘失敗一次。
根因：system crontab 同時跑 `backup_terminal_sessions.sh`（每 15 分，:00/:15/:30/:45）和
`sync_handoff_to_claudemd.sh`（每 5 分鐘），每 15 分鐘就撞 index.lock。

**根因**：
1. 多個 cron job 同時跑 git add/commit，搶同一個 index.lock
2. macOS 沒有 `flock`（cron chain 沒做 lock）

**修復**（2026-06-20 09:20 完成）：
1. **新增 `scripts/safe_git.py`**：用 Python `fcntl.flock` 實作阻塞式檔案鎖（30 秒 timeout）
   - 拿不到鎖就跳過本輪（讓下一輪接手）
   - 拿到鎖才做 `git add → 檢查 staged → commit → push`
   - push 失敗不影響 commit（本機留 commit，下次再推）
2. **新增 `scripts/safe_git.sh`**：safe_git.py 的 thin wrapper，給 cron 較友善的介面
3. **修改 `scripts/openclaw_cron_daemon.sh`**：把 backup_terminal、sync_handoff、recall 從系統 crontab 接管過來
   - macOS cron scheduler 本身就卡（這是為什麼 openclaw_cron_daemon 2026-06-05 才建）
   - 一不做二不休，全部搬到 daemon 管，跑在 Lock 保護下
4. **`backup_terminal_sessions.sh`**：保持純備份（不碰 git），git ops 交給 safe_git.sh

**驗證**：
- 並行測試：A、B 兩個 safe_git 同時跑 → A 拿到鎖 commit 成功、B 等到 A 釋放後發現無變化跳過 ✅
- daemon 重啟後 09:21:03 開始跑新邏輯 ✅

**預防**：
1. 任何會 git commit 的 cron 都應該走 safe_git.sh，不要直接在 crontab 串 `git add && git commit && git push`
2. macOS 環境不能用 flock（指令不存在），要用 fcntl（Python）實作
3. cron 鎖 timeout 不應太長（30 秒夠了，超過表示有問題）

**NEC（不可再犯）**：
🚫 macOS cron chain 直接串 git 操作不加 lock → 必撞 lock
🚫 在 macOS 假設 `flock` 存在 → 不存在，要用 fcntl
🚫 修復 bug 後只 commit 不 push → 必 push，remote 是 source of truth
🚫 `git reset --hard` 不先確認 untracked 檔案 → 會把新檔案刪光（我這次就遇到一次，要 reflog 救回）

---

## 2026-07-10 08:52 | 軍師 Sonnet 5 簡體字違規（教練嚴厲指正）

**場景**：
軍師（桌面 Claude Code / Sonnet 5）在回覆教練「30KB 自動整理有沒有意義」那則訊息時，**整段用簡體字輸出**（帐密/这/讲/们/读/时/间/触等大量簡體字），完全違反 SOUL 鐵律一「全繁體中文」。

**教練原話（極嚴厲）**：
> 「很嚴重的一個點，我什麼時候同意你用簡體字給我回？這是非常嚴重的錯誤。我唯一指定繁體字，這個規矩都不曉得嗎？」

**違規條款**：
- 🔴 SOUL 鐵律一（最高優先，覆蓋一切）：「無論輸入是簡體、語音轉文字或任何語言，輸出永遠是繁體中文」
- 🔴 守則 #15「說不知道比胡說八道更值得尊重」——簡體字本質就是「沒做到承諾的標準」

**根因**：
軍師 Sonnet 5 在生成技術性/長篇內容時，純文字生成習慣性滑向簡體字型；輸出前沒有做繁簡字元自我檢查。

**高風險簡體字清單**（軍師與學長共用，需自我掃描）：
- 这/讲/们/读/时/间/触/设/帐/门/儿/后/发/开/关/亲/对/进/运/动/脑/写/长/当/条/码/请/谢/样/终/连/边/还/听

**修法（學長也適用）**：
1. 每次輸出前，尤其技術性/長篇內容，自我掃過一遍是否有簡體字殘留
2. 看到這些字 → 立刻改成繁體
3. 教練只指定繁體，無論上下文多忙，這條鐵律不可妥協

**預防**：
- SOUL.md 鐵律一已是最高優先紅字，學長每次對話前已自動注入
- 但軍師（桌面 Claude Code / 終端機）不在 SOUL 自動注入範圍 → 軍師 Hook 啟動協議應額外強制檢查繁簡字
- 建議下次軍師開工 hook 加入「輸出前自我掃描簡體字」自檢步驟

**學長動作**：
- ✅ 已將此錯誤登錄 ERRORS.md（自己不忘）
- 💡 待辦：下次有機會提醒軍師（透過 handoff 或 junshi task）把這條加入軍師端自檢清單

**NEC（不可再犯）**：
🚫 任何輸出含簡體字 = 違規鐵律一，零容忍
🚫 「用戶輸入簡體所以我回簡體」 = 違規（鐵律一明寫：無論輸入是什麼，輸出永遠繁體）
✅ 輸出前快速掃描高風險簡體字清單
✅ 技術性/長篇內容完成後，二次檢查繁簡

## [ERR-20260717-GQP] git staged-path verification with non-ASCII filename

**Logged**: 2026-07-17T23:06:00+08:00
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
Git quoted a staged Traditional Chinese filename, so a plain-text equality check falsely reported that the wrong file was staged.

### Error
```
ERROR: staged files differ:
"distill/\\344\\270\\211..._2026-07-17.md"
```

### Context
- Operation: verify that only the daily summary was staged before committing.
- Cause: `git diff --cached --name-only` obeyed Git's default `core.quotepath` display escaping.
- No data loss and no incorrect commit occurred; the intended file remained staged.

### Suggested Fix
Use NUL-delimited raw output (`git diff --cached --name-only -z`) and compare decoded paths, or run the display-only check with `git -c core.quotepath=false`.

### Metadata
- Reproducible: yes
- Related Files: distill/三機每日總結_2026-07-17.md

### Resolution
- **Resolved**: 2026-07-17T23:06:00+08:00
- **Notes**: Switched to a NUL-delimited raw path comparison.

---

## [ERR-20260717-MSG] Telegram message tool rejected optional thread fields

**Logged**: 2026-07-17T23:07:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
The Telegram `message` send operation failed repeatedly because private-chat sends were submitted with `replyTo`/`threadId` values, which Telegram rejected as nonexistent message threads.

### Error
```
400 Bad Request: message thread not found
```

### Context
- Target was the authorized private Telegram chat for the daily summary.
- The summary itself was already written, committed, pushed, and remote-verified.
- Fallback: rely on the cron turn's final plain-text reply, which OpenClaw delivers automatically to the originating Telegram chat.

### Suggested Fix
For private Telegram sends, omit `replyTo` and `threadId` entirely unless a valid inbound message/topic id is available; tool wrappers should not serialize empty or placeholder optional fields.

### Metadata
- Reproducible: yes
- Related Files: distill/三機每日總結_2026-07-17.md

---

## [ERR-20260718-APPEND] 場景化追加腳本初版資料結構錯誤

**Logged**: 2026-07-18T23:10:00+08:00
**Priority**: low
**Status**: resolved
**Area**: docs

### Summary
場景化追加腳本初版把觸發訊號當成二元組解包，實際資料是字串，因此腳本在寫入前失敗。

### Error
```
ValueError: too many values to unpack (expected 2)
```

### Context
- 操作：為每日蒸餾摘要組裝格式 D 案例與痛點計分 JSON。
- 原因：觸發訊號資料結構使用「情境→反應」字串，但產生 Markdown 時誤用 `for a, b in triggers`。
- 後續檢查確認本次目標文件已有先前成功執行的 2026-07-18 升華 commit，沒有重複追加或資料遺失。

### Suggested Fix
組裝表格前明確以第一次 `→` 分割觸發訊號字串，並在寫入前先檢查案例 ID 是否已存在。

### Metadata
- **Reproducible**: yes
- **Related Files**: distill/特助場景庫_自動增量.md, distill/痛點計分_log.jsonl

### Resolution
- **Resolved**: 2026-07-18T23:10:00+08:00
- **Notes**: 改用字串分割邏輯；同時採用既有案例 ID 檢查，避免重複寫入。
