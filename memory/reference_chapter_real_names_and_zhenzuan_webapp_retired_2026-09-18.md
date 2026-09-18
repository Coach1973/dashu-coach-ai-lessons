---
name: reference-chapter-real-names-and-zhenzuan-webapp-retired-2026-09-18
description: BNI 三分會網域對應真名 + zhenzuan-webapp 是退役服務（不是真鑽線上 webapp）+ 真鑫 active 名單扣掉離會 2 人
metadata:
  type: reference
---

# BNI 三分會網域 / 真鑽 webapp 退役 / 真鑫 active 名單

2026-09-18 更新戰情儀表板時，教練當場糾正 2 個錯誤認知，記下避免再犯。

## 1. 網域 ↔ 分會 真名對照

| 網域 | 真實分會 | DB 路徑 | launchd 服務 |
|---|---|---|---|
| `zhenxin.bymyway.com` | 真鑫 | `~/github_repos/zhenxin-guests/zhenxin_guests.db` | `com.coach.zhenxin-webapp` |
| `real-diamonds.bymyway.com` | 真鑽 | `~/github_repos/zhenzuan-guests/zhenzuan_guests.db` | （**無對應 launchd 服務**） |
| `real-wealth.bymyway.com` | 真貴 | `~/github_repos/zhengui-guests/zhengui_guests.db` | `com.coach.zhengui-webapp` |

**為什麼教練會不爽**：我之前誤把 `com.coach.zhenzuan-webapp` 當成真鑽的線上 webapp，發現它 exit -15 就想重啟。教練說「這個本來就是停用的東西，不要浪費那麼多時間」+ 之後補一句根因「分會的名稱不是我要的我就叫他停了，真鑽有專門的名字」。
**為什麼退役**：分會 repo 用「zhenzuan」(中文拼音) 不是教練要的名字，所以教練叫停了。真鑽的專門名字 = `real-diamonds`，線上走 `real-diamonds.bymyway.com`，本機 Flask 部署方式待查（不是 `com.coach.zhenzuan-webapp`）。
**怎麼應用**：看到 `zhenzuan-webapp` 不在 launchd 服務名單、或 EXITED 都正常，不要動它、不要花時間查它為什麼死。

## 2. 真鑫 members 表 ≠ 應到會員數

- 真鑫 `members` 表有 24 人（id 61-84）
- 教練 09/17 週報的應到是 **22 人**
- 差 2 位已離會：**張晴晴** + **楊為凱**
- 怎麼應用：寫 weekly_data 用 22 人為基準，這 2 位不要再 INSERT row（除非教練重新啟動會籍）

## 3. 戰情儀表板用 `INSERT ... ON CONFLICT(member_id, week_date) DO UPDATE SET <col>=excluded.<col>` 模式

- `weeks` 表欄位：`(week_date PK, label, is_active, note, sort_order)` —— 5 欄不是 3 欄
- `weekly_data` 表欄位：`(member_id, week_date, guests, ones, coffee, early_bird)` —— ones/coffee/early_bird 都允許 NULL（INTEGER，沒 NOT NULL）
- 寫入原則：ones/coffee 沒給就保持 NULL，**不要填 0 假裝沒事**（守則 #15 誠實）
