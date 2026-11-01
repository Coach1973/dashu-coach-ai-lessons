#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 投遞目標防呆閘門（2026-11-01 建立）
用途：送訊息／圖片到 Telegram 群組前，先查目標是不是自己送錯的那一群。

用法：
  python3 telegram_target_guard.py -5115910257
  python3 telegram_target_guard.py -1003877502911 --expect 佩佩老師
  python3 telegram_target_guard.py -5115910257 --media /path/x.jpg

回傳碼：
  0 = 通過（目標存在，且符合 --expect 的名稱關鍵字）
  2 = 目標不在對照表 → 拒絕送出，請人工確認
  3 = 目標存在，但名稱不符合 --expect → 拒絕送出（送錯群的防線）

背景：2026-11-01 21:32 陳佩君 V5 海報誤投到「頂級特助分工群」，
原因是技能檔把兩個 chat_id 寫反。這支腳本就是那次的補救。
"""
import argparse
import json
import os
import sys

REGISTRY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "state", "telegram_chat_registry.json",
)


def load_registry(path=REGISTRY):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def normalize(target):
    """把 telegram:-5115910257 / chat_id:-5115910257 / -5115910257 / g-5115910257 收斂成純數字字串。

    ⚠️ 2026-11-01 修正：舊版會把「正數字 chat_id」一律加上負號，
    導致 Telegram 私聊（教練 DM = 6124913915）永遠查不到而被誤判為「不在對照表裡」。
    現在不再預設加號，改由 resolve() 先照原字串查表、查不到才試「負號變體」。
    """
    t = str(target).strip()
    if ":" in t:
        t = t.split(":")[-1]
    t = t.replace("chat_id", "").replace("g-", "").strip()
    return t


def resolve(tid, chats):
    """先照原字串查對照表；查不到才試「負號變體」（群組 chat_id 漏寫負號的情況）。"""
    if tid in chats:
        return tid
    if tid and not tid.startswith("-") and tid.isdigit():
        alt = "-" + tid
        if alt in chats:
            return alt
    return None


def main():
    ap = argparse.ArgumentParser(description="Telegram 投遞目標防呆閘門")
    ap.add_argument("target", nargs="?", default=None, help="chat id，例如 -5115910257 或 telegram:-5115910257")
    ap.add_argument("--expect", default=None, help="預期的群組名稱關鍵字，例如『佩佩老師』")
    ap.add_argument("--media", default=None, help="要送的媒體路徑（僅供紀錄用）")
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--list", action="store_true", help="列出全部對照")
    args = ap.parse_args()

    reg = load_registry(args.registry)
    chats = reg["chats"]

    if args.list:
        print("【Telegram 投遞目標對照表】")
        for cid, info in chats.items():
            print(f"  {cid:>14}  {info['name']}  [{info['kind']}]  建議帳號：{info['recommendedAccount']}")
            if info.get("note"):
                print(f"{'':>18}└ {info['note']}")
        return 0

    if not args.target:
        print("❌ 請提供要投遞的 chat_id（或用 --list 列出全部對照）。")
        return 2

    raw = normalize(args.target)
    tid = resolve(raw, chats)
    info = chats.get(tid) if tid else None

    if info is None:
        print(f"❌ 拒絕送出：目標 {raw} 不在對照表裡。")
        print("   請先確認這是什麼群，並把對照補進 telegram_chat_registry.json 再送。")
        print("   絕對不要憑印象或舊訊息裡的『已遷移』說法投遞。")
        return 2

    if args.expect:
        if args.expect not in info["name"]:
            print(f"❌ 拒絕送出：目標 {tid} = 「{info['name']}」，不符合預期「{args.expect}」。")
            print("   這就是 11/01 誤投事故的同一種型態，請先確認 chat_id 再送。")
            return 3

    print(f"✅ 通過：{tid} = 「{info['name']}」（{info['kind']}）")
    print(f"   建議帳號：{info['recommendedAccount']}")
    if info.get("note"):
        print(f"   備註：{info['note']}")
    if args.media:
        print(f"   媒體：{args.media}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
