---
name: mac-disk-full-chrome-code-sign-clone
description: Mac 本機 256G 喊空間不足時先查 Chrome code_sign_clone（11/06 堆 24 份 34G）、開工 worktree（87 份 31G）、舊 .bak 備份
metadata:
  node_type: memory
  type: reference
  originSessionId: be77858d-05df-4933-bbd0-c7d9901f8645
  modified: 2026-11-06T04:10:53.522Z
---

2026-11-06 教練存照片說「空間不足」，本機 Data 卷 191G/228G、只剩 17G。

**最大元兇**：`/private/var/folders/_s/6lw5k_0s6qb2180wk8470fmc0000gn/X/com.google.Chrome.code_sign_clone/`，Chrome 每次啟動複製自己一份（每份 1.4G），正常結束才會刪；當機或被自動化程式強制關掉就留下來。11/06 累積 24 份、34G（早上 Chrome 崩潰十幾次＋FB/生日腳本常開關 Chrome）。
- 怎麼判斷能清：`pgrep -x "Google Chrome"`，看執行中的 Chrome 是從 /Applications 跑的；保留最新一份，其餘可清。
- 做法：搬進 `~/.Trash/空間清理_YYYYMMDD/`（可救回），清空垃圾桶這一下留給教練按（不能代按永久刪除）。

**其他大戶**：
- 「開工」worktree：每份 360～860MB，87 份 31G。`get_storage_usage` 看得到；`clean_up_worktrees` 只清 30 天以上沒動的，提早清要逐一 archive_session（每次跳確認），不划算。
- 舊備份 `~/Library/Application Support/Claude/vm_bundles.bak.20261003`（10G）、`Google/Chrome.bak.20261002`（5.2G）：新的在外接 SSD，11/06 已搬垃圾桶。
- `~/.openclaw/.git` 25G 沒動。

**另一個坑**：`~/Downloads` 與 `Claude/vm_bundles` 都是指向外接 SSD（953-SSD）的捷徑，SSD 沒接上時，存檔到下載資料夾會失敗。相關：[[fb-birthday-chrome-dangling-ssd-symlink]]

報告頁：https://claude.ai/artifact/FoSTLaBbZYWEH6BC5KXBBB
