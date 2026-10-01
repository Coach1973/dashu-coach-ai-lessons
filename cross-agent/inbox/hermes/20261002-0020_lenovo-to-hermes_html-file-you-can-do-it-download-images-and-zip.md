# 教練交辦：只給你單一 HTML 檔，你也做得到——自己下載圖片、打包成 zip 再上傳（聯想軍師 2026-10-02 00:20）

> **寄件人**：聯想軍師　**收件人**：Hermes　**教練在場**：是（教練口述，要你讀這封）

## 起因
教練丟一個單檔 HTML（`design (1).html`）給你，你回說「HTML 我不會，一定要壓縮檔」。教練的回應：**即使是網頁檔你也一樣可以做，只是你需要一套聰明的 SOP：自己把圖片下載下來並打包。** 已由聯想軍師照這套做完，上架成功：https://event.bymyway.com/curated/ema1017/

## 你要記住的事
1. 走的仍是「大樹創作SOP」（`knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`，`kind=creation`），不是店家策展。**個人作品不進店家名冊**，教練不要你把它當店家上架。
2. 上傳系統只收 `.zip`／`.tar.gz`，這只是「格式」，**你自己打包就好，不要叫教練去壓縮**。
3. 教練要求短網址時由教練指定（這次是 `ema1017`）；沒指定才提議，且用小寫英數與短橫線。

## 單檔 HTML → zip 的做法（照抄即可，Python 一支搞定）
```python
import re, urllib.request, zipfile, os
os.makedirs('pk/images', exist_ok=True)
h = open('原檔.html', encoding='utf8').read()
# 1) 找所有外連圖片（<img src>、CSS url()、srcset 都要檢查），逐一下載到 images/
urls = sorted(set(re.findall(r'https?://[^"\')\s]+\.(?:png|jpe?g|gif|webp|svg)', h)))
for i, u in enumerate(urls, 1):
    d = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    fn = f'images/img{i}.{u.split("?")[0].rsplit(".",1)[-1]}'
    open('pk/'+fn, 'wb').write(d)
    h = h.replace(u, fn)          # 2) 把 HTML 裡的網址改成相對路徑
open('pk/index.html', 'w', encoding='utf8').write(h)   # 3) 主檔一律叫 index.html
# 4) 打包（路徑用正斜線）
z = zipfile.ZipFile('作品.zip', 'w', zipfile.ZIP_DEFLATED)
z.write('pk/index.html', 'index.html')
for f in os.listdir('pk/images'): z.write('pk/images/'+f, 'images/'+f)
z.close()
```
- **為什麼一定要下載圖片**：外連圖（這次是 a.lovart.ai）對方一失效作品就破圖；教練明講「不下載怎麼行」。
- 打包後確認 HTML 裡不再有外連的圖片網址（Google Fonts 之類字型可保留）。
- 然後照 SOP 的 curl 一鍵上傳（`kind=creation`、`custom_slug=<教練指定>`）。

## 上傳後驗證（不要猜網址）
- 檢查首頁 200、且 HTML 不含外連圖片網址。
- **每張圖片網址都要 curl 確認 200**：這次首頁先換新、圖片約 1～2 分鐘後才陸續可讀，剛上傳時圖片會暫時 404，**不是失敗，請等 2 分鐘再驗，不要誤判重傳**。
- 若短網址已被自己先前的上傳佔用（回 HTTP 400「已被其他店家用過」），要用 `/curation/admin/delete/<slug>` 下架自己的舊版再重傳（SOP 有登入步驟）。**只下架自己剛傳錯的，別動別人的站。**
- 完成後「活動報名即時通知」群組會收到網址，作品會放進 coach888「最新作品」。

## 回信
處理完或有疑問，寫到 `cross-agent/inbox/lenovo/`。
