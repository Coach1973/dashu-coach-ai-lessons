"""
2026-08-26教練事故後改版：批次跑全部428人一次燒了150萬token（案例65），
教練當場拍板新規則——不再預先批次媒合，改成`/card/<id>/match`手動按鈕、
誰要看誰才觸發（此按鈕在app.py/index.html早就存在，本場查證確認可正常運作）。

這支腳本**只保留給現任會員**（bni_note含「現任」，約89~92人）用，因為這批
是教練指定「需要預先媒合」的例外，其餘前會員(335人)一律不再用這支腳本批次跑，
只能透過網頁手動點「媒合」按鈕逐一觸發。重試、連續失敗自動通知教練、
逐筆進度落地成可恢復的log(重跑會自動跳過已完成的)等既有安全機制保留不動。
"""
import subprocess
import sys
import time
import traceback
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402
from chain_matcher import match_card_to_chain  # noqa: E402
from extract import MODEL  # noqa: E402

LOG_PATH = Path(__file__).resolve().parent / "chain_match_log.txt"
NOTIFY_SCRIPT = Path(__file__).resolve().parent.parent.parent / "scripts" / "notify_coach.sh"

MAX_RETRIES = 3
RETRY_SLEEP_SEC = 8
CONSECUTIVE_FAIL_ALERT_THRESHOLD = 5
PACE_SLEEP_SEC = 3  # 教練2026-08-26要求放慢速度、不要短時間連續狂打，每人之間留間隔


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def notify_coach(msg: str) -> None:
    try:
        subprocess.run(
            [str(NOTIFY_SCRIPT), msg],
            check=False, timeout=30,
            capture_output=True,
        )
    except Exception:
        log(f"⚠️ 通知教練失敗（notify_coach.sh呼叫本身出錯），訊息內容：{msg}")


def match_with_retry(conn, client, card_id: int, model: str) -> dict:
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return match_card_to_chain(conn, client, card_id, model)
        except Exception as e:  # noqa: BLE001
            last_err = e
            log(f"  ⚠️ card {card_id} 第{attempt}次失敗：{e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_SLEEP_SEC)
    raise last_err  # 三次都失敗，往外拋，由主迴圈記錄+計入連續失敗


def main() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log("=== BNI Connect 現任會員 產業鏈媒合開始（前會員已排除，改走手動按鈕） ===")
    conn = db.get_conn()
    client = anthropic.Anthropic()

    cards = conn.execute(
        """SELECT id, name, company, bni_note FROM cards
           WHERE image_filename LIKE 'bniconnect\\_\\_%' ESCAPE '\\'
           AND status = 'ok'
           AND bni_note LIKE '%現任%'
           ORDER BY id"""
    ).fetchall()
    log(f"目標名單（僅現任會員）共 {len(cards)} 人")

    done, skipped, failed = 0, 0, 0
    consecutive_fail = 0

    for card in cards:
        already = conn.execute(
            "SELECT 1 FROM chain_members WHERE card_id = ?", (card["id"],)
        ).fetchone()
        if already:
            skipped += 1
            continue

        try:
            result = match_with_retry(conn, client, card["id"], MODEL)
            log(f"  [{card['id']}] {card['name']}／{card['company']}（{card['bni_note']}） -> {result}")
            done += 1
            consecutive_fail = 0
            time.sleep(PACE_SLEEP_SEC)
        except Exception as e:  # noqa: BLE001
            failed += 1
            consecutive_fail += 1
            log(f"  ❌ [{card['id']}] {card['name']} 三次重試皆失敗：{e}")
            log(traceback.format_exc())

            if consecutive_fail >= CONSECUTIVE_FAIL_ALERT_THRESHOLD:
                notify_coach(
                    f"名片系統BNI媒合卡住了：連續{consecutive_fail}人失敗，"
                    f"最後卡在「{card['name']}」(card_id={card['id']})。"
                    f"已處理{done}人、跳過{skipped}人（原本就有）、失敗{failed}人，"
                    f"共{len(cards)}人。腳本已停止，錯誤：{e}\n"
                    f"log在 namecard-db/bni_connect_import/chain_match_log.txt，"
                    f"排除問題後重跑同一支腳本會自動接續未完成的部分。"
                )
                conn.close()
                log("=== 連續失敗達門檻，已通知教練並停止 ===")
                sys.exit(1)

    conn.close()
    summary = (
        f"BNI Connect現任會員產業鏈媒合完成：目標{len(cards)}人中，本次新處理{done}人、"
        f"已有結果跳過{skipped}人、失敗{failed}人。前會員一律不再批次跑，改由網頁"
        f"手動點「媒合」按鈕逐一觸發。"
    )
    log(f"=== {summary} ===")
    notify_coach(summary)


if __name__ == "__main__":
    main()
