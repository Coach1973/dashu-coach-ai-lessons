---
name: project-line-moved-to-e
description: 試金石——LINE 搬家到外接硬碟的成敗對照（D 槽成功 vs E 槽先敗後成），任何機器的 AI 都必須讀懂這段歷史
metadata:
  type: project
  originSessionId: 9c64b31c-9b4d-4490-b41d-77b5d1e7bcf2
  updated: 2026-06-25
---

# 試金石：LINE 桌面版搬家到外接硬碟

> 這是教練在兩台 Windows 電腦上搬移 LINE 的完整經歷。一成一敗的對比，是未來處理同類任務的試金石。

## 一、宏碁筆電（D 槽）—— 成功

- 機器：ACER 筆電，D:\Claude-Data
- 做法：D 槽的 AI 助手一次到位，LINE 搬到 D 碟後正常運作
- 對照報告：https://gist.github.com/johnpeggy0706-bni/262f8346219a029f607f1be1ce9406c6
- 關鍵：整個 AppData\Local\LINE 資料夾用 junction 一次搬，不拆分、不改 registry

## 二、聯想筆電（E 槽）—— 先敗後成

### 失敗經過

教練把 LINE 的 AppData 搬到 E:\Claude-Data\LINE-AppData-Local，結果啟動就跳「Invalid launcher path」。

**AI 嘗試過但全部失敗的方法：**
1. 直接執行 LINE.exe → 一樣報錯
2. 修 Registry 指向新路徑 → 無效
3. 拆分 bin/Data/Cache 各自 junction → 更糟
4. 試圖照搬 D 槽筆電的設定 → 環境不同，不能硬套

**失敗根因：** LINE 安裝本身已經損壞（MSIX 版本不匹配），在壞掉的狀態上做搬家，怎麼搬都不會對。

### 成功 SOP（2026-06-25 驗證通過）

1. **先重裝 LINE**，確認在 C 碟能正常啟動、登入、收發訊息
2. 關閉 LINE
3. `robocopy` 整個資料夾到 E 碟（`/E /COPY:DAT /DCOPY:T /XJ`），驗證大小與檔案數一致
4. 把原資料夾改名為 `.bak`（可逆，不刪）
5. `mklink /J` 建立 junction（整個資料夾，不拆分）
6. 啟動 LINE 驗證 → 成功

## 三、鐵律（用血淚換來的）

| 編號 | 鐵律 | 違反的後果 |
|------|------|-----------|
| 1 | **先裝好、確認能跑，再搬** | 壞掉的 LINE 搬了也是壞的 |
| 2 | **整個資料夾一個 junction，不拆分** | 拆了 bin/Data/Cache 會觸發 Invalid launcher path |
| 3 | **不改 Registry** | junction 自動接管路徑，改 Registry 多此一舉且有風險 |
| 4 | **原資料夾 rename .bak，不刪** | 萬一搬壞了還能回退 |
| 5 | **有成功案例就先去讀那份 SOP** | D 槽筆電已經成功了，應該第一時間拿來對照 |

## 四、驗證題（AI 自證已讀）

1. LINE 搬家前最重要的前提是什麼？ → 先確認 LINE 能正常啟動
2. junction 要建在哪一層？ → 整個 AppData\Local\LINE 資料夾，不拆分
3. 已有成功案例時第一步做什麼？ → 去讀那份成功的 SOP，不要自己瞎猜
