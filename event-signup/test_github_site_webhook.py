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
appmod.GITHUB_WEBHOOK_SECRET = ""
r = send(push("111-wei"))
check("伺服器沒設暗號 → 一律 403", r.status_code == 403 and not CALLS)

print(f"\n{'全部通過' if not fails else '失敗 ' + str(len(fails)) + ' 項'}")
raise SystemExit(1 if fails else 0)
