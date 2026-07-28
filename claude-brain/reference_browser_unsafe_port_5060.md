---
name: browser-unsafe-port-5060
description: Chrome/瀏覽器對SIP協議常用埠(如5060)內建ERR_UNSAFE_PORT黑名單，本機測試Flask服務用127.0.0.1:5060這類埠會被瀏覽器主動擋掉，不是網路問題
metadata: 
  node_type: memory
  type: reference
  originSessionId: bc06c7b1-be23-47a2-acc9-628a3aa5db98
  modified: 2026-07-28T11:14:12.077Z
---

2026-07-28教練測試event-signup的抽獎轉盤功能時，瀏覽器連`http://127.0.0.1:5060/wheel`
出現「無法連上這個網站…ERR_UNSAFE_PORT」。一開始誤判成「127.0.0.1只有這台Mac自己能連」，
教練點出根本原因是`ERR_UNSAFE_PORT`——Chrome/主流瀏覽器對SIP等協議常用的連接埠
(5060/5061等)內建安全黑名單，直接擋掉不讓連線，跟網路是否可達無關。

**How to apply**：以後幫教練架設本機Flask/Node測試服務時，避開瀏覽器黑名單埠
（常見：1、7、9、11、13、15、17、19、20、21、22、23、25、37、42、43、53、69、77、79、
87、95、101、102、103、104、109、110、111、113、115、117、119、123、135、139、143、
179、389、427、465、512-532、540、548、554、556、563、587、601、636、989、990、993、
995、1719、1720、1723、2049、3659、4045、5060、5061、6000、6566、6665-6669、6697、10080）。
遇到「明明服務跑起來了、curl也通，瀏覽器卻連不上」，先檢查瀏覽器開發者工具的錯誤訊息
是不是`ERR_UNSAFE_PORT`，而不是先假設網路/防火牆問題。對外網址(如透過Cloudflare Tunnel
走443)不受此限制，因為瀏覽器看到的是標準的443/80，不是內部真正跑的埠號。

## 🔒 2026-07-28 已升級成確定性Hook（不只是記憶）

教練指示：「不要每次都要我說『記得跳HTML』，然後每次跳出來就是『無法顯示網頁』…把它寫在
我們的SOP裡面。」單純寫記憶檔不夠強——比照`rule_html_chrome_check.sh`的模式，新增PreToolUse
Bash hook `scripts/unsafe_port_check.sh`：偵測到`open -a "Google Chrome"`/`start chrome`
指向`127.0.0.1:<port>`或`localhost:<port>`且該埠落在黑名單裡，直接exit 2攔截，不讓指令執行，
提醒改用對外網址或換一個安全埠。已註冊進`~/.claude/settings.json`的PreToolUse.Bash matcher，
用4種模擬情境測試（踩雷埠/安全埠/對外網址/非Chrome指令）全部正確才commit。

**上線後立刻自打臉**：第一版regex只用「整段指令含有Chrome開啟語法」+「含有埠號文字」兩個
`grep -q`獨立判斷，結果commit訊息描述這支hook自己的文字內容同時包含這兩段文字，被自己
誤判成真的執行指令，連續攔下自己的commit跟echo說明。修正：仿照`netlify_deploy_guard.sh`
加白名單(git/echo/printf/cat/jq開頭直接放行)，且要求Chrome開啟語法必須在指令起始或
`&&/;/|`分隔符之後、緊接`http(s)://`或`file://`才算數，不能是文字中間字面出現。
commit `cb3ff2c12`。**教訓：寫「偵測指令文字」類型的hook，永遠要用自己描述這支hook的
commit訊息當第一個測試案例**，這種自我描述最容易觸發naive字串比對的假陽性。

Related: [[feedback_html_preview_chrome_only]] [[project_bni_tainan_line_migration_2026-07-23]]
