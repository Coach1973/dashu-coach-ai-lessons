---
name: feedback-shortcut-fix
description: 修捷徑失敗五次的教訓——先查正常的那個，不要自己瞎猜
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9c64b31c-9b4d-4490-b41d-77b5d1e7bcf2
---

修 LINE 桌面捷徑時，教練說「工作列那個是正常的」，我卻沒有去查工作列捷徑的實際路徑，反而自己用 WScript.Shell 反覆建捷徑，每次都被 Windows 解析成 E 碟路徑，同一個錯犯了五次。

**Why:** 教練明確給了正確的參照物，我卻忽略了，自己繞了 VBS、AppX、icon 複製等複雜做法，把 4 步能完成的事搞砸了 5 次。
**How to apply:**
1. 教練說「這個是正常的」→ 第一件事就是去查那個正常的東西，複製它的設定
2. 同一個方法失敗兩次就必須換做法，不要第三次（守則 #07）
3. 簡單方案優先，不要過度工程化（守則 #16）
