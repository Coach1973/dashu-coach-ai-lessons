# SOP：PDF 插圖轉「品牌底圖」PPT（2026-09-21 建立）

> 🏷️ **教練簡稱：「BNI PPT SOP」**——教練說這句話，就是指這份SOP+`scripts/pdf_to_branded_pptx.py`這一整套流程，不用重新解釋。

## 適用情境

手上有一份 PDF（例如 NotebookLM 生成的圖文簡報），每頁都是一張完整插圖。
現在要把這些插圖套進一張固定的品牌底圖（例如 BNI ACCELERATE 範本），
底圖角落有 LOGO／裝飾圖案（左下角 LOGO、右下角紅色裝飾），
要求插圖盡量滿版鋪滿，但不能蓋住這些角落的品牌識別元素。

**只要底圖不變，同一套流程可以重複用在不同的 PDF 內容上**——這是 2026-09-21
教練親自交辦「好幾份簡報都要做這個」時確立的可重複 SOP，第一次用在
《建構高效商務系統的建築師》BNI 版簡報。

## 前置需求（第一次用要裝，裝過一次之後不用重裝）

```bash
brew install poppler   # 提供 pdftoppm，把PDF頁面轉成PNG
python3 -m venv ~/pptx_venv   # 建一個獨立的Python環境，避免弄壞系統Python
source ~/pptx_venv/bin/activate
pip install python-pptx Pillow
```

之後每次要跑，只要 `source ~/pptx_venv/bin/activate` 啟用這個環境即可，不用重裝。

## 核心腳本

`scripts/pdf_to_branded_pptx.py`（已寫好、已測試、已進repo）

用法：

```bash
source ~/pptx_venv/bin/activate
python3 /Users/bymyway/.openclaw/workspace/scripts/pdf_to_branded_pptx.py \
  --pdf "/path/to/來源.pdf" \
  --bg  "/path/to/底圖.jpg" \
  --out "/path/to/輸出.pptx"
```

跑完會印出：
1. 抽取了幾頁
2. 合成過程檔案存放位置（`輸出檔名_work/`，裡面有每頁抽出的原圖 + 合成後的每張投影片PNG，確認OK可以自己刪掉）
3. 最終PPTX路徑

**同一份底圖（例如BNI ACCELERATE）重複使用時，不用加任何額外參數**——腳本內建的
遮罩座標就是照這份底圖量出來的，直接換 `--pdf` 跑下一份簡報即可。

## 交付前必做：親眼看過每一張

腳本跑完不算完成，要做這兩步再交給教練：

1. 產生縮圖總覽自己看一遍（把 `輸出檔名_work/slides/slide-*.png` 全部縮小拼成一張大圖），
   確認每一張的LOGO跟裝飾角落都乾淨、沒被插圖蓋到
2. 用 `open 輸出.pptx` 打開實際檔案，抽查1-2頁在PowerPoint/Keynote裡顯示正常

守則#03「結論出來之前自己要先看過」——工具沒報錯不代表畫面是對的，一定要真的看過縮圖或打開檔案。

## 換一張新底圖時才需要做的事：重新量測遮罩

如果哪天要換成不是BNI ACCELERATE的底圖（LOGO位置不同），才需要重新量測，步驟：

1. 用Python讀底圖，找出LOGO跟裝飾圖案的像素範圍：

```python
from PIL import Image
img = Image.open("新底圖.jpg")
w, h = img.size
px = img.load()

def is_white(c, tol=15):
    return all(abs(v-255) < tol for v in c)

# 抓左下角LOGO的bounding box（掃描範圍依實際LOGO大概位置調整）
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(int(h*0.7), h-2):
    for x in range(0, int(w*0.4)):
        if not is_white(px[x, y]):
            minx, maxx = min(minx,x), max(maxx,x)
            miny, maxy = min(miny,y), max(maxy,y)
print("logo比例:", minx/w, miny/h, maxx/w, maxy/h)
```

2. 把量出來的 `x0,y0,x1,y1`（比例值）餵給 `--mask-logo-box`
3. 右下角裝飾如果也是斜對角造型，比照 `pdf_to_branded_pptx.py` 裡 `build_mask()` 的
   邏輯，掃描每隔幾像素找對角線邊界，取起點比例 `x0` 跟頂點比例 `apex_y`，
   餵給 `--mask-swoosh`
4. 先用1張投影片小規模測試，看縮圖沒問題，再跑全部

若裝飾圖案形狀差異很大（不是三角/矩形這種簡單形狀），跟軍師說一聲，
腳本的 `build_mask()` 函式需要客製化畫法（例如換成任意多邊形或圓角遮罩）。

## 常見問題

- **`pdftoppm not found`**：忘記 `brew install poppler`
- **PPT打開圖片模糊**：`--dpi` 預設150，內容文字很多可以拉高到200再跑
- **插圖邊緣跟底圖過渡太生硬/太模糊**：調整 `--feather`（預設28，數字越大越柔和）
- **這次PDF的插圖比例跟底圖差很多，裁切後重點內容被切掉**：目前用「等比裁切置中」
  (cover模式)，如果某幾頁的重要內容剛好在會被裁掉的邊緣，需要單獨手動處理那幾頁，
  不能只靠腳本一次全部跑完

## 相關記錄

- 第一次使用：2026-09-21，PDF《Architecting_Business_Systems_(2).pdf》15頁 →
  《建構高效商務系統的建築師_BNI版.pptx》，教練驗收「做的好」
- lk888圖片生成模型（`scripts/generate_industry_chain.py`）沒有用在這個流程——
  這是「排版合成」不是「重新生圖」，本機圖片處理工具做得更精準也更省錢，
  除非教練明確要求重新生成插圖內容本身
