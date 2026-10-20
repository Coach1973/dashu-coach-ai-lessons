#!/bin/bash
# 雲端對話交件 → Mac 軍師接手（2026-10-21，根治「雲端做完停在『要你同意』沒人接手」）
#
# 流程：雲端把成果推到 claude/* 分支 → GitHub 通知 event.bymyway.com/hooks/github-site → 寫一筆
#   state/cloud_branch_pending/<倉庫>__<分支>.json（事件觸發，不輪詢）→ 開工注入列在最前面（第一件事）。
# 軍師接手 = 驗證 → 用「正式程式」再測 → 合併上線 → 回報教練。全程不問教練同不同意（教練 10/20：「討論的目的是為了執行」）。
#
# 用法：
#   cloud_branch_pickup.sh list                         列出待接手
#   cloud_branch_pickup.sh prep  <倉庫> <分支>           另開獨立資料夾放這個分支（絕不 checkout 進正在上線的資料夾），印出差異與雲端的信
#   cloud_branch_pickup.sh merge <倉庫> <分支> --verified  合併進預設分支並推上去、更新本機上線資料夾、標記完成
#                                                       （--verified = 我已用正式程式測過，不是只看雲端用假資料的測試）
#   cloud_branch_pickup.sh done  <倉庫> <分支> [原因]     不合併也結案（例如被取代、教練說不要）
WS="${CLOUD_WS:-$HOME/.openclaw/workspace}"
PEND="$WS/state/cloud_branch_pending"
VERIFY="$WS/state/cloud_verify"
REPOS_DIR="${CLOUD_REPOS_DIR:-$HOME/github_repos}"
mkdir -p "$PEND"
key() { echo "$1__${2//\//__}"; }
default_branch() { git -C "$1" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true; }

case "${1:-list}" in
  list)
    python3 - "$PEND" <<'PY'
import json, sys, glob
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    if d.get("status") != "pending": continue
    flag = "" if d.get("has_rules_pack", True) else "（⚠️ 這個倉庫還沒有雲端規則包：先跑 python3 scripts/cloud/sync_rules_to_repos.py add " + d["repo"] + "）"
    print(f'{d["repo"]} 的 {d["branch"]}：{d.get("last_message") or "（無說明）"}（{d.get("head","")[:7]}，{d.get("pushed_at","")}）{flag}')
PY
    ;;
  prep)
    repo="$2"; br="$3"; [ -n "$repo" ] && [ -n "$br" ] || { echo "用法：prep <倉庫> <分支>"; exit 2; }
    live="$REPOS_DIR/$repo"; [ -d "$live/.git" ] || { echo "找不到本機複製 $live"; exit 1; }
    git -C "$live" fetch -q origin || { echo "fetch 失敗"; exit 1; }
    db=$(default_branch "$live"); db=${db:-main}
    wt="$VERIFY/$(key "$repo" "$br")"
    if [ ! -d "$wt" ]; then mkdir -p "$VERIFY"; git -C "$live" worktree add -q --detach "$wt" "origin/$br" || exit 1
    else git -C "$wt" checkout -q --detach "origin/$br"; fi
    echo "📂 驗證用資料夾（獨立於正在上線的 $live）：$wt"
    echo "── 與 $db 的差異 ──"; git -C "$wt" diff --stat "origin/$db"...HEAD | tail -25
    echo "── 雲端寫的信 ──"
    git -C "$wt" ls-tree -r --name-only HEAD -- docs/to_junshi/ | while read -r f; do echo "▶ $f"; git -C "$wt" show "HEAD:$f"; done
    echo "── 下一步 ──"
    echo "1) 讀信裡的驗證步驟，在 $wt 用『正式程式』（真資料庫的備份複本／真清理程式）再測；雲端用假資料測的部分要補測"
    echo "2) 測過 → cloud_branch_pickup.sh merge $repo $br --verified ；有問題 → 直接在 $wt 修好再 merge"
    ;;
  merge)
    repo="$2"; br="$3"; [ "$4" = "--verified" ] || { echo "要加 --verified（代表已用正式程式測過）"; exit 2; }
    live="$REPOS_DIR/$repo"; git -C "$live" fetch -q origin || exit 1
    db=$(default_branch "$live"); db=${db:-main}
    wt="$VERIFY/$(key "$repo" "$br")-merge"
    [ -d "$wt" ] && { echo "$wt 已存在，上次合併沒做完？請先看一下"; exit 1; }
    git -C "$live" worktree add -q --detach "$wt" "origin/$db" || exit 1
    if ! git -C "$wt" -c user.name=CoachWU -c user.email=bymyway7@gmail.com merge --no-ff -q -m "[Mac] 合併雲端分支 $br（已驗證）" "origin/$br"; then
      echo "❌ 合併有衝突，已停下：$wt （解完衝突再 commit，然後 git push origin HEAD:$db）"; exit 1; fi
    git -C "$wt" push -q origin "HEAD:$db" || { echo "❌ 推送失敗"; exit 1; }
    sha=$(git -C "$wt" rev-parse --short HEAD)
    git -C "$live" worktree remove --force "$wt" 2>/dev/null
    # 本機上線資料夾跟上（有未存檔修改就不動，只提醒）
    if [ -z "$(git -C "$live" status --porcelain)" ] && [ "$(git -C "$live" symbolic-ref --short HEAD)" = "$db" ]; then
      git -C "$live" pull -q --ff-only origin "$db" && echo "✅ 本機上線資料夾已更新到 $sha"
    else echo "⚠️ $live 有未存檔修改或不在 $db 分支，沒自動更新；請手動處理"; fi
    bash "$0" done "$repo" "$br" "已合併 $sha"
    echo "✅ 已合併上線：$repo $db $sha"
    ;;
  done)
    repo="$2"; br="$3"; why="${4:-結案}"; f="$PEND/$(key "$repo" "$br").json"
    [ -f "$f" ] || { echo "沒有這筆待接手紀錄：$f"; exit 1; }
    python3 - "$f" "$why" <<'PY'
import json, sys
f, why = sys.argv[1], sys.argv[2]
d = json.load(open(f, encoding="utf-8")); d["status"] = "done"; d["done_note"] = why
from datetime import datetime; d["done_at"] = datetime.now().isoformat(timespec="seconds")
json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
    wt="$VERIFY/$(key "$repo" "$br")"; [ -d "$wt" ] && git -C "$REPOS_DIR/$repo" worktree remove --force "$wt" 2>/dev/null
    echo "已結案：$repo $br（$why）"
    ;;
  *) echo "用法：$0 list|prep|merge|done"; exit 2 ;;
esac
