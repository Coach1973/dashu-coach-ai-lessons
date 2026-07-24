---
name: project-line-moved-to-e
description: 試金石——LINE 搬家血淚全紀錄（4GB 資料丟失 + 版本差異導致 junction 失敗 + 2026-07-24 junction未拆就解除安裝二度驚魂），任何機器的 AI 都必須讀懂
metadata:
  type: project
  originSessionId: 9c64b31c-9b4d-4490-b41d-77b5d1e7bcf2
  updated: 2026-06-25
  modified: 2026-07-24T07:58:10.114Z
---

# 試金石：LINE 桌面版搬家到外接硬碟

> 這是教練在兩台 Windows 電腦上搬移 LINE 的完整經歷，包含一次**嚴重資料丟失事故**。

## 🔴🔴🔴 最慘痛教訓：4GB 聊天記錄永久丟失

### 事故經過

1. 聯想筆電 LINE 原有約 4GB 聊天記錄（含對話、圖片、影片、檔案）
2. 搬家到 E 碟失敗後，AI 建議重裝 LINE，教練同意
3. 重裝前 E 碟有一份 robocopy 備份（`LINE-AppData-Local.old.20260625-*`）
4. **AI 在同一場對話中把 C 碟 .bak 和 E 碟 .old 備份全部 `Remove-Item -Recurse -Force` 刪除**
5. SOP 白紙黑字寫「保留 7 天再刪」，AI 卻當場刪光

### 為什麼無法恢復

- **LINE 電腦版沒有雲端備份功能**（官方確認）
- 手機版的雲端備份只能還原到手機，不能還原到電腦版
- UltFone for LINE 備份（146 GB）也只能還原到手機
- `Remove-Item -Force` 永久刪除，不進回收桶

### 鐵律（用教練 4GB 資料換來的）

| 編號 | 鐵律 | 違反的後果 |
|------|------|-----------|
| 🔴1 | **.bak 備份 7 天內絕對不刪** | SOP 寫了就要遵守，這次就是沒遵守 |
| 🔴2 | **重裝任何軟體前，先把原始資料完整備份到獨立位置** | 重裝會清掉資料，不備份就是不可逆 |
| 🔴3 | **LINE 電腦版唯一備份方式 = 手動複製 AppData\Local\LINE** | 沒有雲端備份，沒有第二條路 |
| 🔴4 | **`Remove-Item -Recurse -Force` 是不可逆指令，必須過五道閘門** | 教練的資料一刪就沒了 |

---

## 一、宏碁筆電（D 槽）—— 成功

- 機器：ACER 筆電，D:\Claude-Data
- LINE 版本：**9.12.0**（舊版，LineLauncher 沒有路徑驗證）
- 做法：整個 AppData\Local\LINE 用 junction 一次搬到 D 碟
- 對照報告：https://gist.github.com/johnpeggy0706-bni/262f8346219a029f607f1be1ce9406c6
- 結果：**一次成功**，junction 完全透明

## 二、聯想筆電（E 槽）—— 失敗

- 機器：聯想筆電，E:\Claude-Data
- LINE 版本：**26.3.0**（新版，LineLauncher 加了路徑驗證）
- 做法：同樣用 junction，結果報「Invalid launcher path」

### 失敗根因（版本差異）

**ACER 能成功、聯想失敗的唯一原因：LINE 版本不同。**

LINE 26.x 的 LineLauncher.exe 會用 `GetModuleFileName()` 取得自己的實際路徑，跟 Registry 中的 `LauncherPath` 比對。透過 junction 啟動時，Windows 解析成 E 碟真實路徑，跟 Registry 的 C 碟路徑不匹配，就報錯。LINE 9.x 沒有這個驗證，所以 ACER 不受影響。

### 最終可行方案（2026-06-25 二次驗證通過，含 4GB 聊天記錄）

**bin 留 C 碟，Data + Cache 用 junction 搬到 E 碟：**

1. 關閉 LINE（`Stop-Process -Name LINE,LineLauncher -Force`）
2. `robocopy` Data 和 Cache 到 E 碟（`/E /COPY:DAT /R:1 /W:1`，**禁用 /COPYALL** 否則報權限錯誤）
3. 用 `/MIR` 再跑一次確保 E 槽無多餘殘留
4. 比對來源和 E 槽檔案數 + 大小，**差異必須為 0 才能繼續**
5. Rename 原始 Data、Cache 為 `.bak.YYYYMMDD-HHmmss`（**🔴 保留 7 天不刪，到期：2026-07-02**）
6. `mklink /J` 建 junction（Data → E 碟、Cache → E 碟）
7. 啟動 LINE，確認聊天記錄都在

這樣 LineLauncher 從 C 碟的 bin 啟動，不觸發路徑驗證。Data 和 Cache 佔 95% 以上空間，搬到 E 碟達到省空間目的。

**第二次實際數據（2026-06-25）：**
- Data：1,663.5 MB（20,713 個項目）→ E 槽
- Cache：2,030.3 MB（111,395 個項目）→ E 槽
- bin：377 MB → 留 C 槽
- 省下 C 槽：3.6 GB

---

## 三、完整鐵律表

| 編號 | 鐵律 | 違反的後果 |
|------|------|-----------|
| 🔴1 | **.bak 備份 7 天內絕對不刪** | 4GB 聊天記錄永久丟失 |
| 🔴2 | **重裝前先備份到獨立位置** | 重裝會清掉資料 |
| 🔴3 | **LINE 電腦版沒有雲端備份** | 手動複製是唯一方式 |
| 4 | **先裝好、確認能跑，再搬** | 壞掉的搬了也是壞的 |
| 5 | **LINE 26.x 不能整個資料夾 junction** | LineLauncher 路徑驗證會失敗 |
| 6 | **LINE 26.x 折衷：bin 留 C，Data+Cache junction** | 兼顧省空間和啟動正常 |
| 7 | **有成功案例先讀那份 SOP** | 不要自己瞎猜 |
| 8 | **不改 Registry** | junction 自動接管 |

## 六、2026-07-24 二度驚魂：junction 還接著就解除安裝，E 槽真資料被沿路刪光（幸好有備份接住）

**起因**：LINE 卡死打不開（開了程序但視窗生不出來，CPU 幾乎零，殭屍程序越點越多）。查證後找到兩個線索：
1. `E:\Claude-Data\LINE-Cache` 底下光一個子資料夾就有 2.6 萬+ 檔案，掃描/初始化極慢
2. Windows Temp 資料夾裡有殘留的 `qtsingleapp-line*-lockfile`——LINE 用 Qt 的單一實例鎖定機制，只要上次是被 `Stop-Process -Force` 強制關掉（無論是當機、斷電，還是 AI 自己動手），這個鎖定檔就不會被清掉，下次啟動去驗證這個殘留鎖定檔時卡住，正是「開了程序、視窗生不出來、CPU 不動」的元兇

**修復動作**：清空 Cache、清殘留鎖定檔、改用 `LineLauncher.exe --booting` 正確啟動方式——這些都對，但這次還是沒解決，於是決定乾淨重裝。

**🔴🔴🔴 真正出事的地方**：重裝第一輪，junction（`C:\...\LINE\Data` → `E:\Claude-Data\LINE-Data`）已經接對確認過（8683 項/1311.7MB），但因為要進一步除錯，junction 沒有先拆掉。教練接著自己動手做了第二輪「解除安裝→重裝」，解除安裝程式在清理 `C:\...\LINE\Data` 時，**沿著還連著的 junction 把 E 槽的真實資料也一起清空了**——直接查 `E:\Claude-Data\LINE-Data`（不透過 junction）發現變成 0 個項目。跟本檔案最上面「4GB 聊天記錄永久丟失」事故的死法幾乎一模一樣，只是這次角色換成解除安裝程式，不是 AI 自己下 Remove-Item。

**這次沒有釀成災難的唯一原因**：一開始拆第一次 junction 前，就先做了一份獨立備份到 `E:\Claude-Data\LINE-Data.bak.<timestamp>`（用 robocopy，跟來源比對項目數與大小完全一致才算數）。事後直接從這份備份 robocopy 回填、重新驗證項目數/大小相符，再重建 junction，資料完全復原。

**新增鐵律（比照 🔴1~4 同等級）**：

| 編號 | 鐵律 | 違反的後果 |
|------|------|-----------|
| 🔴9 | **junction 只要還接著，絕對不能對那個 App 做解除安裝／移除／重裝，一定要先拆 junction** | 解除安裝程式不會分辨 junction，會沿著連結把外接硬碟的真實資料也一起清掉 |
| 🔴10 | **每一次要拆 junction 或重裝，都要重新走一次「先獨立備份」流程，不能因為「上次做過了」就省略** | 這次差點出事就是因為除錯中途分心，忘記在第二次操作前重新確認 junction 狀態 |
| 🔴11 | **拆 junction 一律用 `[System.IO.Directory]::Delete(path, $false)` 或不帶 -Recurse 的 Remove-Item，絕不能用遞迴刪除指令去清 junction 所在的父資料夾** | 遞迴刪除會穿透 junction 刪到真正的目標內容 |

Related: 這次事故最終仍未修好 LINE 開不了的根本問題（懷疑跟這台機器 WMI/CIM 子系統異常有關，多個 PowerShell 存放體查詢指令會無故卡住，需要系統管理員權限才能繼續往下查），教練最終決定用 2026-07-11 的 C 槽系統映像一鍵還原解決，D/E 槽不受影響。還原後需要補裝 7/12 之後新增的軟體：NordVPN(7/17)、Comet(7/22)、Gan Jing Browser(7/24)。LINE 本身不用重裝，還原後會回到搬家前的正常狀態。

## 五、聯想機（TREE）過期備份清理完成（2026-07-08）

聯想筆電（主機名 TREE，E:\Claude-Data）上，LINE 之外還有 GanJing（乾淨世界）、Perplexity（Comet）、Claude 桌面版沙盒（vm_bundles）也用同一套「junction 搬到 E 槽＋原地留 .bak」模式。查證五組 .bak（LINE Data+Cache、GanJing User Data、Perplexity Comet、Claude vm_bundles）都已超過 7 天保留期，E 槽現役資料都驗證有當天寫入紀錄，教練自己另做了一鍵備份當保險後，確認清除，共釋放 C 槽約 13.8GB。事後教練逐一重開 LINE、乾淨世界、Perplexity、Google（Chrome）、Claude 桌面版，全部正常。

**教訓**：這台機器搬家搬的不只 LINE，凡是曾經 junction 到 E 槽的 App，搬家當天的 .bak 都要記得追蹤 7 天到期，不會自動提醒，要主動查。

## 四、驗證題（AI 自證已讀）

1. LINE 電腦版有雲端備份嗎？ → **沒有**，唯一備份方式是手動複製資料夾
2. .bak 備份最少保留幾天？ → **7 天**，任何情況不得提前刪除
3. LINE 26.x 為什麼不能整個資料夾 junction？ → LineLauncher 會驗證路徑，junction 解析成真實路徑後不匹配
4. 正確的折衷方案是什麼？ → bin 留 C 碟，Data + Cache 用 junction 搬到外碟
