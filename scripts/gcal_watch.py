#!/usr/bin/env python3
"""向 Google 申請「教練日曆一有變動就通知預約網站」（取代每 15 分鐘輪詢；2026-10-13）

流程：教練在 Google 日曆改行程 → Google 主動敲 https://event.bymyway.com/hooks/gcal-push →
預約網站等 3 秒後跑 coach_schedule.py sync-google（Google→總表）。
這個「通知通道」Google 只給幾天壽命（最長約 7 天），所以要定期續約：不是去問有沒有新行程，只是續約。

用法：
  gcal_watch.py start     # 申請新通道（有舊的就在新的成功後停掉舊的）
  gcal_watch.py renew     # 同 start；給續約排程用，剩餘不到 2 天才換（--force 強制）
  gcal_watch.py status    # 看目前通道還剩多久
  gcal_watch.py stop      # 停掉通道

授權沿用 gog 已存好的 bymyway7@gmail.com（只暫時匯出到暫存檔、換成短時效 access token 後馬上刪掉）。
"""
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ACCOUNT = "bymyway7@gmail.com"
WS = os.path.expanduser("~/.openclaw/workspace")
STATE = os.path.join(WS, "state", "gcal_watch.json")
TOKEN_FILE = os.path.join(WS, "state", "gcal_watch_token.txt")
ADDRESS = "https://event.bymyway.com/hooks/gcal-push"
CRED = os.path.expanduser("~/Library/Application Support/gogcli/credentials.json")
TTL = 604800   # 7 天（Google 可能給更短）


def access_token():
    with open(CRED) as f:
        c = json.load(f)
    fd, tmp = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.unlink(tmp)                      # gog export 要求輸出檔不存在
    try:
        r = subprocess.run(["/opt/homebrew/bin/gog", "-a", ACCOUNT, "--no-input", "auth", "tokens", "export", ACCOUNT, "--out", tmp],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            raise SystemExit("匯出授權失敗：" + (r.stderr or r.stdout)[-200:])
        with open(tmp) as f:
            rt = json.load(f)
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    refresh = rt.get("refresh_token") or rt.get("refreshToken")
    if not refresh:
        raise SystemExit("授權檔裡找不到 refresh_token（欄位：%s）" % list(rt.keys()))
    body = urllib.parse.urlencode({"client_id": c["client_id"], "client_secret": c["client_secret"],
                                   "refresh_token": refresh, "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body), timeout=30) as r:
        return json.load(r)["access_token"]


def api(path, payload, tok):
    req = urllib.request.Request("https://www.googleapis.com/calendar/v3" + path, data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit("Google 回 %s：%s" % (e.code, e.read().decode("utf-8", "replace")[:600]))


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except OSError:
        return {}


def save_state(d):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(STATE), suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)


def secret():
    try:
        with open(TOKEN_FILE) as f:
            s = f.read().strip()
            if s:
                return s
    except OSError:
        pass
    s = secrets.token_urlsafe(32)
    fd = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(s + "\n")
    return s


def left_days(st):
    return (st.get("expiration_ms", 0) / 1000 - time.time()) / 86400


def start(force=False):
    old = load_state()
    if old and not force and left_days(old) > 2 and sys.argv[1] == "renew":
        print("通道還有 %.1f 天，不用換" % left_days(old))
        return
    tok = access_token()
    cid = str(uuid.uuid4())
    res = api("/calendars/%s/events/watch" % urllib.parse.quote(ACCOUNT),
              {"id": cid, "type": "web_hook", "address": ADDRESS, "token": secret(), "params": {"ttl": str(TTL)}}, tok)
    new = {"channel_id": res["id"], "resource_id": res["resourceId"], "expiration_ms": int(res["expiration"]),
           "address": ADDRESS, "created": time.strftime("%Y-%m-%d %H:%M:%S")}
    save_state(new)
    if old.get("channel_id") and old.get("resource_id"):
        try:
            api("/channels/stop", {"id": old["channel_id"], "resourceId": old["resource_id"]}, tok)
        except SystemExit as e:
            print("（舊通道停止時回報：%s，它自己會過期，不影響）" % str(e)[:120])
    print("✅ 通知通道已建立，還有 %.1f 天到期" % left_days(new))


def stop():
    st = load_state()
    if not st.get("channel_id"):
        print("目前沒有通道")
        return
    api("/channels/stop", {"id": st["channel_id"], "resourceId": st["resource_id"]}, access_token())
    save_state({})
    print("✅ 已停止")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd in ("start", "renew"):
        start(force="--force" in sys.argv)
    elif cmd == "stop":
        stop()
    else:
        st = load_state()
        print("尚無通道" if not st else "通道 %s 還有 %.1f 天到期（建立於 %s）" % (st["channel_id"][:8], left_days(st), st.get("created")))
