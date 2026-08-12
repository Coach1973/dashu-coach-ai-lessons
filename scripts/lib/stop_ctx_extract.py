#!/usr/bin/env python3
"""Stop hook 共用對話紀錄解析器（2026-08-12 全面體檢第2項）

起因：Stop hook 原本有 10 支各自 spawn python3、各自把整份 transcript jsonl
      讀進來 json.loads 一遍——同一份檔案在同一個 Stop 事件裡被重複解析 10 次以上，
      對話越長成本越高（transcript 會長到數 MB）。

做法：把每一支 rule 需要的欄位一次算完輸出成一份 JSON，由 lib/stop_ctx.sh 快取，
      同一個 Stop 事件只解析一次，其餘 rule 讀快取。

🔴 鐵律：本檔案的每個欄位都必須跟原本各 rule 的抽取邏輯「逐字等價」——
      這些 rule 的白名單/索引比較都是血淚案例調校出來的（案例38 誤報、案例46、
      案例52 正則放寬又收緊），改動語意等於偷偷放掉守則防線。
      要改判斷邏輯請改各 rule 自己的 grep 段，不要改這裡的抽取語意。
"""
import json
import re
import sys


def load_lines(path):
    try:
        with open(path, encoding='utf-8') as f:
            return [l for l in f if l.strip()]
    except Exception:
        return None


def parse(line):
    try:
        return json.loads(line)
    except Exception:
        return None


def last_assistant_text(lines):
    """對應原本 rule12 / rule05 / rule03 / rule08 / rule_proactive /
    rule_traditional_chinese / delivery_check 的抽取：最後一筆 assistant 事件的 text 區塊。
    （rule_traditional_chinese 版本另外容許 content 是純字串，取聯集不影響其他 rule）"""
    for line in reversed(lines):
        evt = parse(line)
        if not evt or evt.get('type') != 'assistant':
            continue
        content = evt.get('message', {}).get('content')
        if isinstance(content, list):
            texts = [c.get('text', '') for c in content
                     if isinstance(c, dict) and c.get('type') == 'text']
            return '\n'.join(texts)
        if isinstance(content, str):
            return content
        return ''
    return ''


def turn_segments(lines):
    """對應原本 rule07_polling_check 的抽取：往回掃到上一個 user 事件為止（=這整個回合），
    收 assistant text + Write/Edit 的 content/new_string + Bash 的 command。
    （案例：設計寫進 Write 的檔案內容，不出現在最後一句 text，只看 text 會漏抓）"""
    segments = []
    for line in reversed(lines):
        evt = parse(line)
        if not evt:
            continue
        t = evt.get('type')
        if t == 'user':
            break
        if t != 'assistant':
            continue
        for c in evt.get('message', {}).get('content', []):
            if not isinstance(c, dict):
                continue
            ctype = c.get('type')
            if ctype == 'text':
                segments.append(c.get('text', ''))
            elif ctype == 'tool_use':
                name = c.get('name', '')
                inp = c.get('input', {}) or {}
                if name in ('Write', 'Edit'):
                    segments.append(inp.get('content', ''))
                    segments.append(inp.get('new_string', ''))
                elif name == 'Bash':
                    segments.append(inp.get('command', ''))
    return '\n'.join(reversed(segments))


def _extract_texts(node):
    """只抓「實際內容文字」，跳過信封層的 timestamp 欄位。
    🔴 案例38 後補：每個事件本身的 "timestamp" 一定含 UTC Z 格式，
    若用整行 raw JSONL 判斷會讓 touched_utc 恆為 true。"""
    texts = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'timestamp':
                continue
            if k == 'text' and isinstance(v, str):
                texts.append(v)
            elif k == 'content' and isinstance(v, str):
                texts.append(v)
            else:
                texts.extend(_extract_texts(v))
    elif isinstance(node, list):
        for item in node:
            texts.extend(_extract_texts(item))
    return texts


UTC_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')


def touched_utc(lines):
    """對應原本 rule_taiwan_time_check：這一輪有沒有真的處理過原始 UTC timestamp。
    起點=最後一個「真人發話」的 user 事件（跳過 tool_result 型態的 user 事件）。
    🔴 排除 type=="attachment"：那是 UserPromptSubmit hook 每輪注入的守則提醒，
       本身寫死含範例 Z 時間當教材，會讓判斷恆為 true（案例38 後首次真實對話誤報根因）。"""
    last_user_idx = None
    for i in range(len(lines) - 1, -1, -1):
        evt = parse(lines[i])
        if not evt or evt.get('type') != 'user':
            continue
        content = evt.get('message', {}).get('content')
        if isinstance(content, str) or (isinstance(content, list) and any(
            isinstance(c, dict) and c.get('type') == 'text' for c in content
        )):
            last_user_idx = i
            break
    if last_user_idx is None:
        last_user_idx = 0

    content_texts = []
    for line in lines[last_user_idx:]:
        evt = parse(line)
        if not evt or evt.get('type') == 'attachment':
            continue
        content_texts.extend(_extract_texts(evt.get('message', evt)))
    return bool(UTC_PATTERN.search('\n'.join(content_texts)))


def checked_memory_files(lines):
    """對應原本 rule03 的第二段 python：最近 40 筆事件裡，有沒有 Grep/Read
    去查過 memory / SOP / 特助心法 / 試金石——有查過代表肯定式宣稱是有根據的。"""
    for line in lines[-40:]:
        evt = parse(line)
        if not evt or evt.get('type') != 'assistant':
            continue
        for c in evt.get('message', {}).get('content', []):
            if not isinstance(c, dict) or c.get('type') != 'tool_use':
                continue
            name = c.get('name', '')
            tin = c.get('input', {}) or {}
            target = (str(tin.get('file_path', '')) + str(tin.get('pattern', ''))
                      + str(tin.get('path', '')))
            if name in ('Grep', 'Read') and (
                'memory' in target or 'SOP' in target
                or '特助心法' in target or '試金石' in target
            ):
                return True
    return False


def user_turns(lines):
    """對應原本 rule_proactive_session_reminder_check 的輪數計算
    （與 session_length_hook.sh 同一套算法：只數真人發話，不數 tool_result）。"""
    n = 0
    for line in lines:
        evt = parse(line)
        if not evt or evt.get('type') != 'user':
            continue
        c = (evt.get('message') or {}).get('content')
        if isinstance(c, str) and c.strip():
            n += 1
        elif isinstance(c, list):
            has_text = any(isinstance(b, dict) and b.get('type') == 'text' for b in c)
            has_tr = any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in c)
            if has_text and not has_tr:
                n += 1
    return n


CHROME_PATTERN = re.compile(r"open\s+-a\s+\"?Google Chrome\"?", re.IGNORECASE)
# 只認「動詞後面緊接真正的檔案路徑」，不認純文字描述（案例52 同日兩次調校的結果）
HTML_DEPLOY_PATTERN = re.compile(
    r'\b(?:cp|mv|rsync|git\s+add)\s+(?:[\w.-]+\s+)*([~./][\w./~-]*\.html)\b'
)


def html_chrome(lines):
    """對應原本 rule_html_chrome_check：只看最近 100 筆事件，
    回傳「最後一次改動 .html 的位置」與「最後一次 open -a Google Chrome 的位置」，
    索引是 lines[-100:] 這個切片內的相對位置（原本就是這樣比大小，保持一致）。"""
    recent = lines[-100:]
    html_edit_idx = -1
    html_files = []
    chrome_evidence_idx = -1

    for i, line in enumerate(recent):
        evt = parse(line)
        if not evt or evt.get('type') != 'assistant':
            continue
        for c in evt.get('message', {}).get('content', []):
            if not isinstance(c, dict) or c.get('type') != 'tool_use':
                continue
            name = c.get('name', '')
            tin = c.get('input', {}) or {}

            if name in ('Edit', 'Write'):
                fp = str(tin.get('file_path', ''))
                if fp.lower().endswith('.html'):
                    html_edit_idx = i
                    if fp not in html_files:
                        html_files.append(fp)

            if name == 'Bash':
                command = str(tin.get('command', ''))
                if CHROME_PATTERN.search(command):
                    chrome_evidence_idx = i
                m = HTML_DEPLOY_PATTERN.search(command)
                if m:
                    html_edit_idx = i
                    if m.group(1) not in html_files:
                        html_files.append(m.group(1))

    return html_edit_idx, html_files, chrome_evidence_idx


def main():
    if len(sys.argv) < 2:
        print('{}')
        return
    lines = load_lines(sys.argv[1])
    if lines is None:
        print('{}')
        return

    edit_idx, files, chrome_idx = html_chrome(lines)
    print(json.dumps({
        'last_assistant_text': last_assistant_text(lines),
        'turn_segments': turn_segments(lines),
        'touched_utc': touched_utc(lines),
        'checked_memory_files': checked_memory_files(lines),
        'user_turns': user_turns(lines),
        'html_edit_idx': edit_idx,
        'html_files': files,
        'chrome_evidence_idx': chrome_idx,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
