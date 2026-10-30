#!/usr/bin/env python3
"""VisionStory API 客戶端（talking-avatar 影片／TTS）。文件：https://developers.visionstory.ai/

金鑰：環境變數 VISIONSTORY_API_KEY；沒有就讀 workspace/路徑大全_憑證層.md 的「VisionStory API」段。
不印金鑰、錯誤訊息一律遮蔽。只用標準函式庫。

用法：
  python3 scripts/visionstory_api.py credits                 # 剩餘點數（唯讀、不扣點）
  python3 scripts/visionstory_api.py models                  # 影片模型
  python3 scripts/visionstory_api.py avatars [--public]      # 頭像清單
  python3 scripts/visionstory_api.py voices [--locale zh-TW] # 聲音清單
  python3 scripts/visionstory_api.py create-video --avatar-id ID --voice-id ID --text "…" \\
        [--model vs_character_v4] [--aspect 9:16] [--resolution 720p] [--output out.mp4]   # 會扣點數
  python3 scripts/visionstory_api.py video-status VIDEO_ID
  python3 scripts/visionstory_api.py tts --voice-id ID --text "…" [--output out.mp3]        # 會扣點數
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request, uuid

BASE = "https://openapi.visionstory.ai"
CRED = os.path.expanduser("~/.openclaw/workspace/路徑大全_憑證層.md")


def get_key():
    k = os.environ.get("VISIONSTORY_API_KEY")
    if k:
        return k.strip()
    try:
        txt = open(CRED, encoding="utf-8").read()
        m = re.search(r"VisionStory API.*?(sk-vs-[A-Za-z0-9]+)", txt, re.S)
        if m:
            return m.group(1)
    except OSError:
        pass
    sys.exit("找不到 VisionStory 金鑰（環境變數或路徑大全_憑證層.md）")


def redact(s, key):
    return s.replace(key, "sk-vs-***") if key else s


def call(method, path, params=None, body=None):
    key = get_key()
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-API-Key", key)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %s：%s" % (e.code, redact(e.read().decode("utf-8", "ignore"), key)[:500]))


def download(url, out):
    with urllib.request.urlopen(url, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())
    return out


def show(d):
    print(json.dumps(d, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("credits")
    sub.add_parser("models")
    p = sub.add_parser("avatars"); p.add_argument("--public", action="store_true"); p.add_argument("--limit", type=int, default=20)
    p = sub.add_parser("voices"); p.add_argument("--locale"); p.add_argument("--limit", type=int, default=20)
    p = sub.add_parser("create-video")
    p.add_argument("--avatar-id", required=True); p.add_argument("--voice-id", required=True)
    p.add_argument("--text", required=True); p.add_argument("--model", default="vs_character_v4")
    p.add_argument("--aspect", default="9:16"); p.add_argument("--resolution", default="720p")
    p.add_argument("--speech-rate", default="normal"); p.add_argument("--output", default="result.mp4")
    p = sub.add_parser("video-status"); p.add_argument("video_id")
    p = sub.add_parser("tts")
    p.add_argument("--voice-id", required=True); p.add_argument("--text", required=True)
    p.add_argument("--locale"); p.add_argument("--speech-rate", default="normal"); p.add_argument("--output", default="speech.mp3")
    a = ap.parse_args()

    if a.cmd == "credits":
        show(call("GET", "/api/v1/billing/credits"))
    elif a.cmd == "models":
        show(call("GET", "/api/v1/models"))
    elif a.cmd == "avatars":
        show(call("GET", "/api/v1/avatars", {"is_public": "true" if a.public else None, "limit": a.limit}))
    elif a.cmd == "voices":
        show(call("GET", "/api/v1/voices", {"locale": a.locale, "limit": a.limit}))
    elif a.cmd == "video-status":
        show(call("GET", "/api/v1/video", {"video_id": a.video_id}))
    elif a.cmd == "create-video":
        body = {"model_id": a.model, "avatar_id": a.avatar_id, "client_request_id": uuid.uuid4().hex,
                "text_script": {"text": a.text, "voice_id": a.voice_id, "speech_rate": a.speech_rate},
                "aspect_ratio": a.aspect, "resolution": a.resolution}
        vid = call("POST", "/api/v1/video", body)["data"]["video_id"]
        print("video_id:", vid)
        deadline = time.time() + 600
        while time.time() < deadline:
            time.sleep(5)
            d = call("GET", "/api/v1/video", {"video_id": vid}).get("data", {})
            st = d.get("status")
            print("status:", st)
            if st == "created":
                print("已存：", download(d["video_url"], a.output))
                return
            if st == "failed":
                sys.exit("生成失敗：" + json.dumps(d, ensure_ascii=False)[:500])
        sys.exit("等超過 10 分鐘，video_id=%s，稍後用 video-status 查" % vid)
    elif a.cmd == "tts":
        body = {"text": a.text, "voice_id": a.voice_id, "speech_rate": a.speech_rate}
        if a.locale:
            body["locale"] = a.locale
        show(call("POST", "/api/v1/tts", body))


if __name__ == "__main__":
    main()
