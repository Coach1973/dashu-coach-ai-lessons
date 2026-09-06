# 專案卡：真鑫/真鑽/真貴分會「來賓戰情儀表板」（跟 bni-chapters 是兩套不同系統）

- **跟 bni-chapters 的關係**：分會官網(chapters.bymyway.com，會員自助登錄簡介頁)是另一套系統，這個是**每週來賓/1對1/咖啡會議次數追蹤儀表板**，兩者共用「分會」這個詞但完全獨立的repo/DB/網址，教練口語常混用「戰報系統」「戰情儀表板」兩種說法指同一件事
- **三個分會，同架構，各自獨立repo/DB/port**：

  | 分會 | repo（`~/github_repos/`下） | port | 正式網址 |
  |---|---|---|---|
  | 真鑫 | `zhenxin-guests` | 5092 | https://zhenxin.bymyway.com |
  | 真鑽 | `zhenzuan-guests` | 5093 | https://real-diamonds.bymyway.com |
  | 真貴 | `zhengui-guests` | 5094 | https://real-wealth.bymyway.com |

- **每週數據更新SOP（2026-09-07）**：完整curl/SQL指令見`claude-brain/reference_bni_guest_dashboard_weekly_update_sop_2026-09-07.md`。摘要：1對1／咖啡會議走公開`/api/update_metric`curl即可；來賓數沒有公開API(官方報表非會員自填)，改直接寫`weekly_data`表；新一週要先在`weeks`表建好`is_active=1`的記錄才能填。**軍師/Hermes/小龍蝦皆可直接執行，不用逐次確認**。
- **改完不用重啟服務**：Flask每次都即時查DB。
- **命名血淚**：正式網址早已從`zhenzuan`/`zhengui`改名成`real-diamonds`/`real-wealth`，但本機repo資料夾名稱還是舊的`zhenzuan-guests`/`zhengui-guests`沒跟著改，查證時兩套名字都要認得
- **`zhenxin-guests`曾經zero雲端備份**：2026-09-01發現這個repo建立以來從未設git remote，已修復補推GitHub，往後新建repo記得`git remote -v`確認有輸出
