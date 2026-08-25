"""
處理公開上傳排隊中的名片（status='pending'）：逐張PaddleOCR+MiniMax辨識、
寫回資料庫、跑產業鏈媒合。

教練的構想：上傳不追求立即出結果，網頁存檔後馬上放行，辨識工作交給
後台慢慢消化，不管一次丟幾十張、幾百張都不會卡住使用者。

用法：
    python3 process_pending.py --once     處理一批(預設最多20張)就結束
    python3 process_pending.py --limit 50 處理一批最多50張

觸發方式：/upload路由存完檔後，用subprocess非阻塞方式直接叫這支程式跑一次
(事件觸發，不是定時輪詢——上傳這個動作本身就是觸發點)。若當下已經有一個
process_pending在跑，claim_for_processing()的UPDATE...WHERE status='pending'
確保不會重複處理同一筆，多個平行進程互不干擾，各自搶各自的份。
"""
import argparse
import os

import anthropic

import db
from chain_matcher import match_card_to_chain
from extract import MODEL, extract_card_fields
from dedup import run_dedup

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_UPLOAD_FOLDER = os.path.join(_THIS_DIR, "public_uploads")


def process_once(limit: int = 20) -> int:
    conn = db.get_conn()
    client = anthropic.Anthropic()
    pending = db.list_pending_cards(conn, limit=limit)
    processed = 0
    any_success = False
    for card in pending:
        if not db.claim_for_processing(conn, card["id"]):
            continue  # 被其他平行worker搶走了，跳過
        image_path = os.path.join(PUBLIC_UPLOAD_FOLDER, card["image_filename"])
        if not os.path.exists(image_path):
            db.update_card_after_extraction(
                conn, card["id"], {"_error": "找不到圖片檔案", "_raw": ""}
            )
            continue
        print(f"[處理中] {card['image_filename']}")
        try:
            fields = extract_card_fields(image_path, client)
        except Exception as e:  # noqa: BLE001 — 單張失敗不能讓整批停掉
            fields = {"_error": str(e), "_raw": ""}
        db.update_card_after_extraction(conn, card["id"], fields)
        processed += 1
        if "_error" in fields:
            print(f"  ⚠️ 失敗：{fields['_error']}")
        else:
            any_success = True
            print(f"  ✅ {fields.get('name')} / {fields.get('company')}")
            try:
                match_result = match_card_to_chain(conn, client, card["id"], MODEL)
                print(f"  🔗 產業鏈媒合：{match_result}")
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠️ 媒合失敗：{e}")

    if any_success:
        try:
            run_dedup(client)
        except Exception:  # noqa: BLE001
            pass

    conn.close()
    print(f"本次處理 {processed} 張")
    return processed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    db.init_db()
    process_once(limit=args.limit)


if __name__ == "__main__":
    main()
