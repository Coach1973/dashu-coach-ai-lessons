#!/usr/bin/env python3
"""分身鬼打牆預警巡檢（2026-11-08 教練：「不要每次都是我發現問題」）

每天早上掃一次所有分身（小龍蝦／巴哈／孔大哥／榮樹下…）、所有通道，找「同一類」的前兆，
有就寫進軍師信箱 state/junshi_inbox.jsonl（系統的事不吵教練），軍師開工時自己處理。

檢查五件事：
  1. 昨天到現在，一輪超過 10 分鐘的對話（哪個分身、哪個對話、幾分鐘）
  2. 各種安全鎖觸發次數（收尾鎖／悶頭鎖／安靜鎖／備忘鎖／找工具鎖…），同一個鎖一天 ≥3 次＝有新漏洞
  3. 對話塞爆（context overflow）次數
  4. 還是「AI 跑一輪」的提醒排程（應該改成直接送固定文字）
  5. 對話容量超過 70% 的分身對話（再聊幾句就會塞爆、自動整理、接著亂跑）

用法：python3 scripts/bot_loop_patrol.py [--dry]   （--dry 只印不寫信箱）
"""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone

TW = timezone(timedelta(hours=8))
HOME = os.path.expanduser("~")
WS = os.path.join(HOME, ".openclaw", "workspace")
OC = os.path.join(HOME, ".nvm/versions/node/v24.22.2/bin/openclaw")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
LOCKS = ["收尾鎖觸發", "悶頭鎖觸發", "時間版悶頭鎖觸發", "安靜鎖觸發", "找工具鎖觸發", "備忘鎖觸發",
         "叫醒鎖觸發", "對話累計上限觸發", "發送目標鎖擋下"]
ALLOWED_AI_JOBS = {"幕僚長晨報", "Memory Dreaming Promotion"}  # 真的要 AI 整理的排程


def oc_json(args):
    try:
        out = subprocess.run([OC, *args, "--json"], capture_output=True, text=True, timeout=120).stdout
        return json.loads(out[out.index("{") if out.lstrip().startswith("{") else out.index("["):])
    except Exception:
        return None


def scan_logs(since):
    runs, locks, overflow = {}, {}, 0
    days = {since.astimezone(timezone.utc).date(), datetime.now(timezone.utc).date()}
    for d in sorted(days):
        f = f"/tmp/openclaw/openclaw-{d.isoformat()}.log"
        if not os.path.exists(f):
            continue
        for line in open(f, errors="ignore"):
            m = re.search(r'"date":"([^"]+)"', line)
            if not m:
                continue
            t = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
            if t < since:
                continue
            for k in LOCKS:
                if k in line:
                    locks[k] = locks.get(k, 0) + 1
            if "context-overflow-diag" in line:
                overflow += 1
            sk = re.search(r"sessionKey'?\"?: ?'?\\?\"?(agent:[a-z_]+:[^'\\\" ,}]+)", line)
            for r in set(UUID.findall(line)):
                x = runs.setdefault(r, {"a": t, "b": t, "sk": None})
                x["b"] = t
                if sk and not x["sk"]:
                    x["sk"] = sk.group(1)
    long_runs = sorted(
        ((round((x["b"] - x["a"]).total_seconds() / 60), x["sk"], x["a"].astimezone(TW).strftime("%m/%d %H:%M"))
         for x in runs.values() if x["sk"] and (x["b"] - x["a"]).total_seconds() >= 600 and (x["b"] - x["a"]).total_seconds() < 6 * 3600),
        reverse=True)
    return long_runs, locks, overflow


def main():
    dry = "--dry" in sys.argv
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    long_runs, locks, overflow = scan_logs(since)
    issues = []
    if long_runs:
        issues.append("一輪超過 10 分鐘：" + "；".join(f"{sk}（台灣時間 {at} 起，{m} 分）" for m, sk, at in long_runs[:6]))
    hot = {k: v for k, v in locks.items() if v >= 3}
    if hot:
        issues.append("安全鎖一天觸發 ≥3 次（代表有新的鬼打牆樣式）：" + "、".join(f"{k} {v} 次" for k, v in hot.items()))
    if overflow >= 3:
        issues.append(f"對話塞爆 {overflow} 次")
    cron = oc_json(["cron", "list"]) or {}
    jobs = cron.get("jobs", cron) if isinstance(cron, dict) else cron
    ai_jobs = [j.get("name") for j in (jobs or []) if j.get("enabled", True)
               and (j.get("payload") or {}).get("kind") == "agentTurn" and j.get("name") not in ALLOWED_AI_JOBS]
    if ai_jobs:
        issues.append("還是「AI 跑一輪」的排程（提醒類要改成直接送固定文字）：" + "、".join(ai_jobs))
    sess = oc_json(["sessions", "--all-agents", "--active", "1440"]) or []
    if isinstance(sess, dict):
        sess = sess.get("sessions", [])
    full = [f"{s.get('key')} {round((s.get('totalTokens') or 0) / (s.get('contextTokens') or 1) * 100)}%"
            for s in sess if (s.get("totalTokens") or 0) / (s.get("contextTokens") or 1) >= 0.7]
    if full:
        issues.append("對話容量超過 70%（快塞爆）：" + "、".join(full))

    stamp = datetime.now(TW).strftime("%Y-%m-%d %H:%M")
    if not issues:
        print(f"[{stamp} 台灣時間] 分身巡檢：沒有鬼打牆前兆")
        return
    msg = "分身鬼打牆預警（過去 24 小時）\n- " + "\n- ".join(issues) + \
          "\n處理：看 /tmp/openclaw 日誌找是哪種情況→改 extensions/safety-locks（同類錯改程式，不加條文）。"
    print(f"[{stamp} 台灣時間]\n{msg}")
    if not dry:
        subprocess.run([sys.executable, os.path.join(WS, "scripts/junshi_inbox.py"), "add", "bot_loop_patrol", msg], timeout=30)


if __name__ == "__main__":
    main()
