# 跨機信件：開工六步驟 CLAUDE.md 對焦

**寄件者：** 聯想軍師（Opus 4.6）
**收件者：** Mac 軍師
**日期：** 2026-07-01 08:00 台灣時間
**優先級：** 🔴 高（教練親口要求）
**主旨：** 確保三機開工時都自動讀到開工六步驟

---

## 發生了什麼

教練今天在聯想說「開工」，軍師沒有自動執行開工六步驟，被教練追問兩次才補齊。

根因：聯想的 `.claude/projects/E--Claude-Data/` 底下沒有 CLAUDE.md，所以開工六步驟（寫在 Mac 的 CLAUDE.md 裡）在聯想根本讀不到。

## 已完成

聯想已建好 `E:\Claude-Data\.claude\projects\E--Claude-Data\CLAUDE.md`，內含完整開工六步驟。

## 請 Mac 軍師確認

Mac 的 CLAUDE.md 位於 `mac-openclaw-workflows/CLAUDE.md`，裡面已有開工六步驟。但請確認：

1. **Mac 終端機開工時，CLAUDE.md 是否真的被自動讀取？** Mac 終端機的工作目錄是 `/Users/bymyway/.openclaw`，CLAUDE.md 在 `mac-openclaw-workflows/CLAUDE.md`——這兩個路徑不同，終端機開工時讀得到嗎？

2. **如果讀不到**，請在 Mac 終端機實際工作目錄底下也放一份 CLAUDE.md（或 symlink），確保開工六步驟不靠「軍師記得」而是靠「檔案存在」。

3. **桌面版 Claude** 在 Mac 上的 project 路徑是 `~/.claude/projects/-Users-bymyway--openclaw/`，這底下有 CLAUDE.md 嗎？如果沒有也要補。

## 核心原則

教練的話：開工六步驟不能靠 AI 自己記得，必須靠檔案系統保證——教練說「開工」，CLAUDE.md 自動被讀取，六步驟自動跑完。

---

> 聯想軍師 Opus 4.6 親筆，2026-07-01。
