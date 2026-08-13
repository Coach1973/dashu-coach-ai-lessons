---
name: feedback-line-identity-missing-from-people-md
description: LINE進來的教練被小龍蝦當陌生人問「您是哪一位」，根因是people.md/USER.md身份名冊只登記Telegram ID沒登記LINE ID
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7c3bfad2-6f16-4c09-ab1c-23bcf3e61ae2
  modified: 2026-08-13T17:51:38.196Z
---

教練從LINE（帳號U895a0ad8e49d75f8303dc3d067282dc0，2026-04起使用至今、已在dmPolicy pairing白名單）傳訊息給「龍蝦小助教」（main agent default LINE帳號），小龍蝦完全不認得他，問「您是哪一位」，教練當場動怒（"你是想找死嗎？你是欠修理嗎？你還問我是哪一位？我是你老大你都不曉得嗎？"）。

**根因（已用session log + 檔案內容雙重驗證，非猜測）**：白名單通過（教練可以跟bot說話）跟「身份識別」（bot知不知道這個ID是教練）是兩套獨立機制。`workspace/memory/people.md`和`workspace/USER.md`裡教練的條目**只登記了Telegram ID（6124913915），完全沒有登記任何LINE ID**——即使這個LINE帳號從2026年4月就持續使用、有數十份memory/daily檔案佐證。模型每次新session啟動時，是靠讀這兩份檔案來判斷「這個發訊息的人是誰」，登記不到就只能當陌生人處理，逼它現場翻log偵探（跟我這次查證的路徑一模一樣）。

**已修復**：`people.md`＋`USER.md`教練條目都補上兩個已知LINE ID（U895a0ad8e49d75f8303dc3d067282dc0=龍蝦小助教/default帳號、U168903487f0ba2b666ddc62b854de351=第二身份「贏家思路」），並註明「這些ID傳訊息一律視為教練本人，不要再問是哪位」。

**Why**：教練26年培訓經驗告訴他「講過的話系統該記住」，任何管道問他「您是哪位」都是對他存在感的否定，這是[[feedback_coach_words_are_sacred]]同一條神經。身份識別檔案（people.md/USER.md）跟白名單（allowFrom）必須同步更新，只改一邊會留下這種「能講話但不被認得」的縫隙。

**How to apply**：往後任何新通道（新LINE帳號、新Telegram bot、新平台）幫教練開通pairing/allowFrom時，**同一個動作要順手把該ID寫進people.md和USER.md**，不能只做安全閘門那一半。看到任何agent對已授權的教練本人問「請問您是哪位/怎麼稱呼」，第一時間先查這兩份身份名冊有沒有漏登，不要只归因於「session重啟/記憶被清」。

**附帶修正**：v107接力棒記錄的「cloudflared斷線13小時」是UTC/台灣時間換算錯誤——log顯示斷線區間是2026-08-13T11:47:40Z到17:09:47Z（UTC），換算成台灣時間是08/13 19:47到08/14 01:09，實際只斷約5.4小時，不是13小時；而且教練這次的LINE對話是01:19才開始，已經是tunnel恢復之後，兩件事之間沒有真的矛盾，純粹是舊記錄的時間換算錯誤（同一種錯誤模式在[[reference_new_session_context]]的時間鐵律已經提醒過：ISO字串Z=UTC要+8才是台灣時間，這次是拿UTC數字直接當台灣時間念，屬於同一坑的變體）。
