#!/usr/bin/env python3
"""小龍蝦升級評估週報（2026-09-24 教練交辦）。

教練：「升級肯定都會有些bug，是不是要定義每隔多少時間去偵測版本、評估有沒有必要升級？
充足收集資訊、確認有沒有災情。」

官方發新版不會推播給我們（npm/GitHub 對別人的套件都沒有可訂閱的事件），只能定期查；
一週一次（週日09:30，launchd ai.openclaw.upgrade-watch）。只收集事實＋套固定規則給建議，
不自動升級——升不升由教練決定。

規則（任一成立就「繼續觀望」）：新版發布未滿7天／發布說明自己警告先別更新／
近7天有P0等級的升級或遷移災情／當初讓小二暫停的 #122261 仍未修。

用法：openclaw_upgrade_watch.py [--dry-run]
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WS = Path.home() / ".openclaw" / "workspace"
SEEN = WS / "state" / "openclaw_version_seen.json"
VPS_STATE = WS / "logs" / "vps_healthcheck_state.json"
OUT = WS / "logs" / "openclaw_upgrade_watch.json"
NOTIFY = WS / "scripts" / "notify_coach.sh"
REPO = "openclaw/openclaw"
BLOCKER = 122261
MIN_AGE_DAYS = 7
ENV = {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": str(Path.home())}


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True, timeout=90, env=ENV).stdout


def dist_tags():
    return json.loads(sh("npm", "view", "openclaw", "dist-tags", "--json"))


def release(version):
    data = json.loads(sh("gh", "release", "view", f"v{version}", "-R", REPO, "--json", "publishedAt,body") or "{}")
    published = datetime.fromisoformat(data["publishedAt"].replace("Z", "+00:00")) if data.get("publishedAt") else None
    age = (datetime.now(timezone.utc) - published).days if published else None
    warns = bool(re.search(r"do not update|don't update|withdrawn", data.get("body", ""), re.I))
    return age, warns


def p0_update_issues():
    since = (datetime.now(timezone.utc).date().toordinal() - 7)
    since_s = datetime.fromordinal(since).strftime("%Y-%m-%d")
    out = sh("gh", "search", "issues", "--repo", REPO, "--state", "open", "--label", "P0",
             f"created:>={since_s}", "--limit", "50", "--json", "number,title")
    items = json.loads(out or "[]")
    return [i for i in items if re.search(r"update|upgrade|migrat|schema|rollback|crash|unresponsive", i["title"], re.I)]


def blocker_open():
    data = json.loads(sh("gh", "issue", "view", str(BLOCKER), "-R", REPO, "--json", "state") or "{}")
    return data.get("state") == "OPEN"


def assess(installed, target, label, issues, blocker, lts=False):
    if not target:
        return f"{label}：查不到官方版本資訊"
    if installed == target:
        return f"✅ {label}：{installed}，已是這條線的最新版"
    age, warns = release(target)
    # 最新版這條線：主線上的P0都算。長期穩定版：只算標題明確點名它的（主線回報常寫成「(9.5)」簡寫，
    # 用版本號字串排除會漏網，反過來只收明確點名的才準）
    line = ".".join(target.split(".")[:2]) + "."
    related = [i for i in issues if line in i["title"] or "extended-stable" in i["title"].lower()] if lts else issues
    reasons = []
    if age is not None and age < MIN_AGE_DAYS:
        reasons.append(f"{target} 才發布{'不到 1' if age == 0 else f' {age}'} 天（滿 {MIN_AGE_DAYS} 天再評估）")
    if warns:
        reasons.append("官方發布說明自己警告先別更新")
    if related:
        reasons.append(f"近7天有 {len(related)} 個跟這條版本線有關的最嚴重等級（P0）升級/當機回報")
    if blocker:
        reasons.append(f"當初讓小二暫停的 #{BLOCKER}（工具重試迴圈拖垮主程式）仍未修")
    head = f"{label}：目前 {installed or '不明'}，可升到 {target}"
    if reasons:
        return f"⏸️ {head}\n   建議繼續觀望：" + "；".join(reasons)
    return f"🟢 {head}\n   沒有發現災情，可以考慮升級（請叫軍師先備份、挑不急的時段再升）"


def main():
    dry = "--dry-run" in sys.argv
    try:
        tags = dist_tags()
        issues = p0_update_issues()
        blocker = blocker_open()
    except Exception as e:  # noqa: BLE001
        msg = f"🔖 小龍蝦升級評估週報：這週查不到官方資料（{type(e).__name__}），下週再查"
        print(msg) if dry else subprocess.run([str(NOTIFY), msg])
        return
    mac = json.loads(SEEN.read_text()).get("version") if SEEN.exists() else None
    vps = json.loads(VPS_STATE.read_text()).get("app_version") if VPS_STATE.exists() else None
    lines = [
        f"🔖 小龍蝦升級評估週報 {datetime.now():%m/%d}（台灣時間）",
        "",
        assess(mac, tags.get("latest"), "Mac小龍蝦（最新版這條線）", issues, blocker),
        assess(vps, tags.get("extended-stable"), "VPS小龍蝦（長期穩定版這條線）", issues, False, lts=True),
    ]
    if issues:
        lines += ["", "近7天P0升級/當機回報（官方GitHub）："] + [f"・#{i['number']} {i['title'][:60]}" for i in issues[:5]]
    lines += ["", "（每週日09:30自動評估，不會自動升級；要升請跟軍師說）"]
    msg = "\n".join(lines)
    OUT.write_text(json.dumps({
        "checkedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "dist_tags": tags,
        "mac": mac, "vps": vps, "p0_issues": issues, "blocker_open": blocker,
    }, ensure_ascii=False, indent=1))
    if dry:
        print(msg)
    else:
        subprocess.run([str(NOTIFY), msg], check=False)


if __name__ == "__main__":
    main()
