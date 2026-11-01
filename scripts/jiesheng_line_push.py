#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""結繩領導學・LINE 行銷推播執行器

安全設計（遵守教練常設禁令）：
  1. 必須先有 state/LINE_PUSH_APPROVED 的時間戳（10 分鐘有效），否則拒絕推播
  2. 檢查 LINE 月配額，剩餘低於保留線（30 則）就停手，不做無謂失敗
  3. 每位收件人的成功／失敗都記錄到 state/jiesheng_sent_log.jsonl
  4. 成功的當天標記到 state/jiesheng_marketing.json 的 sent，避免重複發送

用法：python3 scripts/jiesheng_line_push.py [--dry-run]
"""
import json, os, re, sys, time, urllib.request, urllib.error
from datetime import date, datetime
from pathlib import Path

WS = Path("/Users/bymyway/.openclaw/workspace")
STATE = WS / "state/jiesheng_marketing.json"
FLAG = WS / "state/LINE_PUSH_APPROVED"
LOG = WS / "state/jiesheng_sent_log.jsonl"
ENV = WS / "event-signup/.env"
APPROVE = WS / "scripts/line_push_approve.sh"

SIGNUP = "https://rplconstw.pse.is/Taipei1125"
MESSAGE = """📚 結繩領導學・兩日實戰工作坊（台北場 11/25-26）

公司走到 10-80 人，授權了事情還是回到你身上？
這不是演講，是拿你的真實團隊來做「看見→判斷→操作→帶走」的結構重建實驗室。

✅ 四大模組：靜力學（信任地基）／材料力學（識人選人）／結構抗壓（危機阻尼器）／美學連結（編織人脈）
✅ 連續兩天各 8 小時，含實作演練與現場回饋
✅ 帶走一份專屬你的「組織結構重建計畫」
✅ 適合：企業主、二代接班人、10-80 人團隊的中高階主管

📍 劍潭青年活動中心（台北）
💰 憑《結繩領導學》報名優惠 NT$10,000（原價 16,800）
🔗 報名：{signup}

名額有限，確認報名後即保留席次。"""

RESERVE = 30


def token():
    if not ENV.exists():
        sys.exit("找不到 event-signup/.env")
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("EVENT_LINE_CHANNEL_ACCESS_TOKEN"):
            v = line.split("=", 1)[1].strip().strip("'\"")
            if v:
                return v
    sys.exit("憑證層沒有 EVENT_LINE_CHANNEL_ACCESS_TOKEN")


def approved():
    """回傳剩餘秒數；<=0 代表沒許可或已過期"""
    if not FLAG.exists():
        return 0
    try:
        ts = int(FLAG.read_text(encoding="utf-8").strip())
    except Exception:
        return 0
    return ts + 600 - int(time.time())


def quota(tok):
    def q(p):
        r = urllib.request.Request(f"https://api.line.me/v2/bot/message/{p}",
                                   headers={"Authorization": f"Bearer {tok}"})
        with urllib.request.urlopen(r, timeout=8) as resp:
            return json.loads(resp.read())
    try:
        lim = q("quota").get("value", 0)
        used = q("quota/consumption").get("totalUsage", 0)
        return lim - used
    except Exception:
        return None


def push(tok, uid, text):
    body = json.dumps({"to": uid, "messages": [{"type": "text", "text": text}]}).encode()
    req = urllib.request.Request("https://api.line.me/v2/bot/message/push", data=body,
                                 method="POST", headers={"Content-Type": "application/json",
                                                        "Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        return resp.status == 200


def main():
    dry = "--dry-run" in sys.argv
    if not STATE.exists():
        sys.exit("名單檔不存在，先跑 jiesheng_marketing_list.py --build")
    left = approved()
    if left <= 0:
        sys.exit("沒有有效的 LINE 推播許可（需要 10 分鐘內的 timestamp），拒絕執行")

    d = json.loads(STATE.read_text(encoding="utf-8"))
    batch = d.get("today_bot_batch", [])
    if not batch:
        print("今日機器人批次已清空（可能全部發完或名單未建）")
        return

    tok = token()
    remain = quota(tok)
    if remain is not None and remain < RESERVE:
        sys.exit(f"LINE 本月配額剩 {remain} 則，低於保留線 {RESERVE}，不推播")

    msg = MESSAGE.format(signup=SIGNUP)
    print(f"=== 結繩領導學 LINE 推播（許可剩 {left//60} 分 {left%60} 秒）===")
    if remain is not None:
        print(f"    本月配額剩餘：{remain} 則（保留線 {RESERVE}）")
    print(f"    本次目標：{len(batch)} 位／今日上限 {d.get('daily_batch_size')}")

    if dry:
        for r in batch:
            print(f"  [DRY] {r['name']} {r['phone']} {r['title'][:8]}")
        return

    ok, fail = [], []
    for i, r in enumerate(batch, 1):
        left = approved()
        if left <= 0:
            print(f"  ⚠️ 許可視窗已到期（剩 {left}s），停止於第 {i}/{len(batch)} 位")
            break
        try:
            good = push(tok, r["line_id"], msg)
        except urllib.error.HTTPError as e:
            good = False
            err = f"HTTP {e.code}"
        except Exception as e:
            good = False
            err = type(e).__name__
        else:
            err = ""
        rec = {"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "date": date.today().isoformat(),
               "name": r["name"], "phone": r["phone"], "line_id": r["line_id"],
               "ok": bool(good), "err": err, "channel": "bot"}
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if good:
            ok.append(r)
            print(f"  [{i}/{len(batch)}] ✓ {r['name']} {r['phone']}")
        else:
            fail.append((r, err))
            print(f"  [{i}/{len(batch)}] ✗ {r['name']} {r['phone']}  {err}")
        time.sleep(0.4)

    # 標記成功者為已發
    sent = d.setdefault("sent", {})
    today = date.today().isoformat()
    for r in ok:
        sent[r["phone"]] = today
    d["sent"] = sent
    STATE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"=== 完成：成功 {len(ok)}／失敗 {len(fail)}／未跑 {len(batch)-len(ok)-len(fail)} ===")
    if fail:
        print("失敗名單（下次重試）：" + "、".join(f"{n['name']}({n['phone']})" for n, _ in fail))
    print(f"日誌：{LOG}")


if __name__ == "__main__":
    main()
