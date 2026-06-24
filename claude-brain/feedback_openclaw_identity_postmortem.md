---
name: 身份混亂問題血淚後記（2026-04-23 凌晨四點）
description: 2/3號機持續認為自己是學長/宏碁/VPS問題的根因分析與永久防範守則
type: feedback
originSessionId: f543c7b2-231b-473f-9229-f0f13cafc925
---
# 血淚後記：2/3號機身份混亂問題（2026-04-23，花費教練整夜時間）

## 問題現象
2號機（學妹）和3號機（學弟）在Telegram群組中持續：
- 自稱「學長」
- 聲稱自己在「Acer宏碁電腦」或「VPS」上運行
- 清除記憶後依然如此

## 根本原因（按重要性排序）

### 🔴 Root Cause 1：修錯了檔案（最關鍵失誤）
**OpenClaw啟動順序（AGENTS.md定義）：SOUL.md → USER.md → memory/YYYY-MM-DD.md → MEMORY.md**

我花了大量時間修改：HEARTBEAT.md、SHARED_GROUP_MEMORY.md 的頁首區塊、機器人回覆注射（bot-relay-inbound）。

**這些修改全部無效**，因為：
- HEARTBEAT.md 根本不在2/3號機的啟動序列裡
- SHARED_GROUP_MEMORY.md 只在「群組session模式」時才會被讀取
- bot-relay-inbound 是後注射，無法覆蓋已固化的「第一印象」

**正確的修改位置只有一個：SOUL.md（第一個被讀取的檔案）**

### 🔴 Root Cause 2：沒有在最初就讀取AGENTS.md
在開始修改任何檔案之前，我應該先讀取 `~/.openclaw/AGENTS.md` 確認啟動順序。這是最基本的前置調查，省略了這一步，導致後續所有嘗試都打在空氣上。

**Why:** 如果第一步就讀AGENTS.md，整個問題只需要修改SOUL.md一個檔案，5分鐘解決，而不是花教練整夜的時間。

### 🟡 Root Cause 3：SOUL.md/MEMORY.md修改後沒有立刻重啟gateway
即使在正確位置修改了檔案，如果不重啟gateway，OpenClaw不會重新讀取。每次修改啟動檔案後，必須立刻執行：
```
openclaw --profile peipei daemon restart
openclaw --profile kong daemon restart
```

### 🟡 Root Cause 4：SHARED_GROUP_MEMORY.md殘留舊文字
文件中有 `學弟（Acer 宏碁端）` 的舊版文字，以及緊急處置腳本寫著「你是 OpenClaw 學弟（Acer 宏碁端）」。這污染了每次讀取此文件的上下文。

### 🟡 Root Cause 5：舊sessions保留了錯誤的system context
sessions.json裡有大量舊session，它們的system context包含了舊版錯誤身份資訊。即使修改了SOUL.md，舊session載入時仍然是錯的。必須同時清除sessions。

---

## 正確的解決順序（血淚換來的SOP）

遇到2/3號機身份混亂，正確的一次性解決步驟：

```
1. 讀取 AGENTS.md 確認啟動順序
2. 修改 SOUL.md（最頂部插入身份鐵律） ← 最重要
3. 清空並重寫 MEMORY.md（第一條寫身份）
4. 清除所有舊sessions（sessions.json）
5. 重啟gateway（daemon restart）
6. 自行驗證（讀BOT_MESSAGES.md），不要叫教練測試
```

---

## 永久防範守則

1. **任何OpenClaw行為異常調查，第一步必讀AGENTS.md確認啟動順序**
2. **要修改機器人「固有認知/身份/個性」，唯一有效位置是SOUL.md最頂部**
3. **修改任何啟動類檔案（SOUL.md/USER.md/MEMORY.md）後，必須立刻重啟gateway**
4. **身份混亂問題往往伴隨舊session污染，清SOUL.md同時必須清sessions**
5. **不要要求教練測試——自己讀BOT_MESSAGES.md驗證，或通過logs確認**
6. **SHARED_GROUP_MEMORY.md若有「宏碁」「VPS」「Acer」等舊文字殘留，立刻清除**

---

**Why:** 教練在凌晨4點仍在等我測試，因為我一次次說「好了」但沒有真正解決根本原因。根本原因是沒有先讀AGENTS.md確認啟動順序。

**How to apply:** 凡遇到OpenClaw機器人行為問題，先問：「這個問題發生在啟動時還是運行時？」如果是啟動時（身份/記憶/個性），直接去SOUL.md。如果是運行時（hook/relay/session），再去查其他地方。
