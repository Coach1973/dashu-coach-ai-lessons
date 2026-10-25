#!/bin/bash
# junshi_task_worker.sh — 小龍蝦→軍師 任務橋接
# WatchPaths 觸發：state/JUNSHI_TASK_QUEUE 一寫入就執行
# 2026-06-13 軍師建立（教練親定）

set -uo pipefail

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8

QUEUE="/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_QUEUE"
RESULT="/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_RESULT"
LOCKFILE="/tmp/junshi_task_worker.lock"
LOGFILE="/Users/bymyway/Library/Logs/openclaw/junshi_task_worker.log"
# 2026-08-25 體檢：token 原本硬編碼在此行，改成從 openclaw.json 讀
MAIN_BOT_TOKEN=$(python3 -c "
import json
try:
    d = json.load(open('/Users/bymyway/.openclaw/openclaw.json'))
    print(d['channels']['telegram']['accounts']['bot_main']['botToken'])
except Exception:
    print('')
")
COACH_CHAT_ID="6124913915"
CLAUDE_CLI="/Users/bymyway/.local/bin/claude"
GH_CLI="/opt/homebrew/bin/gh"

mkdir -p "$(dirname "$LOGFILE")"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOGFILE"; }

notify_telegram() {
  local msg="$1"
  # 2026-08-25教練親口要求：跟小龍蝦(AI)自己講的話要分得清楚，統一加標籤
  curl -sS -X POST "https://api.telegram.org/bot${MAIN_BOT_TOKEN}/sendMessage" \
    -d chat_id="$COACH_CHAT_ID" \
    -d text="🤖【賈維斯自動通知】
$msg" \
    -d parse_mode="Markdown" > /dev/null 2>&1 || true
}

# 防止重複執行
if [ -f "$LOCKFILE" ]; then
  lock_age=$(( $(date +%s) - $(stat -f %m "$LOCKFILE") ))
  if [ "$lock_age" -lt 300 ]; then
    log "SKIP: lockfile exists (${lock_age}s old)"
    exit 0
  fi
  log "WARN: stale lockfile (${lock_age}s), removing"
  rm -f "$LOCKFILE"
fi

cleanup() {
  rm -f "$LOCKFILE"
  # 不管成功失敗都清 QUEUE，避免卡住重複觸發
  if [ -f "$QUEUE" ]; then
    tail -n +2 "$QUEUE" > "${QUEUE}.tmp" 2>/dev/null || true
    mv "${QUEUE}.tmp" "$QUEUE" 2>/dev/null || true
    [ -s "$QUEUE" ] || rm -f "$QUEUE"
  fi
}
trap cleanup EXIT
touch "$LOCKFILE"

# 沒有任務就退出
if [ ! -f "$QUEUE" ] || [ ! -s "$QUEUE" ]; then
  log "No tasks in queue"
  exit 0
fi

# 讀取第一行任務
TASK_LINE=$(head -1 "$QUEUE")
log "Processing: $TASK_LINE"

TASK_TYPE=$(/opt/homebrew/bin/python3 -c "import json,sys; print(json.loads(sys.argv[1]).get('type','unknown'))" "$TASK_LINE" 2>/dev/null || echo "unknown")
TASK_ID=$(/opt/homebrew/bin/python3 -c "import json,sys; print(json.loads(sys.argv[1]).get('id','?'))" "$TASK_LINE" 2>/dev/null || echo "?")

write_result() {
  local status="$1" message="$2"
  printf '%s\n%s\n%s' "$TASK_ID" "$status" "$message" | /opt/homebrew/bin/python3 -c "
import json, datetime, sys
lines = sys.stdin.read().split('\n', 2)
r = {'id': lines[0], 'status': lines[1], 'message': lines[2] if len(lines)>2 else '', 'ts': datetime.datetime.now().astimezone().isoformat()}
with open('$RESULT', 'w') as f:
    json.dump(r, f, ensure_ascii=False, indent=2)
"
}

remove_first_line() {
  tail -n +2 "$QUEUE" > "${QUEUE}.tmp" 2>/dev/null || true
  mv "${QUEUE}.tmp" "$QUEUE" 2>/dev/null || true
  # 如果檔案空了就刪掉（避免 WatchPaths 重複觸發）
  [ -s "$QUEUE" ] || rm -f "$QUEUE"
}

case "$TASK_TYPE" in
  push)
    REPO=$(/opt/homebrew/bin/python3 -c "import json,sys; print(json.loads(sys.argv[1]).get('repo',''))" "$TASK_LINE")
    BRANCH=$(/opt/homebrew/bin/python3 -c "import json,sys; print(json.loads(sys.argv[1]).get('branch','main'))" "$TASK_LINE")
    REPO_PATH="/Users/bymyway/github_repos/${REPO}"

    if [ ! -d "$REPO_PATH/.git" ]; then
      MSG="❌ 推送失敗：找不到 repo ${REPO}（路徑 ${REPO_PATH}）"
      log "$MSG"
      write_result "error" "$MSG" || log "WARN: write_result failed"
      notify_telegram "🔴 軍師任務失敗\n${MSG}" || true
      exit 1
    fi

    cd "$REPO_PATH"
    LATEST_COMMIT=$(git log --oneline -1)
    touch .git/PUSH_APPROVED

    if PUSH_OUTPUT=$(git push origin "$BRANCH" 2>&1); then
      MSG="✅ 推送成功\nRepo: ${REPO}\nBranch: ${BRANCH}\nCommit: ${LATEST_COMMIT}"
      log "$MSG"
      write_result "ok" "$MSG" || log "WARN: write_result failed"
      notify_telegram "🟢 *軍師推送完成*\n📦 ${REPO} → ${BRANCH}\n📝 ${LATEST_COMMIT}" || true
    else
      MSG="❌ 推送失敗\nRepo: ${REPO}\n錯誤: ${PUSH_OUTPUT}"
      log "$MSG"
      write_result "error" "$MSG" || log "WARN: write_result failed"
      notify_telegram "🔴 *軍師推送失敗*\n📦 ${REPO}\n${PUSH_OUTPUT}" || true
    fi
    ;;

  task)
    PROMPT=$(/opt/homebrew/bin/python3 -c "import json,sys; print(json.loads(sys.argv[1]).get('prompt',''))" "$TASK_LINE")

    if [ -z "$PROMPT" ]; then
      MSG="❌ 任務失敗：prompt 為空"
      log "$MSG"
      write_result "error" "$MSG" || log "WARN: write_result failed"
      notify_telegram "🔴 軍師任務失敗：沒有 prompt" || true
      exit 1
    fi

    log "Running claude -p: ${PROMPT:0:100}..."
    notify_telegram "⏳ *軍師開始執行任務*\n📋 ${PROMPT:0:100}..."

    TASK_STDERR=$(mktemp)
    # 2026-10-25 修：派工橋的 claude -p 只認「當前工作目錄」，
    # 導致軍師讀不到 /Users/bymyway/github_repos 底下的 repo
    # （錯誤：「For security, Claude Code may only list files in the allowed working directories」）。
    # 用 --add-dir 開通 github_repos + claude-code workspace，這是「被允許的存取範圍」不是提權。
    TASK_OUTPUT=$("$CLAUDE_CLI" -p "$PROMPT" \
        --add-dir /Users/bymyway/github_repos \
        --add-dir /Users/bymyway/.claude-code/workspace \
        --add-dir /Users/bymyway/.openclaw/workspace \
        --permission-mode acceptEdits --output-format text 2>"$TASK_STDERR" | tail -c 3000) || true
    if [ -s "$TASK_STDERR" ]; then
      log "claude stderr: $(head -c 500 "$TASK_STDERR")"
    fi
    rm -f "$TASK_STDERR"

    log "Task output (first 500): ${TASK_OUTPUT:0:500}"
    write_result "ok" "$TASK_OUTPUT" || log "WARN: write_result failed"
    notify_telegram "🟢 *軍師任務完成*\n📋 ${PROMPT:0:80}...\n📝 ${TASK_OUTPUT:0:300}" || true
    ;;

  *)
    MSG="❌ 未知任務類型: ${TASK_TYPE}"
    log "$MSG"
    write_result "error" "$MSG" || log "WARN: write_result failed"
    notify_telegram "🔴 軍師：未知任務類型 ${TASK_TYPE}" || true
    ;;
esac

remove_first_line
log "Task $TASK_ID done"
