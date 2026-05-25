#!/usr/bin/env python3
"""
場景蒸餾品質檢查器
用途：驗證格式D案例是否符合SOP標準
用法：python3 distill/quality_checker.py <案例檔案.md>
      python3 distill/quality_checker.py distill/特助場景庫_格式D.md

檢查項目：
  1. 10個必填欄位是否完整
  2. 6個收錄標準是否至少符合一個
  3. 🌱是否提煉核心而非描述症狀
  4. 守則對照表格式是否正確
"""

import re
import sys
import os
from pathlib import Path

# ====== SOP 標準常數 ======

REQUIRED_FIELDS = {
    'title':     (r'##\s+.*案例\s+\[?[A-Z0-9]+\]?[:：]',  '案例標題（## 案例 XXX）'),
    'date':      (r'\*\*犯錯日期[：:]\*\*|\*\*日期[：:]\*\*',  '日期（**犯錯日期：** 或 **日期：**）'),
    'type':      (r'\*\*類型[：:]\*\*',                    '類型（**類型：** ❌失敗 / ✅成功）'),
    'rule':      (r'\*\*(違反|對應)(守則[：:])\*\*',        '守則標註（**違反守則：** 或 **對應守則：**）'),
    'quote':     (r'###\s+📣\s+教練原話',                  '📣教練原話'),
    'insight':   (r'###\s+🌱\s+悟到什麼',                  '🌱悟到什麼'),
    'dna':       (r'###\s+🧬\s+DNA',                      '🧬DNA層次對應'),
    'trigger':   (r'###\s+⚡\s+觸發訊號',                  '⚡觸�發訊號'),
    'action':    (r'###\s+✅\s+行動指引',                  '✅行動指引'),
    'table':     (r'###\s+📊\s+守則對照表',               '📊守則對照表'),
}

# 格式D成功案例用「對應守則」，失敗案例用「違反守則」
VALID_RULE_HEADERS = ['違反守則', '對應守則']

# 🌱症狀關鍵詞（說明沒有提煉核心）
INSIGHT_SYMPTOM_KEYWORDS = [
    '教練生氣', '教練不高興', '教練抱怨', '教練不滿', '教練火大',
    '教練累了', '教練很無奈', '教練嘆氣',
    'AI搞砸了', 'AI失敗了', 'AI又犯了',
]

# 🌱核心關鍵詞（說明有提煉核心）
INSIGHT_CORE_KEYWORDS = [
    '核心', '本質', '根本', '底層', '原則', '鐵律', '底層邏輯',
    '不是...而是...', '要先...才能...', '只有...才...',
]

# 6個收錄標準
RECORD_CRITERIA = [
    ('新規則建立', r'守則.*起源|新規則|最高指導原則'),
    ('AI錯誤糾正', r'糾正|犯錯|失敗|問題所在|搞砸'),
    ('價值判斷', r'信念|使命|願景|理念|道德|對的事'),
    ('關鍵决策', r'决策|分工|優先|方向|拍板'),
    ('錯誤重複', r'重複|又犯|同樣的錯|屡次'),
    ('具體數字', r'\d+分鐘|\d+小時|\d+MB|\d+次|\d+個'),
]

# 守則對照表格式
TABLE_PATTERN = re.compile(
    r'\|\s*守則\s*\|[^|]*\|[^|]*\|\s*\n'
    r'\|\s*[-| ]+\s*\|[-| ]+\s*\|[-| ]+\s*\|'
)


def extract_cases(text: str):
    """從Markdown文字中拆出所有案例"""
    # 以 ## 案例 作為分割點
    parts = re.split(r'(?=##\s+[^#\n]+案例\s+)', text)
    cases = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # 找標題（支援 [03001] 或 案例 03001 或 案例 034 等各種格式）
        title_match = re.search(r'##\s+[^#\n]+案例\s+(\[?\w+\d+\]?)[:：]\s*(.*)', part)
        if not title_match:
            continue
        case_id = title_match.group(1)
        title = title_match.group(2).strip()
        cases.append({'id': case_id, 'title': title, 'text': part})
    return cases


def check_field(text: str, field_name: str) -> tuple[bool, str]:
    """檢查單一欄位是否存在"""
    pattern, desc = REQUIRED_FIELDS[field_name]
    if re.search(pattern, text):
        return True, f'✅ {desc}'
    else:
        return False, f'❌ 缺少：{desc}'


def check_all_fields(text: str) -> dict:
    """檢查所有10個必填欄位"""
    results = {}
    for field_name in REQUIRED_FIELDS:
        ok, msg = check_field(text, field_name)
        results[field_name] = ok
    return results


def check_insight(text: str) -> dict:
    """檢查🌱是否提煉核心而非症狀"""
    # 找🌱區塊（支援兩種格式：> 引用格式 或 普通文字格式）
    match = re.search(r'###\s+🌱\s+悟到什麼.*?\n(>.*?\n)?(.*?)(?=###|\Z)', text, re.DOTALL)
    if not match:
        return {'ok': False, 'reason': '找不到🌱區塊', 'level': '❌'}

    # 嘗試從 blockquote 提取
    bq_match = re.search(r'###\s+🌱\s+悟到什麼.*?\n(>.*?\n)(.*?)(?=###|\Z)', text, re.DOTALL)
    if bq_match:
        insight_text = re.sub(r'[#*>`|\-]', '', bq_match.group(1)).strip()
    else:
        insight_text = re.sub(r'[#*>`|\-]', '', match.group(2) if match.group(2) else '').strip()

    if not insight_text:
        return {'ok': False, 'reason': '🌱內容為空（待填寫狀態）', 'level': '❌', 'text': insight_text[:100]}

    has_symptom = any(kw in insight_text for kw in INSIGHT_SYMPTOM_KEYWORDS)
    has_core = any(kw in insight_text for kw in INSIGHT_CORE_KEYWORDS)

    if has_symptom and not has_core:
        return {
            'ok': False,
            'reason': f'🌱描述症狀而非核心（關鍵詞：{"/".join([k for k in INSIGHT_SYMPTOM_KEYWORDS if k in insight_text])}）',
            'level': '❌',
            'text': insight_text[:100]
        }

    if len(insight_text) < 10:
        return {'ok': False, 'reason': '🌱內容太短（少於10字）', 'level': '❌', 'text': insight_text[:100]}

    if has_core:
        return {'ok': True, 'reason': '✅ 有核心提煉關鍵詞', 'level': '🟢', 'text': insight_text[:100]}
    else:
        return {'ok': True, 'reason': '⚠️  無核心關鍵詞但不構成明顯症狀', 'level': '🟡', 'text': insight_text[:100]}


def check_record_criteria(text: str) -> dict:
    """檢查是否符合6個收錄標準"""
    matches = []
    for name, pattern in RECORD_CRITERIA:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(name)

    if matches:
        return {'ok': True, 'matched': matches, 'level': '🟢'}
    else:
        return {'ok': False, 'matched': [], 'level': '❌', 'reason': '未符合任何收錄標準'}


def check_rule_header(text: str) -> dict:
    """檢查守則標題：失敗案例用違反，成功案例用對應"""
    # 先確認是成功還是失敗
    type_match = re.search(r'\*\*類型[：:]\*\*\s*(.*)', text)
    if not type_match:
        return {'ok': False, 'reason': '找不到類型'}

    case_type = type_match.group(1)

    # 找守則標題
    rule_match = re.search(r'\*\*([違反|對應])守則[：:]\*\*', text)
    if not rule_match:
        return {'ok': False, 'reason': '找不到守則標題'}

    rule_header = rule_match.group(1)

    if '失敗' in case_type or '❌' in case_type:
        expected = '違反守則'
        actual = rule_header
    else:  # 成功
        expected = '對應守則'
        actual = rule_header

    if expected == actual:
        return {'ok': True, 'reason': f'✅ 標題正確（{actual}）', 'level': '🟢'}
    else:
        return {
            'ok': False,
            'reason': f'❌ 標題錯誤：{actual}（成功案例應為「對應守則」，失敗案例應為「違反守則」）',
            'level': '❌',
            'expected': expected,
            'actual': actual
        }


def check_table_format(text: str) -> dict:
    """檢查守則對照表格式"""
    # 找表格
    table_match = re.search(r'(###\s+📊\s+[守則對照表|對應守則表].*?\n\n\|.*)', text, re.DOTALL)
    if not table_match:
        return {'ok': False, 'reason': '找不到守則對照表', 'level': '❌'}

    table_text = table_match.group(1)

    # 檢查三列格式
    lines = [l for l in table_text.split('\n') if l.strip().startswith('|')]
    if len(lines) < 2:
        return {'ok': False, 'reason': '表格格式錯誤（少於2行）', 'level': '❌'}

    # 檢查每行是否有3列
    bad_lines = [l for l in lines if l.count('|') < 3]
    if bad_lines:
        return {'ok': False, 'reason': f'表格有{len(bad_lines)}行列數不足', 'level': '❌'}

    # 成功案例：表頭應為「對應內容」而非「違反內容」
    if re.search(r'\*\*對應守則', text):
        if '違反內容' in table_text:
            return {'ok': False, 'reason': '成功案例的表格應用「對應內容」而非「違反內容」', 'level': '❌'}
        elif '對應內容' in table_text:
            return {'ok': True, 'reason': '✅ 成功案例表格格式正確', 'level': '🟢'}
        else:
            return {'ok': True, 'reason': '✅ 表格格式正確（無「違反內容」關鍵詞）', 'level': '🟢'}

    return {'ok': True, 'reason': '✅ 表格格式正確', 'level': '🟢'}


def check_dna_completeness(text: str) -> dict:
    """檢查🧬DNA對應是否包含使命/願景/信念/理念"""
    # 找DNA區塊
    match = re.search(r'###\s+🧬\s+DNA.*?(?=###|\Z)', text, re.DOTALL)
    if not match:
        return {'ok': False, 'reason': '找不到DNA區塊', 'level': '❌'}

    dna_text = match.group(0)

    required = ['使命', '願景', '信念', '理念']
    found = [r for r in required if r in dna_text]
    missing = [r for r in required if r not in dna_text]

    if missing:
        return {
            'ok': False,
            'reason': f'❌ 缺少：{"、".join(missing)}',
            'level': '❌',
            'missing': missing,
            'found': found
        }
    return {'ok': True, 'reason': f'✅ DNA完整（使命/願景/信念/理念都有）', 'level': '🟢', 'found': found}


def check_trigger_signal(text: str) -> dict:
    """檢查⚡觸發訊號是否有表格"""
    match = re.search(r'###\s+⚡\s+觸發訊號.*?\n\n(\|.*?\n){2,}', text, re.DOTALL)
    if match:
        return {'ok': True, 'reason': '✅ 有觸發訊號表格', 'level': '🟢'}
    return {'ok': False, 'reason': '⚠️  無觸發訊號表格（建議要有）', 'level': '🟡'}


def score_case(case: dict) -> dict:
    """對單一案例評分"""
    text = case['text']
    case_id = case['id']
    title = case['title']

    # 1. 欄位檢查
    fields = check_all_fields(text)
    field_score = sum(fields.values()) / len(fields) * 100

    # 2. 🌱檢查
    insight = check_insight(text)

    # 3. 收錄標準
    criteria = check_record_criteria(text)

    # 4. 守則標題
    rule_header = check_rule_header(text)

    # 5. 表格格式
    table = check_table_format(text)

    # 6. DNA完整性
    dna = check_dna_completeness(text)

    # 7. 觸發訊號
    trigger = check_trigger_signal(text)

    # 總分：欄位×0.3 + 核心×0.2 + 收錄×0.15 + 標題×0.15 + 表格×0.1 + DNA×0.1
    # 不含觸發訊號（建議性）
    total_score = (
        field_score * 0.30 +
        (100 if insight['ok'] else 0) * 0.20 +
        (100 if criteria['ok'] else 0) * 0.15 +
        (100 if rule_header['ok'] else 0) * 0.15 +
        (100 if table['ok'] else 0) * 0.10 +
        (100 if dna['ok'] else 0) * 0.10
    )

    # 最終判定：總分≥70 且 欄位≥80% 且 🌱合格 且 收錄標準起碼1個
    passed = (
        total_score >= 70 and
        field_score >= 80 and
        insight['ok'] and
        criteria['ok'] and
        rule_header['ok']
    )

    return {
        'case_id': case_id,
        'title': title,
        'score': round(total_score, 1),
        'passed': passed,
        'field_score': round(field_score, 1),
        'field_detail': fields,
        'insight': insight,
        'criteria': criteria,
        'rule_header': rule_header,
        'table': table,
        'dna': dna,
        'trigger': trigger,
    }


def print_report(results: list):
    """印出檢查報告"""
    print('\n' + '='*60)
    print('🏁 場景蒸餾品質檢查報告')
    print('='*60)

    passed = [r for r in results if r['passed']]
    failed = [r for r in results if not r['passed']]

    print(f'\n📊 總覽：{len(results)} 個案例 | ✅合格 {len(passed)} | ❌不合格 {len(failed)}')

    # 總分排名
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    print(f'📈 平均分：{avg_score:.1f}分')

    print('\n' + '-'*60)
    print('🔴 不合格案例（需要修改）')
    print('-'*60)
    if not failed:
        print('  （無）')
    for r in failed:
        print(f'\n  ❌ {r["case_id"]}：{r["title"][:40]}')
        print(f'     總分：{r["score"]}分 | 欄位：{r["field_score"]}%')
        reasons = []
        if not r['insight']['ok']: reasons.append(f"🌱{r['insight']['reason']}")
        if not r['criteria']['ok']: reasons.append(f"📋{r['criteria']['reason']}")
        if not r['rule_header']['ok']: reasons.append(f"守則{r['rule_header']['reason']}")
        if not r['table']['ok']: reasons.append(f"📊{r['table']['reason']}")
        if not r['dna']['ok']: reasons.append(f"🧬{r['dna']['reason']}")
        print(f'     問題：{" | ".join(reasons)}')

    print('\n' + '-'*60)
    print('🟢 合格案例')
    print('-'*60)
    for r in sorted_results:
        if r['passed']:
            print(f'\n  ✅ {r["case_id"]}：{r["title"][:40]}')
            print(f'     總分：{r["score"]}分 | 欄位：{r["field_score"]}%')
            reasons = []
            if r['insight']['ok']: reasons.append(f"🌱{r['insight']['level']}")
            if r['criteria']['ok']: reasons.append(f"📋符合{len(r['criteria']['matched'])}個標準")
            if r['rule_header']['ok']: reasons.append(f"守則✅")
            if r['dna']['ok']: reasons.append(f"🧬完整")
            print(f'     良好：{" | ".join(reasons)}')

    print('\n' + '-'*60)
    print('📋 欄位完整度（所有案例）')
    print('-'*60)
    field_names = list(REQUIRED_FIELDS.keys())
    for field in field_names:
        count = sum(1 for r in results if r['field_detail'].get(field, False))
        pct = count / len(results) * 100 if results else 0
        bar = '█' * int(pct/10) + '░' * (10 - int(pct/10))
        field_desc = REQUIRED_FIELDS[field][1]
        print(f'  {field_desc:<30} {bar} {pct:.0f}%')

    print('\n' + '='*60)
    if failed:
        print('⚠️  有不合格案例，請根據上述問題修改後重新檢查')
    else:
        print('🎉 所有案例合格！')
    print('='*60 + '\n')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print('\n使用範例：')
        print('  python3 distill/quality_checker.py distill/特助場景庫_格式D.md')
        print('  python3 distill/quality_checker.py distill/100場景_追加_終端機B.md')
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f'❌ 找不到檔案：{filepath}')
        sys.exit(1)

    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    cases = extract_cases(text)
    if not cases:
        print(f'❌ 在 {filepath} 中找不到任何案例（需要包含「## 案例 XXX」標題）')
        sys.exit(1)

    print(f'🔍 找到 {len(cases)} 個案例，開始品質檢查...\n')

    results = []
    for case in cases:
        r = score_case(case)
        results.append(r)
        status = '✅' if r['passed'] else '❌'
        print(f'  {status} {r["case_id"]:6s} | {r["score"]:5.1f}分 | {r["title"][:35]}')

    print_report(results)

    # 如果是不合格的就exit 1
    failed = [r for r in results if not r['passed']]
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
