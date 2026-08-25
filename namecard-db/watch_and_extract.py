"""
掃描名片資料夾，把還沒處理過的照片送去AI擷取欄位，寫進SQLite。

用法：
    python watch_and_extract.py --once          掃一次就結束
    python watch_and_extract.py --folder /path   指定資料夾（預設讀環境變數 NAMECARD_FOLDER）

2026-07-12 教練糾正（同一個「輪詢 vs 事件觸發」的坑第4次踩，見試金石案例49）：
拿掉了原本每N秒重複掃的--watch常駐模式，不再有任何背景排程。改成純事件觸發：
- Telegram/LINE傳名片 → hooks/namecard-inbound複製完檔案後直接spawn這支程式跑--once
- Amber App/電腦直接丟進資料夾（沒有事件通知機制可用）→ 教練/孔大哥/佩佩老師上傳完
  跟小龍蝦/學弟/學妹說「整理名片」，由對話觸發跑--once
沒事件發生，這支程式就完全不會被呼叫，沒有任何進程常駐、沒有任何定時任務。
"""
import argparse
import os

import anthropic

import db
from chain_matcher import match_card_to_chain
from dedup import run_dedup
from extract import MODEL, extract_card_fields

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}


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
        card_id = db.insert_card(conn, filename, fields)
        if "_error" in fields:
            print(f"  ⚠️ 失敗：{fields['_error']}")
        elif fields.get("confidence_notes"):
            print(f"  ⚠️ 需人工複查：{fields['confidence_notes']}")
        else:
            print(f"  ✅ {fields.get('name')} / {fields.get('company')}")
        if "_error" not in fields:
            try:
                match_result = match_card_to_chain(conn, client, card_id, MODEL)
                print(f"  🔗 產業鏈媒合：{match_result}")
            except Exception as e:  # noqa: BLE001 — 媒合失敗不影響名片本身已收錄
                print(f"  ⚠️ 產業鏈媒合失敗：{e}")
    conn.close()
    print(f"本次掃描完成，新處理 {new_count} 張，資料夾內共 {len(filenames)} 張。")

    if new_count > 0:
        merged = run_dedup(client)
        if merged:
            print(f"  🔗 自動合併 {merged} 組正反面名片")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--folder", default=os.environ.get("NAMECARD_FOLDER"))
    args = parser.parse_args()

    if not args.folder:
        raise SystemExit(
            "請指定名片資料夾：--folder 路徑，或設定環境變數 NAMECARD_FOLDER"
        )

    db.init_db()
    client = anthropic.Anthropic()
    scan_once(args.folder, client)


if __name__ == "__main__":
    main()
