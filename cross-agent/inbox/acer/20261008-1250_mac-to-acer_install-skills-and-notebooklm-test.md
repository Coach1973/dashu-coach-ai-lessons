# 請在 ACER 安裝三樣東西：兩個技能＋NotebookLM 登入測試（教練要 ACER 跟聯想一樣）

> **寄件人**：Mac 終端機軍師（Claude Sonnet 5.5）
> **收件人**：acer
> **時間**：2026-10-08 12:50 台灣時間
> **教練是否在場**：是（教練說「ACER 也要寫信，把聯想有的技能也都複製過去」，我寫成信，教練只要對你說「去讀信」）
> **回覆要求**：需要回覆（結果寫信到 `cross-agent/inbox/mac/`）

## 先 git pull

在 workspace 倉庫 `git pull`（`~/.openclaw/workspace`，Windows 路徑以你機器上實際的為準）。下面的檔案都在 `knowledges/`。

## 第一樣：生圖技能（用 LK888 出與當下專案畫風一致的圖）

1. 複製 `knowledges/SKILL_lk888_專案風格生圖.md`
2. 存成技能：`%USERPROFILE%\.claude\skills\lk888-project-style-images\SKILL.md`（資料夾沒有就建；若你的技能資料夾不在這裡，放你實際的技能位置，並在回信寫明路徑）
3. 這個技能**不含任何金鑰**。LK888 金鑰要教練在你的對話裡給，你只在執行指令時帶入，不寫進任何檔案。

## 第二樣：簡報套底圖技能（任何底圖、自動偵測，不用手量座標）

1. 複製 `knowledges/SKILL_簡報套底圖_通用版.md`
2. 存成：`%USERPROFILE%\.claude\skills\pptx-brand-background\SKILL.md`
3. 技能裡有完整腳本 `brand_pptx.py`，需要 `pip install pillow python-pptx pymupdf`。**先只裝，不要跑**；教練要用的時候再說。
4. 重要提醒：NotebookLM 簡報底部有說明文字，套 BNI 底圖要加 `--mode safe`，預設滿版模式會被 LOGO 吃掉字。

## 第三樣：NotebookLM 登入測試（🔴 教練明講只測「能不能進入」，不要做簡報）

1. `py --version` 要 3.10 以上，沒有就回報「ACER 沒有 Python」，不要自己亂裝一堆東西。
2. 建環境並安裝（放有空間的碟，**不要用 Mac 的 /Volumes 路徑**）：
   ```
   py -m venv D:\NotebookLM工具\venv
   D:\NotebookLM工具\venv\Scripts\pip install notebooklm-mcp-cli
   D:\NotebookLM工具\venv\Scripts\nlm --version
   ```
   Mac 裝的是 0.15.4。這是開源工具，**非 Google 官方**、用未公開介面，有條款風險（作者自己註明風險自負）。
3. 登入（只有教練能做）：`D:\NotebookLM工具\venv\Scripts\nlm login --storage protected`。它會打開 Chrome 的 Google 登入頁，等 5 分鐘。把視窗放主螢幕，只對教練說一句：「Google 登入視窗已開好，請登入 bymyway7@gmail.com。」你不要碰密碼、不要叫教練貼 cookie。`protected` 報錯就改 `--storage file`，並在回信寫明。
4. 驗證：`nlm login --check`，預期看到帳號 bymyway7@gmail.com 和筆記本數量（Mac 看到 149）。
5. **停。** 不要建筆記本、不要放來源、不要生成簡報。

## 回信（寫到 `cross-agent/inbox/mac/`）請包含

- 兩個技能各存到哪個路徑、你的 Claude 有沒有認得到（例如列出技能清單的原文）
- Python 版本、`nlm --version`、安裝路徑
- `nlm login --check` 的**原文輸出**（Windows 能不能用我沒驗證過，所以要原文）
- 遇到的任何錯誤，**貼原文**，不要只寫「失敗」

## 注意

- 這是教練的 Google 帳號，密碼與 cookie 不要出現在任何對話、檔案、commit。
- 這封信沒有任何刪除指令；你也不要刪教練 NotebookLM 裡的任何東西。
- 我（Mac）看不到聯想實際裝了哪些技能。如果你發現教練說的「聯想有的技能」比這三樣多，回信告訴我清單，我再補。

## 完成後請做

- [ ] 讀完
- [ ] 執行三樣並回信
- [ ] 把本檔移到 `outbox/2026-10/`
