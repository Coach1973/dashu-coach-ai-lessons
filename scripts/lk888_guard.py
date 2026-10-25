#!/usr/bin/env python3
"""LK888 收費閘門：所有會花錢的 LK888 出圖呼叫都必須經過這裡。

起因（試金石案例85，2026-09-26）：小龍蝦在同一回合裡把教練一句「直接跑下一張」
當成新指令重跑 21 次（p04）、15 次（p10），教練實際只要 28 張，LK888 後台出了 96 張，
額度燒光。9/19 也發生過兩個 AI 重複跑同一張、雙倍扣點。模型會鬼打牆，所以擋在花錢這一關。

用法（腳本端）：把打 LK888 的那一行
    with urllib.request.urlopen(req, timeout=180) as resp:
換成
    with lk888_guard.urlopen(req, timeout=180) as resp:
其餘程式不用改。非 LK888 的網址會原樣放行。

規則：
  1. 一模一樣的出圖要求 24 小時內只付一次錢，再叫直接回傳上次的圖（不扣點）。
  2. 教練明說重畫才可設 LK888_REDO=1；同一張 5 分鐘內不准連續重畫。
  3. 同一張 24 小時內最多付費 3 次。
  4. 超過上限要繼續，必須教練同意後 touch state/LK888_APPROVED（10 分鐘有效）。

  （2026-10-26 教練「不需要設限，請繼續」→ 已移除每小時付費總量上限與暫停通知機制；
    同一張 24 小時上限、5 分鐘重畫間隔、24 小時 cache、核准 token 仍在。）
  5. 兩個程式同時要畫同一張，第二個排隊等第一個畫完，直接拿結果。

  6. 多組金鑰備援（2026-09-26教練開第二個帳戶）：路徑大全_憑證層.md 的 lk888 段落可放多行
     「API Key：sk-...」，第一行是主要的；某組回報額度/餘額不足時，同一次請求自動改用下一組，
     不重跑、不多扣（額度不足的請求沒有出圖，本來就不扣點）。

查帳：python3 scripts/lk888_guard.py report [--hours 24]
"""

import base64
import fcntl
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
STATE = WORKSPACE / "state"
LEDGER = STATE / "lk888_ledger.jsonl"
CACHE_DIR = STATE / "lk888_cache"
LOCK_DIR = STATE / "lk888_locks"
APPROVAL_TOKEN = STATE / "LK888_APPROVED"

GUARDED_HOST = "api.lk888.ai"
CACHE_TTL = 24 * 3600
REDO_MIN_GAP = 5 * 60
MAX_PAID_PER_IMAGE_24H = 3
APPROVAL_TTL = 10 * 60
LOCK_WAIT_SECONDS = 300
TPE = timezone(timedelta(hours=8))
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
QUOTA_HINTS = ("quota", "insufficient", "balance", "额度", "額度", "余额", "餘額", "exhausted", "用尽", "用盡")


class LK888Blocked(RuntimeError):
    pass


def _now():
    return time.time()


def _caller():
    return Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "unknown"


def _record(event, fp, url_path, redo, detail=""):
    STATE.mkdir(parents=True, exist_ok=True)
    line = {
        "ts": datetime.now(TPE).isoformat(timespec="seconds"),
        "epoch": round(_now(), 3),
        "event": event,
        "fp": fp,
        "caller": _caller(),
        "path": url_path,
        "redo": bool(redo),
        "detail": detail,
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def _ledger(since_epoch):
    if not LEDGER.exists():
        return []
    out = []
    with open(LEDGER, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("epoch", 0) >= since_epoch:
                out.append(d)
    return out


def _approved():
    try:
        return _now() - APPROVAL_TOKEN.stat().st_mtime <= APPROVAL_TTL
    except FileNotFoundError:
        return False


def _fingerprint(req):
    body = req.data or b""
    if isinstance(body, str):
        body = body.encode("utf-8")
    ctype = req.get_header("Content-type") or ""
    if "boundary=" in ctype:
        boundary = ctype.split("boundary=", 1)[1].strip().strip('"').encode("utf-8")
        body = body.replace(boundary, b"")
    h = hashlib.sha256()
    h.update(req.get_method().encode())
    h.update(req.full_url.encode())
    h.update(body)
    return h.hexdigest()[:24]


PEIPEI_DIR = Path.home() / ".openclaw" / "agents" / "peipei"
BAHAI_ALLOWED = {"poster_new_person.py"}


def _bahai_offpath():
    """2026-10-25 教練：巴哈（peipei）做海報只能走 poster_new_person.py 那一行。
    從巴哈資料夾發出、或程式本身放在巴哈資料夾的出圖（舊的自己寫程式那條路），一律擋下。
    10/24 晚巴哈繞路，一個人跑 100 多步、5 小時燒掉 MiniMax 1.18 億 token。"""
    if _caller() in BAHAI_ALLOWED:
        return ""
    cands = []
    for get in (lambda: Path(sys.argv[0]).resolve(), lambda: Path.cwd().resolve()):
        try:
            cands.append(str(get()))
        except Exception:  # noqa: BLE001
            pass
    if os.environ.get("OPENCLAW_AGENT_DIR"):
        cands.append(os.environ["OPENCLAW_AGENT_DIR"])
    if any(c.startswith(str(PEIPEI_DIR)) for c in cands):
        return ("巴哈做海報只能跑這一行，不准自己寫程式、裁照片、寫提示詞："
                "python3 ~/.openclaw/workspace/scripts/poster_new_person.py --photo <照片> --name <名字> --role <職稱> "
                "--titles \"<頭銜1>/<頭銜2>\"（只重做一張加 --only 橫版 或 --only 直版）")
    return ""


def _block(fp, url_path, redo, reason):
    _record("blocked", fp, url_path, redo, reason)
    msg = f"🛑 LK888收費閘門擋下（沒有扣點）：{reason}"
    print(msg, file=sys.stderr)
    raise LK888Blocked(msg)


def _normalize_for_cache(raw):
    """把回應裡的圖片網址先下載成 b64 存起來，避免快取的網址過期。"""
    try:
        d = json.loads(raw.decode("utf-8"))
    except ValueError:
        return raw
    changed = False
    for item in d.get("data") or []:
        if isinstance(item, dict) and not item.get("b64_json") and item.get("url"):
            try:
                with urllib.request.urlopen(item["url"], timeout=120) as r:
                    item["b64_json"] = base64.b64encode(r.read()).decode("ascii")
                changed = True
            except Exception:
                pass
    return json.dumps(d).encode("utf-8") if changed else raw


class _Resp(io.BytesIO):
    status = 200

    def getcode(self):
        return 200

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def _cached(fp):
    p = CACHE_DIR / f"{fp}.json"
    try:
        if _now() - p.stat().st_mtime <= CACHE_TTL:
            return p.read_bytes()
    except FileNotFoundError:
        pass
    return None


def _prune_cache():
    if not CACHE_DIR.exists():
        return
    cutoff = _now() - CACHE_TTL
    for p in CACHE_DIR.glob("*.json"):
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
        except FileNotFoundError:
            pass


def urlopen(req, timeout=None, **kwargs):
    if isinstance(req, str) or GUARDED_HOST not in req.full_url or req.get_method() != "POST":
        return urllib.request.urlopen(req, timeout=timeout, **kwargs)

    redo = os.environ.get("LK888_REDO") == "1"
    fp = _fingerprint(req)
    url_path = req.full_url.split(GUARDED_HOST, 1)[1]
    off = _bahai_offpath()
    if off:
        _block(fp, url_path, redo, off)
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOCK_DIR / f"{fp}.lock", "w") as lock:
        deadline = _now() + LOCK_WAIT_SECONDS
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if _now() > deadline:
                    _block(fp, url_path, redo, "同一張圖另一個程式正在畫，等了5分鐘還沒畫完，請稍後再查結果，不要重跑")
                time.sleep(2)

        if not redo:
            cached = _cached(fp)
            if cached is not None:
                hits = sum(1 for d in _ledger(_now() - CACHE_TTL) if d["fp"] == fp and d["event"] == "cache_hit") + 1
                _record("cache_hit", fp, url_path, redo, f"第{hits}次重複要求")
                print(f"♻️ LK888收費閘門：這張圖剛才已經畫好了（24小時內第{hits}次重複要求），"
                      f"已免費回傳同一張，沒有扣點。不要再重跑，直接把這張交給教練並結束這一輪。",
                      file=sys.stderr)
                return _Resp(cached)

        recent = _ledger(_now() - 24 * 3600)
        mine = [d for d in recent if d["fp"] == fp and d["event"] == "attempt"]
        if redo and mine and _now() - mine[-1]["epoch"] < REDO_MIN_GAP:
            ago = int(_now() - mine[-1]["epoch"])
            _block(fp, url_path, redo, f"同一張圖{ago}秒前才付費畫過，5分鐘內不准再重畫（疑似鬼打牆重跑）。請先把已畫好的圖交給教練")
        if len(mine) >= MAX_PAID_PER_IMAGE_24H and not _approved():
            _block(fp, url_path, redo, f"同一張圖24小時內已付費{len(mine)}次，達上限。請停下來問教練；教練同意後才可 touch ~/.openclaw/workspace/state/LK888_APPROVED（10分鐘有效）")
        _record("attempt", fp, url_path, redo)
        try:
            raw = _send_with_key_failover(req, fp, url_path, redo, timeout, kwargs)
        except Exception as e:
            _record("fail", fp, url_path, redo, f"{type(e).__name__}: {str(e)[:200]}")
            raise
        _record("success", fp, url_path, redo)
        (CACHE_DIR / f"{fp}.json").write_bytes(_normalize_for_cache(raw))
        _prune_cache()
        return _Resp(raw)


def _all_keys():
    """路徑大全_憑證層.md 的 lk888 段落裡所有「API Key：sk-...」，照出現順序（第一行＝主要）。"""
    try:
        text = CRED_FILE.read_text(encoding="utf-8")
    except OSError:
        return []
    keys, in_lk = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            in_lk = "lk888" in line.lower()
        elif in_lk and line.startswith("API Key：sk-"):
            keys.append(line.split("：", 1)[1].strip())
    return keys


def _is_quota_error(e):
    if not isinstance(e, urllib.error.HTTPError) or e.code not in (401, 402, 403, 429):
        return False
    try:
        body = e.read().decode("utf-8", "replace").lower()
    except Exception:
        body = ""
    return any(h in body for h in QUOTA_HINTS)


def _send_with_key_failover(req, fp, url_path, redo, timeout, kwargs):
    used = (req.get_header("Authorization") or "").replace("Bearer ", "").strip()
    backups = [k for k in _all_keys() if k != used]
    while True:
        try:
            with urllib.request.urlopen(req, timeout=timeout, **kwargs) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if not backups or not _is_quota_error(e):
                raise
            nxt = backups.pop(0)
            _record("key_failover", fp, url_path, redo, f"HTTP {e.code} 額度不足，改用備援金鑰 …{nxt[-4:]}")
            print(f"🔁 LK888：金鑰 …{used[-4:]} 額度不足，自動改用備援金鑰 …{nxt[-4:]}（同一張，不重跑）", file=sys.stderr)
            req.add_header("Authorization", f"Bearer {nxt}")
            used = nxt


def report(hours=24):
    rows = _ledger(_now() - hours * 3600)
    by_event = {}
    for d in rows:
        by_event[d["event"]] = by_event.get(d["event"], 0) + 1
    print(f"═══ LK888 收費閘門帳本（最近 {hours} 小時）═══")
    print(f"實際付費呼叫：{by_event.get('attempt', 0)} 次（成功 {by_event.get('success', 0)}、失敗 {by_event.get('fail', 0)}）")
    print(f"重複要求免費擋回：{by_event.get('cache_hit', 0)} 次　｜　閘門擋下：{by_event.get('blocked', 0)} 次")
    per = {}
    for d in rows:
        if d["event"] == "attempt":
            key = (d["caller"], d["fp"])
            per[key] = per.get(key, 0) + 1
    multi = {k: v for k, v in per.items() if v > 1}
    if multi:
        print("同一張付費超過一次：")
        for (caller, fp), n in sorted(multi.items(), key=lambda x: -x[1]):
            print(f"  {caller} {fp}：{n} 次")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "report":
        h = 24
        if "--hours" in sys.argv:
            h = float(sys.argv[sys.argv.index("--hours") + 1])
        report(h)
    else:
        print(__doc__)
