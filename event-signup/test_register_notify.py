#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/api/register 通知路徑驗證（教練 2026-08-24「報名通知必須一致」交辦）

用 Flask test client 走真實路由，但把 _notify_xiaolongxia 換成假的記錄器——
這樣能完整驗證「哪些情況會發通知、發給誰、內容對不對」，
又不會在半夜真的把教練跟佩佩老師從睡夢中吵醒（守則#11：主動要用心）。

執行：cd event-signup && python3 test_register_notify.py
"""
import json
import sys

import app as appmod

SENT = []


def fake_notify(text, chat_id=appmod.TELEGRAM_NOTIFY_CHAT_ID):
    SENT.append({"chat_id": chat_id, "text": text})
    return True


appmod._notify_xiaolongxia = fake_notify
GROUP = appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID

CASES = [
    # (說明, payload, 期待有通知嗎, 通知裡應出現的關鍵字)
    ("正常報名（官網已知場次）",
     {"slug": "bigtree-0828", "name": "測試勿理", "phone": "0900000001",
      "company": "測試公司", "email": "t@example.com", "source": "unit-test"},
     True, ["測試勿理", "0900000001"]),
    ("場次代碼對不上（新場次忘了建）",
     {"slug": "bigtree-9999", "name": "測試勿理", "phone": "0900000002", "source": "unit-test"},
     True, ["場次代碼對不上", "bigtree-9999"]),
    ("沒帶場次代碼（前端 if(slug) 沒送）",
     {"name": "測試勿理", "phone": "0900000003", "source": "unit-test"},
     True, ["資料不完整", "0900000003"]),
    ("只填姓名沒電話",
     {"slug": "bigtree-0828", "name": "測試勿理", "source": "unit-test"},
     True, ["資料不完整"]),
    ("完全空的（機器人亂打）",
     {}, False, []),
]


def main() -> int:
    client = appmod.app.test_client()
    passed = failed = 0

    for desc, payload, expect_notify, keywords in CASES:
        SENT.clear()
        r = client.post("/api/register", json=payload)
        got_notify = len(SENT) > 0
        ok = got_notify == expect_notify
        detail = ""

        if ok and expect_notify:
            sent = SENT[0]
            if sent["chat_id"] != GROUP:
                ok = False
                detail += f" ❌送錯對象 {sent['chat_id']}（應為報名群組 {GROUP}）"
            missing = [k for k in keywords if k not in sent["text"]]
            if missing:
                ok = False
                detail += f" ❌通知內容缺少 {missing}"
            if ok:
                detail = f" → 已通知報名群組，首行「{sent['text'].splitlines()[0]}」"

        print(f"{'✅' if ok else '❌'} {desc}｜HTTP {r.status_code}｜通知={got_notify}(期待{expect_notify}){detail}")
        passed += ok
        failed += (not ok)

    # 清掉測試留下的報名資料，不能污染教練的真實名單
    # 報名是 attendees（人）+ signups（人×場次）兩張表，兩邊都要清乾淨才不留孤兒
    import db
    conn = db.get_conn()
    ids = [r[0] for r in conn.execute(
        "SELECT id FROM attendees WHERE name = ? AND phone LIKE '090000000%'", ("測試勿理",)
    ).fetchall()]
    n_sign = 0
    for aid in ids:
        n_sign += conn.execute("DELETE FROM signups WHERE attendee_id = ?", (aid,)).rowcount
    n_att = conn.execute(
        "DELETE FROM attendees WHERE name = ? AND phone LIKE '090000000%'", ("測試勿理",)
    ).rowcount
    conn.commit()
    left = conn.execute(
        "SELECT COUNT(*) FROM attendees WHERE phone LIKE '090000000%'").fetchone()[0]
    conn.close()
    print(f"\n🧹 已清除測試資料：報名紀錄 {n_sign} 筆、來賓 {n_att} 筆｜殘留檢查：{left} 筆"
          + ("（乾淨）" if left == 0 else " ⚠️還有殘留！"))
    print(f"結果：{passed} 通過 / {failed} 失敗（共 {len(CASES)}）")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
