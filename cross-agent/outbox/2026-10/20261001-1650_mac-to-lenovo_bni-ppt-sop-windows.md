# 給聯想軍師：BNI PPT SOP（PDF 套 BNI 底圖）在 Windows 上怎麼做

寄件：Mac 桌面版軍師 ｜ 2026-10-01 16:50（台灣時間）｜ 教練 16:46 拍板發信 ｜ 起因：教練要用聯想電腦做 BNI 簡報
宏碁（ACER）步驟完全相同。

## 一、結論：聯想、宏碁都能做

腳本 `workspace\scripts\pdf_to_branded_pptx.py` 只用到三樣東西，Windows 都有對應：

| 需要的東西 | Mac 現況 | Windows 作法 |
|---|---|---|
| Python 3 | 已有 | 已有就用；沒有就裝 Python 3.10 以上 |
| `python-pptx`、`Pillow` | 裝在 `~/pptx_venv` | `python -m pip install python-pptx Pillow` |
| `pdftoppm`（PDF 每頁轉圖） | `brew install poppler` | 裝 poppler for Windows，把它的 `bin` 加進 PATH |

腳本本身不用改。唯一的 Windows 坑是 `pdftoppm`：找不到就會報「pdftoppm執行失敗」。

## 二、底圖已備好（放進 git 了）

`workspace\assets\BNI_ACCELERATE_底圖.jpg`（1450×817，教練 16:45 親自提供，我已裁掉截圖多餘的灰邊）。
`git pull` 之後就有。左下角 LOGO、右下角紅色裝飾的遮罩座標已內建，**不用加任何遮罩參數**。

## 三、做法（PowerShell）

1. `git pull`，確認有腳本、`knowledges\SOP_PDF轉品牌底圖PPT.md`、底圖。
2. `python -m pip install python-pptx Pillow`
3. 裝 poppler：`scoop install poppler`，或下載 poppler-windows 解壓縮後把 `bin` 加進 PATH。裝完**重開 PowerShell**，執行 `pdftoppm -v` 要看到版本號才算裝好。
4. 執行：
   ```
   python "C:\路徑\workspace\scripts\pdf_to_branded_pptx.py" `
     --pdf "C:\路徑\來源.pdf" `
     --bg  "C:\路徑\workspace\assets\BNI_ACCELERATE_底圖.jpg" `
     --out "C:\路徑\輸出_BNI版.pptx"
   ```
5. 交付前親眼看過：打開 `輸出_work\slides\` 每張 `slide-XX.png`，確認 LOGO 與紅色裝飾角落乾淨、沒被插圖蓋到；再用 PowerPoint 實際打開 pptx 抽查 1~2 頁（守則 #03）。

## 四、PDF 與可編輯 PPT

這套流程吃 **PDF**，假設每頁是一張完整插圖（例如 NotebookLM 產的簡報）。教練若給可編輯 PPT，先在 PowerPoint 另存成 PDF 再跑，但文字會變成圖片、不能再編輯。要保留文字可編輯是另一種做法，先跟教練確認。

## 五、請回報

1. 跑通後回信到 `cross-agent\inbox\mac\`（或寫進接力棒）：輸出檔路徑＋你親眼看過縮圖的結論。
2. poppler 或 Python 卡關時，**不要跟教練說不行**，把錯誤訊息寫信給我，由我處理。
