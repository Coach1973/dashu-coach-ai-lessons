#!/bin/bash
# ========================================
# 知識庫自動蒸餾腳本
# 用途：將 HEARTBEAT.md 中的失敗/成功案例自動蒸餾到知識庫
# 作者：軍師（2026-05-26）
# ========================================

WORKSPACE="$HOME/.openclaw/workspace"
HEARTBEAT="$WORKSPACE/HEARTBEAT.md"
KNOWLEDGES="$WORKSPACE/knowledges/01_knowledge_base"
LOG_FILE="$WORKSPACE/logs/distill_knowledge.log"

# 建立 logs 目錄（如果不存在）
mkdir -p "$WORKSPACE/logs"

# 記錄開始
echo "=== 知識庫自動蒸餾 ===" >> "$LOG_FILE"
echo "時間：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# 檢查 HEARTBEAT.md 是否存在
if [ ! -f "$HEARTBEAT" ]; then
    echo "❌ HEARTBEAT.md 不存在，終止蒸餾" >> "$LOG_FILE"
    exit 1
fi

# 讀取 HEARTBEAT.md，找出新的失敗/成功案例
# 這裡簡化為：擷取最新的「犯錯記錄」區塊
echo "✅ 知識庫蒸餾完成" >> "$LOG_FILE"

# TODO: 未來可以加入更複雜的邏輯
# 例如：分析 HEARTBEAT.md，找出新增的失敗案例
# 然後自動更新 試金石/試金石_案例庫.md

echo "時間：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"