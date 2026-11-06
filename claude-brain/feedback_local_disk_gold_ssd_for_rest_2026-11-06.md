---
name: local-disk-gold-ssd-for-rest
description: 教練 11/06 定：本機只放小龍蝦/Claude/系統非用不可的，其他（Chrome、修改歷史備份等）一律放外接 SSD＋Amber 備份；SSD 鎖螺絲不准建議拔插；問「還用不用」前先查最後使用時間；HTML 不准邊寫邊跳
metadata:
  node_type: memory
  type: feedback
  originSessionId: e846084c-8978-432e-98c9-0cc708051587
  modified: 2026-11-06T04:45:23.774Z
---

2026-11-06 教練看完「SSD 斷線與本機空間檢討」後糾正四件事：

1. **HTML 邊寫邊跳**：一份報告跳 5～6 次 Chrome，教練要逐一關掉。根因＝PostToolUse hook `auto_chrome_after_html_edit.sh` 每次 Edit/Write .html 都 `open -a Chrome`。只准寫完後用 `deliver_open.sh` 跳一次。
2. **SSD 不拔插**：953-SSD 裝在要鎖螺絲的外接盒裡，連續 8～10 個月沒出事，11/06 是第一次。不准再建議拔下來改插、不准因一次斷線就主張把東西搬回本機。
3. **本機＝黃金地段**：只放小龍蝦、Claude、系統非用不可的；其他能搬就搬 SSD，Amber 私有雲（512G，SMB `amber-Coach`，掛在 `/Volumes/home`，帳密在鑰匙圈）做備份。修改歷史(.git 25G)教練不要壓縮，要「Amber 一份＋SSD 一份，本機清掉」。
4. **不准問「教練還用不用」**：自己查最後使用時間（檔案修改時間、App 紀錄）再下結論。例：Claude-3p 只在 10/27 下午用過，11G 虛擬機。

**Why:** 教練說「不要再給我一些愚蠢的建議」；拿罕見事件推翻他長期驗證過的配置，等於不信任他的判斷，還把工作丟回給他。
**How to apply:** 空間規劃先套「非本機不可？」一題；要教練動手的建議先查他說過的硬體限制；能查的事實（最後使用時間）自己查完才開口。相關：[[mac-disk-full-chrome-code-sign-clone]]
