"""
掃描名片資料夾，把還沒處理過的照片送去AI擷取欄位，寫進SQLite。

用法：
    python watch_and_extract.py --once          掃一次就結束
    python watch_and_extract.py --watch          每 INTERVAL_SECONDS 掃一次，一直跑
    python watch_and_extract.py --folder /path   指定資料夾（預設讀環境變數 NAMECARD_FOLDER）
"""
import argparse
import os
import time

import anthropic

import db
from extract import extract_card_fields

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
INTERVAL_SECONDS = 60


def scan_once(folder: str, client: anthropic.Anthropic) -> None:
    conn = db.get_conn()
    filenames = sorted(
        f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in IMAGE_EXTS
    )
    new_count = 0
    for filename in filenames:
        if db.already_processed(conn, filename):
            continue
        new_count += 1
        image_path = os.path.join(folder, filename)
        print(f"[處理中] {filename}")
        try:
            fields = extract_card_fields(image_path, client)
        except Exception as e:  # noqa: BLE001 — 單張失敗不能讓整批停掉
            fields = {"_error": str(e), "_raw": ""}
        db.insert_card(conn, filename, fields)
        if "_error" in fields:
            print(f"  ⚠️ 失敗：{fields['_error']}")
        elif fields.get("confidence_notes"):
            print(f"  ⚠️ 需人工複查：{fields['confidence_notes']}")
        else:
            print(f"  ✅ {fields.get('name')} / {fields.get('company')}")
    conn.close()
    print(f"本次掃描完成，新處理 {new_count} 張，資料夾內共 {len(filenames)} 張。")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--folder", default=os.environ.get("NAMECARD_FOLDER"))
    args = parser.parse_args()

    if not args.folder:
        raise SystemExit(
            "請指定名片資料夾：--folder 路徑，或設定環境變數 NAMECARD_FOLDER"
        )

    db.init_db()
    client = anthropic.Anthropic()

    if args.watch:
        print(f"開始監控資料夾：{args.folder}（每 {INTERVAL_SECONDS} 秒掃一次，Ctrl+C 停止）")
        while True:
            scan_once(args.folder, client)
            time.sleep(INTERVAL_SECONDS)
    else:
        scan_once(args.folder, client)


if __name__ == "__main__":
    main()
