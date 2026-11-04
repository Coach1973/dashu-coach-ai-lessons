#!/usr/bin/env python3
"""系統健康檢查（技能「健康檢查」用）：把 2026-10-16 一整天手動查過的事，一次跑完、用白話回報。

用法：python3 scripts/system_health_check.py          （約 30～90 秒）
      python3 scripts/system_health_check.py --quick  （不測網站，約 5 秒）
只讀不改。每一項印 ✅ 或 ⚠️，最後一行是總結。
"""
import glob, json, os, plistlib, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

HOME = os.path.expanduser("~")
WS = f"{HOME}/.openclaw/workspace"
OC = f"{HOME}/.openclaw"
LA = f"{HOME}/Library/LaunchAgents"
QUICK = "--quick" in sys.argv
problems = []


def sh(cmd, cwd=None, timeout=60):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip()


def ok(msg): print("✅ " + msg)


def bad(msg):
    print("⚠️ " + msg)
    problems.append(msg)


# 1. 兩個主要資料夾：分支對、沒卡住、跟 GitHub 同步、檔案齊全
for repo, want in ((WS, "main"), (OC, "master")):
    name = "工作資料夾 workspace" if repo == WS else "小龍蝦資料夾 ~/.openclaw"
    _, br = sh(["git", "-C", repo, "branch", "--show-current"])
    stuck = [x for x in ("rebase-merge", "rebase-apply", "MERGE_HEAD") if os.path.exists(f"{repo}/.git/{x}")]
    _, lr = sh(["git", "-C", repo, "rev-list", "--left-right", "--count", f"{want}...origin/{want}"])
    ahead, behind = (lr.split() + ["?", "?"])[:2]
    fs = subprocess.run(["git", "-c", "core.quotepath=off", "-C", repo, "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "ignore").split("\0")
    files = str(sum(1 for f in fs if f and not os.path.lexists(os.path.join(repo, f))))
    if br != want: bad(f"{name}：分支是「{br or '（沒有分支，卡在半路）'}」，應該是「{want}」")
    elif stuck: bad(f"{name}：有 git 動作卡在半路（{', '.join(stuck)}）")
    elif files.strip() != "0": bad(f"{name}：有 {files.strip()} 個檔案不見了")
    elif ahead != "0" or behind != "0": bad(f"{name}：跟 GitHub 差 {ahead} 個沒推上去、{behind} 個沒拉下來")
    else: ok(f"{name}：分支正確、檔案齊全、跟 GitHub 同步")

# 2. 教練說話時跑的檢查程式：檔案都在、沒有任何一支會擋人
d = json.load(open(f"{HOME}/.claude/settings.json"))
missing = []
for ev, arr in d.get("hooks", {}).items():
    for m in arr:
        for h in m.get("hooks", []):
            for p in re.findall(r"(/Users/\S+?\.(?:sh|py))", h.get("command", "")):
                if not os.path.exists(p): missing.append(os.path.basename(p))
inp = json.dumps({"prompt": "健康檢查測試", "session_id": "health-check", "hook_event_name": "UserPromptSubmit", "cwd": OC})
blockers = []
for m in d["hooks"].get("UserPromptSubmit", []):
    for h in m["hooks"]:
        r = subprocess.run(["sh", "-c", h["command"]], input=inp, capture_output=True, text=True, timeout=60)
        if r.returncode == 2: blockers.append(h["command"][-60:])
if missing: bad(f"自動檢查程式有 {len(missing)} 支檔案不見：{', '.join(sorted(set(missing)))}")
if blockers: bad(f"有 {len(blockers)} 支檢查會擋住教練說話：{blockers}")
if not missing and not blockers: ok("教練說話時跑的檢查程式：檔案都在，沒有任何一支會擋人")

# 3. 自動服務：重開機／登出後會不會自己起來
_, ll = sh(["launchctl", "list"])
loaded = {l.split("\t")[2] for l in ll.splitlines()[1:] if l.count("\t") == 2}
# 被 launchctl 明確停用（disabled）的是教練有意停的（例：ai.openclaw.fb-birthday，10/30 不貼 FB），不報「沒在跑」
_, dis = sh(["launchctl", "print-disabled", f"gui/{os.getuid()}"])
disabled = set(re.findall(r'"([^"]+)"\s*=>\s*disabled', dis))
ours = sorted(glob.glob(f"{LA}/com.coach.*.plist") + glob.glob(f"{LA}/ai.openclaw.*.plist"))
sv = []
for p in ours:
    try: dd = plistlib.load(open(p, "rb"))
    except Exception: sv.append(f"{os.path.basename(p)} 設定檔壞了"); continue
    lab = dd.get("Label"); args = dd.get("ProgramArguments") or [dd.get("Program", "")]
    if lab not in loaded and lab not in disabled: sv.append(f"{lab} 沒在跑")
    for q in re.findall(r"(/Users/bymyway/[^\s;\"']+)", " ".join(map(str, args))):
        if not os.path.exists(q.rstrip(")")): sv.append(f"{lab} 指到不存在的 {q}")
bk = {os.path.basename(x) for x in glob.glob(f"{WS}/ops/launchagents_backup/*.plist")}
unprot = [os.path.basename(p) for p in ours if os.path.basename(p) not in bk]
if sv: bad("自動服務有問題：" + "；".join(sv[:8]))
if unprot: bad(f"有 {len(unprot)} 個自動服務沒被守門員保護：{', '.join(unprot)}")
if not sv and not unprot: ok(f"自動服務 {len(ours)} 個：都在跑、程式都在、全部有守門員保護（登出／重開機會自己回來）")

# 4. 網站
if not QUICK:
    sites = [f"https://{h}.bymyway.com/" for h in "chapters trust event shops mentor100 namecard peipei-event sincere team team01 real-wealth zhenxin real-diamonds".split()]
    aw = f"{HOME}/github_repos/all-works"
    _, more = sh(f"grep -rohE 'https://[a-z0-9.-]*bymyway\\.com/[A-Za-z0-9._~/%-]*' --exclude-dir=.git '{aw}' | sort -u")
    urls = sorted(set(sites + more.splitlines()))
    def code(u):
        return u, sh(["curl", "-sL", "-o", "/dev/null", "-m", "15", "-w", "%{http_code}", u], timeout=30)[1]
    with ThreadPoolExecutor(16) as ex: res = list(ex.map(code, urls))
    down = [f"{u}（{c}）" for u, c in res if c != "200"]
    if down: bad(f"{len(down)}/{len(urls)} 個網頁打不開：" + "、".join(down[:10]))
    else: ok(f"網站：{len(urls)} 個網址（13 個主站＋作品一覽所有頁）全部打得開")

# 5. 所有網站專案：沒有卡住、沒有忘了推
gp = []
for g in sorted(glob.glob(f"{HOME}/github_repos/*/.git")):
    r = os.path.dirname(g); n = os.path.basename(r)
    if any(os.path.exists(f"{g}/{x}") for x in ("rebase-merge", "rebase-apply", "MERGE_HEAD")): gp.append(f"{n} 卡在半路")
    rc, up = sh(["git", "-C", r, "rev-list", "--count", "@{u}..HEAD"])
    if rc == 0 and up not in ("", "0"): gp.append(f"{n} 有 {up} 個沒推上去")
if gp: bad("網站專案：" + "；".join(gp))
else: ok(f"網站專案 {len(glob.glob(f'{HOME}/github_repos/*/.git'))} 個：沒有卡住、沒有忘了推")

# 6. 自動同步有沒有又把東西留在暫存清單（10/16 修好後應該是 0）
_, st = sh(["git", "-C", WS, "stash", "list", "--format=%ct"])
new = [t for t in st.split() if t.isdigit() and int(t) > time.time() - 7 * 86400 and int(t) > 1792141200]  # 10/16 19:00 之後
if new: bad(f"最近有 {len(new)} 筆自動暫存沒放回去（應該要自動放回）")
else: ok("自動同步：沒有新的「放不回去」暫存")

# 7. 接力棒鏡像、背景排程
cm = f"{WS}/CLAUDE.md"
m = re.search(r"最後同步：(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", open(cm, errors="ignore").read()[:3000]) if os.path.exists(cm) else None
hm = os.path.getmtime(f"{WS}/JUNSHI_HANDOFF_LATEST.md")
if not m: bad("接力棒鏡像：CLAUDE.md 找不到同步時間")
else:
    synced = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").timestamp()
    if hm - synced > 15 * 60: bad(f"接力棒鏡像：接力棒改過了，但 CLAUDE.md 停在 {m.group(1)} 沒跟上")
    else: ok(f"接力棒鏡像：新對話讀得到最新一棒（同步於 {m.group(1)}）")
log = "/tmp/openclaw_cron_daemon.log"
if os.path.exists(log):
    since = datetime.fromtimestamp(time.time() - 20 * 60).strftime("%Y-%m-%d %H:%M")  # 只看最近 20 分鐘＝現在還壞著的
    fails = [l for l in open(log, errors="ignore").read().splitlines()[-400:] if "失敗" in l and l[1:17] >= since]
    beat = os.path.getmtime(log) > time.time() - 300
    if not beat: bad("背景排程：超過 5 分鐘沒有心跳（可能停了）")
    elif fails: bad(f"背景排程：最近 20 分鐘失敗 {len(fails)} 次（{fails[-1][22:60]}）")
    else: ok("背景排程：心跳正常、最近 20 分鐘沒有失敗")

# 8. 硬碟
_, df = sh("df -h / | tail -1 | awk '{print $4, $5}'")
free, used = (df.split() + ["?", "?"])[:2]
(bad if used.rstrip("%").isdigit() and int(used.rstrip("%")) > 90 else ok)(f"硬碟：剩 {free}（已用 {used}）")

print("\n" + ("🟢 總結：全部正常" if not problems else f"🟠 總結：{len(problems)} 項要處理（上面 ⚠️ 那幾行）"))
