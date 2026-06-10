#!/bin/bash
# ============================================================
# 推送鎖安裝器（2026-06-11 軍師建立，教練拍板）
#
# 起因：試金石案例 G + H——AI 未經教練確認就 git push，
#       jiesheng-leadership 是「push 即部署即扣點」站，共損失 30 點。
#       規則寫在 SOP 裡沒用，AI 會忘；這個鎖讓「想犯錯也犯不了」。
#
# 原理：在網站資料夾裝一道 pre-push 關卡。
#       AI 要 push 之前，必須先有「教練已說推」的通行證檔案。
#       沒有通行證 → push 直接被擋下，推不出去。
#       通行證用一次就銷毀（單次有效），且 30 分鐘過期。
#
# 用法：
#   安裝：  bash install-push-lock.sh /Users/bymyway/github_repos/某網站
#   發通行證（教練說「推」之後才能執行）：
#           touch /Users/bymyway/github_repos/某網站/.git/PUSH_APPROVED
#   然後：  git push   （這一次會放行，通行證自動銷毀）
# ============================================================

set -e

REPO="$1"
if [ -z "$REPO" ] || [ ! -d "$REPO/.git" ]; then
  echo "用法：bash install-push-lock.sh <git 資料夾路徑>" >&2
  exit 1
fi

HOOK="$REPO/.git/hooks/pre-push"

cat > "$HOOK" <<'PREPUSH'
#!/bin/bash
# 🔒 推送鎖（pre-push）——未經教練說「推」，不得 push
# 由 ~/.openclaw/workspace/scripts/install-push-lock.sh 安裝
# 起因：試金石案例 G(2026-06-09) + H(2026-06-11)，未確認就 push 扣 30 點

TOKEN="$(git rev-parse --git-dir)/PUSH_APPROVED"
MAX_AGE=1800  # 通行證有效期 30 分鐘

if [ ! -f "$TOKEN" ]; then
  echo "" >&2
  echo "🔒🔒🔒 推送鎖：這次 push 已被擋下 🔒🔒🔒" >&2
  echo "" >&2
  echo "這個網站「push 即上線」（Netlify 自動部署會扣點 / GitHub Pages 直接公開）。" >&2
  echo "規定：所有修改全部做完 → 預覽給教練看 → 教練親口說「推」→ 才能 push 一次。" >&2
  echo "" >&2
  echo "教練已經說「推」了嗎？" >&2
  echo "  是 → 執行：touch \$(git rev-parse --git-dir)/PUSH_APPROVED && git push" >&2
  echo "  否 → 先預覽給教練確認，不要繞過這道鎖。" >&2
  echo "" >&2
  exit 1
fi

# 檢查通行證是否過期（30 分鐘）
NOW=$(date +%s)
TOKEN_TIME=$(stat -f %m "$TOKEN" 2>/dev/null || stat -c %Y "$TOKEN")
AGE=$(( NOW - TOKEN_TIME ))
if [ "$AGE" -gt "$MAX_AGE" ]; then
  rm -f "$TOKEN"
  echo "🔒 推送鎖：通行證已過期（超過 30 分鐘），已銷毀。請重新取得教練同意。" >&2
  exit 1
fi

# 放行，通行證單次有效、用後即焚
rm -f "$TOKEN"
echo "🔓 推送鎖：通行證有效，放行這一次 push（通行證已銷毀，下次 push 需重新取得）。" >&2
exit 0
PREPUSH

chmod +x "$HOOK"
echo "✅ 推送鎖已安裝：$HOOK"
