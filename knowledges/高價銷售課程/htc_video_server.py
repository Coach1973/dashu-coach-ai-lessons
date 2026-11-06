#!/usr/bin/env python3
"""高價銷售課程：只讀影片伺服器（Mac 本機，經 cloudflared 通道對外）。
- 只提供 ~/amber-Videos 底下的 .mp4，GET/HEAD，支援 Range（拖曳進度條）
- 網址是 /v/<16 碼雜湊>.mp4，不可猜；沒有目錄列表；只回應來自 bymyway.com 的嵌入（Referer/Origin 檢查）
- 對照表寫進 htc_videos.json（WEEK、檔名 → 網址代碼），上架課程時用
用法：python3 htc_video_server.py            # 開伺服器 127.0.0.1:5075
      python3 htc_video_server.py --manifest # 只重建對照表"""
import hashlib, json, os, re, sys, unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.expanduser("~/amber-Videos")
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "htc_videos.json")
PORT = 5075
ALLOWED = re.compile(r"^https://(www\.)?bymyway\.com(/|$)")
SECRET = "htc-video-v1"  # 只用來讓代碼不可由檔名推回；非密碼

def code(rel):
    return hashlib.sha256((SECRET + unicodedata.normalize("NFC", rel)).encode()).hexdigest()[:16]

def scan():
    out = {}
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f.startswith(".") or not f.lower().endswith(".mp4"): continue
            p = os.path.join(dp, f)
            rel = unicodedata.normalize("NFC", os.path.relpath(p, ROOT))
            out[code(rel)] = {"rel": rel, "size": os.path.getsize(p)}
    return out

def write_manifest():
    m = scan()
    if m:  # Amber 還沒掛上（開機剛啟動）時掃到 0 支，不能蓋掉舊對照表
        json.dump(m, open(MANIFEST, "w"), ensure_ascii=False, indent=1)
        return m
    try: return json.load(open(MANIFEST))
    except Exception: return {}

class H(BaseHTTPRequestHandler):
    server_version = "htc"
    def log_message(self, *a): pass
    def _deny(self, c=403): self.send_response(c); self.end_headers()
    def _serve(self, head):
        m = re.match(r"^/v/([0-9a-f]{16})\.mp4$", self.path.split("?")[0])
        if not m: return self._deny(404)
        ref = self.headers.get("Referer", "") or self.headers.get("Origin", "")
        if not ALLOWED.match(ref): return self._deny(403)
        ent = self.server.catalog.get(m.group(1))
        if not ent: return self._deny(404)
        p = os.path.join(ROOT, ent["rel"])
        try: size = os.path.getsize(p)
        except OSError: return self._deny(404)
        a, b = 0, size - 1
        rg = re.match(r"bytes=(\d*)-(\d*)$", self.headers.get("Range", ""))
        status = 200
        if rg and (rg.group(1) or rg.group(2)):
            if rg.group(1): a = int(rg.group(1)); b = int(rg.group(2)) if rg.group(2) else size - 1
            else: a = max(0, size - int(rg.group(2)))
            b = min(b, size - 1)
            if a > b: return self._deny(416)
            status = 206
        self.send_response(status)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(b - a + 1))
        if status == 206: self.send_header("Content-Range", f"bytes {a}-{b}/{size}")
        self.send_header("Cache-Control", "private, max-age=3600")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if head: return
        try:
            with open(p, "rb") as f:
                f.seek(a); left = b - a + 1
                while left > 0:
                    buf = f.read(min(1 << 20, left))
                    if not buf: break
                    self.wfile.write(buf); left -= len(buf)
        except (BrokenPipeError, ConnectionResetError): pass
    def do_GET(self): self._serve(False)
    def do_HEAD(self): self._serve(True)
    def do_POST(self): self._deny(405)
    do_PUT = do_DELETE = do_PATCH = do_POST

if __name__ == "__main__":
    cat = write_manifest()
    if "--manifest" in sys.argv:
        print(f"對照表 {len(cat)} 支 → {MANIFEST}"); sys.exit(0)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    srv.catalog = cat
    print(f"htc 影片伺服器 127.0.0.1:{PORT}，{len(cat)} 支", flush=True)
    srv.serve_forever()
