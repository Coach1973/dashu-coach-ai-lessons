"""
產業鏈媒合：找出名片資料庫裡「誰跟誰的產業有上下游／互轉介關係」。

做法（避免對每一對名片都呼叫AI，2000張名片會有近200萬組合，太貴太慢）：
1. 先把資料庫裡所有名片的「產業類別」去重，變成一份很短的類別清單（通常幾十到幾百個）
2. 只呼叫一次AI，請AI從這份類別清單裡，判斷哪些類別彼此是上下游或互轉介關係
3. 再用類別關係，回頭把屬於這些類別的名片兩兩配對寫進 matches 表

用法：python match.py
"""
import itertools
import json
import os

import anthropic

import db

MODEL = os.environ.get("NAMECARD_MODEL", "MiniMax-M3")

MATCH_PROMPT = """以下是一份商務名片資料庫裡出現過的產業類別清單（每行一個）：

{categories}

請你判斷這些類別之間，哪些組合在「商務轉介／異業合作」的情境下特別值得互相認識——
可能是上下游關係（例如原料商跟加工廠、設計師跟工班），也可能是常見的異業合作圈
（例如保險、會計、地政士、銀行貸款常互轉介客戶）。

只挑「真的有業務關聯、值得主動介紹認識」的類別配對，不要為了湊數硬掰。
不確定、關聯薄弱的就不要列。同一個類別配對只列一次。

只輸出一個 JSON 陣列，不要有其他文字，格式：
[{{"a": "類別A", "b": "類別B", "reason": "一句話說明為什麼值得互相認識"}}]
"""


def _pair_key(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def build_category_relationships(categories: list[str], client: anthropic.Anthropic) -> list[dict]:
    if len(categories) < 2:
        return []
    prompt = MATCH_PROMPT.format(categories="\n".join(categories))
    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = "".join(
        block.text for block in message.content if getattr(block, "type", None) == "text"
    )
    start, end = raw_text.find("["), raw_text.rfind("]")
    if start == -1 or end == -1:
        print("⚠️ AI沒有回傳可解析的JSON，略過本次媒合")
        return []
    try:
        return json.loads(raw_text[start : end + 1])
    except json.JSONDecodeError:
        print("⚠️ JSON解析失敗，略過本次媒合")
        return []


def main() -> None:
    conn = db.get_conn()
    rows = conn.execute(
        "SELECT id, category FROM cards WHERE category IS NOT NULL AND status != 'failed'"
    ).fetchall()

    by_category: dict[str, list[int]] = {}
    for r in rows:
        by_category.setdefault(r["category"], []).append(r["id"])

    categories = sorted(by_category.keys())
    print(f"共 {len(rows)} 張有類別的名片，{len(categories)} 種類別，呼叫AI判斷類別關聯…")

    client = anthropic.Anthropic()
    relationships = build_category_relationships(categories, client)
    print(f"AI判斷出 {len(relationships)} 組值得互相認識的類別關聯")

    inserted = 0
    for rel in relationships:
        cat_a, cat_b, reason = rel.get("a"), rel.get("b"), rel.get("reason")
        ids_a = by_category.get(cat_a, [])
        ids_b = by_category.get(cat_b, [])
        if not ids_a or not ids_b:
            continue

        if cat_a == cat_b:
            card_pairs = itertools.combinations(ids_a, 2)
        else:
            card_pairs = itertools.product(ids_a, ids_b)

        for id_a, id_b in card_pairs:
            key_a, key_b = _pair_key(id_a, id_b)
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO matches (card_id_a, card_id_b, relation_reason) VALUES (?,?,?)",
                    (key_a, key_b, reason),
                )
                inserted += 1
            except Exception as e:  # noqa: BLE001
                print(f"  寫入失敗 {key_a}-{key_b}：{e}")

    conn.commit()
    conn.close()
    print(f"完成，共寫入/更新 {inserted} 組候選配對。到 /matches 網頁查看。")


if __name__ == "__main__":
    main()
