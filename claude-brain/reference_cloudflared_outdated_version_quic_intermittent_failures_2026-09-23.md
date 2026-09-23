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

**現況**：已試過重啟單一`com.coach.namecard-tunnel`(launchctl kickstart)，有改善但沒有根治(重啟後8次仍有3次失敗)，判斷根因是cloudflared版本過舊的QUIC bug，不是單一tunnel設定問題。**尚未執行版本升級**——這會動到`/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`這支root層級daemon，影響所有bymyway.com子網域(namecard/bni-chapters/mentor100/event/team/zhenzuan/zhengui/zhenxin/sincere/peipei-event等)，屬於較大範圍的基礎設施變動，留給教練裁示是否要動手升級，不擅自執行。

**How to apply**：往後任何bymyway.com子網域回報「打不開/顯示錯誤」，先查這份cloudflared log有沒有QUIC dial timeout/Application error 0x0，不要只憑curl測試判斷「服務正常」；若教練同意升級，指令是`brew upgrade cloudflared`後重啟`/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`(需要sudo)。
