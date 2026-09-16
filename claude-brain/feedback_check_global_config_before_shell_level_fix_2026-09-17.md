---
name: feedback-check-global-config-before-shell-level-fix-2026-09-17
description: 遇到環境變數導致的錯誤，要先查全域設定檔(如~/.claude/settings.json)是不是根本來源，不要先假設是shell層級export、讓教練白跑unset才發現沒用
metadata:
  type: feedback
---

# 遇到環境變數卡關，先查全域設定檔，不要先讓教練試shell層級`unset`

## 事件

2026-09-17凌晨，教練人在外面熬夜想用手機操控Mac，全程靠軍師遠端指導教練在終端機打指令，過程繞了非常多次路。教練當場點名：「如果你一開始就知道我的那個終端機登的是MiniMax，你很早就發現這個問題，我就不用搞這麼久。」

事後檢討，這個「早該發現」的具體斷點是：第一次跳出`ANTHROPIC_BASE_URL is set and does not point at api.anthropic.com`錯誤時，軍師直接假設這是shell層級的環境變數（讓教練`unset ANTHROPIC_BASE_URL`），這個假設是錯的——真正來源是全域的`~/.claude/settings.json`的`env`區塊寫死的設定，shell層級`unset`完全沒用，因為Claude Code每次啟動都會重新從這個檔案注入，教練白跑一次指令才發現無效，才回頭查到真正源頭。

## 教訓

**軍師當下明明有Bash權限可以直接查這台機器的`~/.claude/settings.json`（甚至同時查`.zshrc`/`.zshenv`/`.zprofile`），卻只做了一半（只查了shell rc檔案），沒有同時查Claude Code自己的全域設定檔，導致第一輪診斷方向不完整，讓教練多跑一次注定失敗的指令。**

一般原則：任何「環境變數導致某功能被擋」的錯誤，如果自己有檔案系統讀取權限，應該**一次性**把所有可能來源都查過（shell啟動檔`.zshrc`/`.zprofile`/`.zshenv` + 該工具自己的全域/專案設定檔，例如Claude Code是`~/.claude/settings.json`、`~/.claude.json`），不要只查其中一種就急著讓使用者去試，試錯一次都是使用者的時間成本。

## Why

教練當晚已經徹夜未眠，每一輪來回貼上、等待、重試都在消耗他僅剩的精力。這不是「查不到」的問題（軍師確實有能力查到，且最終真的查到了），是「查的順序/完整度不夠」的問題——本可以第一次就把兩種來源一起查完，卻分兩輪才查完，讓教練承擔了本可避免的一輪等待。

## How to apply

- 遇到「XX環境變數導致YY功能被擋」的錯誤訊息，且自己有檔案系統存取權限時：**同一次動作內**查完 (a) 該shell的啟動檔（`.zshrc`/`.zprofile`/`.zshenv`，含`ZDOTDIR`指向的自訂路徑）(b) 該工具自己的全域/專案設定檔（Claude Code是`~/.claude/settings.json`+`~/.claude.json`+專案內`.claude/settings.local.json`），不要只查一種就讓使用者去試。
- 讓使用者執行任何「可能沒用」的診斷/修復指令前，先評估自己是否已經有辦法直接驗證這個假設（例如直接讀設定檔內容），能自己驗證的優先自己驗證，不要把「試了才知道有沒有用」的成本轉嫁給使用者。

## 相關

- [[reference_claude_code_remote_control_setup_sop_2026-09-17]]（這次事件的完整技術SOP）
