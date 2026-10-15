#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub 推送自動換新 /hooks/github-site（2026-10-10）。
假的同步工作、假通知，不真的 git pull、不發 Telegram。執行：cd event-signup && ./venv/bin/python test_github_site_webhook.py"""
import hashlib
import hmac
import json

import app as appmod

SECRET = "test-secret"
appmod.GITHUB_WEBHOOK_SECRET = SECRET
CALLS = []
appmod._github_sync_worker = lambda kind, key, sha: CALLS.append((kind, key, sha))
appmod._notify_xiaolongxia = lambda *a, **k: True


class SyncThread:  # 測試時同步執行，才看得到有沒有被呼叫
    def __init__(self, target, args, daemon=True):
        self.t, self.a = target, args

    def start(self):
        self.t(*self.a)


appmod.threading.Thread = SyncThread
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def send(payload, event="push", secret=SECRET, sig=None):
    body = json.dumps(payload).encode()
    if sig is None:
        sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return client.post("/hooks/github-site", data=body, content_type="application/json",
                       headers={"X-GitHub-Event": event, "X-Hub-Signature-256": sig})


def push(name, ref="refs/heads/main"):
    return {"ref": ref, "after": "abcdef1234567", "repository": {"name": name, "default_branch": "main"}}


CALLS.clear()
r = send(push("111-wei"), sig="sha256=00")
check("簽章錯誤 → 403，且不同步", r.status_code == 403 and not CALLS)
r = send(push("111-wei"), secret="wrong")
check("用錯暗號簽 → 403", r.status_code == 403 and not CALLS)
r = client.post("/hooks/github-site", data=b"{}", content_type="application/json", headers={"X-GitHub-Event": "push"})
check("沒有簽章 → 403", r.status_code == 403)
r = send({"zen": "hi"}, event="ping")
check("GitHub 掛上時的 ping → 200", r.status_code == 200 and r.get_json().get("pong"))
r = send(push("111-wei"))
check("策展站 111-wei 推送 → 202 並排進同步", r.status_code == 202 and CALLS == [("curated", "111-wei", "abcdef1234567")])
CALLS.clear()
r = send(push("111-wei", ref="refs/heads/test"))
check("非主分支 → 不同步", r.status_code == 200 and not CALLS)
r = send(push("not-our-site-xyz"))
check("不認得的 repo → 404 不同步", r.status_code == 404 and not CALLS)
r = send(push("../../etc"))
check("怪名字 → 400", r.status_code == 400 and not CALLS)
r = send(push("tut-alumni"))
check("舊站 tut-alumni（不在策展名單）→ 404 不碰", r.status_code == 404 and not CALLS)
r = send({"action": "opened"}, event="issues")
check("其他事件 → 忽略", r.status_code == 200 and not CALLS)
# ── 雲端對話推 claude/* 分支 → 電報通知教練（2026-10-15）──
appmod.GITHUB_WEBHOOK_SECRET = SECRET
NOTES = []
appmod._notify_xiaolongxia = lambda text, *a, **k: NOTES.append(text) or True
appmod._CLOUD_PUSH_LAST.clear()
cloud = push("rongtree", ref="refs/heads/claude/rongtree-redesign")
cloud["commits"] = [{"message": "榮樹下改版：主題清單\n\n細節"}]
CALLS.clear()
r = send(cloud)
check("雲端分支推送 → 通知教練一次（含倉庫與分支與最新說明），且不同步正式站",
      r.status_code == 200 and len(NOTES) == 1 and "rongtree" in NOTES[0] and "claude/rongtree-redesign" in NOTES[0]
      and "榮樹下改版：主題清單" in NOTES[0] and not CALLS)
r = send(cloud)
check("同一分支 10 分鐘內再推 → 不重複通知", len(NOTES) == 1)
r = send(push("rongtree", ref="refs/heads/feature/x"))
check("一般分支（非 claude/*）→ 不通知", len(NOTES) == 1)
gone = push("rongtree", ref="refs/heads/claude/other"); gone["deleted"] = True
r = send(gone)
check("刪除分支 → 不通知", len(NOTES) == 1)
appmod._notify_xiaolongxia = lambda *a, **k: True

appmod.GITHUB_WEBHOOK_SECRET = ""
r = send(push("111-wei"))
check("伺服器沒設暗號 → 一律 403", r.status_code == 403 and not CALLS)

print(f"\n{'全部通過' if not fails else '失敗 ' + str(len(fails)) + ' 項'}")
raise SystemExit(1 if fails else 0)
