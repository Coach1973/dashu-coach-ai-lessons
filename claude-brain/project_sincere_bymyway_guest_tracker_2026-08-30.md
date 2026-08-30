---
name: project-sincere-bymyway-guest-tracker-2026-08-30
description: 真誠分會邀約來賓/121/咖啡會議/全國見証分享會/培訓出席戰情儀表板，sincere.bymyway.com，會員自助輸入即時存檔
metadata: 
  node_type: memory
  type: project
  originSessionId: 0f9618ae-e25f-4bf7-a476-73d71acabdd7
  modified: 2026-08-30T03:57:29.683Z
---

**repo**：`Coach1973/zhencheng-guests`（私有，注意repo名稱仍是舊名，跟現在網址`sincere`不一致，純命名遺留不影響功能）｜本機路徑`/Users/bymyway/github_repos/zhencheng-guests`｜Flask+SQLite（`zhencheng_guests.db`，未版控）

**正式站**：https://sincere.bymyway.com （本機Flask port 5090，launchd `com.coach.sincere-webapp`+`com.coach.sincere-tunnel`）

**設計**：仿[[reference_bymyway_subdomain_530_missing_launchd_2026-08-29]]同款webapp+tunnel雙launchd看護模式，避免斷線後沒人發現。仿`bni-dna`（大台南南區DnA團隊戰情儀表板）的月報表視覺格式改成週版。

**資料範圍**：真誠分會13位在籍會員（王者飛翔/百聖維尼/羽宙奇蹟三組，各自指定助理大使），07/23起週四聚會、08/20內訓週不列入計算。8/27新會員張育慈加入王者飛翔組，邀約來賓起算週從9/3開始算（教練指定，跟入會日期不同）。

**三項核心指標**（來賓/121/咖啡會議）：來賓由教練口述提供、軍師更新；121與咖啡會議開放會員自行輸入、即時存檔。連續4週無紀錄🟡黃標，連續8週🔴紅標（建議寄警告信/評估離會）。

**另外兩區塊**：全國見証分享會出席（週一場8/3~8/31、週四場8/6~8/27，YES/NO）、培訓出席（8月三場+9月五場，✅/❌），皆開放會員自行點選即時存檔。三者的門檻/連續無紀錄邏輯完全獨立計算。

**🔴 待決事項**：bni-chapters裡有另一個對話框幾乎同時間獨立做的重複版本（`/admin/chapters/1/invites`，唯讀，功能較陽春），教練尚未裁示留哪一個，見[[feedback_check_git_log_for_parallel_builds_2026-08-30]]。

**技術地雷**：Jinja2樣板dict鍵名不能叫`values`，會跟Python內建方法撞名導致資料靜默消失，見[[reference_jinja2_dict_values_key_collision_2026-08-30]]。seed.py已改成安全UPSERT版，重跑不會洗掉會員自填資料。

Related: [[reference_bymyway_subdomain_530_missing_launchd_2026-08-29]]
