---
name: feedback-windows-file-proof-use-explorer-not-browser
description: Windows下要向教練證明本機檔案真實存在，必須用檔案總管 explorer.exe /select 反白，不能靠瀏覽器打開HTML——教練會誤以為是網頁、不知道存在哪裡
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1770c262-04fd-4812-9b49-c06f84deed0b
---

Windows 機器上，當教練問「檔案在哪裡」「這是不是真的存在」，要用 `explorer.exe /select,"絕對路徑"` 開檔案總管並反白選取該檔案，讓教練親眼看到圖示躺在資料夾裡；**不要用瀏覽器（Chrome）打開 HTML 檔案來證明它存在**。

**Why：** 2026-07-02 血淚——先幫教練合併四瀏覽器書籤產出 `四瀏覽器書籤合併.html`，教練問「檔案放在哪」，軍師用 Chrome 打開該 HTML 檔給教練看。教練看到的是瀏覽器渲染出來的書籤清單畫面，完全看不出這是一個「躺在桌面的檔案」，反而以為是網頁、不知道它存在什麼地方，甚至說「它連檔案都不是」。改用 `explorer.exe /select` 讓檔案總管跳出來、桌面資料夾內該檔案圖示反白，教練才第一次真正理解「這是一個真實存在硬碟上的檔案」。教練原話確認：「你這一次才有做對，我這一次才真正看到它存在在桌面上。之前我只有看到網頁，我都不知道這網頁存在什麼地方。」

**How to apply：** 教練是電腦小白（見 [[feedback_plain_chinese_no_jargon]]），對「檔案」與「網頁」沒有直覺的區分——瀏覽器渲染出來的畫面對他來說一律是「網頁」，不管背後是不是本機檔案。凡是教練問檔案位置、要確認檔案真的產出、或要教他把檔案帶去別台電腦用，一律先 `explorer.exe /select,"路徑"`（Windows）或 `open -R 路徑`（Mac，見 [[feedback_do_everything_for_user_fileoperation]]）讓檔案總管/Finder 反白選取實體圖示，用「這是一個檔案，位置在桌面，跟你平常看到的 Word 檔一樣」這種類比說明，再教怎麼帶走（隨身碟／LINE傳自己／雲端硬碟）。瀏覽器打開只適合「看內容對不對」，不能拿來當「證明檔案存在」的動作。

**追加教訓（同一事件的第二層）：** 第一次存檔時軍師直接用 Windows 系統預設桌面路徑 `C:\Users\bymyw\Desktop\`，結果教練登入畫面實際看到的桌面是登錄檔重新指向的 `D:\Users\Desktop\`（`HKCU\...\User Shell Folders\Desktop` 查得到，`C:\Users\bymyw\Desktop` 本身不是 junction，只是沒人再用的孤兒資料夾）——這正是 `聯想 CLAUDE.md`「⚡ 聯想環境速查」表格裡早就寫好的 `桌面路徑 | D:\Users\Desktop\`，軍師卻沒查表直接用系統預設路徑猜。**以後在聯想這台機器存檔到「桌面」，一律用 `D:\Users\Desktop\`，存檔前若不確定路徑，先查 CLAUDE.md 路由表或登錄檔 `User Shell Folders`，不要用 OS 預設路徑假設。**
