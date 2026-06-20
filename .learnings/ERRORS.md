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
