"""
一次性補跑：把資料庫裡已辨識完成、但還沒做過產業鏈媒合的舊名片全部跑一次。
給教練在新增產業鏈媒合功能上線時，把既有資料一次補齊用，不用等新名片才有結果。
"""
import anthropic

import db
from chain_matcher import match_card_to_chain
from extract import MODEL


def main() -> None:
    db.init_db()
    conn = db.get_conn()
    client = anthropic.Anthropic()

    cards = conn.execute(
        "SELECT id, name, company FROM cards WHERE status IN ('ok', 'needs_review') ORDER BY id"
    ).fetchall()
    print(f"共 {len(cards)} 張已辨識完成的名片，開始逐張媒合...")

    done, skipped = 0, 0
    for card in cards:
        already = conn.execute(
            "SELECT 1 FROM chain_members WHERE card_id = ?", (card["id"],)
        ).fetchone()
        if already:
            skipped += 1
            continue
        result = match_card_to_chain(conn, client, card["id"], MODEL)
        print(f"  [{card['id']}] {card['name']}／{card['company']} -> {result}")
        done += 1

    conn.close()
    print(f"\n完成：新處理 {done} 張，已有結果跳過 {skipped} 張")


if __name__ == "__main__":
    main()
