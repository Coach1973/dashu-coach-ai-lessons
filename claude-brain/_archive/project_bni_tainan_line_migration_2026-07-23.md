---
name: project-bni-tainan-line-migration-2026-07-23
description: BNI大台南小幫手LINE機器人從Coze搬到小龍蝦本機+MiniMax-M3，webhook尚待教練切換
metadata: 
  node_type: memory
  type: project
  originSessionId: 067a8574-730c-47d8-8983-64b8999cb011
  modified: 2026-07-22T18:18:47.543Z
---

教練原本用Coze串接「BNI大台南小幫手」LINE官方帳號（Channel ID 2008741664），2026-07-23決定搬到小龍蝦（OpenClaw）本機、換用MiniMax-M3，理由：不想被Coze的「User message billing」按訊息計費卡住，且相信本機小龍蝦能做出比VPS版更多功能。

**Why：** 教練親口拍板三件事——①LINE官方帳號本身不換，繼續用現有的；②一定要跑在這台Mac（不是Hermes VPS），因為期待本機能做出更多功能；③既然在本機，模型直接用MiniMax-M3（教練說比GPT-4o mini好）。其他技術細節全權交給AI決定。

**已完成（commit `bf560a96`，外層repo已push）：**
- 新增OpenClaw agent `bni_tainan`（workspace `~/.openclaw/agents/bni_tainan/`），人設完整搬自Coze的「大台南小幫手總指令.txt」+3份知識庫（Podcast菁華錄/經典PODCAST/產業專業表），存在`AGENTS.md`+`knowledge/`
- LINE帳號用`openclaw channels add --channel line --account bni_tainan`註冊，token/secret存`credentials/line-bni_tainan-*.txt`
- 用`openclaw agents bind`把`line:bni_tainan`綁到這個agent；教練個人LINE小龍蝦（default帳號）完全沒被動到
- 本機測試3題（引薦單必填欄位/DnA防幻覺guardrail/曜董是誰）回答品質、格式、案例引用皆正確

**副產品（意外發現的真bug，非本次引入）：** LINE channel plugin從2026.6.1外掛啟用機制上線後就沒被宣告進`plugins.entries`，導致`/line/webhook`一直404——教練個人LINE小龍蝦這條線可能已經silent斷線一段時間（cloudflared tunnel本身活著，但gateway沒mount這條路徑）。已補上`plugins.entries.line={enabled:true}`修復，同一次commit。見[[reference_xiaolongxia_line_tunnel_cloudflared]]。

**尚未做（卡在教練決定）：**
- BNI新系統已就位但**沒上線**——Coze那邊的舊webhook還在正常服務會員，兩套系統目前並存
- 要正式切換，需教練登入LINE Developers Console，把「BNI大台南小幫手」那個帳號的Webhook URL從Coze的換成跟教練個人LINE小龍蝦一樣的網址（同一條cloudflared tunnel，OpenClaw靠webhook payload的destination欄位自動分流不同帳號，不需要新開一條tunnel）
- 這一步刻意沒有自己動手——LINE webhook屬於「帳號設定變更」且會立刻影響BNI大台南會員正在用的真實LINE通道，即使教練已授權「全部去做」，這個特定動作仍在切換前找教練做最後確認

**How to apply：** 下次教練問「BNI那個LINE弄好了嗎」或提到「切換」，先確認上面待辦有沒有被執行；如果教練說「切了」，記得回頭關心一下Coze那邊的舊機器人要不要停用（教練沒交代前不要主動關）。
