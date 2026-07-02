#!/bin/bash
# 用途：掃描試金石案例庫，找出被違反 2 次以上的守則，
#       對照現有機關（hook/script），列出「值得建機關但還沒建」的缺口。
# 觸發時機：新增試金石案例後手動跑，或由 Stop hook 自動觸發。
# 起因（2026-07-02 教練親口）：「不能每次都是我提醒你要建機關」
set -uo pipefail

CASE_FILE="$HOME/.openclaw/workspace/試金石/試金石_案例庫.md"
SCRIPTS_DIR="$HOME/.openclaw/workspace/scripts"

[[ ! -f "$CASE_FILE" ]] && { echo "❌ 找不到試金石案例庫"; exit 1; }

python3 - "$CASE_FILE" "$SCRIPTS_DIR" <<'PYEOF'
import re, sys, os, glob

case_file = sys.argv[1]
scripts_dir = sys.argv[2]

with open(case_file, encoding='utf-8') as f:
    text = f.read()

# Parse cases and find violated rules
pattern = r'## 案例 (\S+?)[\s：:](.*?)(?=\n## 案例 |\Z)'
matches = re.findall(pattern, text, re.DOTALL)

violations = {}
for case_id, body in matches:
    if case_id == 'X-日期':
        continue
    title_match = re.search(r'^(.+?)$', body.strip(), re.MULTILINE)
    title = title_match.group(1)[:50] if title_match else '?'
    rules = set(re.findall(r'#(\d+)', body[:600]))
    for r in rules:
        violations.setdefault(int(r), []).append(case_id)

# Known guardrails mapped to rules
guardrails = {
    5: ('rule05_hash_check.sh', 'Stop hook：檢查 commit hash'),
    7: ('rule07_polling_check.sh', 'Stop hook：攔截輪詢設計語言（部分覆蓋）'),
    12: ('rule12_porter_check.sh', 'Stop hook：攔截叫教練複製貼上'),
}
# Other hooks not directly tied to specific rules
other_hooks = [
    'delete_guard.sh — 刪除鎖（PreToolUse）',
    'netlify_deploy_guard.sh — 部署鎖（PreToolUse）',
    'screenshot_lock.sh — 截圖鎖（PreToolUse）',
    'cross_machine_dispatch_guard.sh — 跨機指令鎖（PreToolUse）',
    'delivery_check.sh — 交付格式檢查（Stop）',
]

print('=' * 60)
print('🔍 試金石案例庫 — 守則違反次數 vs 機關覆蓋狀態')
print('=' * 60)
print()

gaps = []
covered = []

for rule, cases in sorted(violations.items(), key=lambda x: -len(x[1])):
    count = len(cases)
    if count < 2:
        continue

    has_guard = rule in guardrails
    status = f'✅ 已有機關：{guardrails[rule][1]}' if has_guard else '⚠️  無機關'

    print(f'  守則#{rule:02d} — 違反 {count} 次（案例 {", ".join(cases)}）')
    print(f'    {status}')
    print()

    if not has_guard:
        gaps.append((rule, count, cases))
    else:
        covered.append((rule, count))

print('-' * 60)
print()

if gaps:
    print('🔴 以下守則被違反 2 次以上但尚無機關，值得跟教練討論：')
    print()
    rule_names = {
        3: '思考就是問問題（自我驗證再交付）',
        4: '解決問題比解釋問題更重要',
        6: '完美交接是負責任的表現',
        8: '花時間討論就是為了執行',
        15: '說不知道比胡說八道更值得尊重',
        16: '複雜的解法不一定是正確的解法',
        17: '用戶所在環境確認原則',
    }
    for rule, count, cases in sorted(gaps, key=lambda x: -x[1]):
        name = rule_names.get(rule, '（見特助心法）')
        print(f'  #{rule:02d} {name}')
        print(f'      違反 {count} 次，案例：{", ".join(cases)}')
        print()
else:
    print('✅ 所有高頻違反的守則都已有對應機關。')

print('-' * 60)
print()
print('📋 現有機關清單：')
for rule, (script, desc) in sorted(guardrails.items()):
    print(f'  守則#{rule:02d} → {desc}')
for h in other_hooks:
    print(f'  通用 → {h}')
print()
print('💡 判斷標準：同一條守則被違反 2 次以上 = 值得討論是否建機關')
print('   參考：Block（不可逆+教練生氣過）/ Warn（灰色地帶提醒）/ Allow（一般操作）')
print('   每 3-6 個月回頭檢視：這個鎖保護的風險還存在嗎？不存在就砍。')
PYEOF
