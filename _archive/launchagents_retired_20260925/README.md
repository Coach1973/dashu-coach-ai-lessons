# 2026-09-25 封存的背景項目（教練：「有用就留著，沒有用的就不要留」）

實體檔案移到 `~/Library/LaunchAgents_archive_2026-09-25/`（內含 API 金鑰，**不放進 git**）。要復原：搬回 `~/Library/LaunchAgents/` 再 `launchctl bootstrap gui/$(id -u) <檔案>`。

| 項目 | 為什麼沒用 | 查證 |
|---|---|---|
| `ai.openclaw.kong.plist`（node，port 18790） | 2026-04 孔大哥獨立 gateway 舊架構 | 未載入、無行程、18790 無人監聽、無腳本引用；孔大哥現由主 gateway `openclaw.json` bindings[2,4] 服務 |
| `ai.openclaw.peipei.plist`（node，port 18793） | 2026-04 佩佩老師獨立 gateway 舊架構 | 同上；現由 bindings[3,5] 服務 |
| `ai.openclaw.gateway.plist.bak-155801` | 2026-05-22 的 gateway 設定舊備份 | launchd 不讀 .bak，純殘留 |

搬移後驗證：`ai.openclaw.gateway` 仍在跑（pid 10710），本機 18789 回 200。
其餘 52 項背景項目都有在用（網站＋上網管線 24、小龍蝦排程與監看 13、赫米斯 5、Google/Zoom/RustDesk/macFUSE/Cloudflare 系統元件），全部保留。
