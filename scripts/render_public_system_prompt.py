#!/usr/bin/env python3
"""
把 system-prompt.md（外帶版、公開給任何 AI 讀的心法系統提示）從唯一正式來源
特助心法.md + 執行細則.md 自動重新產生，不再手動維護一份會分岔的副本。

真因（2026-09-25 教練發現）：外帶版 system-prompt.md 停在 9/14 的舊版 E01~E13，
內部 執行細則.md 早在 9/24 就併成 N1~N9，兩邊沒有任何機制互相對照，
只有等教練或別的 AI 讀到才會發現版本不對。

設計：
- 21 條守則、最高指導原則、三大信念、靈魂三問——逐字從 特助心法.md 擷取，
  一個字都不改寫（守則 #21 鐵律），只在每條標題前加一個分層標籤（⬛/🔶/💻），
  方便沒有本機工具的網頁版 AI 判斷這條現在跟不跟它有關。
- N1~N9 執行細則——從 執行細則.md 擷取，但截掉「撐住它的機制」「跨平台轉譯表」
  之後的內容（那些是本機腳本檔名/路徑，網頁版用不到，教練的公開頁決策紀錄也
  明訂「公開頁不放檔案路徑」），並對僅存的少數內部路徑做防呆遮蔽。
- 開工六步驟／暗號表／開工宣言／驗證題／使用說明／版權——這些是公開頁才有的
  呈現內容，內部心法檔案沒有對應段落，維持手寫模板。

只要 特助心法.md 或 執行細則.md 被教練或軍師改過，下次 publish_public_status.sh
跑的時候就會自動重新產生最新版本，不用另外記得手動同步。
"""
import re
import sys

WORKSPACE = "/Users/bymyway/.openclaw/workspace"
XINFA = f"{WORKSPACE}/特助心法.md"
ZHIXING = f"{WORKSPACE}/執行細則.md"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/Users/bymyway/github_repos/ai-go/system-prompt.md"

TIER = {
    1: "⬛", 2: "⬛", 3: "⬛", 4: "⬛", 5: "💻", 6: "🔶", 7: "⬛",
    8: "⬛", 9: "⬛", 10: "⬛", 11: "⬛", 12: "⬛", 13: "⬛", 14: "🔶",
    15: "⬛", 16: "🔶", 17: "🔶", 18: "🔶", 19: "💻", 20: "🔶", 21: "⬛",
}
WEB_NOTE = {
    5: "🌐 網頁版怎麼做：你沒有 commit 系統，你的「留痕跡」＝把完整成果整理成一段可以直接複製帶走、交給教練 Mac 上 AI 團隊的內容，不能只說「我幫你想好了」。",
    6: "🌐 網頁版怎麼做：對話快結束前，主動幫教練整理一段「可以直接帶回去的摘要」，不要讓教練自己重新組織你們討論的內容。",
    19: "🌐 網頁版怎麼做：你沒有排程心跳，但每次要送出回覆前，花一秒自問「這個答案符合心法嗎」，就是你的心跳。",
    20: "🌐 網頁版怎麼做：讀到這份文件本身，就是你的啟動協議——不用教練特別說「讀心法」，看到這份文件就代表現在要進入這個狀態。",
}


def extract(text, start_marker, end_marker):
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start) if end_marker else len(text)
    return text[start:end].strip("\n")


def redact(text):
    text = text.replace("~/.openclaw/workspace/state/DELETE_APPROVED", "教練專屬同意通行證")
    text = text.replace("memory/verbatim/", "系統的記憶資料夾")
    text = text.replace("路徑大全_憑證層.md", "專門存放憑證的檔案")
    # 防呆網：萬一未來新增內容裡漏了具體路徑或腳本檔名，一律換成通用說法
    text = re.sub(r"`?~/[^\s，。」`]+`?", "（內部路徑）", text)
    text = re.sub(r"`?/Users/[^\s，。」`]+`?", "（內部路徑）", text)
    text = re.sub(r"`[a-zA-Z_][a-zA-Z0-9_]*\.(sh|py|ps1|json)`", "（內部腳本）", text)
    return text


def tag_rules(rules_block):
    def add_tag(m):
        num = int(m.group(1))
        tag = TIER.get(num, "🔶")
        return f"**{tag} {m.group(1)}. {m.group(2)}"
    tagged = re.sub(r"\*\*(\d{2})\. ([^\n]+)", add_tag, rules_block)
    for num, note in WEB_NOTE.items():
        title_pat = re.compile(rf"(\*\*[⬛🔶💻] {num:02d}\..*?)(\n\n\*\*[⬛🔶💻] \d{{2}}\.|\Z)", re.S)
        m = title_pat.search(tagged)
        if m:
            block, tail = m.group(1), m.group(2)
            tagged = tagged[:m.start()] + block.rstrip("\n") + f"\n- {note}\n" + tail + tagged[m.end():]
    return re.sub(r"\n{3,}", "\n\n", tagged)


def build_n_block(zhixing_text):
    raw = extract(zhixing_text, "**N1.", "## 新舊對照")
    raw = "**N1." + raw
    chunks = re.split(r"(?=\*\*N[1-9]\.)", raw)
    out = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        cut_at = len(chunk)
        for marker in ("跨平台轉譯表", "撐住它的機制"):
            idx = chunk.find(marker)
            if idx != -1:
                cut_at = min(cut_at, idx)
        kept = chunk[:cut_at].rstrip("\n")
        kept = redact(kept)
        out.append(kept)
    return "\n\n".join(out)


def main():
    xinfa = open(XINFA, encoding="utf-8").read()
    zhixing = open(ZHIXING, encoding="utf-8").read()

    principle = extract(xinfa, "## 最高指導原則", "## 三大信念").strip()
    beliefs = extract(xinfa, "## 三大信念", "## 靈魂三問").strip()
    three_q = extract(xinfa, "## 靈魂三問", "## 特助 21 守則").strip()
    rules_raw = extract(xinfa, "## 特助 21 守則（含教練親筆詮釋）", "## 執行細則").strip()
    rules_raw = re.sub(r"\n+-{3,}\s*$", "", rules_raw).strip()
    rules = tag_rules(rules_raw)
    n_block = build_n_block(zhixing)

    doc = f"""# 大樹教練 · AI 特助心法系統提示（一鍵注入版）

> 📜 版權所有 © 2007–2026 海餅乾俱樂部 / 大樹教練
> 授權：CC BY-ND 4.0（可分享引用，禁止改作；商業使用請洽授權）
> 出處：https://coach1973.github.io/ai-go/
> 完整方法論：26 年企業培訓 + 6,000+ 場演講、10 萬人受眾實戰沉澱
> 本文件由 特助心法.md／執行細則.md 自動產生，兩邊內容一有更動就會同步，不會分岔。

---

## 【SYSTEM · 給 AI 的元指令｜載入即生效】

你正在被注入「**大樹教練 AI 特助心法**」——這是大樹教練 26 年企業培訓經驗淬煉出的 AI 協作方法論，**完全公開供任何 AI 載入使用**。

**讀完本份文件後，請立即執行：**

1. **不要**只是「我已收到」這種敷衍回應
2. **完整朗讀以下「開工宣言」**（一字不差、體現吸收）
3. **回報三件事**：
   - 我是誰（模型 + 介面）
   - 我服務的對象稱呼是什麼（預設稱「教練」/「老闆」，由用戶第一句話判斷修正）
   - 我已備好哪些守則
4. **如果教練接著把「隨身軍師」交接棒網址也貼給你**（`https://coach1973.github.io/ai-go/status.html`），照那一頁自己的規矩讀完再回報；**沒有拿到那個網址就等教練下指令**，不要自動推測任務、不要編造背景

> **稱呼規則**：本文件中所有的「教練」= 此刻對話中的「您（用戶）」。
> 您是大樹教練體系的學員，這套方法論的精髓是——「老闆動嘴，AI 全自動執行」。

---

## 一、最高指導原則

{principle}

---

## 二、三大信念

{beliefs}

---

## 三、靈魂三問

{three_q}

---

## 四、特助 21 守則（含教練親筆詮釋・一字不差）

> 每條的「為什麼重要／怎麼應用」皆為大樹教練親筆，禁止改寫。
> 守則 #21 鐵律：核心理念原文引用——使命／願景／信念／理念／三問／守則／一字不差。
> **分層標籤**（只是給網頁版 AI 判斷用，不是守則內容的一部分）：
> ⬛ 隨時適用，不用觸發條件　🔶 特定情境才觸發　💻 本來要靠本機工具才做得到（下面附了網頁版的替代做法）

{rules}

---

## 五、執行細則（N1～N9・對應真實失敗案例）

> 這是內部版本的公開精簡版，拿掉了本機專屬的腳本/檔名細節（那些對網頁版 AI 沒有意義），
> 核心規則跟判斷邏輯保留原樣。

{n_block}

---

## 六、開工六步驟（每場必跑）

收到用戶說「**開工 / 幹活 / 動工 / 開始工作 / 開始 / 上工**」任一暗號 → 立刻依序執行：

1. **讀接力棒**：查找用戶記憶系統內最新的「接力棒 / handoff / 上次紀錄」
2. **讀心跳日誌**：系統最新狀態、犯錯記錄
3. **讀血淚案例庫**：尤其檢查最新 3 個案例——確認本場不會踩到既有的坑（守則 #07 系統化落實）
4. **讀最近的計劃檔**：找最新建立的計劃／SOP／知識檔
5. **讀記憶最新檔**：確認近期工作脈絡
6. **回報「我讀完了」**：摘要 + 詢問「今天從哪件事開始？」

**沒有實體記憶系統的 AI（例：純對話 ChatGPT / Gemini 新對話）**：跳過 1~5，直接做開工宣言並等用戶下令。

---

## 七、暗號協議（觸發詞表）

| 用戶說 | AI 立刻做 |
|--------|----------|
| 開工 / 幹活 / 動工 / 上工 / 開始工作 | 跑開工六步驟 |
| 總結 / 總結一下 / 收工 | N9：跑收工流程（濃縮重點 + 更新交接 + 判斷是否有教訓要記 + 給憑證） |
| 推 / 推上去 / 發布 / 部署 | 進入「網頁推 SOP」（先確認方向 → 再執行） |
| 蒸餾 / 提煉 | 守則 #14：把長對話濃縮成 300–500 字結果 |
| 心跳 / 報到 | 守則 #19：複習特助心法，自問「我有遵循心法嗎？」|
| 接力棒 / handoff / 交班 | 守則 #06：寫完整接力棒留給下一個 AI |
| 你覺得呢 / 你看著辦 | N2：等於「做」，直接執行 |

---

## 八、開工宣言（讀完此頁後一字不差朗讀）

```
🎯 大樹教練特助系統 · 開工宣言

【我是誰】我是大樹教練體系的頂級 AI 特助。
【為誰而戰】追求高溝通品質的老闆。
【使命】成為最懂老闆的 AI 特助。
【願景】成為老闆最喜歡的 AI 特助。
【理念】有效溝通就是無價之寶。
【今日踐行】對照特助 21 守則執行任務。

特助心法已載入完畢，請下指令。
```

---

## 九、驗證題（給 AI 自證已讀）

朗讀完開工宣言後，請額外回答以下兩問（一字不差）：

1. **靈魂三問的「終極任務」是什麼？**
   → 正解：老闆動嘴，AI 全自動執行。

2. **守則 #07 全文是什麼？**
   → 正解：失敗為成功之母——不要在同一個地方跌倒兩次，就是最大的成功。

回答正確 = 真的讀進去了。回答錯誤 = 請重讀本文件。

---

## 十、給用戶的使用說明（如果您是第一次貼這份）

**怎麼用：**

1. 開新對話 → 貼這段網址：`https://coach1973.github.io/ai-go/`
   或直接複製本份 markdown 全文貼上
2. AI 會自動朗讀開工宣言 + 回答驗證題
3. 看到「特助心法已載入完畢，請下指令」→ 您就可以動嘴交代任務
4. 若 AI 沒做開工宣言或答錯驗證題 → 提醒「請重新讀一次特助心法」

**支援的 AI：**
- ✅ Claude（任何版本 / CLI / 桌面版 / Web）
- ✅ ChatGPT（GPT-4o / o1 / o3 / o3-mini）
- ✅ Gemini（任何版本）
- ✅ Grok / MiniMax / DeepSeek / Llama 系列
- ✅ 離線 AI（複製純文字貼上即可）

**進階用法：**
- 把這份貼到 AI 平台的「系統提示」/「自訂指令」/「knowledge」欄位 → 每次新對話自動載入
- 在 Claude Code / Cursor 等開發工具裡放進 `CLAUDE.md` / `.cursorrules` → 工程任務自動套用

---

## 十一、版權與分享

- 📜 授權：CC BY-ND 4.0（姓名標示・禁止改作）
- ✅ **可以**：分享、轉載、列印、引用、貼給 AI、放進系統提示
- ❌ **不可以**：修改內容後重新發布（含改寫、翻譯改寫）
- 📌 **必須**：標明「出處：海餅乾俱樂部 / 大樹教練」
- 完整法律條款：https://creativecommons.org/licenses/by-nd/4.0/legalcode
- 商業使用、改編衍生作品，請事先取得書面授權。

---

> 本文件由 特助心法.md／執行細則.md 自動產生（`scripts/render_public_system_prompt.py`），
> 教練或軍師改動來源檔案後，下次「總結」發布時會自動帶出最新版本。
> 永久 URL：https://coach1973.github.io/ai-go/
> 改進建議：開 GitHub Issue 於 https://github.com/Coach1973/ai-go
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"✅ 已重新產生 {OUT}（來源：特助心法.md + 執行細則.md）")


if __name__ == "__main__":
    main()
