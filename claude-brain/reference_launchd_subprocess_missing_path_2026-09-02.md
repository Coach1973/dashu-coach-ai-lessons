---
name: reference-launchd-subprocess-missing-path
description: launchd背景服務(Flask app等)用subprocess呼叫openclaw/node/homebrew工具會找不到指令，因為launchd預設PATH只有/usr/bin:/bin:/usr/sbin:/sbin
metadata:
  node_type: memory
  type: reference
  originSessionId: 8413cc54-aeab-49dc-81d8-2b7c18c27451
  modified: 2026-09-02T09:26:44.096Z
---

任何用launchd管理的長駐服務（`com.coach.*.plist`跑的Flask app等），內部用Python `subprocess.run(["openclaw", ...])`或呼叫任何homebrew/node安裝的CLI工具，會拋`FileNotFoundError`（先是`No such file or directory: 'openclaw'`，補上絕對路徑後變成`env: node: No such file or directory`，因為openclaw本身是`#!/usr/bin/env node`的node script）。

**Why**：`launchctl print gui/<uid>/<label>`可查到launchd服務的`default environment`只有`PATH => /usr/bin:/bin:/usr/sbin:/sbin`，不含`/opt/homebrew/bin`（openclaw符號連結所在）也不含`~/.local/bin`（node實際安裝位置）。這跟終端機互動session的PATH完全不同，subprocess.run用list形式呼叫（非shell=True）也不會去讀`.zshrc`之類的shell設定檔。

**How to apply**：任何launchd服務要用subprocess呼叫外部CLI工具時：
1. 優先用絕對路徑呼叫執行檔本身（如`/opt/homebrew/bin/openclaw`），不要依賴PATH解析。
2. 若該執行檔本身是script（如openclaw是node script），絕對路徑也不夠，還要幫`subprocess.run`額外傳入`env`參數，把homebrew跟node的bin目錄補進PATH：
   ```python
   _ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/Users/bymyway/.local/bin:{os.environ.get('PATH', '')}"}
   subprocess.run([...], env=_ENV)
   ```
3. 除錯時先用`launchctl print gui/$(id -u)/<label> | grep -A3 environment`確認該服務實際能看到的PATH，不要假設跟終端機一樣。

實戰案例：`event-signup/app.py`的待辦提醒系統(`todo_reminder_check.py`)需要在Flask路由裡呼叫`openclaw cron create`排程一次性提醒，一開始只用裸指令名稱`"openclaw"`失敗，補絕對路徑後又因node找不到而失敗，最後補上`env`參數才成功。

Related: [[project_namecard_login_gate_and_guest_history_2026-09-02]]（同一天處理的另一個namecard-db架構變更，性質不同但同一場session）
