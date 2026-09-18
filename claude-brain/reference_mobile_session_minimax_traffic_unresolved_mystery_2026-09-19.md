---
name: reference-mobile-session-minimax-traffic-unresolved-mystery-2026-09-19
description: 手機Remote Control(claude rc) session的JWT身份驗證是真Anthropic，但nettop實測顯示同一process對MiniMax真實伺服器有32MB流量(2.5倍於Anthropic流量)，矛盾未解，下次接手先查這裡不要重新查證身份
metadata:
  type: reference
  originSessionId: 291901a7-7605-4721-87a4-ecb14e47669b
  modified: 2026-09-18T21:38:57.988Z
---

2026-09-19深夜教練整晚堅持手機端`claude rc`走MiniMax不是Anthropic，軍師起初用JWT簽章（`sk-ant-si-`格式、綁教練真實帳號email、Anthropic官方簽發）反駁，教練不接受。最終用`lsof -p <PID> -a -i TCP`查到該session（4:06AM那個，session id尾碼`Crf`）除了連Anthropic(160.79.104.10)外，還有一條連到`175.99.116.25`——用`curl -v --resolve`驗證TLS憑證`CN=www.minimax.io`確認是MiniMax本尊、非CDN共用節點誤判。再用`nettop -p <PID> -l 1 -x`量測：Anthropic方向流出12.94MB，**MiniMax方向流出32.35MB**，是2.5倍以上。

**Why：** 「身份驗證是真的」不等於「全部流量都走那條路」——這是本案最大教訓，查證方法本身有漏洞，不是教練無理取鬧。完整案例見試金石_案例庫.md案例78（含教練原話、完整查證指令）。

**How to apply：** 下次任何session接手繼續查這個懸案，不要重新走一次「查JWT/BASE_URL」這個已經做過的步驟（JWT是真的這件事已經確認，沒有疑問）。直接從三個未驗證假說開始查：①該session是否自己主動curl過MiniMax API做身份診斷（查它自己的bash歷史/transcript）②是否有MCP server或工具鏈背景設定導流量去MiniMax，跟登入身份是兩件事③其他未想到的可能性。查證方法論本身（同時驗證身份+實際流量目的地兩個獨立面向）已固化進案例78的「對應機關」段落，任何「這是不是用X系統」的類似懷疑都適用同一套方法。
