#!/usr/bin/env python3
"""蒸餾小龍蝦（1號機 Telegram對話）：從 BOT_MESSAGES.md 讀取教練訊息"""
import json
from datetime import datetime

IN = '/Users/bymyway/.openclaw/workspace/BOT_MESSAGES.md'
OUT_DIR = '/Users/bymyway/.openclaw/workspace/distill'

SKIP_PREFIX = ['教練，我來', '收到！', '學弟', '學妹', '學長', '好的', '了解', '收到，']
BOT_SIGNATURES = ['學長', '學弟', '學妹', '🦐', '📋', '**學']

msgs = []
with open(IN) as f:
    for line in f:
        line = line.strip()
        if not line or not line.startswith('{'): continue
        try:
            e = json.loads(line)
        except: continue
        text = e.get('text', '')
        bot_id = e.get('botId', '')
        ts = e.get('ts', '')[:10]  # "2026-05-22"

        # 跳過 bot 回覆
        if any(text.startswith(p) for p in BOT_SIGNATURES):
            continue
        if bot_id not in ('', '0', '教練'):  # 空或教練才是真實訊息
            continue
        # 跳過系統噪音
        if len(text) < 10: continue
        if 'Recent memories' in text: continue

        msgs.append({'date': ts, 'text': text})

print(f'從 BOT_MESSAGES.md 讀到 {len(msgs)} 則教練訊息')

# 按月份分組
from collections import defaultdict
by_month = defaultdict(list)
for m in msgs:
    by_month[m['date'][:7]].append(m)

# 寫入摘要
out_tsv = OUT_DIR + '/lobster_telegram_summary.tsv'
with open(out_tsv, 'w') as f:
    f.write('月份\t日期\t字數\n')
    for m in sorted(msgs, key=lambda x: x['date'], reverse=True):
        f.write(f"{m['date'][:7]}\t{m['date']}\t{len(m['text'])}\n")

# 寫入完整訊息
out_md = OUT_DIR + '/lobster_telegram_messages.md'
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('# 小龍蝦 Telegram——教練訊息蒸餾預備\n\n')
    f.write(f'> 蒸餾時間：{now_str}\n')
    f.write(f'> 來源：BOT_MESSAGES.md\n')
    f.write(f'> 教練訊息：{len(msgs)} 則\n')
    for month in sorted(by_month.keys(), reverse=True):
        f.write(f'> {month}：{len(by_month[month])} 則\n')
    f.write('\n## 依月份排列（最新在上）\n\n')
    for month in sorted(by_month.keys(), reverse=True):
        f.write(f'### {month}（{len(by_month[month])}則）\n\n')
        for m in sorted(by_month[month], key=lambda x: x['date'], reverse=True):
            f.write(f'**{m['date']}**\n> {m['text'][:400]}\n\n')

print(f'寫入完成：')
print(f'  {out_md}')
print(f'  {out_tsv}')
print(f'月份分布：')
for month in sorted(by_month.keys(), reverse=True):
    print(f'  {month}: {len(by_month[month])}則')