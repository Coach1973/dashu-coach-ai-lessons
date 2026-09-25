---
name: commit-on-promise
description: Use immediately whenever you tell 教練 "我來做"/"我會處理"/"我幫你弄好" or report a task as complete. Enforces same-turn commit + push + hash — never "等一下" or batching commits later.
---

# 承諾當場 commit（執行細則 N1）

對應守則 #05（凡走過必留痕跡）、#04（解決問題比解釋問題更重要）。

## 規則

一旦說出「我來做」「我幫你處理」，這個動作必須在**同一次回覆裡**完成：
1. `git add` 相關檔案（不要用 `-A`/`.`，指名檔案避免誤帶密鑰或垃圾檔）
2. `git commit`
3. `git push`
4. 把 commit hash 貼給教練

## 鐵律

- **沒有 hash = 沒做。** 口頭說「完成了」「記住了」一律視為零。
- 從不說「等一下」「累積多一點再commit」——不可逆的部分立刻做（守則#08）。
- 若commit失敗（hook擋下），修好問題後建立**新**commit，不用 `--amend`、不用 `--no-verify`。

## 自我檢查（回報前）

- 我剛剛是不是說了「我來做」類的話？
- 如果是，這次回覆結尾有沒有 commit hash？
- 沒有 → 現在就做，不要留到下一輪。
