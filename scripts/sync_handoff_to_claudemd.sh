#!/bin/bash
# 用途：把 JUNSHI_HANDOFF_LATEST.md 自動鏡像到 CLAUDE.md 的標記區段，
#       讓桌面版 Claude.app 啟動讀 CLAUDE.md 時直接看到最新接力棒，不靠模型自律去翻檔案。
# 觸發：手動跑 / cron 每 5 分鐘 / 軍師結束 session 改完接力棒後跑一次
# 設計：HANDOFF mtime > 上次同步時間才動工，沒變化就不動 CLAUDE.md（避免 git noise）

set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
CLAUDE_MD="$WS/CLAUDE.md"
HANDOFF="$WS/JUNSHI_HANDOFF_LATEST.md"
MARKER_DIR="$WS/.sync_markers"
SYNC_MARKER="$MARKER_DIR/handoff_last_sync"
# 不能寫進HEARTBEAT.md：那是小龍蝦每次開機必讀的檔，2026-09-25查到軍師日誌佔它78%、
# 撐破OpenClaw每檔2萬字上限（後段被截斷）。日誌改寫本機log，*.log已被gitignore不會跨機同步。
LOG="$WS/state/junshi_automation.log"

START_MARK="<!-- HANDOFF_AUTOINJECT_START -->"
END_MARK="<!-- HANDOFF_AUTOINJECT_END -->"

mkdir -p "$MARKER_DIR"

# 檔案檢查
[[ -f "$CLAUDE_MD" ]] || { echo "❌ CLAUDE.md 不存在"; exit 1; }
[[ -f "$HANDOFF"   ]] || { echo "❌ JUNSHI_HANDOFF_LATEST.md 不存在"; exit 1; }

HANDOFF_MTIME=$(stat -f %m "$HANDOFF")
LAST_SYNC=0
[[ -f "$SYNC_MARKER" ]] && LAST_SYNC=$(cat "$SYNC_MARKER")

# HANDOFF 沒變動就退出（避免每分鐘無謂改 CLAUDE.md）
if [[ "$HANDOFF_MTIME" -le "$LAST_SYNC" ]]; then
  exit 0
fi

# 用 python 處理多行替換（sed 多行麻煩）
/opt/homebrew/bin/python3 - "$CLAUDE_MD" "$HANDOFF" "$START_MARK" "$END_MARK" <<'PYEOF'
import re, sys, datetime
from pathlib import Path

claude_md_path, handoff_path, start_mark, end_mark = sys.argv[1:5]
claude_md = Path(claude_md_path)
handoff   = Path(handoff_path)

claude_content  = claude_md.read_text(encoding="utf-8")
handoff_content = handoff.read_text(encoding="utf-8")
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 2026-09-30 案例91：09-28小龍蝦直接整份覆蓋JUNSHI_HANDOFF_LATEST.md（沒有v-number開頭、
# 沒有「給跨對話框軍師讀的總結摘要」標題），這支腳本照樣忠實鏡像進CLAUDE.md並commit+push，
# 讓每一台開這個repo的機器連續近40小時讀到的都是壞掉的接力棒，直到09-30教練說「總結」
# 手動git pull撞見衝突才發現。以後鏡像前先驗證格式，不像才擋下、不寫CLAUDE.md、留log給人查。
# 2026-10-14：10/01 起接力棒標題改用時間、不再寫「新的一棒 vN」，原本兩個都要的條件把正常接力棒也擋掉，
# CLAUDE.md 鏡像停在 10/01 兩週沒人發現。改成只認「總結摘要」標題（案例91被覆蓋時這個標題本來就不在）。
# 2026-10-16 第二次誤擋正常棒：有 AI 在最上面加「本場追加」段，標題被擠出前 500 字，鏡像停 4 小時。
# 案例91是整份被蓋掉、全文都沒有這個標題，所以改成查全文，一樣抓得到案例91。
if "給跨對話框軍師讀的總結摘要" not in handoff_content:
    print(f"❌ 拒絕鏡像：{handoff_path} 開頭不像正常接力棒格式（沒有「給跨對話框軍師讀的總結摘要」或「新的一棒 vN」），"
          f"疑似被整份覆蓋，不寫入CLAUDE.md（案例91）。請人工檢查 {handoff_path} 是不是被誰直接蓋掉了。")
    sys.exit(1)

# 2026-11-04 教練同意（賈維斯體檢建議1）：開工 hook 已會送接力棒，這裡只留「最新一棒」＋🙋區，
# 不再貼整份（原本 9 千多字、跟開工注入重複讀兩遍；三關全文已在全域 CLAUDE.md 的 N2）。
def _latest_only(txt):
    key = "## 🔴 給跨對話框軍師讀的總結摘要"
    i = txt.find(key)
    if i == -1:
        return txt
    j = txt.find("\n## ", i + len(key))
    latest = txt[i:] if j == -1 else txt[i:j]
    ask = ""
    k = txt.find("### 🙋 要教練決定")
    if k != -1:
        m = txt.find("\n### ", k + 5)
        n = txt.find("\n## ", k + 5)
        ends = [x for x in (m, n) if x != -1]
        ask = txt[k:min(ends)] if ends else txt[k:]
    out = latest.rstrip() + "\n"
    if ask and ask not in latest:
        out += "\n" + ask.rstrip() + "\n"
    out += "\n> 前一棒、🤫／🔧 待辦、封存索引：需要才讀 `JUNSHI_HANDOFF_LATEST.md`。問教練之前的三關：見執行細則 N2。\n"
    return out
handoff_content = _latest_only(handoff_content)

new_section = f"""{start_mark}
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，只鏡像 `JUNSHI_HANDOFF_LATEST.md` 的最新一棒＋🙋區。
> **最後同步：{stamp}**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

{handoff_content}

---

> ⬆️ 接力棒鏡像結束。以下回到 CLAUDE.md 原本內容。
{end_mark}"""

if start_mark in claude_content and end_mark in claude_content:
    # 已有標記區段：用字串切片替換（避開 re.sub 對 \\C、\\U 等的 template 解析）
    # 2026-06-19 修：Python 3.14 即使傳 callable 也會觸發 _compile_template，導致 handoff 含
    # Windows 路徑（C:\\Users\\...）時拋 re.PatternError: bad escape \\C
    s_idx = claude_content.find(start_mark)
    e_idx = claude_content.find(end_mark, s_idx)
    if s_idx != -1 and e_idx != -1:
        new_content = (
            claude_content[:s_idx]
            + new_section
            + claude_content[e_idx + len(end_mark):]
        )
    else:
        new_content = claude_content  # 找不到標記，不動
else:
    # 首次安裝：在第一個「## 🎖️ Claude 軍師接位提示」之前插入
    anchor = "## 🎖️ Claude 軍師接位提示"
    if anchor in claude_content:
        new_content = claude_content.replace(
            anchor,
            new_section + "\n\n---\n\n" + anchor,
            1
        )
    else:
        # 退而求其次：放最上面（# 標題之後）
        lines = claude_content.split("\n", 1)
        new_content = lines[0] + "\n\n" + new_section + "\n\n" + (lines[1] if len(lines) > 1 else "")

if new_content != claude_content:
    claude_md.write_text(new_content, encoding="utf-8")
    print(f"✅ CLAUDE.md 已同步最新接力棒（{stamp}）")
else:
    print("ℹ️ 內容無變化，跳過寫入")
PYEOF

RC=$?

if [[ "$RC" -eq 0 ]]; then
  echo "$HANDOFF_MTIME" > "$SYNC_MARKER"
  # 寫進心跳檔留證
  {
    echo ""
    echo "## 🔄 接力棒→CLAUDE.md 自動同步 $(date '+%Y-%m-%d %H:%M')"
    echo "- ✅ 同步成功"
    echo "- HANDOFF mtime: $HANDOFF_MTIME"
  } >> "$LOG" 2>/dev/null || true

  # A 段：CLAUDE.md 有實際變動才 commit + push（避免 git noise）
  cd "$WS" 2>/dev/null || exit 0
  if ! git diff --quiet CLAUDE.md 2>/dev/null; then
    PUSH_RESULT="push 失敗（離線或網路問題，commit 已留本機）"
    if git add CLAUDE.md 2>/dev/null \
       && git commit -m "auto: 接力棒鏡像同步 $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1; then
      COMMIT_HASH=$(git rev-parse --short HEAD)
      # 2026-08-26 跟進聯想同款修復：commit 後直接 push，若同時間有其他機器
      # 也推過就會被拒（! [rejected] fetch first），東西永遠卡在本機。
      # 推送前先 pull --rebase 一次，失敗才是真的離線/衝突。
      git pull --rebase origin main >/dev/null 2>&1
      if git push origin main >/dev/null 2>&1; then
        PUSH_RESULT="✅ 已推上雲端（commit $COMMIT_HASH）"
      else
        PUSH_RESULT="⚠️ commit $COMMIT_HASH 已留本機，但 push 失敗"
      fi
    fi
    {
      echo "- 雲端同步：$PUSH_RESULT"
    } >> "$LOG" 2>/dev/null || true
  fi
fi

exit $RC
