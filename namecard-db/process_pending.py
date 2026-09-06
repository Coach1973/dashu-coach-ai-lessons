"""
處理公開上傳排隊中的名片（status='pending'）：逐張PaddleOCR+MiniMax辨識、
寫回資料庫、跑產業鏈媒合。

教練的構想：上傳不追求立即出結果，網頁存檔後馬上放行，辨識工作交給
後台慢慢消化，不管一次丟幾十張、幾百張都不會卡住使用者。

2026-08-25教練追加要求：一張照片可以拍多張名片(如6~8張)一次上傳，
不用一張一張拍——效率更高。實測MiniMax-M3有vision能力且邊界框判斷
準確，處理每張pending圖片前先用card_splitter偵測這張照片裡有幾張
名片，偵測到2張以上就自動裁切成獨立圖片，各自走原本的辨識管線。

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
from card_splitter import detect_card_regions, split_image
from chain_matcher import match_card_to_chain
from extract import MODEL, extract_card_fields
from dedup import run_dedup

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_UPLOAD_FOLDER = os.path.join(_THIS_DIR, "public_uploads")


def _extract_and_match(conn, client: anthropic.Anthropic, card_id: int, image_path: str) -> bool:
    """對單張已裁切好的名片圖跑辨識+媒合，回傳是否成功(供dedup判斷要不要跑)"""
    print(f"[處理中] {os.path.basename(image_path)}")
    try:
        fields = extract_card_fields(image_path, client)
    except Exception as e:  # noqa: BLE001 — 單張失敗不能讓整批停掉
        fields = {"_error": str(e), "_raw": ""}
    if fields.get("_is_roster"):
        n = db.insert_directory_roster(conn, os.path.basename(image_path), fields, card_id=card_id)
        print(f"  📇 偵測為通訊錄「{fields.get('org_name')}」，收錄 {n} 位聯絡人")
        return True
    db.update_card_after_extraction(conn, card_id, fields)
    if "_error" in fields:
        print(f"  ⚠️ 失敗：{fields['_error']}")
        return False
    print(f"  ✅ {fields.get('name')} / {fields.get('company')}")
    try:
        match_result = match_card_to_chain(conn, client, card_id, MODEL)
        print(f"  🔗 產業鏈媒合：{match_result}")
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠️ 媒合失敗：{e}")
    return True


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

        try:
            regions = detect_card_regions(image_path, client, MODEL)
        except Exception as e:  # noqa: BLE001 — 偵測失敗就當單張處理，不卡流程
            print(f"  ⚠️ 多名片偵測失敗，當單張處理：{e}")
            regions = []

        if len(regions) >= 2:
            base_name = os.path.splitext(card["image_filename"])[0]
            print(f"[偵測到{len(regions)}張名片] {card['image_filename']}，開始裁切")
            try:
                split_files = split_image(image_path, regions, PUBLIC_UPLOAD_FOLDER, base_name)
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠️ 裁切失敗，改當單張處理：{e}")
                split_files = []

            if split_files:
                db.delete_card(conn, card["id"])  # 移除原始合照容器記錄，改成N筆獨立名片
                for split_file in split_files:
                    new_card_id = db.insert_card_pending(conn, split_file)
                    db.claim_for_processing(conn, new_card_id)
                    split_path = os.path.join(PUBLIC_UPLOAD_FOLDER, split_file)
                    if _extract_and_match(conn, client, new_card_id, split_path):
                        any_success = True
                    processed += 1
                continue

        # 單張名片(或偵測/裁切失敗的容錯)：走原本流程
        if _extract_and_match(conn, client, card["id"], image_path):
            any_success = True
        processed += 1

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
