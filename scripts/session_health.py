"""
Session 健康度自我監測系統
適用：終端機 CLI / 小龍蝦 Telegram / VPS赫茲米

⚠️ 重要說明：
Claude Code 的 session 填充不只靠「對話輪數」，
還包括：系統提示、工具結果、檔案歷史⋯⋯
這些無法從外面計數，所以本腳本只追蹤「對話輪數」作為代理指標。

實際使用時，請在每次任務開始前或每15分鐘，
執行一次 `python3 session_health.py cli` 來獲取健康度報告。

實測參考：
  5-10 輪  → 正常閒聊
  15-20 輪 → 開始有實質工作內容
  25-30 輪 → 接近不穩定邊界（建議reload）
  35+ 輪  → 高風險，已開始丟內容

使用方法：
  python3 session_health.py [模式] [輪數]

模式：
  cli      — 終端機 CLI 模式（預設）
  telegram — 小龍蝦 Telegram 模式
  vps      — VPS 赫茲米模式

範例：
  python3 session_health.py cli 20
  python3 session_health.py telegram 12
  python3 session_health.py vps 35
"""

import sys
import json
import os
from datetime import datetime

# ─── 參數設定 ───────────────────────────────────────────────

# CLI 模式門檻（對話輪數）
# 實測經驗值：Claude Code session 約 15-20 輪後開始不穩定
CLI_THRESHOLDS = {
    'green': (0, 15),      # 🟢 正常
    'yellow': (16, 25),     # 🟡 警戒
    'orange': (26, 35),     # 🟠 警告
    'red': (36, 50),       # 🔴 危急
    'critical': (51, 9999), # 🚨 已超載
}

# Telegram 模式門檻（小龍蝦session較短）
TELEGRAM_THRESHOLDS = {
    'green': (0, 20),      # ✅ 正常
    'yellow': (21, 35),     # 💛 警戒
    'orange': (36, 50),     # ⚠️ 警告
    'red': (51, 70),       # 🚨 危急
    'critical': (71, 9999), # 💥 已超載
}

# VPS 模式門檻（赫茲米蒸餾session）
VPS_THRESHOLDS = {
    'green': (0, 15),      # 🟢 正常
    'yellow': (16, 25),     # 🟡 警戒
    'orange': (26, 40),     # 🟠 警告
    'red': (41, 60),       # 🔴 危急
    'critical': (61, 9999), # 🚨 已超載
}

# ─── 核心函數 ───────────────────────────────────────────────

def get_status(turns, thresholds):
    """根據輪數回傳狀態（green/yellow/orange/red/critical）"""
    for status in ('critical', 'red', 'orange', 'yellow', 'green'):
        lo, hi = thresholds[status]
        if lo <= turns <= hi:
            return status
    return 'green'

def estimate_tokens(turns):
    """估算目前token使用量"""
    return turns * AVG_TURN_TOKENS

def calc_ratio(turns, limit):
    """計算使用比例"""
    est = estimate_tokens(turns)
    return min(est / limit, 1.0)

def distance_to_refresh(thresholds, turns):
    """計算距離刷新線的輪數"""
    status = get_status(turns, thresholds)
    if status == 'critical':
        return 0  # 已經太晚
    if status == 'red':
        return 0  # 等不及了
    lo, hi = thresholds['orange']
    return max(0, lo - turns)

def format_health_cli(turns):
    """CLI 格式：完整健康度報告"""
    status = get_status(turns, CLI_THRESHOLDS)
    emoji = {'green': '🟢', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴', 'critical': '🚨'}
    dist = distance_to_refresh(CLI_THRESHOLDS, turns)

    lines = [
        f"━━━ 健康度 {emoji[status]} 輪 #{turns} | 距離刷新線：{dist}輪",
    ]

    if status == 'green':
        lines.append("(正常，不干擾)")
    elif status == 'yellow':
        lines.append(f"💡 小提醒：session已運行 {turns} 輪，隨時可以 /compact 或重新開工。")
    elif status == 'orange':
        lines.append(f"⚠️ 教練，session快滿了。建議 /compact 或重新開工（還有 ~{dist} 輪安全區）。")
    elif status == 'red':
        lines.append("🚨 教練，session已超載！立即 /compact 或重新開工，舊內容由接力棒銜接。")
    else:
        lines.append("💥 教練，session已過度壓縮！請立即重新開工並讀取接力棒。")

    return '\n'.join(lines)

def format_health_telegram(turns):
    """Telegram 格式：適合放在heartbeat末尾"""
    status = get_status(turns, TELEGRAM_THRESHOLDS)
    emoji = {'green': '✅', 'yellow': '💛', 'orange': '⚠️', 'red': '🚨', 'critical': '💥'}
    dist = distance_to_refresh(TELEGRAM_THRESHOLDS, turns)

    if status == 'green':
        return f"✅ 健康 #{turns}輪 | 還可聊 ~{dist}輪"

    msgs = [
        f"健康度 {emoji[status]} #{turns}輪"
    ]
    if status == 'yellow':
        msgs.append(f"（session已過半，隨時可重新開工）")
    elif status == 'orange':
        msgs.append(f"⚠️ 快滿！建議重新開工（還有~{dist}輪）")
    elif status == 'red':
        msgs.append(f"🚨 超載！立即重新開工銜接")
    else:
        msgs.append(f"💥 已壓縮！請重新開工")

    return ' | '.join(msgs)

def format_health_vps(turns):
    """VPS 格式：適合蒸餾後的自動報告"""
    status = get_status(turns, VPS_THRESHOLDS)
    emoji = {'green': '🟢', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴', 'critical': '💥'}
    dist = distance_to_refresh(VPS_THRESHOLDS, turns)

    lines = [f"[Session健康度] {emoji[status]} #{turns}輪"]

    if status == 'green':
        lines.append(f"✅ 正常（還可~{dist}輪）")
    elif status == 'yellow':
        lines.append(f"💡 已{turns}輪，建議下次蒸餾後reload")
    elif status == 'orange':
        lines.append(f"⚠️ 即將超載，應立即蒸餾並reload")
    elif status == 'red':
        lines.append(f"🚨 超載，需立即reload")
    else:
        lines.append(f"💥 已過度壓縮，內容可能已損失")

    return ' '.join(lines)

def check_and_warn(mode, turns, silent_ok=True):
    """檢查並發出警告（如果需要）"""
    status_fn = {
        'cli': lambda t: get_status(t, CLI_THRESHOLDS),
        'telegram': lambda t: get_status(t, TELEGRAM_THRESHOLDS),
        'vps': lambda t: get_status(t, VPS_THRESHOLDS),
    }
    format_fn = {
        'cli': format_health_cli,
        'telegram': format_health_telegram,
        'vps': format_health_vps,
    }

    status = status_fn[mode](turns)

    # 健康時安靜（不說話打擾教練）
    if status == 'green' and silent_ok:
        return None

    return format_fn[mode](turns)

# ─── 主程式 ───────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    mode = args[0] if args else 'cli'

    if mode not in ('cli', 'telegram', 'vps'):
        print(f"用法：python3 {sys.argv[0]} [cli|telegram|vps] [輪數]")
        sys.exit(1)

    # 如果沒有傳輪數，嘗試從 state/session_counter.json 讀取
    if len(args) < 2:
        counter_path = os.path.expanduser('~/.openclaw/workspace/state/session_counter.json')
        try:
            if os.path.exists(counter_path):
                with open(counter_path) as f:
                    data = json.load(f)
                    turns = data.get('count', 0)
            else:
                turns = 0
        except:
            turns = 0
        if turns == 0:
            print(f"用法：python3 {sys.argv[0]} {mode} [輪數]")
            print(f"（state/session_counter.json 不存在，請直接指定輪數）")
            sys.exit(1)
    else:
        turns = int(args[1])

    warning = check_and_warn(mode, turns)
    if warning:
        print(warning)

    # 也支援讀取字元密度（Telegram模式專用）
    if mode == 'telegram' and len(args) >= 3:
        char_count = int(args[2])
        density = char_count / 2000  # 2000字為段落上限
        print(f"[密度] {char_count}字 / 2000 = {density*100:.0f}%")

if __name__ == '__main__':
    main()
