#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""報名通知含關鍵字 → 同步轉進 LINE 群 的回歸測試（教練 2026-10-19「香檳下午茶」→「小旭老師報名通知」群）

不碰網路、不寫真的 log：urlopen 換成假的、金鑰檔與失敗紀錄檔都指到暫存資料夾，
所以不會真的在教練的 Telegram 群或 LINE 群發任何訊息。
執行：cd event-signup && ./venv/bin/python test_line_group_forward.py"""
import json
import os
import tempfile
import threading
import urllib.error

import app as appmod

fails = []


def check(label, cond, detail=""):
    print(("✅" if cond else "❌"), label, "" if cond else f"→ {detail}")
    if not cond:
        fails.append(label)


TMP = tempfile.mkdtemp(prefix="line_forward_test_")
CFG = os.path.join(TMP, "openclaw.json")
with open(CFG, "w", encoding="utf-8") as f:
    json.dump({"channels": {"line": {"channelAccessToken": "FAKE-LINE-TOKEN"},
                            "telegram": {"accounts": {"bot_main": {"botToken": "FAKE-TG-TOKEN"}}}}}, f)
appmod.OPENCLAW_CONFIG_PATH = CFG
appmod.NOTIFY_FAIL_LOG = os.path.join(TMP, "notify_failures.log")
# 常設禁令閘門（教練 2026-10-20）：測試用暫存資料夾當 state，預設先放一面「已許可」旗標，
# 讓底下原本要驗「會推播」的案例照舊；最後一段再作廢旗標，驗證預設就是擋。
appmod.LINE_PUSH_STATE_DIR = TMP + os.sep
APPROVAL_FLAG = os.path.join(TMP, "LINE_PUSH_APPROVED")
open(APPROVAL_FLAG, "w").close()

GROUP = appmod.GROUP_FORWARD_RULES[0]["group_id"]
SAMPLE = ("【大樹小講・官網報名】\n場次：香檳下午茶國際禮儀沙龍｜台灣形象設計發展協會（台南・11/09）\n"
          "姓名：測試勿理\n公司：測試公司\n電話：0900000001\nEmail：t@example.com\n（新報名，由bymyway.com官方發送）")

CALLS = []
STATE = {"used": 27, "limit": 200, "push_error": False, "tg_error": False}


class FakeResp:
    def __init__(self, data):
        self._d = json.dumps(data).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._d


def fake_urlopen(req, timeout=None):
    url = req.full_url
    body = json.loads(req.data.decode("utf-8")) if req.data else None
    CALLS.append({"url": url, "auth": req.get_header("Authorization"), "body": body})
    if url.endswith("/message/quota"):
        return FakeResp({"type": "limited", "value": STATE["limit"]})
    if url.endswith("/message/quota/consumption"):
        return FakeResp({"totalUsage": STATE["used"]})
    if url.endswith("/message/push"):
        if STATE["push_error"]:
            raise urllib.error.HTTPError(url, 429, "quota", {}, None)
        return FakeResp({})
    if "api.telegram.org" in url:
        if STATE["tg_error"]:
            raise urllib.error.URLError("測試用：Telegram 連不上")
        return FakeResp({"ok": True})
    raise AssertionError("測試不該打到這個網址：" + url)


appmod.urllib.request.urlopen = fake_urlopen


def reset(used=27, push_error=False, tg_error=False):
    CALLS.clear()
    STATE.update(used=used, push_error=push_error, tg_error=tg_error)
    open(appmod.NOTIFY_FAIL_LOG, "w").close()


def fail_log():
    return open(appmod.NOTIFY_FAIL_LOG, encoding="utf-8").read()


def pushes():
    return [c for c in CALLS if c["url"].endswith("/message/push")]


# 1. 含關鍵字：推進對的群、內容一字不差、用的是 LINE 金鑰
reset()
appmod._forward_by_keyword(SAMPLE)
p = pushes()
check("含「香檳下午茶」→ 推一則", len(p) == 1, str(CALLS))
if p:
    check("收件群是小旭老師報名通知", p[0]["body"]["to"] == GROUP, p[0]["body"])
    check("內容與 Telegram 那則一字不差", p[0]["body"]["messages"][0]["text"] == SAMPLE)
    check("用 LINE 金鑰（不是 Telegram 的）", p[0]["auth"] == "Bearer FAKE-LINE-TOKEN", p[0]["auth"])
check("成功時沒有失敗紀錄", fail_log() == "", fail_log())

# 2. 沒有關鍵字：一個 HTTP 都不打
reset()
appmod._forward_by_keyword("【大樹小講・官網報名】\n場次：AI微論壇\n姓名：某人")
check("沒提到香檳下午茶 → 完全不打 LINE", CALLS == [], str(CALLS))

# 3. 額度快用完（剩 20 < 保留線 30）：不推、留紀錄
reset(used=180)
appmod._forward_by_keyword(SAMPLE)
check("額度剩 20 則 → 不推", pushes() == [], str(pushes()))
check("額度不足有寫進失敗紀錄", "額度剩 20" in fail_log(), fail_log())

# 4. 額度剛好在保留線上（剩 30）：照推
reset(used=170)
appmod._forward_by_keyword(SAMPLE)
check("額度剩 30 則 → 照推", len(pushes()) == 1)

# 5. LINE 回 429：不丟例外、留紀錄
reset(push_error=True)
try:
    appmod._forward_by_keyword(SAMPLE)
    raised = False
except Exception:
    raised = True
check("LINE 推播失敗不會丟例外出去", not raised)
check("LINE 推播失敗有寫紀錄", "429" in fail_log(), fail_log())

# 6. 讀不到金鑰檔：不丟例外、留紀錄
reset()
good = appmod.OPENCLAW_CONFIG_PATH
appmod.OPENCLAW_CONFIG_PATH = os.path.join(TMP, "不存在.json")
try:
    appmod._forward_by_keyword(SAMPLE)
    raised = False
except Exception:
    raised = True
appmod.OPENCLAW_CONFIG_PATH = good
check("讀不到金鑰檔不丟例外", not raised)
check("讀不到金鑰檔有寫紀錄", "金鑰" in fail_log(), fail_log())

# 7. 真的從出口 _notify_xiaolongxia 走：報名群會轉、教練個人對話不轉
SEEN = []
done = threading.Event()
real_forward = appmod._forward_by_keyword
appmod._forward_by_keyword = lambda t: (SEEN.append(t), done.set())

reset()
done.clear()
appmod._notify_xiaolongxia(SAMPLE, chat_id=appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
check("發到「活動報名即時通知」群時會觸發轉發", done.wait(3) and SEEN == [SAMPLE], str(SEEN))
check("Telegram 那則照發", any("api.telegram.org" in c["url"] for c in CALLS))

SEEN.clear()
done.clear()
appmod._notify_xiaolongxia(SAMPLE, chat_id=appmod.TELEGRAM_NOTIFY_CHAT_ID)
check("發給教練個人對話時不轉發", not done.wait(0.5) and SEEN == [], str(SEEN))
appmod._forward_by_keyword = real_forward

# 8. Telegram 專屬群規則（教練 10/20：另開「小旭老師活動報名通知」Telegram 群，不扣 LINE 額度）
TG_TARGET = "-1009999999999"
saved_rules = appmod.GROUP_FORWARD_RULES
rule_tg = {"keyword": "香檳下午茶", "telegram_chat_id": TG_TARGET, "name": "小旭老師活動報名通知"}
rule_line = saved_rules[0]


def tg_calls():
    return [c for c in CALLS if "api.telegram.org" in c["url"]]


appmod.GROUP_FORWARD_RULES = [rule_tg]
reset()
appmod._forward_by_keyword(SAMPLE)
check("Telegram 規則：轉進指定 Telegram 群一則", len(tg_calls()) == 1 and tg_calls()[0]["body"]["chat_id"] == TG_TARGET, str(CALLS))
check("Telegram 轉發內容與原通知一字不差", bool(tg_calls()) and tg_calls()[0]["body"]["text"] == SAMPLE)
check("Telegram 規則不碰 LINE（不查額度、不推播）", all("api.line.me" not in c["url"] for c in CALLS), str(CALLS))

reset()
appmod._forward_by_keyword("【大樹小講・官網報名】\n場次：AI微論壇\n姓名：某人")
check("沒提到關鍵字 → Telegram 規則也完全不發", CALLS == [], str(CALLS))

reset(tg_error=True)
try:
    appmod._forward_by_keyword(SAMPLE)
    raised = False
except Exception:
    raised = True
check("Telegram 轉發失敗不丟例外", not raised)
check("Telegram 轉發失敗有寫紀錄（含目標群編號）", TG_TARGET in fail_log(), fail_log())

# 兩種規則並存、LINE 額度又不夠：Telegram 照轉，LINE 不推、留紀錄
appmod.GROUP_FORWARD_RULES = [rule_tg, rule_line]
reset(used=190)
appmod._forward_by_keyword(SAMPLE)
check("並存：LINE 額度不夠時 Telegram 照轉", len(tg_calls()) == 1)
check("並存：LINE 額度不夠時 LINE 不推", pushes() == [], str(pushes()))
check("並存：LINE 額度不足有留紀錄", "額度剩 10" in fail_log(), fail_log())
appmod.GROUP_FORWARD_RULES = saved_rules

# 9. 常設禁令閘門：沒有教練許可旗標 → LINE 推播一則都不能發（不打 push 網址），但會留下紀錄
appmod.GROUP_FORWARD_RULES = [rule_line]
os.utime(APPROVAL_FLAG, (946684800, 946684800))  # 旗標作廢（mtime 設回 2000 年）
reset(used=27)
appmod._forward_by_keyword(SAMPLE)
check("閘門：沒有許可 → 不發任何 LINE 推播", pushes() == [], str(pushes()))
check("閘門：沒有許可 → 擋下有寫進 line_push_blocked.log",
      os.path.exists(os.path.join(TMP, "line_push_blocked.log")) and "event-signup-forward" in open(os.path.join(TMP, "line_push_blocked.log"), encoding="utf-8").read())
check("閘門：沒有許可 → 原文留進 notify_failures.log 可事後補轉", "常設禁令" in fail_log() and "測試勿理" in fail_log(), fail_log())
os.utime(APPROVAL_FLAG, None)  # 旗標更新成現在 → 放行
reset(used=27)
appmod._forward_by_keyword(SAMPLE)
check("閘門：有許可旗標 → 照推一則", len(pushes()) == 1, str(CALLS))
appmod.GROUP_FORWARD_RULES = saved_rules

print()
print("全部通過" if not fails else f"❌ {len(fails)} 項沒過：{fails}")
raise SystemExit(1 if fails else 0)
