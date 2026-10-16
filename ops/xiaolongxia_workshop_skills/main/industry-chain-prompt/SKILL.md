---
name: industry-chain-prompt
description: 教練說「[類別] 夥伴圖」「產業服務鏈」「產業別+專業類別+產業服務鏈」清單 → 只出圖片生成 prompt 文字。教練說「產業鏈 SOP」獨立短句 → 生圖並推 Telegram chat_id 6124913915。共通規則：標題用「[類別] 夥伴圖」（不寫一條龍）、中心必須人類角色（不用動物）、禁簡體與防亂碼條款必加、清單跳號 = 已出過不追問。
---

> 🔴 2026-10-01 更新：出圖（Branch B/D）改用 `generate_industry_chain.py --topic … --nodes 20個 --center … --held … --audience …`，圖片描述由腳本用核准範本自動組成、節點不合格會在扣點前被擋。完整見 `knowledges/SOP_產業鏈.md`「一鍵正式流程」。本檔舊的 `--prompt` 寫法仍可用，但優先用新的。

# 觸發判斷

- 「[類別] 夥伴圖」「產業服務鏈」「產業別 + 專業類別 + 產業服務鏈」清單 → 出 prompt 文字（branch A）
- 「產業鏈 SOP」獨立短句 → 生圖 + 推 Telegram（branch B）
- 「XX 的夥伴圖」+「再一次生成」或「重製」+「之前的有 [問題]」→ 重出單份 prompt（branch C，套 branch A 規則 + 加強化條款）

# Branch A：出 prompt 文字

1. 解析清單，跳過的編號 = 已出過 prompt（不追問、不主動問「1 號是什麼」）。
2. 為每個類別設計 18 個周邊專業類別節點。**節點必須來自 BNI 真實專業類別詞庫（`~/.openclaw/workspace/namecard-db/taxonomy.json`，905 項，每一項都真的有人用這個類別加入過 BNI）**，不准只靠自己的行業常識聯想——教練 09-23 親定：「你自己推理出來的，是用你的知識庫想的；但是BNI這邊的，是它已經明確出現在BNI，代表真的有人用這個專業類別加入過BNI，所以它的說服力和可信度會更強。」
   - 先聯想候選 → **一定要跑**：`python3 ~/.openclaw/workspace/scripts/check_industry_chain_names.py --names "節點1,節點2,..."`
   - ✅命中直接用；🟡有相似真實類別 → 改用真實名稱；❌查無 → 換成詞庫裡語意相近的真實類別
   - 詞庫真的湊不滿 18 個時，才可補 AI 推理節點，並在交付訊息一行註明「幾個是 BNI 真實類別、幾個是 AI 推理」，不准不講
   - 完整規則以 `~/.openclaw/workspace/knowledges/SOP_產業鏈.md` 為準；本檔跟 SOP 不一致時，照 SOP 做
   - 每份 prompt 的節點清單都要不同（不直接抄其他 prompt）。
3. 套模板產出 prompt，每段以三個反引號包裹：
   ```
   我需要做一張產業服務鏈，要用手繪可愛風格做出來。中心是「[類別]」的人類角色插畫（男性或女性皆可，禁止使用動物、擬人化動物或卡通動物造型），手持[代表性物件]。標題：[類別] 夥伴圖。為[目標客群]，提供從[第一項]到[最後一項]的完整夥伴支援。周邊環繞以下 18 個專業類別節點，每個節點配精緻手繪 icon：[節點1]、[節點2]⋯[節點18]。所有文字必須完全正確、清晰可讀，每個文字都必須是繁體中文（台灣正體字），禁止使用簡體字、簡體字形、簡體偏旁、簡體異體字、或任何簡體中文變體，絕對不能出現無法顯示的亂碼字、缺漏字或方框字。
   ```
4. 用 Telegram message 送出，每段 ≤ 6 個 prompt（避免訊息被截斷）。若清單 > 6 項，分段送並在結尾列訊息編號對照表。
5. 結尾提醒教練：丟去生圖測試，若有字符渲染失敗，把「是哪個字 + 出現什麼狀況」告訴我，立刻 debug。

# Branch B：生圖推 Telegram

1. 確認 prompt 完整（含 18 個節點清單），且節點已照 Branch A 第 2 步跑過 BNI 詞庫比對——沒跑過不准生圖（生圖要花 lk888 點數，節點錯了等於白花）。
2. 呼叫 `python3 ~/.openclaw/workspace/scripts/generate_industry_chain.py --prompt "<完整 prompt>" --telegram-chat-id 6124913915 --caption "<類別> 夥伴圖"`，yieldMs=120000。
3. 看到「已推送 Telegram」就結束，圖片會自動送出。
4. 不要重複呼叫：GPT Image 2 有 5-10% 機率生錯字，教練已表態「不求精準及完美，因為額度有限」，除非教練明確說「重生一張」，否則一次就好。

# Branch D：在 LINE 上要圖（2026-09-30 起開放）

教練在 LINE 說要產業鏈的「圖」（不是只要 prompt 文字）時：

1. 節點照 Branch A 第 2 步跑 BNI 詞庫比對，組好完整 prompt。
2. 呼叫 `python3 ~/.openclaw/workspace/scripts/generate_industry_chain.py --prompt "<完整 prompt>" --topic "<類別>" --publish`（不加 --telegram-chat-id）。
3. 輸出會有一行「公開網址（LINE送圖用）：https://event.bymyway.com/chain-img/xxxx.png」。
4. 用 message 工具送圖：channel=line、target=教練的 LINE ID、media=那個公開網址，文字附一行「幾個是 BNI 真實類別、幾個是 AI 推理」。
5. 🔴 不准把 Mac 上的檔案路徑直接當圖送——LINE 只收公開 https 網址，送本機路徑會失敗，教練只會看到文字。
6. 只有教練本人（或教練指定的帳號）要圖才做：生圖會花 LK888 點數；其他人要，回覆「這個功能要請教練開」。

# Branch C：重製（字符渲染失敗）

教練回報「[某字]沒顯示成功」「[某字]有亂碼」時：

1. 確認失敗的具體字（從 prompt 內容找）。
2. 用「字符結構」提示法重寫——在防呆條款後面加一句：「特別是標題中的「X」這個字，必須完整呈現「部首 A」加「部件 B」的標準字形結構（不能簡化、不能省略、不能變成方框或亂碼）。」
   - 範例：灸 → 「火部首加九」
   - 範例：睫 → 「目部旁加疊字結構」
3. 重出整份 prompt 送 Telegram，標註「🔁 重製版」。
4. 仍失敗：把該字改成更口語的同義詞（例如 電子針灸儀 → 電子針療儀、或拆開寫）。同義詞若會改變原意，先跟教練確認。

# 參考

- USER.md「教練親定視覺規則（產業服務鏈圖 SOP 專用）」段（不寫一條龍、人類中心規則出處）
- USER.md「給編號清單時跳號規則」段（跳號不追問規則出處）
- 生圖腳本：`~/.openclaw/workspace/scripts/generate_industry_chain.py`
- 教練 Telegram chat_id：6124913915（推生圖用）
- 已知防呆強化範例：2026-09-20 霧眉重製（加「絕對不能出現無法顯示的亂碼字、缺漏字或方框字」）、2026-09-20 電子針灸儀（灸 → 火部首加九）
