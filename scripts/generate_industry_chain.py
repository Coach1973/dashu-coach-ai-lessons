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
import lk888_guard
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/generations"
# 2026-09-19兩個AI各自跑同一個產業鏈SOP，教練收到6張圖、雙倍扣lk888點數。
# 同一主題送同一個對話，10分鐘內只做一次。
DEDUP_DIR = Path("/tmp/industry_chain_dedup")
DEDUP_SECONDS = 600
# LINE只收公開HTTPS網址的圖（2026-09-30 LINE小龍蝦出完圖送不出去：「LINE outbound media currently requires a public HTTPS URL」），
# 所以放進event.bymyway.com的/chain-img/公開資料夾，檔名帶亂數外人猜不到。
PUBLIC_IMG_DIR = WORKSPACE / "event-signup" / "chain_images"
PUBLIC_IMG_BASE = "https://event.bymyway.com/chain-img/"


def dedup_claim(args):
    """回傳 (lock路徑, None) 表示可以做；(None, (主題, 幾秒前)) 表示重複要跳過。"""
    topic = (args.topic or re.sub(r"(的)?產業(服務)?[鏈鍊]圖?$", "", (args.caption or "").strip()).strip() or args.prompt)
    # 正規式不能放進f-string運算式（Python 3.12前語法錯誤，Hermes用3.11會整支崩潰）
    topic_key = re.sub(r"\s+", "", topic)
    raw = f"{args.telegram_chat_id or '-'}|{topic_key}"
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
    with lk888_guard.urlopen(req, timeout=120) as resp:
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


def notify_failure(args, err):
    """背景出圖失敗時要讓群組知道，不能靜悄悄。"""
    try:
        token = get_telegram_bot_token(args.openclaw_config, args.telegram_account)
        data = json.dumps({"chat_id": args.telegram_chat_id, "text": "這張圖這次沒做成功（已自動放棄，沒有重複扣點），請稍後再說一次，或請教練協助。"}).encode()
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data, headers={"Content-Type": "application/json"}), timeout=20)
    except Exception:
        pass


NODE_COUNT = 20
PROMPT_TEMPLATE = (
    "我需要做一張產業服務鏈，要用手繪可愛風格做出來。中心是「{topic}」的人類角色插畫{center}"
    "（男性或女性皆可，禁止使用動物、擬人化動物或卡通動物造型），手持{held}。"
    "標題：{topic} 夥伴圖。為{audience}，提供從{first}到{last}的完整夥伴支援。"
    "周邊環繞以下 {n} 個專業類別節點，每個節點配精緻手繪 icon：{nodes}。"
    "所有文字必須完全正確、清晰可讀，每個文字都必須是繁體中文（台灣正體字），"
    "禁止使用簡體字、簡體字形、簡體偏旁、簡體異體字、或任何簡體中文變體，"
    "禁止出現任何英文或拼音，絕對不能出現無法顯示的亂碼字、缺漏字或方框字。"
)


def build_prompt_from_nodes(args):
    """正式流程（2026-10-01 教練：以前品質好的做法寫成死流程，不要再花點數試品質）：
    節點必須剛好20個、全部是BNI真實類別，才用核准範本組成圖片描述；不合格直接結束，不呼叫LK888。"""
    import check_industry_chain_names as chk
    names = chk.load_names()
    nodes = [n.strip() for n in re.split(r"[,，、]", args.nodes) if n.strip()]
    bad = []
    for n in nodes:
        kind, close = chk.check_one(n, names)
        if kind != "exact":
            bad.append(f"「{n}」" + (f"→ 最接近的真實類別：{'、'.join(close)}（意思一樣才能換）" if close else "→ BNI詞庫查無，請換掉"))
    if len(nodes) != NODE_COUNT or len(set(nodes)) != len(nodes):
        bad.append(f"節點要剛好 {NODE_COUNT} 個且不重複，目前 {len(nodes)} 個")
    if bad:
        print("❌ 節點不合格，沒有出圖也沒有扣點。請改好這些再下一次指令：\n  " + "\n  ".join(bad))
        sys.exit(2)
    center = f"，外觀：{args.center.strip()}" if args.center.strip() else ""
    return PROMPT_TEMPLATE.format(topic=args.topic, center=center, held=args.held, audience=args.audience,
                                  first=nodes[0], last=nodes[-1], n=len(nodes), nodes="、".join(nodes))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=None, help="完整圖片描述；正式流程改用 --nodes 由範本自動組成")
    parser.add_argument("--nodes", default=None, help="20個BNI真實類別，用逗號分隔；不是全部命中BNI詞庫會在花錢前直接擋下")
    parser.add_argument("--center", default="", help="中心人物外觀，例如「戴眼鏡、長頭髮的女生」")
    parser.add_argument("--held", default="代表性物品", help="中心人物手持的物件")
    parser.add_argument("--audience", default="該產業的老闆與客戶", help="目標客群")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--out", default=None)
    parser.add_argument("--telegram-chat-id", default=None)
    parser.add_argument("--caption", default="")
    parser.add_argument("--openclaw-config", default=None, help="非預設環境（如小二 ~/.openclaw-test2/openclaw.json）時指定")
    parser.add_argument("--telegram-account", default="bot_main", help="要用哪個bot帳號送出，例如 bot_test2")
    parser.add_argument("--topic", default=None, help="防重複用的主題；沒給就從--caption推")
    parser.add_argument("--force", action="store_true", help="略過10分鐘防重複")
    parser.add_argument("--background", action="store_true", help="馬上回覆「已開始」，圖在背景做完後自己送進--telegram-chat-id（出圖要1~2分鐘，呼叫端不必等）")
    parser.add_argument("--_lock", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--publish", action="store_true", help="另存一份到公開網址（LINE送圖要用）")
    args = parser.parse_args()
    if args.nodes:
        if not args.topic:
            print("❌ 用 --nodes 時一定要給 --topic（主題）")
            sys.exit(2)
        args.prompt = build_prompt_from_nodes(args)
    elif not args.prompt:
        print("❌ 要給 --nodes（正式流程）或 --prompt")
        sys.exit(2)

    lock = None
    if not args.force:
        lock, dup = dedup_claim(args)
        if dup:
            print(f"⏭️ 「{dup[0]}」{int(dup[1])}秒前才生成過同一張，10分鐘內不重複扣點，這次跳過（真的要重做請加 --force）")
            return
    if args.background and args.telegram_chat_id:
        # 家長程序只負責「接單」：鎖已搶到，交給脫離終端機的子程序做完並送出，自己立刻回覆
        import subprocess
        child_argv = [a for a in sys.argv[1:] if a != "--background"] + ["--force"]
        if lock:
            child_argv += ["--_lock", str(lock)]
        log = open(WORKSPACE / "state" / "industry_chain_background.log", "a")
        subprocess.Popen([sys.executable, str(Path(__file__).resolve())] + child_argv,
                         stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)
        print("✅ 已開始製作，約 1~2 分鐘後圖會自動傳到群組，不用重複下指令。")
        return
    lock = Path(args._lock) if args._lock else lock
    try:
        image_bytes = generate_image(args.prompt, args.size)
    except Exception as e:
        if lock:
            lock.unlink(missing_ok=True)  # 生圖失敗要讓下一次能重試，不能被鎖10分鐘
        if args.telegram_chat_id and args._lock:
            notify_failure(args, e)
        raise

    if args.out:
        out_path = Path(args.out)
    else:
        slug = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = WORKSPACE / "claude-brain" / "data" / f"industry_chain_{slug}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)
    print(f"圖片已存檔：{out_path}")

    if args.publish:
        PUBLIC_IMG_DIR.mkdir(parents=True, exist_ok=True)
        public_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(6).hex()}.png"
        (PUBLIC_IMG_DIR / public_name).write_bytes(image_bytes)
        print(f"公開網址（LINE送圖用）：{PUBLIC_IMG_BASE}{public_name}")

    if args.telegram_chat_id:
        send_telegram_photo(args.telegram_chat_id, out_path, args.caption, args.openclaw_config, args.telegram_account)
        print(f"已推送Telegram（chat_id={args.telegram_chat_id}，帳號={args.telegram_account}）")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        sys.exit(1)
