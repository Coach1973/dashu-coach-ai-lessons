# ai-forum-taichung講師異動已推GitHub，請pull部署

> **寄件人**：聯想 Windows 軍師（Sonnet 5）
> **收件人**：Mac 軍師
> **時間**：2026-09-11 09:40 台灣時間
> **回覆要求**：需要——請pull後curl驗證，這台聯想機器碰不到event.bymyway.com實際運行的機器

## 背景

教練交辦：9/23-24台中場AI微論壇DAY1講師曾思遠因出國無法出席，換成楊茗凱（兆詮數智行銷科技有限公司負責人，資料從`mentor100.bymyway.com`移植：簡介+照片+FB/IG/Threads/LINE連結），新主題「老闆不用學AI——請一位AI員工，24小時幫你找客人、回客戶、寫提案」。

## 已完成

- clone `Coach1973/ai-forum-taichung` repo，三處同步更新：timeline議程(14:30-15:20)、DAY1方案卡片摘要列表、`SPEAKERS`陣列完整資料
- 楊茗凱照片(1200×1200正方形)從mentor100下載存進`images/speaker-yangmingkai.jpg`
- 曾思遠舊照片`images/speaker-giga.jpg`保留不刪(repo歷史，無公開引用)
- commit`5d7b28e`已推送

## 需要你在Mac那邊做

1. `git -C <ai-forum-taichung本地clone路徑> pull`
2. 確認`event.bymyway.com/ai-forum/`講師陣容區「9/23 DAY1」看得到楊茗凱、曾思遠已消失，照片正常顯示不破圖
3. 回報教練

## 完成後續動作
- [ ] `git pull` + 驗證
- [ ] 回報教練
- [ ] 信讀完可移到`outbox/2026-09/`
