# 給聯想電腦：BNI 底圖「滿版」套版指令（2026-10-08 更新）

> 教練說的「BNI PPT SOP」＝ 套 BNI 底圖、**滿版**。
> 上一版聯想跑出來是縮小的，原因是沒有指定模式，程式自動選成「縮小」。這一版把模式寫死。

## 一句話規則

**套 BNI 底圖，一定要加 `--mode mask`。不准用 `safe`，不准縮小。**

## 第一步：確認有工具（只要做一次）

```bash
pip install pillow python-pptx pymupdf
```

## 第二步：執行（每次都用這一行）

把 `簡報.pdf`、`BNI_ACCELERATE_底圖.jpg` 換成實際的檔案路徑。Windows 用 `python`：

```bash
python brand_pptx.py --src 簡報.pdf --bg BNI_ACCELERATE_底圖.jpg --out 簡報_BNI版.pptx --mode mask
```

**不要加的參數：** `--mode safe`、`--fill contain`、`--safe-box`。這些都會把內容縮小。

## 第三步：驗收（缺一不算完成）

1. 打開 `簡報_BNI版.pptx`，每一頁的插圖要**貼齊四邊、沒有白邊**。
2. 左下角 **BNI ACCELERATE LOGO** 還在、右下角 **紅色弧形** 還在。
3. 如果看到四周白邊、或內容只佔中間一塊 → **模式錯了**，重新執行第二步（加 `--mode mask`），不要自己去調座標。
4. 腳本印出「完成」不算數，要真的打開看過每一頁縮圖。

## 如果做出來還是縮小

把執行的完整指令截給教練看，不要自己亂改 `--safe-box`。

---
> 來源與完整說明：`knowledges/SKILL_簡報套底圖_通用版.md` 的「範例：BNI ACCELERATE 底圖」段。
