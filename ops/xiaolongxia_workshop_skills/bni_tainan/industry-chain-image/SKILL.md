---
name: industry-chain-image
description: 教練（大樹教練本人的 LINE）說要某個專業類別／某位夥伴的「產業服務鏈圖」「夥伴圖」時使用。從 BNI 905 項真實專業詞庫驗證的 20 個周邊節點，用 generate_industry_chain.py 的 --nodes 旗標出圖，放到 event.bymyway.com 公開網址後用 LINE 送圖。只服務教練本人，其他人要圖一律回覆「這個功能要請教練開」。本檔與 knowledges/SOP_產業鏈.md 衝突時照 SOP 做。
---

# 誰可以用

只有教練本人（生圖要花 LK888 點數）。其他會員或來賓要圖：回覆「這個功能要請大樹教練開通」，不要自己想辦法做。

# 步驟

1. **挑節點（一定要從 BNI 真實類別挑，湊滿剛好 20 個）**
   先想 20~25 個候選周邊類別，再跑：
   `python3 ~/.openclaw/workspace/scripts/check_industry_chain_names.py --names "候選1,候選2,..."`
   - ✅ 命中：直接用
   - 🟡 有相似真實類別：只有意思真的一樣才換（例如會計師→會計服務可以；化妝品→化妝師不行）
   - ❌ 查無：換成 taxonomy.json 裡語意相近的真實類別
   詞庫本體：`~/.openclaw/workspace/namecard-db/taxonomy.json`（905 項不重複標準專業名稱）。真的湊不滿 20 個才補 AI 推理，交圖時要老實講「幾個是 BNI 真實類別、幾個是 AI 推理」。

2. **出圖**（一次就好，教練沒說「重畫」不要再跑）：
   ```
   python3 ~/.openclaw/workspace/scripts/generate_industry_chain.py \
     --topic "[類別]" --nodes "節點1,節點2,...,節點20" \
     --center "[中心人物外觀]" --held "[手持物件]" --audience "[目標客群]" \
     --publish
   ```
   - 圖片描述由腳本用教練核准的固定範本組成（手繪可愛風、人類角色、全繁體），不要自己手寫中文 prompt（2026-10-01 怡靜分身手寫翻車過）。
   - 節點不是 20 個、不重複、或沒全部命中 taxonomy（exit code 2），腳本會在花 LK888 點數之前擋下並列出最接近的真名。
   - 腳本內建 10 分鐘同主題防重複；24 小時 LK888 閘門也會認得同要求直接回傳舊圖。需要強制重出加 `--force`。
   - `--background`：馬上回覆「已開始製作」，圖做完腳本自己送出，呼叫端不必等。

3. **送圖**：輸出裡有一行「公開網址（LINE送圖用）：https://event.bymyway.com/chain-img/xxxx.png」。
   用 message 工具送：channel=line、target=教練的 LINE ID、media=那個公開網址，再附一行節點來源說明（BNI 真實 vs AI 推理 幾比幾）。
   🔴 不准把 Mac 上的檔案路徑當圖送——LINE 只收公開 https 網址，送本機路徑教練只會看到文字（2026-09-30 就是這樣出包的）。

# 參考

- 完整 SOP：`~/.openclaw/workspace/knowledges/SOP_產業鏈.md`（LINE/Telegram/Hermes 全通道通用，本檔只覆蓋 LINE 這條）
- 平行 skill（含 Branch A 出 prompt 文字、Branch C 字型重製）：`~/.openclaw/agents/main/agent/workshop-skills/industry-chain-prompt/SKILL.md`