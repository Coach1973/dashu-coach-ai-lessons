#!/bin/bash
# Hook: Stop（Mac 端）
# 用途: Session 結束時自動把接力棒/記憶/心跳 push 到 GitHub，
#       讓 Windows 軍師下次「開工」git pull 就拿到 Mac 最新進度，教練不當搬運工。
# 設計:
#   - 只 push 同步相關檔（接力棒、心跳、memory/、knowledges/）
#   - 沒實質變動就不 commit（避免 git noise）
#   - 10 秒鎖：同 session 重複 Stop 不重跑
#   - 失敗靜默退出，不阻塞 hook 鏈
set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
# 2026-07-08 Fable5 稽核修復：推送紀錄改寫 /tmp，不寫 HEARTBEAT.md。
# 原因：HEARTBEAT.md 在同步清單裡，寫進去會讓它永遠是髒的 → 每次 Stop 都
# 觸發一次只推「上次推送紀錄」的空轉 commit（自我餵養循環）。
# 推送憑證改由 commit 本身留痕（git log 可查），不需要重複記帳。
LOG="/tmp/session_end_push.log"
LOCK="/tmp/session_end_push.lock"

# 10 秒內重複觸發直接退出（Stop hook 可能連續觸發）
if [[ -f "$LOCK" ]]; then
  AGE=$(( $(date +%s) - $(stat -f %m "$LOCK" 2>/dev/null || echo 0) ))
  [[ "$AGE" -lt 10 ]] && exit 0
fi
touch "$LOCK"

cd "$WS" 2>/dev/null || exit 0

# ~/.claude/ 的全域規則與技能不在 git 裡，雲端工作頁讀不到；每次回覆結束複製一份進 cloud_sync/
bash "$WS/scripts/cloud/mirror_to_cloud_sync.sh" 2>/dev/null

# 只追蹤同步相關檔（避免 push noise，例如 node_modules、log）
SYNC_PATHS=(
  "JUNSHI_HANDOFF_LATEST.md"
  "CLAUDE.md"
  "HEARTBEAT.md"
  "memory/"
  "knowledges/"
  "試金石/"
  "scripts/"
  "cloud_sync/"
  ".claude/settings.json"
)

# 過濾出真的有變動的路徑
DIRTY=()
for p in "${SYNC_PATHS[@]}"; do
  if [[ -e "$p" ]] && ! git diff --quiet -- "$p" 2>/dev/null; then
    DIRTY+=("$p")
  fi
  # untracked 新檔也算
  if [[ -e "$p" ]] && git ls-files --others --exclude-standard -- "$p" 2>/dev/null | grep -q .; then
    DIRTY+=("$p")
  fi
done

# 軍師自己的記憶（~/.claude/projects/…/memory 連到 claude-brain）：只同步 .md，data/ 底下的名單不自動推
# 2026-10-05 發現 10/04～10/05 寫的 7 篇記憶從沒進 git（上面只有小龍蝦的 memory/）
while IFS= read -r f; do
  [[ -n "$f" ]] && DIRTY+=("$f")
done < <(git -c core.quotePath=false ls-files -m -o --exclude-standard -- 'claude-brain/*.md' 2>/dev/null)

# 空清單先擋（bash 3.2 在 set -u 下展開空陣列會報 unbound variable，
# 舊版因 HEARTBEAT 永遠髒、此路徑從未走到；2026-07-08 斷循環後現形，一併修正）
if [[ ${#DIRTY[@]} -eq 0 ]]; then
  exit 0
fi

# 去重
DIRTY=($(printf '%s\n' "${DIRTY[@]}" | sort -u))

# 加入 stage
git add "${DIRTY[@]}" 2>/dev/null

# 確認 stage 有東西才 commit
if git diff --cached --quiet 2>/dev/null; then
  exit 0
fi

STAMP=$(date '+%Y-%m-%d %H:%M')
COMMIT_MSG="[Mac] session-end 自動同步 $STAMP"

PUSH_RESULT="❓ unknown"
if git commit -m "$COMMIT_MSG" >/dev/null 2>&1; then
  COMMIT_HASH=$(git rev-parse --short HEAD)

  # 2026-08-26 聯想查出「三台各自為政」第4層根因，Mac的.sh版同樣中招：
  # 原本commit完直接push，只要聯想/ACER剛好在這之間推過東西就會被"fetch first"
  # 拒絕，東西永遠留在本機、其他機器看不到，而且訊息誤標成「離線/網路」蓋掉真因。
  # 修法跟聯想的.ps1版本對齊：push前先stash(保護剛commit後可能還有的雜項變動)→
  # pull --rebase → push → stash pop。
  STASHED=0
  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    if git stash push -u -m "auto-push-stash-$(date +%Y%m%d%H%M%S)" --quiet 2>/dev/null; then
      STASHED=1
    fi
  fi

  PULL_OK=0
  if git pull --rebase --quiet 2>/dev/null; then
    PULL_OK=1
  fi

  PUSH_OK=0
  if git push origin main >/dev/null 2>&1; then
    PUSH_OK=1
  fi
  COMMIT_HASH=$(git rev-parse --short HEAD)

  STASH_NOTE=""
  if [[ "$STASHED" -eq 1 ]]; then
    if ! git stash pop --quiet 2>/dev/null; then
      STASH_NOTE="（⚠️ stash pop 有衝突，改動保留在 git stash list 未遺失）"
    fi
  fi

  if [[ "$PUSH_OK" -eq 1 ]]; then
    PUSH_RESULT="✅ pushed ${COMMIT_HASH}${STASH_NOTE}"
  elif [[ "$PULL_OK" -eq 0 ]]; then
    PUSH_RESULT="⚠️ commit ${COMMIT_HASH} 本機留底，pull --rebase 失敗（衝突需手動處理）${STASH_NOTE}"
  else
    PUSH_RESULT="⚠️ commit ${COMMIT_HASH} 本機留底，push 失敗（離線/credential）${STASH_NOTE}"
  fi
else
  PUSH_RESULT="ℹ️ 沒實質變動"
fi

# 寫心跳留證
{
  echo ""
  echo "## 🚀 Session-End 雲端同步 $STAMP（Mac）"
  echo "- $PUSH_RESULT"
  echo "- 同步路徑：${DIRTY[*]}"
} >> "$LOG" 2>/dev/null || true

# ===== Phase 2：掃描 github_repos/* 網站專案，push 掉任何領先 origin 的 commit =====
# 2026-08-23新增。起因：bigtree-tw 8/14的雙寫程式碼commit在本機做完就結束，
# 沒有push，剛好這類站台用git archive HEAD本機打包部署，deploy當下成功掩蓋了
# 「沒推」這件事——一週後另一台機器在缺這段程式碼的origin基礎上疊加新commit並push，
# 把它永久蓋掉，直到金門場報名數對不上才被查出來。上面這段只保護workspace自己，
# 完全沒保護底下22個網站專案repo，這裡補上同等保護：E01「commit必須同輪push」
# 這條鐵律過去只是文件承諾、沒有工具強制，現在改成每輪結束自動檢查+補推，
# 讓「commit了卻忘記push」這件事在架構上不可能再安靜躺過一週不被發現。
REPOS_ROOT="/Users/bymyway/github_repos"
REPO_LOCK="/tmp/session_end_repo_push.lock"

if [[ -d "$REPOS_ROOT" ]]; then
  REPO_LOCK_STALE=1
  if [[ -f "$REPO_LOCK" ]]; then
    REPO_AGE=$(( $(date +%s) - $(stat -f %m "$REPO_LOCK" 2>/dev/null || echo 0) ))
    [[ "$REPO_AGE" -lt 10 ]] && REPO_LOCK_STALE=0
  fi

  if [[ "$REPO_LOCK_STALE" -eq 1 ]]; then
    touch "$REPO_LOCK"
    for repo_dir in "$REPOS_ROOT"/*/; do
      [[ -d "$repo_dir/.git" ]] || continue
      repo_name=$(basename "$repo_dir")
      ( cd "$repo_dir" 2>/dev/null || exit 0
        # 沒設定 upstream 的跳過（可能是刻意的本機專案，不動它）
        git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1 || exit 0
        AHEAD=$(git rev-list '@{u}..HEAD' --count 2>/dev/null || echo 0)
        [[ "$AHEAD" -gt 0 ]] || exit 0
        if git push >/dev/null 2>&1; then
          echo "$(date '+%Y-%m-%d %H:%M') ✅ $repo_name: 補推了 $AHEAD 筆先前未推送的 commit" >> "$LOG"
        else
          {
            echo ""
            echo "## ⚠️ 未推送 commit 補推失敗 $STAMP（$repo_name）"
            echo "- $repo_name 有 $AHEAD 筆本機 commit 領先 origin，自動 push 失敗（離線/衝突），需人工檢查 \`cd $repo_dir && git push\`"
          } >> "$WS/HEARTBEAT.md" 2>/dev/null || true
        fi
      )
    done
  fi
fi

exit 0
