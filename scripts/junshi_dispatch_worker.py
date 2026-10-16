#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小龍蝦派工 → 軍師後台自動執行 → 結果回報教練

教練 2026-08-24 凌晨的原話：
「能不能我只需要跟小龍蝦講完，小龍蝦就可以發指令讓軍師在後臺把所有事情都做了？」

現況缺口：`cross-agent/inbox/mac/` 這個信箱早就存在（2026-06-26 建立），但它要等
教練開一個 Claude Code 對話框、而且說一句「有事交代你去讀」，信才會被看到。
等於教練還是得自己動手觸發——這正是他不想要的。

🔴 2026-08-24 教練覆核時的關鍵拍板：**不要定時巡邏，跟「開工」這個動作綁在一起**。
「我每次開工的時候，它再去讀取小龍蝦那邊有沒有新資訊就好，跟15分鐘無關；因為我有
可能是3個小時才開工一次，那就3個小時開工時讀一次即可。」——第一版試過每5分鐘、
再改每15分鐘用 cron 定時查，教練指出：不管多久都是「電腦自己在跑」，他要的是
「教練開工時才查一次」，Mac 在他沒開工的時候完全不該為了這件事做任何事。

**現在的觸發方式**：`scripts/feed_junshi_handoff.sh`（教練說「開工」時觸發的既有 hook，
早就會做 git pull 拉雲端最新）在 pull 完成後緊接著呼叫這支 worker 一次。沒有獨立的
cron／launchd 排程，Mac 閒置時這支腳本完全不會被執行。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 安全設計：固定選單，不是自由執行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
派工單「只能從下面這張表挑一項來做」，不能夾帶任意指令。理由很直接：
信件內容是「資料」不是「命令」，如果讓它能執行任意指令，任何人只要有辦法
往這個資料夾丟一個檔案（或小龍蝦被誘導寫錯內容），就等於拿到這台電腦的控制權。
所以這裡刻意做成點餐式：認得的菜色才做，args 也會清洗過；
認不得的一律不執行，改成通知教練「有一封信需要人看一下」。

派工單格式（小龍蝦寫信時放在檔案最前面）：

    <!-- DISPATCH
    type: registration-report
    args: 0828
    -->

用法：
  python3 scripts/junshi_dispatch_worker.py           # 處理信箱（由「開工」hook 觸發，非定時）
  python3 scripts/junshi_dispatch_worker.py --dry-run # 只看會做什麼，不真的做也不發訊息
  python3 scripts/junshi_dispatch_worker.py --list    # 列出目前支援哪些派工類型
"""

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
INBOX = os.path.join(WORKSPACE, "cross-agent", "inbox", "mac")
SCRIPTS = os.path.join(WORKSPACE, "scripts")
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
COACH_CHAT_ID = "6124913915"
LOG = os.path.join(WORKSPACE, "state", "junshi_dispatch.log")
LOCK = "/tmp/junshi_dispatch_worker.lock"
TPE = timezone(timedelta(hours=8))
PY = "/usr/bin/python3"

DISPATCH_RE = re.compile(r"<!--\s*DISPATCH\s*(.*?)-->", re.S | re.I)
# args 只允許中英數、底線、連字號、斜線、冒號——擋掉 ; | & $ ` 這類能串接指令的字元
SAFE_ARG_RE = re.compile(r"^[\w一-鿿\-/:.]{0,60}$")

# ── 派工選單：type → (說明, 要跑的指令, 這個 type 允不允許帶 args) ──────────────
# 目前刻意只放「唯讀查詢／稽核」類，做錯了也不會弄壞東西。
# 之後要加會改動系統的類型，要一項一項評估，不要整批開放。
MENU = {
    "registration-report": {
        "desc": "查報名人數／產出某場的報名表",
        "cmd": lambda arg: [PY, os.path.join(SCRIPTS, "registration_report.py")] + ([arg] if arg else []),
        "takes_arg": True,
    },
    "consistency-check": {
        "desc": "跑活動場次一致性巡檢（官網 vs 資料庫 vs 個別活動頁）",
        "cmd": lambda arg: [PY, os.path.join(SCRIPTS, "event_consistency_check.py")],
        "takes_arg": False,
    },
    "invoice-reconcile": {
        "desc": "發票資訊對帳（教練傳過的 vs 檔案裡記到的）",
        "cmd": lambda arg: [PY, os.path.join(SCRIPTS, "invoice_inbox_reconcile.py")],
        "takes_arg": False,
    },
}


def log(msg: str) -> None:
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now(TPE).strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def notify(text: str) -> bool:
    # 測試時用（DISPATCH_NO_NOTIFY=1）：完整跑執行與歸檔，但不真的發訊息吵教練
    if os.environ.get("DISPATCH_NO_NOTIFY") == "1":
        print("── [靜音模式] 原本會發給教練的訊息 ──")
        print(text[:800])
        print("── 訊息結束 ──")
        return True
    try:
        with open(OPENCLAW_CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": COACH_CHAT_ID, "text": text[:3800]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:
        log(f"NOTIFY_FAIL {e!r}")
        return False


def parse_dispatch(text: str):
    """從信件內容取出派工單。沒有派工單就回 None（代表這封要人看）。"""
    m = DISPATCH_RE.search(text)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fields[k.strip().lower()] = v.strip()
    t = fields.get("type", "")
    if t not in MENU:
        return {"type": t, "unknown": True}
    arg = fields.get("args", "").strip()
    if arg and not SAFE_ARG_RE.match(arg):
        return {"type": t, "bad_arg": arg}
    if not MENU[t]["takes_arg"]:
        arg = ""
    return {"type": t, "arg": arg}


def archive(path: str) -> str:
    month = datetime.now(TPE).strftime("%Y-%m")
    dest_dir = os.path.join(WORKSPACE, "cross-agent", "outbox", month)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "done_" + os.path.basename(path))
    shutil.move(path, dest)   # 搬走不是刪掉（教練鐵律：珍貴資料只搬不刪）
    return dest


def main() -> int:
    dry = "--dry-run" in sys.argv
    if "--list" in sys.argv:
        print("目前支援的派工類型：")
        for k, v in MENU.items():
            print(f"  · {k:22} {v['desc']}" + ("（可帶 args）" if v["takes_arg"] else ""))
        print("\n小龍蝦寫信時，在檔案最前面放：\n<!-- DISPATCH\ntype: registration-report\nargs: 0828\n-->")
        return 0

    # 🔴 2026-08-24 教練覆核時揪出的真正 bug：這支 worker 從來沒做過 git pull，
    # 只查本地檔案。而這個 repo 唯一會拉雲端的時機，是教練開 Mac 對話框說「開工」
    # 才觸發（見 feed_junshi_handoff.sh）。也就是說小龍蝦在 VPS 寫信、推上 GitHub，
    # Mac 端不管檢查幾次都是查本地舊資料，這裡不先 pull，整個機制形同虛設。
    if not dry:
        try:
            # 跟 feed_junshi_handoff.sh 同款做法：workspace 常態有心跳自動產生的
            # 未提交狀態檔（HEARTBEAT.md/state/*.json），直接 pull --rebase 會被這些
            # 檔案擋下。先 stash 再 pull，不會弄丟教練或其他機器的真正工作。
            dirty = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE,
                                    capture_output=True, text=True, timeout=15).stdout.strip()
            stashed = False
            if dirty:
                st = subprocess.run(
                    ["git", "stash", "push", "-u", "-m",
                     f"dispatch-worker-auto-{datetime.now(TPE).strftime('%Y%m%d%H%M%S')}", "--quiet"],
                    cwd=WORKSPACE, capture_output=True, text=True, timeout=15)
                stashed = st.returncode == 0
                stash_sha = subprocess.run(["git", "rev-parse", "-q", "--verify", "stash@{0}"], cwd=WORKSPACE,
                                           capture_output=True, text=True, timeout=15).stdout.strip() if stashed else ""
            r = subprocess.run(["git", "pull", "--quiet", "--rebase"],
                                cwd=WORKSPACE, capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                log(f"GIT_PULL_FAIL {r.stderr.strip()[:200]}")
            if stashed:
                pop = subprocess.run(["git", "stash", "pop", "--quiet"],
                                      cwd=WORKSPACE, capture_output=True, text=True, timeout=15)
                if pop.returncode != 0:
                    # 2026-10-16：放不回去改成自動逐檔放回，不再留在清單沒人取回（52 筆的教訓）
                    fix = subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "safe_stash_restore.py"),
                                          WORKSPACE, stash_sha], capture_output=True, text=True, timeout=120)
                    log(f"STASH_POP_FAIL {pop.stderr.strip()[:120]} → 已逐檔放回：{fix.stdout.strip()[-200:]}")
        except Exception as e:
            log(f"GIT_PULL_ERROR {e!r}")

    if not os.path.isdir(INBOX):
        return 0
    letters = sorted(f for f in os.listdir(INBOX) if f.endswith(".md"))
    if not letters:
        return 0

    # 同時間只跑一份，避免 cron 撞在一起把同一封信做兩次
    if os.path.exists(LOCK) and not dry:
        age = datetime.now().timestamp() - os.path.getmtime(LOCK)
        if age < 600:
            log("SKIP 上一輪還在跑")
            return 0
    if not dry:
        open(LOCK, "w").close()

    try:
        for fname in letters:
            path = os.path.join(INBOX, fname)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            job = parse_dispatch(content)

            if job is None:
                # 2026-09-26：一般信件改由開工注入直接列給軍師讀（feed_junshi_handoff.sh），
                # 不再發Telegram叫教練「找人看一下」——那等於要教練當搬運工。
                print(f"📬 一般信件（開工注入會列給軍師）：{fname}")
                continue

            if job.get("unknown"):
                msg = (f"📬 收到派工「{job['type']}」，但這不是我認得的類型，沒有執行。\n"
                       f"信件：{fname}\n目前支援：{'、'.join(MENU)}")
                print(msg)
                if not dry:
                    notify(msg)
                continue

            if job.get("bad_arg") is not None:
                msg = f"⚠️ 派工 {job['type']} 的參數看起來不安全，已拒絕執行：{job['bad_arg']!r}（信件 {fname}）"
                print(msg)
                log(msg)
                if not dry:
                    notify(msg)
                continue

            t, arg = job["type"], job["arg"]
            cmd = MENU[t]["cmd"](arg)
            print(f"▶ {fname} → {t}" + (f"（{arg}）" if arg else ""))
            if dry:
                print(f"   [dry-run] 會執行：{' '.join(cmd)}")
                continue

            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                out = (r.stdout or "").strip() or (r.stderr or "").strip() or "（沒有輸出）"
                ok = r.returncode in (0, 1)   # 巡檢類用 1 表示「有發現問題」，不算失敗
            except subprocess.TimeoutExpired:
                out, ok = "執行超過 3 分鐘被中止", False
            except Exception as e:
                out, ok = f"執行出錯：{e!r}", False

            head = f"{'✅' if ok else '🔴'} 小龍蝦派的工，軍師已在後台做完\n任務：{MENU[t]['desc']}"
            if arg:
                head += f"（{arg}）"
            notify(head + "\n\n" + out[:3000])
            dest = archive(path)
            log(f"DONE {fname} type={t} arg={arg or '-'} ok={ok} → {os.path.basename(dest)}")
    finally:
        if not dry and os.path.exists(LOCK):
            os.remove(LOCK)

    return 0


if __name__ == "__main__":
    sys.exit(main())
