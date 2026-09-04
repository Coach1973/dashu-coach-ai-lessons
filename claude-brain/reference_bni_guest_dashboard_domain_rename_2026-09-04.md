---
name: reference_bni_guest_dashboard_domain_rename_2026-09-04
description: 真鑽/真貴來賓戰情儀表板正確網址是real-diamonds/real-wealth，不是zhenzuan/zhengui舊命名
metadata: 
  node_type: memory
  type: reference
  originSessionId: 786ed7db-2ca8-4ff8-9a7e-eebbebaafb36
  modified: 2026-09-04T14:10:37.177Z
---

BNI大台南南區「來賓戰情儀表板」系列，真鑽分會＝`https://real-diamonds.bymyway.com/`（port 5093），真貴籌備會＝`https://real-wealth.bymyway.com/`（port 5094）。舊記錄裡用的`zhenzuan.bymyway.com`/`zhengui.bymyway.com`是命名錯誤的初版網址，已改成跟[[project_bni_chapters_public_launch_2026-08-03]]的英文slug命名規則對齊（sincere/real-ai/true-rich/true-love/zhenxin/real-diamonds/real-kungfu/real-age/real-wealth）。

**Why**：2026-09-04全面盤點報告用舊網址curl測出DNS不解析，誤判「還沒部署」，教練糾正才發現只是網址早已改名，服務其實正常運作（launchd`com.coach.zhenzuan-webapp`/`zhengui-webapp`+cloudflared config可查真實hostname）。

**How to apply**：往後查證這兩個分會網站狀態，一律用`real-diamonds`/`real-wealth`兩個網址，不要用`zhenzuan`/`zhengui`；查任何bymyway.com子網域是否存活，DNS不解析先懷疑是不是網址本身改名了，去查對應的launchd plist跟`~/.cloudflared/*.yml`確認真實hostname，不要直接下結論「未部署」。
