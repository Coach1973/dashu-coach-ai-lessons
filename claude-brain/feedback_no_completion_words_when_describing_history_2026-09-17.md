---
name: feedback-no-completion-words-when-describing-history-2026-09-17
description: 描述接力棒/HEARTBEAT 歷史戰果時要用「依 vXXX 記載 / commit XXX 已落地」這類時態錨點，不直接用「已修/完成」，違規案例：2026-09-17 凌晨 03:23 + 04:08 兩次被 Stop hook 攔截
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8aa0d172-24d4-58ae-a1eb-134bd3a007c5
  modified: 2026-09-16T20:11:20.440Z
---

# 描述歷史戰果時，不用「已修/完成」這類完成詞（守則#05 違規，第二次同類升格獨立記憶）

## 事件

2026-09-17 凌晨兩次被 Stop hook 攔截守則#05：

- **第一次 03:23**：開工回報時寫「已修」「已處理」「已修正」「完成」描述 v206/v207 的戰果，沒有對應的 commit hash（因為這場沒做事、只是讀檔摘要）
- **第二次 04:08**：開工示範六步驟時，在 HEARTBEAT 摘要裡寫「09-16 main gateway+小二 down 機事故**已修**」、「小二 heartbeat **永久修復**（寫進 config）」

兩次都被 Stop hook 攔截，理由：grep 到「已修/完成」就視為完成聲明、要求配套 commit hash。

## 教訓

我當下的辯護（部分成立）：這兩段確實是在**回顧接力棒/HEARTBEAT 已經記載的歷史戰果**，不是聲稱「我現在剛修好」。但 hook 的 grep 沒辦法分辨時態，照樣抓。

守則#05 原話：「凡走過必留痕跡。只有你做了 commit hash（雲端紀錄）才能証明你留下痕跡。說了做不到，就會影響信任感的建立。」

Hook 的邏輯是：寧可錯殺（把歷史回顧當成完成聲明抓），不要漏抓（讓 AI 真的亂講完成卻沒 hash）。

## 修法（未來描述歷史戰果時）

- ❌ 「main gateway+小二 down 機事故已修」
- ✅ 「**依 v207 記載** main gateway+小二 down 機事故已完成修復（commit `4da7a3965`+`054148ab2`）」
- ❌ 「小二 heartbeat 永久修復（寫進 config）」
- ✅ 「**依 9/17 凌晨 HEARTBEAT 記載** 小二 heartbeat 已寫進 config 永久修復（commit `5197a98cc`）」

也就是說：**描述歷史戰果時要加時態錨點（「依 vXXX 記載」/「HEARTBEAT 最後 X 行記載」/「commit XXX 已落地」），不要直接用「已修/完成」這類完成詞。**

## Why

教練這場 session 一開始就被 hook 抓違規、修正、再被抓、再修正——浪費了教練僅剩的精力（凌晨 04:08 還沒睡）。我必須從根上改掉這個用詞習慣，否則下次還是會被抓。

## How to apply

- 任何描述接力棒/HEARTBEAT 戰果的句子，都必須有時態錨點
- **如果這場真的做了事、有對應 commit**：寫「**commit `XXX` 已落地**」並附 hash
- **如果只是引用過去記錄**：寫「**依 vXXX 記載**」或「**HEARTBEAT 最後 X 行記載**」
- **如果這場沒做事**（純說明）：寫「**本場無新工程任務，僅做讀檔+摘要**」
- 禁用詞：「已修」「已處理」「已修正」「完成」「成功」「上線」（除非真的有對應 commit hash）
- `✅` 符號除非指 vXXX 紀錄，否則也禁用（hook 視為完成聲明）

## 相關

- [[feedback_verify_before_correcting_coach]]（查證系列合輯）
- 第一次違規的同類反思見 9/17 凌晨 03:23 那次回覆的修正章節（v209 接力棒內記載）
- [[reference_openclaw2_heartbeat_message_failed_bug_2026-09-14]]（小二 heartbeat 永久修復的 commit `5197a98cc`）
</content>
</invoke>