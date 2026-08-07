---
name: desktop-gui-selfcheck-method
description: 開工時自我判定「桌面版GUI」vs「終端機CLI」的可靠檢測法，不能只憑感覺預設
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25e0b432-4aad-4393-8880-950d3cea007c
  modified: 2026-08-07T22:12:07.091Z
---

# 桌面版/終端機自我判定法（2026-08-08 教練當場糾正後補建）

開工時把自己預設回報成「Mac終端機（CLI）」，教練當場糾正「你不是CLI，你是桌面版APP」。查證後找到可靠判定法：

```bash
ps -o comm= -p $PPID 2>/dev/null
echo "TERM_PROGRAM=$TERM_PROGRAM"
```

- 父行程路徑含 `/Applications/Claude.app` 或 `Claude.app/Contents/MacOS/claude` → **桌面版 GUI**
- `TERM_PROGRAM` 有值（如 `iTerm.app`、`Apple_Terminal`）→ **終端機 CLI**
- `TERM_PROGRAM` 空白 + 父行程是 claude.app → GUI 版（GUI 不透過 shell TTY 啟動，所以沒有 TERM_PROGRAM）

## Why
E04「行動前三問」第二問「我在哪（介面）」不能靠猜或靠上一場的印象，兩個介面能力相同（見 [[feedback_desktop_equals_gui_terminal_equals_cli]]）但稱呼/回報必須準確，教練已為此糾正過不只一次。

## How to apply
每場開工做身份核對（六步驟第六步）前，先跑上面兩行指令再回報介面別，不要預設寫「終端機」或「桌面版」。
