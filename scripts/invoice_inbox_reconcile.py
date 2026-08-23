#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""發票資訊對帳稽核（教練 2026-08-24 交辦「小龍蝦統計漏筆必須解決」的系統性解法）

背景：2026-08-20 教練透過 LINE 傳了 4 筆載具給小龍蝦，當時 agent 因 context overflow 連續
回「⚠️ Agent couldn't generate a response」，那幾筆就從此消失，直到 8/24 教練自己反問才補登。
光靠「叫 AI 記得」不可靠，所以拆成兩層：
  第一層 invoice-inbound hook：訊息進來當下就落地（agent 掛掉也不影響）
  第二層（本檔）：把「教練說過的每一筆」跟「知識檔實際記到的」逐筆對帳，有落差就吼出來

資料來源（兩邊都掃，互為備援）：
  A. state/invoice_inbox/*.jsonl   ← 新 hook 從今天起自動落地的
  B. state/inbound_echo/*.jsonl    ← 既有的全訊息存底，回溯歷史用（涵蓋 8/20 那次事故）
比對對象：
  knowledges/2026-08-18_38人培訓發票二聯三聯資訊蒐集中.md

用法：
  python3 scripts/invoice_inbox_reconcile.py            # 印報告
  python3 scripts/invoice_inbox_reconcile.py --notify   # 有落差才發 Telegram 給教練
"""

import json
import os
import re
import sys
import glob
import urllib.request
from datetime import datetime, timedelta, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
INVOICE_INBOX = os.path.join(WORKSPACE, "state", "invoice_inbox")
INBOUND_ECHO = os.path.join(WORKSPACE, "state", "inbound_echo")
# 🔴 2026-08-24 首次執行就學到的教訓：一開始只比對「38人蒐集中」這一份檔案，
# 結果把早就開好票的宋映璇（統編96573265，8/18已開立）誤報成「漏掉」。
# 發票資訊實際散在「蒐集中／已知vs待問／權威總清冊／已開立完成清單」四種檔案，
# 少查一種就會亂喊狼來了——寧可多掃幾個檔，也不能讓教練白緊張一次。
KNOWLEDGE_SOURCES = [
    os.path.join(WORKSPACE, "knowledges", "2026-08-18_38人培訓發票二聯三聯資訊蒐集中.md"),
    os.path.join(WORKSPACE, "knowledges", "2026-08-18_培訓發票開立_已知vs待問名單.md"),
    os.path.join(WORKSPACE, "knowledges", "2026-08-18_大台南南區4至8月培訓出席與開票總清冊_教練提供權威版.md"),
    os.path.join(WORKSPACE, "knowledges", "2026-08-17_出席統編發票交叉比對報告.md"),
]
KNOWLEDGE_GLOBS = [
    os.path.join(WORKSPACE, "claude-brain", "data", "ezpay_training_invoices_*.json"),
    os.path.join(WORKSPACE, "cross-agent", "outbox", "*", "*invoice*.md"),
]
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
COACH_CHAT_ID = "6124913915"
STATE_FILE = os.path.join(WORKSPACE, "state", "invoice_reconcile_state.json")

CARRIER_RE = re.compile(r"/[A-Z0-9.\-+]{7}(?![A-Z0-9.\-+])")
TAXID_LABELLED_RE = re.compile(r"(?:統一?編號?|統編)\s*[:：]?\s*(\d{8})(?!\d)")
TRIGGER_RE = re.compile(r"發票|統編|統一編號|載具|條碼|二聯|三聯|抬頭|開票")
TPE = timezone(timedelta(hours=8))


def load_knowledge_text():
    """把所有「已經記錄下來」的來源串成一大坨文字，回傳 (全文, 實際讀到的檔名清單)。"""
    chunks, used = [], []
    paths = list(KNOWLEDGE_SOURCES)
    for pattern in KNOWLEDGE_GLOBS:
        paths.extend(sorted(glob.glob(pattern)))
    for p in paths:
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                chunks.append(f.read())
            used.append(os.path.basename(p))
        except Exception:
            continue
    return "\n".join(chunks), used


def iter_source_messages():
    """吐出 (來源標籤, 台灣時間字串, 原文) — 只吐發票相關的。"""
    for path in sorted(glob.glob(os.path.join(INVOICE_INBOX, "*.jsonl"))):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                yield ("invoice_inbox", d.get("taipei", ""), d.get("raw", ""))

    for path in sorted(glob.glob(os.path.join(INBOUND_ECHO, "*.jsonl"))):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                text = d.get("text", "") or ""
                # 心跳/系統注入不是教練說的話，排除掉避免誤判
                if d.get("channel") == "heartbeat" or text.startswith("Read HEARTBEAT.md"):
                    continue
                if not (TRIGGER_RE.search(text) or CARRIER_RE.search(text)):
                    continue
                ts = d.get("ts")
                when = (
                    datetime.fromtimestamp(ts / 1000, TPE).strftime("%Y-%m-%d %H:%M")
                    if ts else d.get("iso", "")
                )
                yield ("inbound_echo", when, text)


def collect_claims():
    """把所有訊息裡出現過的載具/統編收集起來，記住第一次出現的時間與原文片段。"""
    carriers, taxids = {}, {}
    for source, when, text in iter_source_messages():
        for c in CARRIER_RE.findall(text):
            carriers.setdefault(c, {"when": when, "source": source, "ctx": _ctx(text, c)})
        for t in TAXID_LABELLED_RE.findall(text):
            taxids.setdefault(t, {"when": when, "source": source, "ctx": _ctx(text, t)})
    return carriers, taxids


def _ctx(text: str, token: str, width: int = 40) -> str:
    i = text.find(token)
    if i < 0:
        return text[:width].replace("\n", " ")
    return text[max(0, i - width): i + len(token) + width].replace("\n", " ").strip()


def notify(text: str) -> bool:
    try:
        with open(OPENCLAW_CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": COACH_CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:
        print(f"⚠️ Telegram 通知失敗：{e}", file=sys.stderr)
        return False


def main() -> int:
    do_notify = "--notify" in sys.argv
    knowledge, used_sources = load_knowledge_text()
    if not knowledge:
        print("❌ 一份發票記錄檔都讀不到，請確認 knowledges/ 與 claude-brain/data/ 路徑")
        return 2

    carriers, taxids = collect_claims()
    missing_carriers = {k: v for k, v in carriers.items() if k not in knowledge}
    missing_taxids = {k: v for k, v in taxids.items() if k not in knowledge}

    print("═══ 發票資訊對帳報告 ═══")
    print(f"時間：{datetime.now(TPE).strftime('%Y-%m-%d %H:%M:%S')} (台灣時間)")
    print(f"教練訊息裡出現過的載具：{len(carriers)} 組｜統編：{len(taxids)} 組")
    print(f"比對來源（{len(used_sources)} 份）：{'、'.join(used_sources)}")
    print()

    if not missing_carriers and not missing_taxids:
        print("✅ 零落差——教練傳過的每一組載具/統編，知識檔裡都找得到。")
    else:
        print(f"🔴 發現 {len(missing_carriers) + len(missing_taxids)} 筆「教練說過但知識檔沒記」：")
        for k, v in missing_carriers.items():
            print(f"  · 載具 {k}｜{v['when']}｜來源 {v['source']}")
            print(f"      原文：…{v['ctx']}…")
        for k, v in missing_taxids.items():
            print(f"  · 統編 {k}｜{v['when']}｜來源 {v['source']}")
            print(f"      原文：…{v['ctx']}…")

    # 狀態落地，讓別台機器/下一場對話能直接看結果，不用重跑
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "checked_at": datetime.now(TPE).isoformat(),
            "carriers_seen": len(carriers),
            "taxids_seen": len(taxids),
            "missing_carriers": missing_carriers,
            "missing_taxids": missing_taxids,
        }, f, ensure_ascii=False, indent=2)

    if do_notify and (missing_carriers or missing_taxids):
        lines = ["🔴 發票對帳：有教練傳過但沒記進檔案的資料"]
        for k, v in list(missing_carriers.items())[:10]:
            lines.append(f"· 載具 {k}（{v['when']}）")
        for k, v in list(missing_taxids.items())[:10]:
            lines.append(f"· 統編 {k}（{v['when']}）")
        lines.append("\n完整報告：state/invoice_reconcile_state.json")
        notify("\n".join(lines))

    return 1 if (missing_carriers or missing_taxids) else 0


if __name__ == "__main__":
    sys.exit(main())
