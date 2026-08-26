"""
MiniMax共用帳號批次呼叫紅線防護（2026-08-27，試金石案例65教訓後建立）

教練原話（2026-08-27）：「畫下一條紅線，之後任何類似這種一次性會把我5個小時、
4500次呼叫額度全部用完的行為，全部都要拉紅線限制」——這支模組是那條紅線的
程式碼實作，不是文件宣告或口頭承諾。任何會迴圈呼叫MiniMax API的批次腳本，
都必須在每次呼叫前先過這一關，越線立刻中止（拋例外），不是事後才發現。

案例65回顧：chain_matcher.py對428人跑批次媒合，系統提示詞沒做快取、
呼叫之間沒有節流，短時間內燒了約150萬token，把帳號5小時4500次呼叫額度
全部打滿，教練所有服務（小龍蝦/BNI小幫手/教練都在想什麼/VPS小龍蝦）
同時停擺3小時。

用法：
    from minimax_batch_guard import guard_call
    guard_call("chain_matcher")   # 放在每次真正呼叫 client.messages.create() 之前
    message = client.messages.create(...)

設計（2026-08-27教練當場調整過一次配額）：
- 帳號真實上限是5小時4500次呼叫（教練親口確認）。教練拍板分配：
  2000次留給批次腳本（教練自己交辦的AI工作），2500次留給小龍蝦/BNI小幫手/
  教練都在想什麼三個LINE帳號的即時真人互動——批次腳本再急，都不該搶真人
  對話當下需要的額度。
- 這個上限拉高後仍然安全，關鍵不在數字大小，而在cache_control（重複的
  系統提示詞不用每次全額計費）+PACE_SLEEP_SEC（每次呼叫間隔3秒）這兩個
  結構性修復還在——案例65會爆炸是「24分鐘內燒300+次無快取呼叫」，2000次
  在3秒節流下要跑約100分鐘才會跑完，是細水長流不是瞬間爆量，跟即時互動
  搶額度的碰撞機率大幅降低。
- 用同一份log檔累計「所有批次腳本」的呼叫次數，不是各腳本各自算，
  因為帳號上限本來就是共用的，同一時間可能不只一支批次腳本在跑。
- 越線即拋例外中止，呼叫端不可用 try/except 吞掉繼續跑；同時主動發
  Telegram通知教練，不用等教練自己發現服務停擺才知道。
- 每滿100次額外提醒一次進度，讓教練有感知，不是悶頭燒到中止才第一次出聲。
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

CEILING = 2000            # 5小時滾動窗口內，「所有批次腳本加總」的呼叫次數上限
                          # 2026-08-27教練親口拍板：帳號總量4500次，2000留給批次腳本(教練自己的AI工作)、
                          # 2500留給小龍蝦/BNI小幫手/教練都在想什麼三個LINE帳號的即時真人互動。
                          # 安全性靠的不是這個數字小，是cache_control+PACE_SLEEP_SEC(3秒/次)沒有拿掉——
                          # 案例65會爆炸的真因是「24分鐘內燒300+次無快取呼叫」，2000次×3秒節流≈100分鐘
                          # 才跑得完，是細水長流不是瞬間爆量，跟即時互動搶額度的碰撞機率大幅降低。
WINDOW_SEC = 5 * 3600     # 5小時，跟MiniMax帳號的重置窗口一致
PROGRESS_NOTIFY_EVERY = 100  # 上限拉高後進度提醒間隔跟著拉開，避免Telegram被洗版

_WORKSPACE = Path(__file__).resolve().parent.parent
LOG_PATH = _WORKSPACE / "state" / "minimax_batch_call_log.jsonl"
NOTIFY_SCRIPT = _WORKSPACE / "scripts" / "notify_coach.sh"


class MiniMaxBatchGuardError(RuntimeError):
    """批次呼叫已達紅線上限，呼叫端必須讓這個例外中止整個批次，不可吞掉。"""


def _load_recent_calls() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    now = time.time()
    kept = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if now - entry.get("ts", 0) <= WINDOW_SEC:
            kept.append(entry)
    return kept


def _notify_coach(msg: str) -> None:
    if not NOTIFY_SCRIPT.exists():
        return
    try:
        subprocess.run(["bash", str(NOTIFY_SCRIPT), msg], timeout=15, check=False)
    except Exception:
        pass


def guard_call(caller: str) -> None:
    """任何批次腳本呼叫MiniMax API前都要先過這關。越線直接拋例外中止整批。"""
    recent = _load_recent_calls()
    count = len(recent)

    if count >= CEILING:
        oldest_ts = min((e["ts"] for e in recent), default=time.time())
        reset_in_min = round((WINDOW_SEC - (time.time() - oldest_ts)) / 60, 1)
        msg = (
            f"🔴🔴🔴 MiniMax批次呼叫紅線觸發！{caller} 想呼叫第{count + 1}次，"
            f"已達5小時滾動窗口內批次腳本專屬上限({CEILING}次)，自動中止避免重演"
            f"案例65(一次燒光150萬token/4500次帳號額度，全服務停擺3小時)。"
            f"約{reset_in_min}分鐘後額度回落，重跑腳本會自動接續未完成的部分。"
        )
        _notify_coach(msg)
        raise MiniMaxBatchGuardError(msg)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "caller": caller}) + "\n")

    if (count + 1) % PROGRESS_NOTIFY_EVERY == 0:
        _notify_coach(
            f"ℹ️ MiniMax批次呼叫進度：{caller} 過去5小時已用 {count + 1}/{CEILING} "
            f"次批次腳本專屬額度（非帳號總量，帳號總量4500次還很充裕）。"
        )
