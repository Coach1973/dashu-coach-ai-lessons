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
import shutil

import anthropic

import db
from card_splitter import detect_card_regions, split_image
from chain_matcher import match_card_to_chain
from dedup import run_dedup
from extract import MODEL, extract_card_fields

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEAM_UPLOAD_FOLDER = os.path.join(_THIS_DIR, "team_uploads")


def _extract_insert_and_match(conn, client: anthropic.Anthropic, filename: str, image_path: str) -> bool:
    """對單張名片圖跑辨識+insert+媒合，回傳是否成功"""
    print(f"[處理中] {filename}")
    try:
        fields = extract_card_fields(image_path, client)
    except Exception as e:  # noqa: BLE001 — 單張失敗不能讓整批停掉
        fields = {"_error": str(e), "_raw": ""}
    card_id = db.insert_card(conn, filename, fields)
    if "_error" in fields:
        print(f"  ⚠️ 失敗：{fields['_error']}")
        return False
    if fields.get("confidence_notes"):
        print(f"  ⚠️ 需人工複查：{fields['confidence_notes']}")
    else:
        print(f"  ✅ {fields.get('name')} / {fields.get('company')}")
    try:
        match_result = match_card_to_chain(conn, client, card_id, MODEL)
        print(f"  🔗 產業鏈媒合：{match_result}")
    except Exception as e:  # noqa: BLE001 — 媒合失敗不影響名片本身已收錄
        print(f"  ⚠️ 產業鏈媒合失敗：{e}")
    return True


def scan_once(folder: str, client: anthropic.Anthropic) -> None:
    os.makedirs(TEAM_UPLOAD_FOLDER, exist_ok=True)
    conn = db.get_conn()
    filenames = sorted(
        f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in IMAGE_EXTS
    )
    new_count = 0
    for filename in filenames:
        if db.already_processed(conn, filename):
            continue
        image_path = os.path.join(folder, filename)
        # 複製一份到本機，網站顯示縮圖才不依賴Amber SMB即時掛載狀態
        local_copy = os.path.join(TEAM_UPLOAD_FOLDER, filename)
        if not os.path.exists(local_copy):
            shutil.copy2(image_path, local_copy)

        # 一張照片可能拍了多張名片(教練要求提升效率)，先偵測再決定要不要裁切
        try:
            regions = detect_card_regions(local_copy, client, MODEL)
        except Exception as e:  # noqa: BLE001 — 偵測失敗就當單張處理，不卡流程
            print(f"  ⚠️ 多名片偵測失敗，當單張處理：{e}")
            regions = []

        if len(regions) >= 2:
            base_name = os.path.splitext(filename)[0]
            print(f"[偵測到{len(regions)}張名片] {filename}，開始裁切")
            try:
                split_files = split_image(local_copy, regions, TEAM_UPLOAD_FOLDER, base_name)
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠️ 裁切失敗，改當單張處理：{e}")
                split_files = []
            if split_files:
                # 原始合照留一筆佔位記錄避免already_processed重複觸發偵測，
                # status='split'不是真實名片，首頁搜尋結果會排除顯示
                db.insert_split_marker(conn, filename)
                new_count += 1
                for split_file in split_files:
                    split_path = os.path.join(TEAM_UPLOAD_FOLDER, split_file)
                    _extract_insert_and_match(conn, client, split_file, split_path)
                    new_count += 1
                continue

        new_count += 1
        _extract_insert_and_match(conn, client, filename, image_path)
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
