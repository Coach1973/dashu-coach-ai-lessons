#!/usr/bin/env python3
"""
產業服務鏈圖片生成：呼叫lk888 AIX聚合引擎的gpt-image-2模型，
輸入完整prompt，輸出PNG圖片，可選擇直接推送Telegram。

用法：
  python3 generate_industry_chain.py --prompt "..." [--out /path/to/file.png] [--telegram-chat-id 6124913915] [--caption "說明文字"]
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/generations"
# 2026-09-19兩個AI各自跑同一個產業鏈SOP，教練收到6張圖、雙倍扣lk888點數。
# 同一主題送同一個對話，10分鐘內只做一次。
DEDUP_DIR = Path("/tmp/industry_chain_dedup")
DEDUP_SECONDS = 600


def dedup_claim(args):
    """回傳 (lock路徑, None) 表示可以做；(None, (主題, 幾秒前)) 表示重複要跳過。"""
    topic = (args.topic or re.sub(r"(的)?產業(服務)?[鏈鍊]圖?$", "", (args.caption or "").strip()).strip() or args.prompt)
    raw = f"{args.telegram_chat_id or '-'}|{re.sub(r'\s+', '', topic)}"
    lock = DEDUP_DIR / f"{hashlib.sha1(raw.encode('utf-8')).hexdigest()[:16]}.lock"
    DEDUP_DIR.mkdir(parents=True, exist_ok=True)
    if lock.exists():
        age = time.time() - lock.stat().st_mtime
        if age < DEDUP_SECONDS:
            return None, (topic, age)
        lock.unlink(missing_ok=True)
    try:
        os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        return None, (topic, 0)
    return lock, None


def get_api_key():
    text = CRED_FILE.read_text(encoding="utf-8")
    m = re.search(r"^API Key：(sk-\S+)", text, re.MULTILINE)
    if not m:
        raise RuntimeError("路徑大全_憑證層.md 裡找不到 lk888 API Key")
    return m.group(1)


def get_telegram_bot_token(config_path: str = None, account: str = "bot_main"):
    cfg_path = Path(config_path) if config_path else Path.home() / ".openclaw" / "openclaw.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"][account]["botToken"]


def generate_image(prompt: str, size: str = "1024x1024") -> bytes:
    api_key = get_api_key()
    payload = json.dumps({"model": "gpt-image-2", "prompt": prompt, "size": size}).encode("utf-8")
    req = urllib.request.Request(
        LK888_API_URL,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    b64 = data["data"][0]["b64_json"]
    return base64.b64decode(b64)


def send_telegram_photo(chat_id: str, image_path: Path, caption: str = "", config_path: str = None, account: str = "bot_main"):
    bot_token = get_telegram_bot_token(config_path, account)
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----IndustryChainBoundary"
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8"))
    if caption:
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode(
            "utf-8"
        )
    )
    body.append(image_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if not result.get("ok"):
        raise RuntimeError(f"Telegram送出失敗: {result}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--out", default=None)
    parser.add_argument("--telegram-chat-id", default=None)
    parser.add_argument("--caption", default="")
    parser.add_argument("--openclaw-config", default=None, help="非預設環境（如小二 ~/.openclaw-test2/openclaw.json）時指定")
    parser.add_argument("--telegram-account", default="bot_main", help="要用哪個bot帳號送出，例如 bot_test2")
    parser.add_argument("--topic", default=None, help="防重複用的主題；沒給就從--caption推")
    parser.add_argument("--force", action="store_true", help="略過10分鐘防重複")
    args = parser.parse_args()

    lock = None
    if not args.force:
        lock, dup = dedup_claim(args)
        if dup:
            print(f"⏭️ 「{dup[0]}」{int(dup[1])}秒前才生成過同一張，10分鐘內不重複扣點，這次跳過（真的要重做請加 --force）")
            return
    try:
        image_bytes = generate_image(args.prompt, args.size)
    except Exception:
        if lock:
            lock.unlink(missing_ok=True)  # 生圖失敗要讓下一次能重試，不能被鎖10分鐘
        raise

    if args.out:
        out_path = Path(args.out)
    else:
        slug = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = WORKSPACE / "claude-brain" / "data" / f"industry_chain_{slug}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)
    print(f"圖片已存檔：{out_path}")

    if args.telegram_chat_id:
        send_telegram_photo(args.telegram_chat_id, out_path, args.caption, args.openclaw_config, args.telegram_account)
        print(f"已推送Telegram（chat_id={args.telegram_chat_id}，帳號={args.telegram_account}）")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        sys.exit(1)
