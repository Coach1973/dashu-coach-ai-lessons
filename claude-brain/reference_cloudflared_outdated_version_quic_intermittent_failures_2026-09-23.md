---
name: reference-cloudflared-outdated-version-quic-intermittent-failures-2026-09-23
description: cloudflared 2026.3.0版本(該升級到2026.9.1)QUIC協定間歇性斷線，導致namecard/bni-chapters等多個bymyway.com子網域間歇性525/520/連線失敗，curl測試會漏抓
metadata:
  type: reference
---

2026-09-23處理namecard-db的HTML Chrome驗證鎖時意外發現：真實Chrome開`namecard.bymyway.com`出現「525: SSL handshake failed」，但同時間`curl`測試卻回傳正常302。連續curl 8次也有3次是`000`(連線失敗)。查`/Library/Logs/com.cloudflare.cloudflared.err.log`（root層級`cloudflared tunnel run --token`daemon的log，管理所有bymyway.com子網域）確認：

- 反覆出現`failed to dial a quic connection error="...timeout: no recent network activity"`和`failed to accept incoming stream requests error="...Application error 0x0 (remote)"`，從2026-09-22就開始間歇發生，非本場對話造成。
- log明確提示：`Your version 2026.3.0 is outdated. We recommend upgrading it to 2026.9.1`。
- 交叉測試確認不只namecard——`chapters.bymyway.com`(bni-chapters)同樣間歇性連線失敗，`mentor100.bymyway.com`目前穩定。

**教訓**：`curl`走的路徑可能跟真實瀏覽器(走公開DNS/Cloudflare edge/QUIC)不完全一致，`curl`測通不代表教練實際用瀏覽器打得開——這正是[[feedback_html_preview_chrome_only]]鐵律要求「必須用Chrome親眼驗證」的另一層意義，這次意外撞見了活生生的案例。

**2026-09-23教練當場裁示「必然一定要升級」，已執行並驗證**：`brew upgrade cloudflared`（2026.3.0→2026.9.1）+ 重啟全部11支使用者層級named tunnel（`launchctl kickstart -k gui/$UID/com.coach.<name>-tunnel`，不需sudo，涵蓋namecard/bni-chapters/mentor100/event/team/team01/zhengui/zhenzuan/zhenxin/sincere/peipei-event）。升級前連續測試namecard 8次有3次失敗，**升級後namecard+bni-chapters+mentor100各10次連續全部成功**，另用真實Chrome複查namecard.bymyway.com畫面正常。

**唯一未處理的尾巴**：root層級`/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`（PID未變，token式tunnel，跑什麼服務未查證）仍是舊binary在記憶體中執行，`sudo launchctl kickstart -k system/com.cloudflare.cloudflared`需要教練本人密碼才能重啟（`sudo -n`測試過確認會卡密碼提示，AI不能代打）。因為所有實測的bymyway.com子網域都是走使用者層級tunnel且已驗證穩定，這支root daemon暫不確定是否服務公開流量，優先度較低，教練有空可自己在終端機跑一次上面那行指令讓它也吃到新版。

**How to apply**：往後任何bymyway.com子網域回報「打不開/顯示錯誤」，先查這份cloudflared log有沒有QUIC dial timeout/Application error 0x0，不要只憑curl測試判斷「服務正常」。
