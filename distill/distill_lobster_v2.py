#!/usr/bin/env python3
"""
小龍蝦對話蒸餾腳本 v3 - 格式D
支援所有 session 格式 + 所有來源路徑 + 實際時間戳過濾
用法: python3 distill_lobster_v2.py [月份] [輸出檔]
例: python3 distill_lobster_v2.py 05 distill/5月場景庫_格式D.md
     python3 distill_lobster_v2.py  展示所有可用 sessions
"""
import json, os, glob, sys, re
from datetime import datetime
from pathlib import Path

# ===== 全域 Session Sources =====
def _glob_sessions(base_path):
    p = Path(base_path)
    if p.exists():
        return list(p.glob('*.jsonl'))
    return []

def _get_desktop_sessions():
    p = Path.home() / 'Library/Application Support/Claude/claude-code-sessions'
    if not p.exists():
        return []
    result = []
    for d in p.glob('*'):
        sj = d / 'local-agent-mode-sessions/session.jsonl'
        if sj.exists():
            result.append(sj)
    return result

SESSION_SOURCES = [
    ('CLI-A', lambda: _glob_sessions(str(Path.home() / '.claude/projects/-Users-bymyway'))),
    ('CLI-B', lambda: _glob_sessions(str(Path.home() / '.claude/projects/-Users-bymyway--openclaw'))),
    ('OpenClaw', lambda: _glob_sessions(str(Path.home() / '.openclaw/agents/main/sessions'))),
    ('Desktop', _get_desktop_sessions),  # call directly, not via lambda
    ('Workspace', lambda: _glob_sessions(str(Path.home() / '.openclaw/workspace/sessions'))),
]

def get_all_sessions():
    sessions = []
    for name, getter in SESSION_SOURCES:
        try:
            files = getter()
            for f in files:
                sessions.append({
                    'source': name,
                    'path': str(f),
                    'name': f.name,
                    'size': f.stat().st_size
                })
        except Exception as e:
            print(f'  讀取 {name} 失敗: {e}')
    return sessions

def get_first_timestamp(filepath):
    """抓第一個 user message 的 timestamp（月份判定用）"""
    try:
        with open(filepath) as f:
            content = f.read().strip()

        if content.startswith('['):
            data = json.loads(content)
            for obj in data[:20]:
                if obj.get('role') == 'user':
                    ts = obj.get('timestamp','')
                    if ts and len(ts) >= 7:
                        return ts[:7]
        else:
            lines = content.split('\n')
            for line in lines[:20]:
                try:
                    obj = json.loads(line)
                    ts = obj.get('timestamp','')
                    if ts and len(ts) >= 7:
                        return ts[:7]
                except:
                    pass
    except:
        pass
    return None

def extract_coach_messages(filepath):
    """從任何 session 格式提取教練訊息"""
    messages = []
    try:
        with open(filepath) as f:
            content = f.read().strip()

        # 格式1: JSON array
        if content.startswith('['):
            try:
                data = json.loads(content)
                for obj in data:
                    if obj.get('role') == 'user':
                        content2 = obj.get('content', '')
                        if isinstance(content2, list):
                            for c in content2:
                                if c.get('type') == 'text':
                                    t = c.get('text','').strip()
                                    if t and len(t) > 15:
                                        ts = obj.get('timestamp','')[:16]
                                        messages.append({'text': t, 'timestamp': ts, 'source': 'array'})
                                        break
                        elif isinstance(content2, str) and len(content2) > 15:
                            messages.append({'text': content2, 'timestamp': '', 'source': 'array_str'})
            except json.JSONDecodeError:
                pass

        # 格式2: JSONL
        else:
            lines = content.split('\n')
            for line in lines:
                try:
                    obj = json.loads(line)
                    t = obj.get('type', '')

                    # Claude Code: type=user + message.content
                    if t == 'user':
                        msg = obj.get('message', {})
                        content2 = msg.get('content', [])
                        if isinstance(content2, list):
                            for c in content2:
                                if isinstance(c, dict) and c.get('type') == 'text':
                                    text = c.get('text','').strip()
                                    if text and len(text) > 15:
                                        ts = obj.get('timestamp','')[:16] if obj.get('timestamp') else ''
                                        messages.append({'text': text, 'timestamp': ts, 'source': 'user_msg'})
                                        break
                        elif isinstance(content2, str) and len(content2) > 15:
                            messages.append({'text': content2, 'timestamp': '', 'source': 'user_str'})

                    # OpenClaw agents: message.role=user
                    elif t in ('message', 'assistant-request') or 'message' in obj:
                        msg = obj.get('message', {})
                        if msg.get('role') == 'user':
                            content2 = msg.get('content', [])
                            if isinstance(content2, list):
                                for c in content2:
                                    if c.get('type') == 'text':
                                        text = c.get('text','').strip()
                                        if text and len(text) > 15:
                                            ts = obj.get('timestamp','')[:16] if obj.get('timestamp') else ''
                                            messages.append({'text': text, 'timestamp': ts, 'source': 'openclaw'})
                                            break
                except:
                    pass
    except Exception as e:
        pass
    return messages

def filter_coach_messages(messages):
    """過濾明顯不是教練的訊息"""
    skip_patterns = [
        r'^[{[{]',
        r'^「.*」$',
        r'^(True|False|null|undefined)$',
        r'^[\[（(]Request',
        r'^```',
    ]
    filtered = []
    for msg in messages:
        text = msg['text']
        skip = False
        for pat in skip_patterns:
            if re.match(pat, text):
                skip = True
                break
        if len(text.strip()) < 20:
            skip = True
        if not skip:
            filtered.append(msg)
    return filtered

def identify_scenes(messages, chunk_size=30):
    """將訊息分組為場景"""
    if not messages:
        return []
    scenes = []
    for i in range(0, len(messages), chunk_size):
        chunk = messages[i:i+chunk_size]
        if len(chunk) < 3:
            continue
        scenes.append({
            'messages': [m['text'] for m in chunk],
            'timestamp': chunk[0].get('timestamp',''),
            'count': len(chunk)
        })
    return scenes

def build_case(case_id, scene, month):
    """生成格式D案例"""
    msgs = scene['messages']
    key_msgs = sorted(msgs, key=lambda x: len(x), reverse=True)[:3]
    coach_quotes = '\n\n'.join([f'> {m}' for m in key_msgs])
    case_type = '❌ 失敗' if any(kw in ' '.join(msgs[:5]) for kw in ['不對','錯','問題','失敗','生氣','抱怨']) else '💬 教練互動'
    rules = []
    if any('commit' in m or '上傳' in m for m in msgs): rules.append('#05')
    if any('問' in m or '不知道' in m for m in msgs): rules.append('#15')
    if any('方向' in m or '地圖' in m for m in msgs): rules.append('#02')
    if any('記住' in m or '記憶' in m for m in msgs): rules.append('#11')
    rule_str = ', '.join(rules) if rules else ''
    title = msgs[0][:40].replace('\n', ' ').strip()
    date_str = f'2026-{month}-XX'
    return f"""## 📖 案例 [{case_id}]{title}...

**犯錯日期：** {date_str}
**類型：** {case_type}
**違反守則：** {rule_str}

### 📣 教練原話（一字不差）
{coach_quotes}

---

### 🌱 悟到什麼（待軍師填寫）
> 悟到什麼：_________________

### 🧬 DNA層次對應（待填寫）
- **使命** →
- **願景** →
- **理念** →
- **信念一/二/三** →

### ⚡ 觸發訊號（待填寫）
| 觸發情境 | AI該有的反應 |
|---------|------------|
|  | |

### ✅ 行動指引（待填寫）
**做：**
**禁：**

### 📊 守則對照表（待填寫）
| 守則 | 違反內容 | 正確做法 |
|------|---------|---------|
|  |  |  |

---
"""

def main():
    sessions = get_all_sessions()
    print(f'=== 小龍蝦對話蒸餾 v3 ===')
    print(f'找到 {len(sessions)} 個 session（所有來源）\n')

    # 無參數：展示所有 sessions
    if len(sys.argv) < 2:
        print('可用 sessions：')
        by_source = {}
        for s in sessions:
            ts = get_first_timestamp(s['path'])
            key = s['source']
            if key not in by_source:
                by_source[key] = []
            by_source[key].append((s['name'][:12], ts, s['size']))

        for src in sorted(by_source.keys()):
            items = by_source[src]
            print(f'\n【{src}】({len(items)} 個)')
            for name, ts, sz in items[:5]:
                print(f'  {name}  ts={ts}  {sz//1024}KB')
            if len(items) > 5:
                print(f'  ... 還有 {len(items)-5} 個')
        print('\n用法: python3 distill_lobster_v2.py <月份> <輸出檔>')
        print('例: python3 distill_lobster_v2.py 05 distill/5月場景庫_格式D.md')
        return

    month = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f'distill/{month}月場景庫_格式D_v3.md'

    # 按實際時間戳過濾
    month_sessions = []
    for s in sessions:
        ts = get_first_timestamp(s['path'])
        if ts and ts[5:7] == month:
            month_sessions.append(s)

    print(f'{month}月 sessions: {len(month_sessions)} 個')
    for s in month_sessions:
        ts = get_first_timestamp(s['path'])
        print(f'  [{s["source"]}] {s["name"][:12]} ts={ts} {s["size"]//1024}KB')

    # 讀取並提取
    all_messages = []
    for s in month_sessions:
        msgs = extract_coach_messages(s['path'])
        print(f'  → {s["name"][:12]}: {len(msgs)}則')
        all_messages.extend(msgs)

    print(f'\n共讀到 {len(all_messages)} 則')
    filtered = filter_coach_messages(all_messages)
    print(f'過濾後 {len(filtered)} 則')
    scenes = identify_scenes(filtered)
    print(f'場景 {len(scenes)} 個')

    # 生成
    prefix = month if len(month) == 2 else f'0{month}'
    cases = [build_case(f'{prefix}{i+1:04d}', s, month) for i, s in enumerate(scenes)]

    header = f"""# 特助場景庫——格式D（{len(cases)}個案例）

> 格式：格式D（統合建議）
> 來源：所有 session 來源（v3 reader）
> 指導框架：特助心法
> 自動產出，需軍師審核補充

---

## 📊 統計

- Session檔：{len(month_sessions)}個
- 教練訊息：{len(filtered)}則
- 場景：{len(scenes)}個

---

"""

    with open(output_file, 'w') as f:
        f.write(header)
        for case in cases:
            f.write(case + '\n')

    print(f'\n✅ 已寫入 {output_file}')

if __name__ == '__main__':
    main()