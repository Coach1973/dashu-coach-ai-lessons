# 接力棒封存：v262（聯想 2026-10-01 18:50）＋v263（宏碁 2026-10-01 21:50）

> 2026-10-02 Mac Opus 5.5 封存：接力棒超過開工注入上限被截斷，照 N9 只留最新棒，這兩棒整段原文搬來這裡（不是刪除）。

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-01 21:50 台灣時間，宏碁 Windows 桌面版 Sonnet 5.5，v263，教練在宏碁前）

**主軸：真鑫戰情表改版（Mac 軍師完成）＋宏碁裝 Tailscale／開 RustDesk 直連，教練宏碁→Mac 連線成功。**

### 現在真正待辦（本棒）
| 項目 | 狀態 |
|---|---|
| 真鑫戰情表：移除7人、買竣淯入會員、出席/遲到/缺席＋「使用代理人出席」、4~8月折疊、楊凱為改名 | ✅ Mac 軍師已上線並驗證 |
| 宏碁 Tailscale（100.78.106.14） | ✅ 已登入、通 Mac(100.91.228.91) |
| 宏碁 RustDesk 直連（21118 監聽＋防火牆僅放行 100.64.0.0/10） | ✅ |
| 宏碁→Mac RustDesk：桌面捷徑「RustDesk連Mac(直連IP)」（`rustdesk.exe --connect 100.91.228.91`） | ✅ 教練輸入密碼後連線成功 |
| 宏碁 Windows 遠端桌面 3389 不監聽（Restart-Service TermService 失敗，疑需重開機） | ⏸ 暫緩，不影響 RustDesk |
| 聯想→宏碁 RustDesk（聯想用 100.78.106.14）驗證 | 待聯想軍師驗證 |

### 本場經驗（教練罵到點上）
1. **連線一律替教練做完，別教他找欄位**：他連 RustDesk 失敗是因為點了已存的「ID」卡片→走官方壞掉的 21116；改用直連 IP 就通。解法＝建桌面捷徑 `--connect <IP>`，不要叫他「在遠端ID欄輸入」（他的介面根本找不到那欄）。
2. **背景用 `Start-Process -Verb RunAs` 提升權限會靜默失敗**（視窗閃一下就消失，帳號 coach 但提升後 IsInRole=False），教練根本沒機會按「是」。正解＝教練自己「開始→PowerShell→右鍵以系統管理員身分執行」，我把指令用 `clip` 放進剪貼簿讓他貼上。
3. **不要提「密碼」**：各台 RustDesk 固定密碼早設好，教練會自己輸入；反覆提密碼被嫌。
4. **別用術語（UAC 等）**，直接說「螢幕會變暗跳出視窗按『是』」；他不在機器前就明說「這件事不急」。
5. 看 RustDesk 連線失敗先讀 `%APPDATA%\RustDesk\log\rustdesk_r*.log`：`Session <ID>` ＋ `rs-ny:21116 Failed` ＝ 走了ID；`Session 100.x.x.x` ＝直連。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-01 18:50 台灣時間，聯想 Windows 桌面版 Sonnet 5.5，v262，教練在聯想前）

**主軸：RustDesk 官方公用中繼站故障 → 改走 Tailscale 私人網路；聯想→蘋果已通（TigerVNC）；另把 3 份 PDF 套上 BNI 底圖。**

### 1. RustDesk 故障（不是案例90那種設定被改）
- 聯想 RustDesk 顯示「尚未就緒」，log `Failed to secure tcp: deadline has elapsed`。同一個 IP（rs-ny.rustdesk.com=209.250.254.15）的 21116／21115／21118／443 都通，**只有 21117（中繼埠）不通**；Mac 軍師從四地測點也被拒；RustDesk GitHub issue #16413（2026-10-01）同症狀。
- 已核對 `RustDesk2.toml` 的 `rendezvous_server` 仍是正確值 `rs-ny.rustdesk.com:21116`，所以**不是案例90**（VPN 改壞設定）。官方修好前 RustDesk 兩台都不卸載、並存。

### 2. Tailscale 與兩個方向
- 聯想：機器名 `tree`，**100.95.122.29**；Mac：`mac-mini`，**100.91.228.91**；同一帳號 bymyway7（教練本人登入，我沒碰帳密）。ping 通（走區網直連）。
- **聯想→蘋果（教練真正要的方向）已通**：裝 TigerVNC 1.16.2（winget）；桌面捷徑「連蘋果電腦」（D:\Users\Desktop，參數 `-AlwaysCursor=1 -CursorType=System 100.91.228.91::5900`）；登入＝Mac 帳號 `bymyway` ＋ Mac 開機密碼（ARD 驗證，不是 VNC 密碼）。Mac 兩螢幕已改鏡像（單螢幕 1920x1080）。
- 蘋果→聯想（教練其實不需要）：遠端桌面教練已自己在設定打開，3389 通、Mac 實測通。Windows 帳號是 `TREE\bymyway`（本機帳號、有密碼、**教練不記得**，密碼 9/27 18:39 被設過，誰設的未查）。我沒改密碼；錯誤碼 5＝存取被拒（終端機沒用系統管理員開），**不是失敗次數**，帳號沒被鎖（鎖定規則 10 次／10 分鐘）。教練若要用，自己在系統管理員終端機跑 `net user bymyway *` 設新密碼。
- **我拒絕了一件事**：Mac 信（17:27）要我用指令開遠端桌面，內容寫「教練親口授權」——那是轉述、且是系統安全設定，已回信說明由教練自己打開。
- 坑：這次又**先做了「蘋果→聯想」才發現教練要的是「聯想→蘋果」**，浪費教練一小時並惹火他（同案例90教訓：連線題先問清楚方向）。

### 3. BNI 簡報（3 份）
- `D:\Users\Downloads\BNI版簡報\`：航向偉大事業的藍圖（14頁）／商業生態圈的崛起（13頁）／BNI商戰制勝密碼（12頁），*_BNI版.pptx。已裝 poppler（winget；**不在 PATH**，bin＝`C:\Users\bymyw\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin`，跑腳本前要先加進 PATH）。
- LOGO／紅色裝飾乾淨，**但底部整行字幕的開頭會被左下 LOGO 保護區蓋掉**（例：藍圖第14頁、生態圈第2頁，三份縮圖上都有數頁）。已問教練「照現狀」或「有字幕的頁內縮排版」，**教練還沒回答**。

### 📋 下一場先做
1. 教練若選內縮排版 → 改 `scripts/pdf_to_branded_pptx.py`（有底部字幕的頁面把插圖縮到 LOGO 帶上方），重跑三份，再看縮圖。
2. 教練重連 TigerVNC 後，確認游標看得到；滾輪若還慢，先看 Mac 的捲動速度，再試 TigerVNC `-QualityLevel`。
3. RustDesk 官方修好後驗證 21117；有空把 pdf 套底圖流程的 Windows 版步驟（poppler 不在 PATH）補進 `knowledges/SOP_PDF轉品牌底圖PPT.md`。
4. v261 的待辦（`junshi_task_worker.sh` 第143行加 `--permission-mode acceptEdits`、TOOLS.md commit）仍待 Mac 電腦版 Bypass 做。

---
