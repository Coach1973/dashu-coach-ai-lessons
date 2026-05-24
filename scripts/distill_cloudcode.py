#!/usr/bin/env python3
import json, os, sys
from datetime import datetime

OUT = '/Users/bymyway/.openclaw/workspace/distill/CloudCode桌面版對話精華_教練原聲.md'
BASE = os.path.expanduser('~/Library/Application Support/Claude/local-agent-mode-sessions/')

sessions = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f == 'audit.jsonl':
            sessions.append(os.path.join(root, f))

sessions.sort(key=lambda x: os.path.getmtime(x))
print(f'掃描 {len(sessions)} 個 session...')

coach_msgs = []
for sp in sessions:
    try:
        with open(sp) as fh:
            for line in fh:
                if not line.strip(): continue
                try:
                    e = json.loads(line)
                    if e.get('type') != 'user': continue
                    content = e.get('message', {}).get('content', '')
                    if isinstance(content, list):
                        texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                        content = ' '.join(texts)
                    content = (content or '').strip()
                    if not content: continue
                    if content.startswith('<local-command>'): continue
                    if content.startswith('</'): continue
                    if len(content) < 6: continue
                    # 過濾操作類噪音
                    skip_kw = ['幫我打開fb', '確認一下是否已擁有', '網頁控制權', '@"/']
                    if any(content.startswith(k) for k in skip_kw): continue
                    dt = datetime.fromtimestamp(os.path.getmtime(sp))
                    coach_msgs.append({
                        'date': dt.strftime('%Y-%m-%d'),
                        'content': content[:600]
                    })
                except Exception:
                    pass
    except Exception:
        pass

print(f'收集到 {len(coach_msgs)} 則教練訊息')

by_date = {}
for m in coach_msgs:
    d = m['date']
    by_date.setdefault(d, []).append(m['content'])

now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
min_d = min(by_date.keys())
max_d = max(by_date.keys())

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('# Cloud Code 桌面版對話精華——教練原聲\n\n')
    fh.write(f'> 蒸餾時間：{now_str}\n')
    fh.write(f'> 來源：{len(sessions)} 個 Claude Desktop App session\n')
    fh.write(f'> 有效教練訊息：{len(coach_msgs)} 則\n')
    fh.write('> ⚠ 以下皆為教練本人親口（打字或語音），非 AI 生成\n')
    fh.write('> 時間就是生命——教練不眠不休26年的代價\n\n')
    fh.write(f'> 日期覆蓋：{min_d} ~ {max_d}\n\n')
    fh.write('---\n\n')
    fh.write('## 教練原聲語錄（按日期排列，最新在上）\n\n')
    for d in sorted(by_date.keys(), reverse=True):
        msgs = by_date[d]
        fh.write(f'### {d}（{len(msgs)}則教練訊息）\n\n')
        for i, msg in enumerate(msgs, 1):
            # 每則訊息block
            fh.write('<blockquote>\n')
            fh.write(f'{msg}\n')
            fh.write('</blockquote>\n\n')
        fh.write('\n')

sz = os.path.getsize(OUT) // 1024
print(f'寫入完成：{OUT}')
print(f'  大小：{sz}KB')
print(f'  日期覆蓋：{min_d} ~ {max_d}')
print(f'  共 {len(coach_msgs)} 則教練原聲')