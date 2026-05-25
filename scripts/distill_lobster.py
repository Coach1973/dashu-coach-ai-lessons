#!/usr/bin/env python3
"""蒸餾小龍蝦（1號機）：處理 ~/.openclaw/agents/main/sessions/*.jsonl"""
import json, os, glob
from datetime import datetime
from collections import defaultdict

BASE = os.path.expanduser('~/.openclaw/agents/main/sessions/')
OUT_DIR = os.path.expanduser('/Users/bymyway/.openclaw/workspace/distill')

files = sorted(glob.glob(os.path.join(BASE, '*.jsonl')))
files = [f for f in files if '.reset.' not in f]  # 排除 reset 過的舊檔
print(f'找到 {len(files)} 個有效 session（排除 reset）')

SKIP_KW = ['<local-command>', '</', '幫我打開', '確認一下', 'Recent memories']
SKIP_PREFIX = ['Recent memories', 'system:']

results = []
for fp in files:
    fname = os.path.basename(fp)
    try:
        mtime = os.path.getmtime(fp)
    except:
        continue
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    coach_msgs = []

    try:
        with open(fp) as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    # 小龍蝦格式：type="message", message.role="user"
                    if e.get('type') != 'message':
                        continue
                    msg = e.get('message', {})
                    if msg.get('role') != 'user':
                        continue
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                        content = ' '.join(texts)
                    content = (content or '').strip()
                    if not content:
                        continue
                    if len(content) < 15:
                        continue
                    # 跳過系統噪音
                    if any(content.startswith(k) for k in SKIP_PREFIX):
                        continue
                    if any(k in content for k in SKIP_KW):
                        continue
                    coach_msgs.append(content[:500])
                except Exception:
                    pass
    except Exception as e:
        print(f'  錯誤 {fname}: {e}')
        continue

    results.append({
        'file': fname,
        'date': date_str,
        'size_kb': os.path.getsize(fp) // 1024,
        'msgs': coach_msgs
    })

print(f'處理完成：{len(results)} 個檔案')

# 按月份分組
by_month = defaultdict(list)
for r in results:
    month = r['date'][:7]  # "2026-05"
    by_month[month].append(r)

# 寫入 TSV 摘要
out_tsv = os.path.join(OUT_DIR, 'lobster_messages_summary.tsv')
with open(out_tsv, 'w') as fh:
    fh.write('月份\t日期\t檔名\t大小(KB)\t教練訊息數\n')
    for month in sorted(by_month.keys(), reverse=True):
        for r in sorted(by_month[month], key=lambda x: x['date'], reverse=True):
            fh.write(f"{month}\t{r['date']}\t{r['file']}\t{r['size_kb']}\t{len(r['msgs'])}\n")

# 寫入所有教練訊息（按月份）
total_msgs = 0
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
out_msg = os.path.join(OUT_DIR, 'lobster_messages_all.md')

with open(out_msg, 'w', encoding='utf-8') as fh:
    fh.write('# 小龍蝦（1號機）——教練訊息蒸餾預備\n\n')
    fh.write(f'> 蒸餾時間：{now_str}\n')
    fh.write(f'> 來源：{len(results)} 個 session\n')
    for month in sorted(by_month.keys(), reverse=True):
        month_msgs = sum(len(r['msgs']) for r in by_month[month])
        total_msgs += month_msgs
        fh.write(f'> {month}：{month_msgs} 則教練訊息\n')
    fh.write(f'\n## 依月份排列（最新在上）\n\n')
    for month in sorted(by_month.keys(), reverse=True):
        fh.write(f'### {month}（{len(by_month[month])}個 session）\n\n')
        for r in sorted(by_month[month], key=lambda x: x['date'], reverse=True):
            fh.write(f'**{r['date']}** — {r['file']}（{len(r['msgs'])}則）\n\n')
            for msg in r['msgs'][:10]:  # 每個 session 最多10則
                fh.write(f'> {msg[:300]}\n\n')
            if len(r['msgs']) > 10:
                fh.write(f'> ... 還有 {len(r["msgs"])-10} 則\n\n')

sz = os.path.getsize(out_msg) // 1024
print(f'寫入完成：')
print(f'  摘要：{out_tsv}')
print(f'  訊息：{out_msg} ({sz}KB)')
print(f'  共 {total_msgs} 則教練訊息')

# 月份分布
print(f'\n月份分布：')
for month in sorted(by_month.keys(), reverse=True):
    cnt = sum(len(r['msgs']) for r in by_month[month])
    print(f'  {month}: {len(by_month[month])} 個 session, {cnt} 則訊息')
