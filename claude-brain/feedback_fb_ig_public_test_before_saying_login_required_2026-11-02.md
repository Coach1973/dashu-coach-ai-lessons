---
name: fb-ig-public-test-before-saying-login-required
description: 教練糾正：FB/IG 多數是公開的，不登入就看得到；沒實測不准說「要登入才看得到」（指令夾曾這樣寫，已改 ed50378）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0d03d2b8-ff1b-4570-aaea-3b485547ab81
  modified: 2026-11-02T09:58:01.232Z
---

指令夾 tava-brand-web-playbook 曾寫「FB、IG 的照片大多要登入才看得到」，教練 2026-11-02 糾正：多數 FB/IG 是公開的，被回報「看不到」好幾次都是沒測就下結論。

**Why:** 查照片來源時少了最大宗的管道（本人 FB/IG），網頁就缺圖。
**How to apply:** 找人物照片先實際開 FB/IG 公開頁測；用 `facebookexternalhit` 身分抓 og:image 可證明公開頁不登入就拿得到（curl 一般瀏覽器身分 FB 回 400 是擋程式，不是要登入）；限制瀏覽的才請教練在已登入的 Chrome 開。不自己輸入教練的 FB 密碼。指令頁已改 `ed50378`。相關：[[feedback-always-name-the-group-bot-site-in-full-2026-10-18]]
