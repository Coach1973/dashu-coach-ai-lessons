---
name: project-line-moved-to-e
description: LINE 桌面版搬家到 E 碟的正確 SOP 和踩坑記錄
metadata: 
  node_type: memory
  type: project
  originSessionId: 9c64b31c-9b4d-4490-b41d-77b5d1e7bcf2
---

LINE 桌面版 AppData 搬到 E:\Claude-Data\LINE-AppData-Local。
Junction：C:\Users\bymyw\AppData\Local\LINE → E:\Claude-Data\LINE-AppData-Local。

**Why:** 教練將 LINE 資料搬到 E 碟節省 C 碟空間。
**How to apply:** LINE 搬家必須遵守以下鐵律，否則會觸發「Invalid launcher path」。

## 正確 SOP（2026-06-25 驗證成功）

1. 先確認 LINE 在 C 碟能正常啟動
2. 關閉 LINE
3. robocopy 整個資料夾到 E 碟（/E /COPY:DAT /DCOPY:T /XJ），驗證大小/檔案數差異為 0
4. rename 原資料夾為 .bak（可逆）
5. mklink /J 建立 junction（整個資料夾，不拆分）
6. 用 WScript.Shell 重建 .lnk 捷徑（修 NTFS Object ID 問題）
7. 啟動驗證

## 踩坑記錄

- 不可拆分 bin/Data/Cache 分開 junction → 會觸發 Invalid launcher path
- 不可修改 Registry（HKCU:\Software\LINE Corporation\LINE）→ 讓 junction 自動接管
- 不可在 LINE 壞掉的狀態下搬家 → 必須先重裝確認能跑再搬
- .lnk 必須重建，不能直接新建 → NTFS Object ID 失效問題
- D 槽筆電對照報告：https://gist.github.com/johnpeggy0706-bni/262f8346219a029f607f1be1ce9406c6
