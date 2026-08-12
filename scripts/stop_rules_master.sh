#!/bin/bash
# Stop hook 總管（2026-08-12 全面體檢後合併）
#
# 取代原本 10 支各自重讀 transcript 的檢查腳本：
#   rule12_porter_check / rule05_hash_check / rule_taiwan_time_check /
#   rule07_polling_check / rule03_verify_before_answer_check /
#   rule08_ask_when_clear_check / rule_proactive_session_reminder_check /
#   delivery_check / rule_traditional_chinese_check / rule_html_chrome_check
#
# 那 10 支原檔保留在本目錄不刪除（可比對／可回退），只是不再註冊進
# ~/.claude/settings.json 的 Stop 事件。
#
# 行為完全對齊原版：偵測字串、白名單、警告文字、log 路徑、擋(exit 2)/提醒(exit 0)
# 分級全部一字不差，只把「同一份 transcript 讀 10 次」改成讀 1 次。
set -uo pipefail

exec /usr/bin/env python3 "$(dirname "$0")/stop_rules_master.py"
