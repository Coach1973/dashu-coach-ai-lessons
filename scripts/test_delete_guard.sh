#!/bin/bash
# 刪檔鎖永久測試套件（案例 F 教訓：改 hook 必先跑測試，全過才能 commit）
S=/Users/bymyway/.openclaw/workspace/scripts/delete_guard.sh
TOKEN=~/.openclaw/workspace/state/DELETE_APPROVED
PASS=0; FAIL=0

check() {
  if [ "$2" = "$3" ]; then echo "✅ $1"; PASS=$((PASS+1)); else echo "❌ $1（期望 $2，實際 $3）"; FAIL=$((FAIL+1)); fi
}
run() { echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$1")}}" | bash $S >/dev/null 2>&1; echo $?; }

HAD=0; [ -f "$TOKEN" ] && HAD=1 && mv "$TOKEN" "$TOKEN.bak"

check "1 rm -rf 家目錄資料→擋"        2 "$(run 'rm -rf /Users/bymyway/Documents/old_project')"
check "2 rm -r 相對路徑→擋"           2 "$(run 'rm -r my_folder')"
check "3 rm -rf /tmp 暫存→放行"       0 "$(run 'rm -rf /tmp/preview-123')"
check "4 rm 單檔不帶 -r→放行"         0 "$(run 'rm -f ~/.openclaw/workspace/state/PUSH_APPROVED')"
check "5 find -delete→擋"             2 "$(run 'find ~/Documents -name "*.bak" -delete')"
check "6 git clean -fd→擋"            2 "$(run 'git clean -fd')"
check "7 rsync --delete→擋"           2 "$(run 'rsync -av --delete src/ dst/')"
check "8 普通指令 ls→放行"            0 "$(run 'ls -la && git status')"
check "9 rm -rf node_modules→放行"    0 "$(run 'rm -rf node_modules')"
check "10 grep 字面提到 rm -rf→放行"  0 "$(run 'grep -n "rm -rf" scripts/foo.sh')"

check "12 heredoc 文件內提到刪除指令→放行" 0 "$(run 'cat >> notes.md <<EOF
說明：rm -r 和 find -delete 都是危險指令
EOF
git add notes.md')"

mkdir -p "$(dirname "$TOKEN")" && touch "$TOKEN"
check "11 有通行證 rm -rf→放行"       0 "$(run 'rm -rf /Users/bymyway/Documents/old_project')"
rm -f "$TOKEN"

[ $HAD = 1 ] && mv "$TOKEN.bak" "$TOKEN"
echo ""; echo "結果：$PASS 過 / $FAIL 失敗"
[ $FAIL = 0 ] && echo "🎉 全數通過" || exit 1
