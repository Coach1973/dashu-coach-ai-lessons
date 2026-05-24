#!/usr/bin/env python3
"""
蒸餾 Cloud Code Desktop session 中教練的互動模式
找出教練的溝通風格、習慣用語、高頻指令形態
"""
import json, os, sys
from datetime import datetime
from collections import Counter

BASE = os.path.expanduser('~/Library/Application Support/Claude/local-agent-mode-sessions/')

sessions = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f == 'audit.jsonl':
            sessions.append((os.path.join(root, f), os.path.getmtime(os.path.join(root, f))))

sessions.sort(key=lambda x: x[1], reverse=True)

# 分析三大重點 session
key_dates = ['2026-05-06', '2026-04-05', '2026-03-28', '2026-03-01']

all_text = {}
for spath, mtime in sessions:
    d = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    if d not in key_dates:
        continue
    with open(spath) as fh:
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
                if not content or content.startswith('<local-command>'):
                    continue
                if len(content) < 8:
                    continue
                all_text.setdefault(d, []).append(content)
            except:
                pass

print("=== 教練溝通模式分析 ===\n")

for d in key_dates:
    if d not in all_text:
        continue
    msgs = all_text[d]
    print(f"\n{'='*40}")
    print(f"📅 {d} — {len(msgs)}則教練訊息")
    print(f"{'='*40}")

    # 行為分類
    categories = {
        'step_directive': [],   # 分步指令："先做A、再做B"
        'example_provided': [], # 給例子："像這樣"
        'correction': [],       # 修正："不是這樣，是..."
        'verification': [],     # 驗收："我確認一下"
        'direct_cmd': [],       # 直接指令："幫我..."
        'question': [],         # 提問
        'context_switch': [],   # 換話題/跳躍
    }

    for msg in msgs:
        l = msg.lower()
        if any(k in l for k in ['不要', '不是', '錯了', '重新', '修正']):
            categories['correction'].append(msg[:100])
        elif any(k in l for k in ['先', '再', '然後', '第一步', '第二步']):
            categories['step_directive'].append(msg[:100])
        elif any(k in l for k in ['像這樣', '例如', '比如', '就是這樣', '這個例子']):
            categories['example_provided'].append(msg[:100])
        elif any(k in l for k in ['確認', '檢查', '看一下', '我看看']):
            categories['verification'].append(msg[:100])
        elif any(k in l for k in ['幫我', '你去', '執行', '做一下']):
            categories['direct_cmd'].append(msg[:100])
        elif '?' in msg or '？' in msg:
            categories['question'].append(msg[:100])
        else:
            categories['context_switch'].append(msg[:100])

    for cat, items in categories.items():
        if items:
            print(f"\n  [{cat}] {len(items)}則")
            for item in items[:3]:
                print(f"    → {item[:80]}")

print("\n\n=== 教練高頻關鍵詞 ===")
all_msgs_flat = [m for msgs in all_text.values() for m in msgs]
words = ' '.join(all_msgs_flat)
# 簡單詞頻統計（忽略單字和常見停用詞）
from re import findall
tokens = findall(r'[\w]{2,}', words)
freq = Counter(tokens)
print("\nTop 20 高頻詞（排除常見詞）：")
stopwords = {'我', '你', '他', '她', '它', '的', '了', '是', '在', '有', '和', '就', '不', '也', '都', '這', '那', '這是', '不要', '什麼', '怎麼', '可以', '一個', '然後', '所以', '但是', '因為', '如果', '什麼'}
for w, c in freq.most_common(200):
    if w not in stopwords and len(w) >= 2:
        print(f"  {w}: {c}")
    if len([x for x in freq.most_common(200) if x[0] not in stopwords and len(x[0]) >= 2]) >= 20:
        pass