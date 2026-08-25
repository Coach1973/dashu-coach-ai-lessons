#!/usr/bin/env python3
"""蒸餾終端機A：處理 projects/-Users-bymyway/*.jsonl（131個session）"""
import json, os, glob
from datetime import datetime
from collections import defaultdict

BASE = os.path.expanduser('~/.claude/projects/-Users-bymyway/')
OUT = '/Users/bymyway/.openclaw/workspace/distill/cli_a_messages.md'
OUT_COUNTS = '/Users/bymyway/.openclaw/workspace/distill/cli_a_session_summary.tsv'

files = sorted(glob.glob(os.path.join(BASE, '*.jsonl')))
print(f'找到 {len(files)} 個 JSONL 檔案')

# 跳過的關鍵詞（操作噪音）
SKIP_KW = [
    '<local-command>', '</', '幫我打開', '確認一下是否已擁有',
    '網頁控制權', '@"/', '打開', '開啟', '告訴我',
]

results = []
for fp in files:
    fname = os.path.basename(fp)
    mtime = datetime.fromtimestamp(os.path.getmtime(fp))
    date_str = mtime.strftime('%Y-%m-%d')
    coach_msgs = []

    try:
        with open(fp) as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    if e.get('type') != 'user':
                        continue
                    content = e.get('message', {}).get('content', '')
                    if isinstance(content, list):
                        texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                        content = ' '.join(texts)
                    content = (content or '').strip()
                    if not content:
                        continue
                    if len(content) < 10:
                        continue
                    # 跳過操作噪音
                    if any(content.startswith(k) for k in SKIP_KW):
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
        'lines': sum(1 for _ in open(fp)) if os.path.getsize(fp) > 0 else 0,
        'msgs': coach_msgs
    })

print(f'處理完成：{len(results)} 個檔案')

# 寫入 session 摘要 TSV
with open(OUT_COUNTS, 'w') as fh:
    fh.write('日期\t檔名\t大小(KB)\t教練訊息數\n')
    for r in results:
        fh.write(f"{r['date']}\t{r['file']}\t{r['size_kb']}\t{len(r['msgs'])}\n")

# 寫入所有教練訊息（按日期）
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
by_date = defaultdict(list)
total_msgs = 0
for r in results:
    for msg in r['msgs']:
        by_date[r['date']].append((r['file'], msg))
        total_msgs += 1

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('# CLI 終端機A——教練訊息蒸餾預備\n\n')
    fh.write(f'> 蒸餾時間：{now_str}\n')
    fh.write(f'> 來源：{len(results)} 個 projects/-Users-bymyway/*.jsonl\n')
    fh.write(f'> 有效教練訊息：{total_msgs} 則\n\n')
    fh.write('## 依日期排列（最新在上）\n\n')
    for d in sorted(by_date.keys(), reverse=True):
        items = by_date[d]
        fh.write(f'### {d}（{len(items)}則）\n\n')
        for fname, msg in items:
            fh.write(f'**{fname}**\n> {msg}\n\n')
        fh.write('\n')

sz = os.path.getsize(OUT) // 1024
print(f'寫入完成')
print(f'  訊息檔：{OUT} ({sz}KB)')
print(f'  摘要表：{OUT_COUNTS}')
print(f'  共 {total_msgs} 則教練訊息，跨越 {len(by_date)} 天')
