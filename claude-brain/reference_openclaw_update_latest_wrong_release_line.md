---
name: reference-openclaw-update-latest-wrong-release-line
description: openclaw update預設抓openclaw@latest可能橫向跳到不同release line(版號較大但發佈日期較早)，升級前要用--tag明確指定extended-stable版本號，不要盲目跑預設update
metadata:
  type: reference
  originSessionId: 84150fda-42bc-4356-acc0-ad3d3b4a8c7a
  modified: 2026-08-25T14:17:53.752Z
---

Mac評估2026.6.33→2026.6.34升級時已發現：`latest`(2026.7.1-2)是不同的release line，版號比較大但發佈日期反而更早，換過去等於橫向跳線，不是真正意義上的「更新」。2026-08-25在VPS(43.245.60.200)升級時再次驗證同款問題：VPS當時running 2026.6.11，`openclaw update --dry-run`預設目標是`openclaw@latest`=`2026.7.1-2`，若直接照跑會跳到錯誤的release line，而不是Mac已經評估過安全、屬於extended-stable線的`2026.6.34`。

**Why：** `openclaw update`指令族群有多條release line並行維護（stable一般更新線 vs extended-stable維護線等），預設的`--tag`（不指定時等同於`openclaw@latest`）不保證跟"目前正在用的這條線的下一版"是同一件事，可能會把你導去另一條完全不同的分支。

**How to apply：**
1. 升級前先跑`openclaw update --dry-run`，看Target version是什麼，跟你原本預期的版本號比對，若不是預期的下一個小版本號，先不要直接update。
2. 若已知安全的目標版本號（例如Mac評估過的2026.6.34），改用`openclaw update --tag <明確版本號> --dry-run`先預覽，確認Target version正確後再拿掉`--dry-run`真的執行，並加`--yes`跳過互動式確認（適合SSH腳本化操作）。
3. `openclaw update --help`裡`--tag <dist-tag|version|spec>`這個參數就是為了這個情境設計的：「One-off package update without persisting」，不會動到`--channel`設定，適合一次性精準升級。
4. 升級後容器內process不會自動重啟（若是`docker exec`跑的update，套件層級版本更新了但正在跑的process還是舊code），需要額外`docker restart <容器名>`才會真正生效，重啟後要再跑一次`--version`確認process版本也更新了，不能只看套件安裝訊息就當作完成。

Related: 見Mac接力棒2026.6.33→2026.6.34升級評估段落（`handoff_archive/`歷史記錄）
