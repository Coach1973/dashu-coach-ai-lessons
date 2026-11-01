#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""結繩領導學・每日行銷回報（送到教練 Telegram）

讀取今日推播結果與名單統計，用 openclaw CLI 送出：
  1) 一則文字回報（成功/失敗/剩餘/配額）
  2) 教練手機手動發送用名單（CSV 附件）

用法：python3 scripts/jiesheng_daily_report.py
"""
import json, os, subprocess, sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

WS = Path("/Users/bymyway/.openclaw/workspace")
STATE = WS / "state/jiesheng_marketing.json"
LOG = WS / "state/jiesheng_sent_log.jsonl"
TARGET = "6124913915"
ACCOUNT = "bot_main"


def oc():
    node = os.path.expanduser("~/.nvm/versions/node/v24.22.2/bin/node")
    mjs = os.path.expanduser("~/.nvm/versions/node/v24.22.2/lib/node_modules/openclaw/openclaw.mjs")
    if os.path.exists(node) and os.path.exists(mjs):
        return [node, mjs]
    import shutil
    return [shutil.which("openclaw") or "openclaw"]


def send(text, media=None):
    cmd = [*oc(), "message", "send", "--channel", "telegram", "--account", ACCOUNT,
           "--target", TARGET, "-m", text]
    if media:
        cmd += ["--media", str(media)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode == 0, out[-400:]


def main():
    if not STATE.exists():
        sys.exit("名單檔不存在")
    d = json.loads(STATE.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    st = d.get("stats", {})
    # 即時重算（build 當下的 stats 是快照，推播後 sent 會變動）
    cands = d.get("candidates", [])
    bot_total = len([r for r in cands if r["channel"] == "bot"])
    phone_total = len([r for r in cands if r["channel"] == "phone"])
    sent_now = len(d.get("sent", {}) or {})
    st = dict(st)
    st["機器人可推(有LINE ID)"] = bot_total
    st["教練手機手動發(只有手機)"] = phone_total
    st["已發過"] = sent_now

    ok, fail, skipped = [], [], []
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("date") != today:
                continue
            (ok if r.get("ok") else fail).append(r)

    remain = st.get("待發", 0)
    phone_pool = st.get("教練手機手動發(只有手機)", 0)
    bot_left = st.get("機器人可推(有LINE ID)", 0) - len(ok)
    lines = [
        "📣 結繩領導學・每日行銷（11/1 14:15 建立；每日 12:15 自動執行）",
        "",
        "✅ 機器人推播（LINE 官方帳號）",
        f"　今日成功 {len(ok)} 則" + (f"、失敗 {len(fail)} 則" if fail else "、失敗 0 則"),
    ]
    if fail:
        lines.append("　失敗名單：" + "、".join(f"{r['name']}({r.get('err') or '未送出'})" for r in fail))
    lines += [
        f"　機器人池剩餘：{max(bot_left, 0)} 位（每天 15 位，配額 200 則/月，保留線 30）",
        "",
        "📱 教練手機手動發（附件名單，10 分鐘內發完）",
        f"　今日名單：{len(d.get('today_phone_batch', []))} 位（決策者優先，每天輪轉不重複轟炸）",
        f"　手機池剩餘：{phone_pool} 位",
        "",
        f"📊 整體：候選 {st.get('總候選', 0)}｜排除 {st.get('排除', 0)}｜待發 {remain}｜已發 {len(ok)}",
        "🔗 報名：https://rplconstw.pse.is/Taipei1125　（11/25-26 劍潭青年活動中心）",
    ]

    sheet = WS / f"state/jiesheng_phone_sheet_{today.replace('-', '')}.csv"
    text = "\n".join(lines)
    ok1, out = send(text, sheet if sheet.exists() else None)
    print("Telegram 回報：", "成功" if ok1 else f"失敗 {out}")
    if not ok1:
        print(text)


if __name__ == "__main__":
    main()