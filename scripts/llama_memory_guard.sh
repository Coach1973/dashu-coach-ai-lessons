#!/bin/bash
# llama_memory_guard.sh — 小龍蝦「記憶搜尋」引擎（llama-server 嵌入程序）記憶體守衛
#
# 起因（2026-10-29 教練：「像 RustDesk 那樣，到一定的量自動釋放，回到正常值」）：
#   活動監視器看到 llama-server 2.11G。10/12 用包裝腳本 llama-server-lite.sh 把 ubatch 壓到 1024
#   （約 0.66GB），但 10/25 19:46:07 外掛載入嵌入模型時把設定檔寫回 2048、同一秒啟動嵌入程序，
#   壓小就失效了。根因在外掛原始碼寫死 LLAMA_CPP_EMBEDDING_UBATCH_SIZE = 2048，每次載入都會覆蓋。
#
# 這支做三件事（都是「壞了才動手」，正常就安靜結束）：
#   1) 外掛原始碼若是 2048（外掛更新會洗掉我們的修改）→ 改回 1024，並重啟小龍蝦閘道讓它生效
#   2) 設定檔 ubatch 若是 2048 → 改回 1024
#   3) 嵌入程序真實記憶體（跟活動監視器同一個數字）超過門檻，或用的還是 2048 → 連同它的上層
#      router 一起結束（只殺嵌入程序，router 會一直回「載入失敗」，10/29 實測），
#      下一次記憶搜尋時外掛會自動重新啟動一套乾淨的
#   有動手就通知教練（同一件事 1 小時內只通知一次）。
#
# 觸發：ai.openclaw.llama-memory-guard
#   - 事件：外掛資料夾或設定檔一有變動就跑（launchd WatchPaths，不輪詢）
#   - 登入時跑一次＋每天 05:10 再量一次記憶體（跟 RustDesk 守衛同一套保底）

set -uo pipefail
THRESHOLD_MB=${LLAMA_GUARD_THRESHOLD_MB:-1200}   # 正常約 0.1～0.66GB；超過 1.2GB 才算異常（環境變數只給測試用）
UBATCH=1024
PLUGIN_GLOB="/Users/bymyway/.openclaw/npm/projects/openclaw-llama-cpp-provider-*/node_modules/@openclaw/llama-cpp-provider/dist/index.js"
INI_GLOB="/Users/bymyway/.openclaw/tools/llama.cpp/models-*.ini"
LOG="/Users/bymyway/.openclaw/workspace/logs/llama_memory_guard.log"
NOTIFY="/Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
ts() { TZ=Asia/Taipei date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

# 同一時間只跑一份（自己改設定檔也會觸發 WatchPaths）
LOCKDIR=/tmp/.llama_memory_guard.lock
mkdir "$LOCKDIR" 2>/dev/null || exit 0
trap 'rmdir "$LOCKDIR" 2>/dev/null' EXIT
sleep "${GUARD_WAIT_SEC:-5}"   # 讓外掛把檔案寫完

ACTIONS=()
RESTART_GATEWAY=0

# 1) 外掛原始碼
for f in $PLUGIN_GLOB; do
  [ -f "$f" ] || continue
  if grep -q "LLAMA_CPP_EMBEDDING_UBATCH_SIZE = 2048;" "$f"; then
    cp -p "$f" "$f.bak-ubatch2048-$(date +%Y%m%d%H%M%S)"
    sed -i '' "s/LLAMA_CPP_EMBEDDING_UBATCH_SIZE = 2048;/LLAMA_CPP_EMBEDDING_UBATCH_SIZE = ${UBATCH};/" "$f"
    if grep -q "LLAMA_CPP_EMBEDDING_UBATCH_SIZE = ${UBATCH};" "$f"; then
      ACTIONS+=("外掛被更新洗回 2048，已改回 ${UBATCH}"); RESTART_GATEWAY=1
    else
      log "❌ 外掛改不回去：$f"
    fi
  fi
done

# 2) 設定檔
for ini in $INI_GLOB; do
  [ -f "$ini" ] || continue
  if grep -Eq '^ubatch-size[[:space:]]*=[[:space:]]*2048[[:space:]]*$' "$ini"; then
    sed -i '' -E "s/^(ubatch-size[[:space:]]*=[[:space:]]*)2048[[:space:]]*$/\1${UBATCH}/" "$ini"
    ACTIONS+=("設定檔 $(basename "$ini") 改回 ${UBATCH}")
  fi
done

if [ "$RESTART_GATEWAY" = 1 ]; then
  # 用 launchd 重啟：/opt/homebrew/bin/openclaw 是舊版、不認得新設定，小龍蝦實際跑的是 nvm 那份
  if launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway" >> "$LOG" 2>&1; then ACTIONS+=("已重啟小龍蝦閘道讓修改生效"); else log "❌ 閘道重啟失敗"; fi
fi

# 3) 嵌入程序記憶體
PID=$(pgrep -f "llama-server --embeddings" | head -1)
if [ -n "$PID" ]; then
  MEM_MB=$(footprint "$PID" 2>/dev/null | sed -nE 's/.*Footprint: ([0-9]+) MB.*/\1/p' | head -1)
  CUR_UB=$(ps -o command= -p "$PID" | sed -nE 's/.*--ubatch-size ([0-9]+).*/\1/p')
  if [ -z "$MEM_MB" ]; then
    log "讀不到記憶體(PID=$PID)，略過"
  elif [ "$MEM_MB" -gt "$THRESHOLD_MB" ] || [ "${CUR_UB:-$UBATCH}" != "$UBATCH" ]; then
    PARENT=$(ps -o ppid= -p "$PID" | tr -d ' ')
    PIDS="$PID"
    ps -o command= -p "${PARENT:-0}" 2>/dev/null | grep -q "llama-server" && PIDS="$PID $PARENT"
    kill -TERM $PIDS 2>/dev/null
    for _ in 1 2 3 4 5 6 7 8 9 10; do kill -0 $PIDS 2>/dev/null || break; sleep 1; done
    for p in $PIDS; do kill -0 "$p" 2>/dev/null && kill -KILL "$p" 2>/dev/null; done
    sleep 1
    if kill -0 "$PID" 2>/dev/null; then
      log "❌ 釋放失敗：PID=$PID 還在（${MEM_MB}MB）"
    else
      ACTIONS+=("記憶搜尋引擎 ${MEM_MB}MB（ubatch ${CUR_UB:-?}）已釋放，下次用到會自動以 ${UBATCH} 重新啟動")
    fi
  else
    log "正常：${MEM_MB}MB、ubatch ${CUR_UB:-?}"
  fi
else
  log "嵌入程序沒在跑（閒置時外掛會自己關），略過記憶體檢查"
fi

if [ ${#ACTIONS[@]} -gt 0 ]; then
  MSG=$(printf '%s；' "${ACTIONS[@]}")
  log "動手：$MSG"
  bash "$NOTIFY" "🧠 小龍蝦記憶搜尋記憶體守衛：${MSG%；}" 3600 llama_memory_guard 2>/dev/null || true
fi
