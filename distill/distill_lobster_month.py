#!/usr/bin/env python3
"""
小龍蝦對話蒸餾腳本 - 格式D
用法: python3 distill_lobster_month.py <月份> <輸出檔>
例: python3 distill_lobster_month.py 03 distill/3月場景庫_格式D.md
"""
import json, os, glob, sys, re
from datetime import datetime

def extract_coach_messages(files):
    """從session檔提取教練訊息"""
    messages = []
    for fpath in sorted(files):
        try:
            with open(fpath) as f:
                for line in f:
                    try:
                        d = json.loads(line.strip())
                        if d.get('type') == 'message':
                            msg = d.get('message', {})
                            if msg.get('role') == 'user':
                                content = msg.get('content', [])
                                for c in content:
                                    if isinstance(c, dict) and c.get('type') == 'text':
                                        text = c['text']
                                        if '"sender": "coach"' in text or '"sender_id": "6124913915"' in text:
                                            # 去掉JSON metadata頭，取實際訊息（格式：}...} 之後的內容）
                                            parts = text.rsplit('}', 1)
                                            if len(parts) > 1:
                                                actual = parts[1].strip()
                                            else:
                                                actual = ''
                                            if actual and len(actual) > 2:
                                                ts = ''
                                                ts_match = re.search(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}', text)
                                                if ts_match:
                                                    ts = ts_match.group()
                                                messages.append({
                                                    'text': actual,
                                                    'timestamp': ts,
                                                    'file': os.path.basename(fpath)
                                                })
                    except:
                        pass
        except Exception as e:
            print(f'  讀取失敗 {fpath}: {e}')
    return messages

def group_into_scenes(messages):
    """將訊息分組為場景（每個session一個場景）"""
    scenes = {}
    for msg in messages:
        key = msg['file']
        if key not in scenes:
            scenes[key] = {
                'file': msg['file'],
                'timestamp': msg['timestamp'],
                'messages': []
            }
        scenes[key]['messages'].append(msg['text'])
    return list(scenes.values())

def analyze_scene(scene, month_num):
    """分析單一場景，找出值得蒸餾的教練訊息"""
    all_text = ' '.join(scene['messages'])

    # 預篩：找關鍵訊號
    worth_distilling = False
    signals = []

    # 信號1: 教練在教AI做事
    if any(kw in all_text for kw in ['守則', '原則', '鐵律', '規定', '必須', '不准', '不要', 'commit', 'hash']):
        worth_distilling = True
        signals.append('新規則/鐵律')

    # 信號2: 教練情緒反應
    if any(kw in all_text for kw in ['不是', '錯了', '搞清楚', '你搞', '重新', '不行', '失敗']):
        worth_distilling = True
        signals.append('糾正/情緒')

    # 信號3: 任務分配/指令
    if any(kw in all_text for kw in ['做', '去', '執行', '處理', '開工', '停下', '停', '慢著']):
        worth_distilling = True
        signals.append('指令/任務')

    # 信號4: 價值判斷
    if any(kw in all_text for kw in ['重要', '優先', '核心', '關鍵', '對的', '錯的', '好', '不行']):
        worth_distilling = True
        signals.append('價值判斷')

    # 從訊息中找最有價值的（第一條或最長的）
    if len(scene['messages']) == 0:
        return None

    best_msg = max(scene['messages'], key=len)
    short_msgs = [m for m in scene['messages'] if len(m) < 200]

    return {
        'scene_id': scene['file'][:8],
        'timestamp': scene['timestamp'],
        'message_count': len(scene['messages']),
        'signals': signals,
        'worth': worth_distilling,
        'best_message': best_msg,
        'sample_messages': short_msgs[:5] if short_msgs else [best_msg]
    }

def format_scene_d(scene, idx, month_str):
    """產出格式D的場景"""
    msg = scene['best_message']
    signals_str = ' / '.join(scene['signals']) if scene['signals'] else '一般對話'
    file_key = scene.get('scene_id', 'unknown') + '.reset.file'

    return f"""
## 📖 案例 [{month_str}{idx:03d}]：{msg[:50]}...

**犯錯日期：** {scene['timestamp'][:10] if scene['timestamp'] else f'2026-{month_str}'}
**類型：**  💬 教練互動（需人工確認是否為失敗案例）
**來源：** 小龍蝦{signals_str}訊號
**訊息筆數：** {scene['message_count']}則

---

### 📣 教練原話（代表性訊息）
> {msg[:500]}{'...' if len(msg) > 500 else ''}

### 🌱 待分析（格式D需軍師填寫）
> 悟到什麼：_________________

### 🧬 DNA層次對應（待填寫）
- **使命** →
- **願景** →
- **理念** →
- **信念一/二/三** →
- **違反守則** →

### ⚡ 觸發訊號（待填寫）
| 觸發情境 | AI該有的反應 |

### ✅ 行動指引（待填寫）
**做：**
**禁：**

### 📊 守則對照表（待填寫）
| 守則 | 違反內容 | 正確做法 |

### 🔗 Commit Hash
- 原始session：[查看](file:///Users/bymyway/.openclaw/agents/main/sessions/{scene['scene_id']}*)
"""

def main():
    if len(sys.argv) < 3:
        print('用法: python3 distill_lobster_month.py <月份MM> <輸出檔路徑>')
        sys.exit(1)

    month = sys.argv[1]
    out_file = os.path.expanduser(sys.argv[2])

    sessions_dir = '/Users/bymyway/.openclaw/agents/main/sessions/'
    files = sorted(glob.glob(f'{sessions_dir}*.reset.*{month}*'))

    print(f'📂 找到 {len(files)} 個 {month}月 session 檔')
    print(f'📝 輸出至: {out_file}')

    messages = extract_coach_messages(files)
    print(f'💬 提取 {len(messages)} 則教練訊息')

    scenes = group_into_scenes(messages)
    print(f'🎬 分組為 {len(scenes)} 個場景')

    # 分析每個場景
    analyzed = [analyze_scene(s, month) for s in scenes]
    analyzed = [a for a in analyzed if a is not None]

    # 產出格式D
    month_name = {'03': '三', '04': '四', '05': '五'}.get(month, month)
    header = f"""# 小龍蝦{month_name}月對話場景庫——格式D

> 格式：格式D（統合建議）
> 來源：小龍蝦 {month_name}月 session 蒸餾
> 指導框架：特助心法
> 自動產出，需軍師審核補充「悟到什麼」與守則對應

---

## 📊 統計

- Session檔：{len(files)}個
- 教練訊息：{len(messages)}則
- 場景：{len(scenes)}個
- 有價值訊號：{sum(1 for a in analyzed if a['worth'])}個

---

"""

    scenes_md = []
    for i, scene in enumerate(analyzed, 1):
        scenes_md.append(format_scene_d(scene, i, month))

    output = header + '\n---\n'.join(scenes_md)

    with open(out_file, 'w') as f:
        f.write(output)

    print(f'✅ 已寫入 {out_file}（{len(output)/1024:.1f}KB）')

    # 預覽前3個場景
    print('\n📋 預覽（前3個場景）：')
    for s in analyzed[:3]:
        print(f"  [{s['scene_id']}] {s['signals']} | {s['best_message'][:60]}...")

if __name__ == '__main__':
    main()