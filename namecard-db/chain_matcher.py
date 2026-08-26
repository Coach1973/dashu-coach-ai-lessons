"""
產業鏈動態媒合：一張名片收錄成功後，判斷它適合補進哪條產業鏈的哪個位置，
或者建議組成一條全新的產業鏈。

「產業鏈」不是預先寫死的固定清單，而是隨名片收錄逐漸長出來的資料——
這符合教練的構想：大家一起貢獻名片，AI從中動態長出精準的媒合建議，
不是套一套人工事先畫好的模板。

參考素材（教練提供的兩張範例圖，只借鏡設計邏輯，不照抄具體內容）：
- 「真誠產業圖」：以九宮格呈現多條產業鏈，每條鏈列出幾個互補角色，
  已有真人的標姓名、缺口標「待招募」
- 「珠寶業產業鍊」：以核心產業為圓心，一圈圈擴散出互補服務（財富傳承／
  藝術收藏／公關媒體），示範「一個產業能長出一整條服務生態」

核心邏輯：每條產業鏈= 一個核心需求/客群 + 幾個互補專業角色。
新名片進來時，優先嘗試補進現有缺口；沒有合適缺口才建議新開一條產業鏈。
"""
import json
import re

import anthropic

from extract import _TAXONOMY_BLOCK

MODEL = None  # 動態從extract模組讀，避免重複讀環境變數

CHAIN_MATCH_PROMPT = f"""你是產業鏈媒合顧問。你的任務是判斷一張新收到的名片，適合被安插進現有的產業鏈，
還是應該建議組成一條全新的產業鏈。

「產業鏈」的定義（教練親自定義，仿BNI九宮格）：以這張名片的核心專業為中心，往外排出一整圈互補角色，
組成一張完整的九宮格產業鏈地圖——上下左右加中心自己，至少要有8個其他角色圍繞著這張名片，
一起服務同一種客群的不同需求面向。例如「珠寶業」核心可以完整長成：珠寶鑑定師、金工修復師、
裸鑽貿易商、產物保險顧問、家族辦公室、遺產律師、稅務顧問、高端當舖精品融資、海外資產配置顧問、
藝術品經紀、拍賣策展人、高級鐘錶經銷、整體造型顧問、彩妝美學師、公關活動策展、商業攝影、
短影音自媒體行銷、私廚無菜單料理、進口名車經銷、雪茄威士忌俱樂部…這種規模才叫完整的產業鏈，
不是隨便湊兩三個相關的人就算數。

輸入會給你：
1. 這張新名片的資料（姓名/公司/職稱/標準分類/標語）
2. 目前資料庫裡「還缺人補位」的產業鏈角色清單（可能是空的，代表目前還沒有任何產業鏈）
3. 下方【標準分類詞庫】：BNI官方533項+大台南南區682+產業全生態戰略總庫整合而成的905個
   標準專業名稱，suggested_gaps的角色要優先從這裡面選、逐字照抄，確保跟名片辨識時用的
   是同一套詞彙，日後才配得上、比對得到

請判斷並只輸出一個JSON物件，不要有其他文字、不要用markdown code block包起來：

情況A - 這張名片剛好能補進某個現有缺口：
{{"action": "fill_gap", "chain_id": 缺口所屬的產業鏈id(數字), "role_name": "缺口的角色名稱(照抄)"}}

情況B - 沒有合適的現有缺口，建議組一條新產業鏈：
{{"action": "new_chain", "chain_name": "產業鏈名稱(4到10字，具體描述這條鏈服務誰、圍繞什麼核心需求)",
 "core_theme": "一句話說明這條產業鏈為誰服務、解決什麼需求",
 "this_card_role": "這張名片在這條鏈裡扮演的角色名稱",
 "suggested_gaps": ["這是硬性規定：至少要列8個、可以更多不能更少的互補角色名稱，
 這些角色目前還沒有人，屬於待招募缺口，彼此不重複、都要跟this_card_role圍繞同一種
 客群服務需求，盡量從下方標準分類詞庫挑選貼切的專業名稱"]}}

情況C - 這張名片的專業太籠統或太個人化，不適合放進任何產業鏈：
{{"action": "skip", "reason": "簡短說明為什麼不適合"}}

判斷原則：
- 優先選情況A，只有在真的沒有任何現有缺口貼合這張名片的專業時，才選情況B
- 產業鏈要有明確的服務對象或核心需求，不能只是把同行業的人湊在一起
- suggested_gaps「至少8個」是硬性要求，少於8個視為不合格答案，你必須認真發想到8個以上
- 姓名/公司/職稱完全空白、只剩下錯誤訊息的名片，一律選情況C

【標準分類詞庫】：
{_TAXONOMY_BLOCK}
"""


def _extract_json(raw_text: str) -> dict:
    candidates = [raw_text]
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1:
        candidates.append(raw_text[start : end + 1])
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return {"action": "skip", "reason": "AI回應無法解析為JSON"}


def match_card_to_chain(conn, client: anthropic.Anthropic, card_id: int, model: str) -> dict:
    """回傳處理結果dict，供呼叫端記錄log用：
    {"action": "fill_gap"|"new_chain"|"skip", ...}
    """
    import db

    card = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    if card is None or card["status"] == "failed":
        return {"action": "skip", "reason": "名片辨識失敗，無資料可媒合"}
    if not card["standard_category"] and not card["category"]:
        return {"action": "skip", "reason": "沒有可判斷的專業分類"}

    card_info = {
        "name": card["name"],
        "company": card["company"],
        "title": card["title"],
        "standard_category": card["standard_category"] or card["category"],
        "tagline": card["tagline"],
    }

    gaps = conn.execute(
        """SELECT cm.id AS member_id, cm.chain_id, cm.role_name, ic.name AS chain_name, ic.core_theme
           FROM chain_members cm JOIN industry_chains ic ON ic.id = cm.chain_id
           WHERE cm.is_gap = 1"""
    ).fetchall()
    gap_list = [
        {
            "chain_id": g["chain_id"],
            "chain_name": g["chain_name"],
            "core_theme": g["core_theme"],
            "role_name": g["role_name"],
        }
        for g in gaps
    ]

    user_content = (
        "這張新名片的資料：\n" + json.dumps(card_info, ensure_ascii=False, indent=2)
        + "\n\n目前資料庫裡還缺人補位的產業鏈角色清單：\n"
        + (json.dumps(gap_list, ensure_ascii=False, indent=2) if gap_list else "（目前沒有任何缺口，資料庫裡還沒有產業鏈）")
    )

    def _call_ai(prompt_content: str) -> dict:
        message = client.messages.create(
            model=model,
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": CHAIN_MATCH_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt_content}]}],
        )
        raw_text = "".join(b.text for b in message.content if getattr(b, "type", None) == "text")
        return _extract_json(raw_text)

    result = _call_ai(user_content)
    action = result.get("action")

    if action == "fill_gap":
        chain_id = result.get("chain_id")
        role_name = result.get("role_name")
        gap_row = conn.execute(
            "SELECT id FROM chain_members WHERE chain_id = ? AND role_name = ? AND is_gap = 1",
            (chain_id, role_name),
        ).fetchone()
        if gap_row is None:
            # AI給的chain_id/role_name對不上真實缺口(幻覺)——明確請AI改走new_chain
            # 重新設計一條完整的產業鏈，而不是直接生一個空殼(教練要求至少8個角色)
            retry_content = user_content + (
                "\n\n（上一次你判斷這張名片能補進某個現有缺口，但比對不到真實資料，"
                "這次請改走情況B(new_chain)，針對這張名片重新設計一條完整的新產業鏈，"
                "suggested_gaps務必列滿至少8個互補角色）"
            )
            result = _call_ai(retry_content)
            action = result.get("action")
        else:
            conn.execute(
                "UPDATE chain_members SET card_id = ?, is_gap = 0, match_reason = ? WHERE id = ?",
                (card_id, "AI媒合：補進既有缺口", gap_row["id"]),
            )
            conn.commit()
            return {"action": "fill_gap", "chain_id": chain_id, "role_name": role_name}

    # LLM有隨機性，偶爾new_chain會漏給suggested_gaps(教練要求至少8個角色)，重試一次補救
    if action == "new_chain" and len(result.get("suggested_gaps") or []) < 7:
        retry_content = user_content + (
            "\n\n（重要提醒：上一次回應的suggested_gaps數量不足，這次務必列滿至少8個"
            "互補角色，這是硬性規定，不可省略）"
        )
        retry_result = _call_ai(retry_content)
        if retry_result.get("action") == "new_chain" and len(
            retry_result.get("suggested_gaps") or []
        ) > len(result.get("suggested_gaps") or []):
            result = retry_result
            action = "new_chain"

    if action == "new_chain":
        chain_name = (result.get("chain_name") or "未命名產業鏈").strip()
        core_theme = result.get("core_theme") or ""
        this_role = (result.get("this_card_role") or card_info["standard_category"] or "成員").strip()
        gaps_suggested = result.get("suggested_gaps") or []

        existing = db.find_chain_by_name(conn, chain_name)
        chain_id = existing["id"] if existing else db.create_chain(conn, chain_name, core_theme)

        db.add_chain_member(conn, chain_id, card_id, this_role, is_gap=False, match_reason="AI媒合：新建產業鏈")
        for gap_role in gaps_suggested:
            gap_role = str(gap_role).strip()
            if gap_role:
                db.add_chain_member(conn, chain_id, None, gap_role, is_gap=True, match_reason="AI建議缺口")
        return {"action": "new_chain", "chain_id": chain_id, "chain_name": chain_name, "role": this_role}

    return {"action": "skip", "reason": result.get("reason", "未知原因")}
