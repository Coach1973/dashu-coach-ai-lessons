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

MODEL = None  # 動態從extract模組讀，避免重複讀環境變數

CHAIN_MATCH_PROMPT = """你是產業鏈媒合顧問。你的任務是判斷一張新收到的名片，適合被安插進現有的產業鏈，
還是應該建議組成一條全新的產業鏈。

「產業鏈」的定義：以某個核心需求或客群為中心，把互補的專業角色組合起來，一起為同一位客戶服務。
例如「珠寶業」核心，可以延伸出：珠寶鑑定師、財富傳承律師、保險顧問、藝術品經紀、公關活動策展
等角色，這些角色彼此不是同一個行業，但服務的是同一種客戶的不同需求面向。

輸入會給你：
1. 這張新名片的資料（姓名/公司/職稱/標準分類/標語）
2. 目前資料庫裡「還缺人補位」的產業鏈角色清單（可能是空的，代表目前還沒有任何產業鏈）

請判斷並只輸出一個JSON物件，不要有其他文字、不要用markdown code block包起來：

情況A - 這張名片剛好能補進某個現有缺口：
{"action": "fill_gap", "chain_id": 缺口所屬的產業鏈id(數字), "role_name": "缺口的角色名稱(照抄)"}

情況B - 沒有合適的現有缺口，建議組一條新產業鏈：
{"action": "new_chain", "chain_name": "產業鏈名稱(4到10字，具體描述這條鏈服務誰、圍繞什麼核心需求)",
 "core_theme": "一句話說明這條產業鏈為誰服務、解決什麼需求",
 "this_card_role": "這張名片在這條鏈裡扮演的角色名稱",
 "suggested_gaps": ["建議再補2到4個互補角色名稱，這些角色目前還沒有人，屬於待招募缺口"]}

情況C - 這張名片的專業太籠統或太個人化，不適合放進任何產業鏈：
{"action": "skip", "reason": "簡短說明為什麼不適合"}

判斷原則：
- 優先選情況A，只有在真的沒有任何現有缺口貼合這張名片的專業時，才選情況B
- 產業鏈要有明確的服務對象或核心需求，不能只是把同行業的人湊在一起
- suggested_gaps的角色要跟this_card_role互補、不重複，共同能服務同一種客戶
- 姓名/公司/職稱完全空白、只剩下錯誤訊息的名片，一律選情況C
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

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=CHAIN_MATCH_PROMPT,
        messages=[{"role": "user", "content": [{"type": "text", "text": user_content}]}],
    )
    raw_text = "".join(b.text for b in message.content if getattr(b, "type", None) == "text")
    result = _extract_json(raw_text)

    action = result.get("action")
    if action == "fill_gap":
        chain_id = result.get("chain_id")
        role_name = result.get("role_name")
        gap_row = conn.execute(
            "SELECT id FROM chain_members WHERE chain_id = ? AND role_name = ? AND is_gap = 1",
            (chain_id, role_name),
        ).fetchone()
        if gap_row is None:
            # AI給的chain_id/role_name對不上真實缺口(幻覺)，降級為new_chain處理
            result = {
                "action": "new_chain",
                "chain_name": f"{card_info['standard_category'] or '未分類'}相關產業鏈",
                "core_theme": "AI媒合回應對不上實際缺口，先建立單點產業鏈待後續補充",
                "this_card_role": card_info["standard_category"] or card_info["title"] or "成員",
                "suggested_gaps": [],
            }
            action = "new_chain"
        else:
            conn.execute(
                "UPDATE chain_members SET card_id = ?, is_gap = 0, match_reason = ? WHERE id = ?",
                (card_id, "AI媒合：補進既有缺口", gap_row["id"]),
            )
            conn.commit()
            return {"action": "fill_gap", "chain_id": chain_id, "role_name": role_name}

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
