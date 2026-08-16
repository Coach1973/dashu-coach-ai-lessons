# 專案卡：LINE 三帳號系統（OpenClaw gateway）

- **設定檔**：`~/.openclaw/openclaw.json`（channels.line）——只跑在這台 Mac mini 單一 gateway，**不需要三機同步**
- **三帳號**：
  1. **龍蝦小助教**（default，@268dptjc）→ 綁 main agent，教練個人+群組已開放
  2. **BNI大台南小幫手**（bni_tainan）→ 服務 BNI 會員，有主動提醒 hook
  3. **教練都在想什麼**（jiaolian_thoughts）→ 121位好友，46萬字知識庫+FTS5檢索
- **🔴 案例56 鐵坑**：LINE 外掛對 accountId="default" **完全不讀** `accounts.default` 底下的 dmPolicy/groupPolicy——default 帳號的行為設定必須放在 `channels.line` 最外層
- **🔴 sessionKey 鐵坑**：default 帳號的 sessionKey 是 `agent:main:...`（不是 default），寫 hook 判斷帳號要正規化
- **命脈**：cloudflared 專線（小龍蝦專線）= LINE webhook 唯一入口，**絕對不能關**；LINE 沒反應先查 tunnel 再查 gateway
- **權限**：`tools.toolsBySender` 教練兩個 LINE ID 白名單全權限；⚠️ cron 觸發的 turn 沒有 senderId 會落到 `"*"` 規則，agent 層級萬用 deny 會誤傷 cron（案例56）
- **教練身分**：本尊 `U895a0ad8...`＋贏家思路 `U168903487...`（people.md 有完整名冊）
- **診斷神器**：合成帶正確簽章的假 webhook 打 `localhost:18789/line/webhook`＋短暫開 debug log
