#!/usr/bin/env python3
# VPS增量蒸餾腳本：每2小時自動執行，蒸餾memory精華進 distill/ 目錄
# 用於：赫米斯VPS 113.29.232.178
# 觸發：systemd timer（每2小時）
# 依賴：Python 3（已預裝）, 無需額外套件

import os, re, sys
from datetime import datetime, timezone, timedelta

BASE = '/root/.hermes/github-sync'
MEMORY_DIR = os.path.join(BASE, 'memory')
DISTILL_DIR = os.path.join(BASE, 'distill')
LOG_PATH = os.path.join(DISTILL_DIR, 'distill.log')

tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime('%Y-%m-%d')
memory_path = os.path.join(MEMORY_DIR, f'{date_str}.md')

def log(msg):
    ts = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    os.makedirs(DISTILL_DIR, exist_ok=True)
    with open(LOG_PATH, 'a') as f:
        f.write(line + '\n')

# 跳過這些pattern（純系統/cron通知，無教練實際行為）
SKIP_PATTERNS = [
    r'async exec command.*completed.*加油',
    r'system notification.*cron job.*加油提醒',
    r'system notification.*completed.*cron job.*加油',
    r'heartbeat cron job.*OpenClaw responded.*HEARTBEAT_OK',
    r'heartbeat poll message.*HEARTBEAT_OK',
    r'received.*async exec.*加油',
    r'received.*system notification.*completed',
    r'partial cron job status output',
    r'Facebook birthday check',
]

def should_skip(text):
    for p in SKIP_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def extract_entries(content):
    # 1. 把 \n 置換成真實換行
    content = content.replace('\\n', '\n')
    
    # 2. 分割段落
    segments = re.split(r'---', content)
    
    # 3. 從每個🦞段落提取 User bullet
    bullet_pat = re.compile(
        r'^-\s+(User\s+(?:asked|said|sent|told|received|wrote|informed|pointed out|gave|provided|attached).+?)(?=\n-(?!\s)|$|\Z)',
        re.MULTILINE | re.DOTALL
    )
    lobster_pat = re.compile(r'🦞 小龍蝦：(.+?)(?=👤 教練：|🦞 小龍蝦：|---|$)', re.DOTALL)
    
    distill_entries = []
    for seg in segments:
        lobster_m = lobster_pat.search(seg)
        if not lobster_m:
            continue
        bullets = bullet_pat.findall(lobster_m.group(1))
        for b in bullets:
            b = b.strip()
            if len(b) < 30:
                continue
            if should_skip(b):
                continue
            distill_entries.append(b[:300])
    
    return distill_entries

log(f'=== 開始蒸餾 {date_str} ===')

if not os.path.exists(memory_path):
    log(f'無 {date_str} memory，結束')
    sys.exit(0)

with open(memory_path, 'r', encoding='utf-8') as f:
    content = f.read()

entries = extract_entries(content)
log(f'提取到 {len(entries)} 個有效紀錄')

if not entries:
    log('無有效紀錄，結束')
    sys.exit(0)

# 寫入 coach_profile.md
os.makedirs(DISTILL_DIR, exist_ok=True)
profile_path = os.path.join(DISTILL_DIR, 'coach_profile.md')

lines = [f'# 教練對話蒸餾（{date_str}）', f'共 {len(entries)} 則', '']
for i, e in enumerate(entries, 1):
    lines.append(f'{i}. {e}')

entry_text = '\n'.join(lines)

if os.path.exists(profile_path):
    with open(profile_path, 'r', encoding='utf-8') as f:
        current = f.read()
    if date_str in current:
        log(f'{date_str} 已蒸餾，結束')
        sys.exit(0)
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(entry_text + '\n\n---\n\n' + current)
else:
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(entry_text)

log(f'✅ 寫入 coach_profile.md，{len(entries)}則')
