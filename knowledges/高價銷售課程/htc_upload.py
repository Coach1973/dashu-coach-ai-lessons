#!/usr/bin/env python3
"""高價銷售課程：把 Amber Videos 的檔案傳到 bymyway.com 媒體庫（直連源站，繞過 Cloudflare 100MB 上限）。
用法：python3 htc_upload.py docs            # 全部附件
      python3 htc_upload.py videos WEEK1    # 指定週的影片
結果累積寫進 htc_media.json（已傳過的會跳過，可重跑）。"""
import json, os, subprocess, sys, unicodedata, hashlib

ROOT = os.path.expanduser("~/amber-Videos")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "htc_media.json")
def _auth():
    # 密碼不放程式裡：執行時從憑證層讀 WordPress bymyway.com 應用程式密碼
    import re
    txt = open(os.path.expanduser("~/.openclaw/workspace/路徑大全_憑證層.md"), encoding="utf-8").read()
    m = re.search(r"應用程式密碼：([A-Za-z0-9 ]+)", txt)
    return "bymyway7:" + m.group(1).strip()
AUTH = _auth()
ORIGIN = "64.176.38.233"
WEEKS = ["WEEK1","WEEK2","WEEK3","WEEK4","WEEK5","WEEK6","WEEK7","WEE8","WEEK9","WEEK10","WEEK11","WEEK12"]
MIME = {".mp4":"video/mp4",".pdf":"application/pdf",".xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation",".png":"image/png",".zip":"application/zip",".txt":"text/plain"}

def load():
    try: return json.load(open(OUT))
    except Exception: return {}

def save(d):
    json.dump(d, open(OUT,"w"), ensure_ascii=False, indent=1)

def week_no(w): return 0 if w=="." else WEEKS.index(w)+1

def slug(week, rel):
    base, ext = os.path.splitext(os.path.basename(rel))
    h = hashlib.md5(unicodedata.normalize("NFC", rel).encode()).hexdigest()[:8]
    return f"htc-w{week_no(week):02d}-{h}{ext.lower()}"

def upload(path, name, mime):
    r = subprocess.run(["curl","-sk","--max-time","3600","-u",AUTH,"--resolve",f"www.bymyway.com:443:{ORIGIN}",
        "-X","POST","https://www.bymyway.com/wp-json/wp/v2/media","-H",f"Content-Type: {mime}",
        "-H",f"Content-Disposition: attachment; filename={name}","--data-binary",f"@{path}",
        "-w","\n%{http_code}"], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    try: j = json.loads(body)
    except Exception: j = {}
    return code, j

def files(kind, weeks):
    for w in weeks:
        d = ROOT if w=="." else os.path.join(ROOT, w)
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.startswith(".") or not os.path.isfile(p): continue
            ext = os.path.splitext(f)[1].lower()
            if (kind=="videos") == (ext==".mp4") and ext in MIME:
                yield w, os.path.relpath(p, ROOT), p, ext

if __name__ == "__main__":
    kind = sys.argv[1]
    weeks = sys.argv[2:] or (["."]+WEEKS)
    db = load()
    for w, rel, p, ext in files(kind, weeks):
        key = unicodedata.normalize("NFC", rel)
        if key in db and db[key].get("id"):
            print("略過（已傳）", key, flush=True); continue
        name = slug(w, rel)
        size = os.path.getsize(p)
        if size > 150_000_000:
            print(f"跳過（>150MB，bymyway.com 主機實測 ≥200MB 上傳會 500，2026-11-06）{key} {size/1e6:.0f}MB", flush=True); continue
        code, j = upload(p, name, MIME[ext])
        if code == "201" and j.get("id"):
            db[key] = {"id": j["id"], "url": j["source_url"], "week": week_no(w), "title": os.path.splitext(os.path.basename(rel))[0], "size": size}
            save(db)
            print(f"OK {code} {j['id']} {key} {size/1e6:.0f}MB", flush=True)
        else:
            print(f"失敗 {code} {key} {str(j)[:300]}", flush=True)
            sys.exit(2)
    print("完成", kind, weeks, flush=True)
