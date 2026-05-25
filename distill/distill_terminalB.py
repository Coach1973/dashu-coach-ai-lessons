#!/usr/bin/env python3
"""
終端機B蒸餾腳本：處理 projects/-Users-bymyway--openclaw/*.jsonl
用途：批次提取教練訊息，供格式D蒸餾
"""
import json, os, sys
from datetime import datetime

PROJ = os.path.expanduser('~/.claude/projects/-Users-bymyway--openclaw')
OUT_DIR = os.path.expanduser('~/.openclaw/workspace/distill')
BATCH_OUT = os.path.join(OUT_DIR, 'terminalB_batches')

os.makedirs(BATCH_OUT, exist_ok=True)

files = sorted([f for f in os.listdir(PROJ) if f.endswith('.jsonl')],
               key=lambda x: os.path.getsize(os.path.join(PROJ, x)), reverse=True)

print(f"共 {len(files)} 個 JSONL 檔")
print(f"總大小: {sum(os.path.getsize(os.path.join(PROJ,f)) for f in files)/1024/1024:.1f} MB")
print()

def extract_messages(filepath):
    """提取JSONL中的教練訊息（type=user）"""
    msgs = []
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    e = json.loads(line)
                    if e.get('type') != 'user': continue
                    msg = e.get('message', {})
                    content = msg.get('content', '')
                    # 處理不同格式
                    if isinstance(content, list):
                        texts = []
                        for c in content:
                            if c.get('type') == 'text':
                                texts.append(c.get('text', ''))
                            elif c.get('type') == 'resource':
                                texts.append(f"[附件: {c.get('source',{}).get('type','')}]")
                        content = ' '.join(texts)
                    content = (content or '').strip()
                    if not content: continue
                    # 跳過系統噪音
                    if content.startswith('<local-command>'): continue
                    if content.startswith('</'): continue
                    if len(content) < 10: continue
                    # 跳過常見噪音關鍵字
                    skip_kw = ['幫我打開', '確認一下是否已擁有', '網頁控制權', '@"/']
                    if any(content.startswith(k) for k in skip_kw): continue
                    msgs.append(content)
                except Exception:
                    pass
    except Exception as e:
        print(f"  ERROR: {filepath}: {e}")
    return msgs

# 按大小分組（超大檔單獨處理）
large_files = [f for f in files if os.path.getsize(os.path.join(PROJ, f)) > 5*1024*1024]
small_files = [f for f in files if os.path.getsize(os.path.join(PROJ, f)) <= 5*1024*1024]

print(f"大檔(>5MB): {len(large_files)} 個")
print(f"小檔(<=5MB): {len(small_files)} 個")
print()

# 先處理所有小檔，提取訊息
print("=== 批次處理小檔 ===")
batch_num = 0
batch_content = []
batch_stats = []

for i, fname in enumerate(small_files):
    fpath = os.path.join(PROJ, fname)
    msgs = extract_messages(fpath)
    size_mb = os.path.getsize(fpath) / 1024 / 1024
    stat = {'file': fname, 'size_mb': round(size_mb,1), 'msgs': len(msgs), 'chars': sum(len(m) for m in msgs)}
    batch_stats.append(stat)
    print(f"  [{i+1}/{len(small_files)}] {fname[:8]}... | {len(msgs)}則訊息 | {size_mb:.1f}MB")

    for m in msgs:
        batch_content.append({
            'file': fname,
            'content': m[:1000],  # 截斷超長訊息
            'char_count': len(m)
        })

    # 每20個檔一批
    if len(batch_content) > 300 or i == len(small_files) - 1:
        batch_num += 1
        batch_file = os.path.join(BATCH_OUT, f'batch_{batch_num:02d}.jsonl')
        with open(batch_file, 'w') as f:
            for item in batch_content:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"  → 寫入 batch_{batch_num:02d}: {len(batch_content)} 則訊息")
        batch_content = []

# 大檔單獨處理
print()
print("=== 大檔清單（需單獨蒸餾）===")
for fname in large_files:
    fpath = os.path.join(PROJ, fname)
    msgs = extract_messages(fpath)
    size_mb = os.path.getsize(fpath) / 1024 / 1024
    print(f"  {fname[:8]}... | {size_mb:.1f}MB | {len(msgs)}則訊息")

# 寫統計報告
stats_file = os.path.join(OUT_DIR, 'terminalB_stats.json')
with open(stats_file, 'w') as f:
    json.dump({'large': large_files, 'small': small_files, 'stats': batch_stats}, f, ensure_ascii=False, indent=2)

# 合併所有批次成一個完整提取
print()
print("=== 合併批次 ===")
all_msgs = []
for bf in sorted(os.listdir(BATCH_OUT)):
    if bf.endswith('.jsonl'):
        with open(os.path.join(BATCH_OUT, bf)) as f:
            for line in f:
                line = line.strip()
                if line:
                    all_msgs.append(json.loads(line))

all_file = os.path.join(OUT_DIR, 'terminalB_all_messages.jsonl')
with open(all_file, 'w') as f:
    for m in all_msgs:
        f.write(json.dumps(m, ensure_ascii=False) + '\n')

total_chars = sum(m['char_count'] for m in all_msgs)
print(f"共提取 {len(all_msgs)} 則教練訊息，總字數 {total_chars:,}")

# 生成簡要清單（每則前100字）
summary_file = os.path.join(OUT_DIR, 'terminalB_message_summary.md')
with open(summary_file, 'w') as f:
    f.write("# 終端機B訊息摘要（待蒸餾）\n\n")
    f.write(f"> 來源：`-Users-bymyway--openclaw` 73個JSONL\n")
    f.write(f"> 提取時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"> 總計：{len(all_msgs)} 則訊息\n\n")
    f.write("---\n\n")
    for i, m in enumerate(all_msgs, 1):
        preview = m['content'][:120].replace('\n', ' ')
        f.write(f"## [{i:03d}] {m['file'][:8]}... ({m['char_count']}字)\n\n")
        f.write(f"{preview}{'...' if len(m['content']) > 120 else ''}\n\n")

print(f"摘要寫入：{summary_file}")
print()
print("=== 完成 ===")
print(f"下一步：閱讀 terminalB_message_summary.md，識別值得蒸餾的場景")
print(f"         然後寫入 distill/100場景_追加.md")
