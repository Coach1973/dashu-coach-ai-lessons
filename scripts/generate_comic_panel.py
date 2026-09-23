#!/usr/bin/env python3
"""
漫畫插畫生成：lk888 GPT Image 2 + 帶 reference 圖（角色臉部錨點）。
從 generate_industry_chain.py 擴充而來，改走 /v1/images/edits 端點。

用法：
  python3 generate_comic_panel.py \
    --prompt "..." \
    --reference /path/to/face_reference.jpg \
    --size 1536x1024 \
    --telegram-chat-id 6124913915 \
    --caption "漫畫插圖 03｜..."
"""
import argparse
import base64
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/edits"


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


def generate_image_with_reference(prompt: str, reference_image_path: Path, size: str = "1536x1024", model: str = "gpt-image-2") -> bytes:
    api_key = get_api_key()

    # /v1/images/edits 走 multipart/form-data
    boundary = "----ComicPanelBoundary" + datetime.now().strftime("%H%M%S")
    body = []

    # image 欄位（參考臉部照片）
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(
        f'Content-Disposition: form-data; name="image"; filename="{reference_image_path.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode("utf-8")
    )
    body.append(reference_image_path.read_bytes())
    body.append(b"\r\n")

    # prompt 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
    body.append(prompt.encode("utf-8"))
    body.append(b"\r\n")

    # model 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.append(model.encode("utf-8"))
    body.append(b"\r\n")

    # size 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="size"\r\n\r\n')
    body.append(size.encode("utf-8"))
    body.append(b"\r\n")

    body.append(f"--{boundary}--\r\n".encode("utf-8"))

    data = b"".join(body)
    req = urllib.request.Request(
        LK888_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    b64 = result["data"][0]["b64_json"]
    return base64.b64decode(b64)


def send_telegram_photo(chat_id: str, image_path: Path, caption: str = "", config_path: str = None, account: str = "bot_main"):
    bot_token = get_telegram_bot_token(config_path, account)
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----TelegramBoundary" + datetime.now().strftime("%H%M%S")
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8"))
    if caption:
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8")
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
    parser.add_argument("--reference", required=True, help="參考圖路徑（教練的臉部照片）")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1536x1024")
    parser.add_argument("--out", default=None)
    parser.add_argument("--telegram-chat-id", default=None)
    parser.add_argument("--caption", default="")
    parser.add_argument("--telegram-account", default="bot_main")
    args = parser.parse_args()

    reference_path = Path(args.reference)
    if not reference_path.exists():
        raise FileNotFoundError(f"參考圖不存在: {reference_path}")

    image_bytes = generate_image_with_reference(args.prompt, reference_path, args.size, args.model)

    if args.out:
        out_path = Path(args.out)
    else:
        slug = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = WORKSPACE / "claude-brain" / "data" / f"comic_panel_{slug}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)
    print(f"圖片已存檔：{out_path}")

    if args.telegram_chat_id:
        send_telegram_photo(args.telegram_chat_id, out_path, args.caption, None, args.telegram_account)
        print(f"已推送Telegram（chat_id={args.telegram_chat_id}，帳號={args.telegram_account}）")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        sys.exit(1)
