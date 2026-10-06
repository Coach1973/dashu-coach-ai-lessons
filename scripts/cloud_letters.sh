#!/bin/bash
# 雲端對話寫給軍師的信：掃指定專案所有遠端分支的 docs/to_junshi/*.md，沒讀過的才列出
# 用法：cloud_letters.sh list（只列，開工 hook 用）｜cat（印全文）｜mark（現有的全部標成已讀）
REPOS="${CLOUD_LETTERS_REPOS:-$HOME/github_repos/bni-chapters}"
STATE="${CLOUD_LETTERS_STATE:-$HOME/.openclaw/workspace/state/cloud_letters_read.txt}"
DIR="docs/to_junshi"
touch "$STATE"

scan() {
  for repo in $REPOS; do
    [ -d "$repo/.git" ] || continue
    # Mac 沒有 timeout 指令（10/06 查證：原本寫 timeout 20 git fetch，指令不存在被 2>/dev/null 吞掉，從來沒真的 fetch 過）
    if [ "${CLOUD_LETTERS_NOFETCH:-0}" != 1 ]; then
      if command -v timeout >/dev/null 2>&1; then timeout 20 git -C "$repo" fetch -q origin 2>/dev/null
      else git -C "$repo" -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=15 fetch -q origin 2>/dev/null; fi
    fi
    name=$(basename "$repo")
    git -C "$repo" for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v '^origin/HEAD$' | while read -r ref; do
      git -C "$repo" ls-tree -r "$ref" -- "$DIR/" 2>/dev/null | while IFS=$'\t' read -r meta path; do
        sha=$(echo "$meta" | awk '{print $3}')
        case "$path" in *.md) echo "$name|$sha|$ref|$path|$repo";; esac
      done
    done
  done | awk -F'|' '!seen[$1"|"$2]++'
}

unread() { scan | while IFS='|' read -r name sha ref path repo; do grep -qxF "$name|$sha" "$STATE" || echo "$name|$sha|$ref|$path|$repo"; done; }

case "${1:-list}" in
  list) unread | while IFS='|' read -r name sha ref path repo; do echo "$name 的 $ref 分支：$path"; done ;;
  cat)  unread | while IFS='|' read -r name sha ref path repo; do
          echo "════ $name / $ref / $path ════"; git -C "$repo" show "$ref:$path"; echo; done ;;
  mark) unread | while IFS='|' read -r name sha ref path repo; do echo "$name|$sha" >> "$STATE"; done; echo "已標為已讀" ;;
  *) echo "用法：$0 list|cat|mark"; exit 2 ;;
esac
