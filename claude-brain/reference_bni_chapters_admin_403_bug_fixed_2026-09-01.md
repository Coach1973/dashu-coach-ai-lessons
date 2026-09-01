---
name: reference_bni_chapters_admin_403_bug_fixed_2026-09-01
description: bni-chapters系統分會帳號(非super)誤訪問通用/admin會被403擋下的真bug，已修復改導向自己分會編輯頁，commit 40448f4
metadata: 
  node_type: memory
  type: reference
  originSessionId: 529f493d-3a80-43be-815c-8e4a5987a014
  modified: 2026-09-01T09:45:51.359Z
---

教練回報`chapters.bymyway.com/admin`「當掉」，查`webapp.error.log`確認process從未crash(無traceback，一直是running狀態)，真正原因是`login_required`裝飾器的邏輯：分會帳號(`admin_scope`是chapter_id數字非"super")造訪通用`/admin`(admin_list，無`chapter_id` kwarg)時，`target_id`永遠是`None`，判斷式必定`abort(403)`。任何拿到分會帳號的人（10組分會帳號之一）只要不小心點到`/admin`而非自己專屬的`/admin/<slug>/login`，就會被403卡死，看起來像系統壞掉。

已修復`app.py`的`login_required`：`target_id is None`時改成`redirect(url_for("admin_edit", chapter_id=admin_scope))`導向自己分會的編輯頁，而非直接abort。用真實Flask test_client模擬三種情境驗證：super帳號訪問`/admin`(200正常)、分會1帳號誤訪問`/admin`(302導向自己編輯頁)、分會2帳號越權訪問分會1編辑頁(403維持不變，安全性不受影響)。commit `40448f4`(bni-chapters repo)。

Related: [[reference_bni_connect_cms_structure]]（同系列BNI後台維運參考）
