import json
import urllib.request
import urllib.parse

MESSAGE = """🌳 這堂課我已經講了十幾場了，我發覺效果非常好，可以幫助許多人。

🤖 第一次使用 AI，就能感受到在不花錢的前提下，就可以把 AI 用得淋漓盡致，一個在培訓界講溝通的老師，果然會帶給聽眾們從一個不一樣的角度去切入 AI。

如果你從來沒有聽過教練講的這堂課，歡迎一起來學習！

👉 https://bigtree-tw.netlify.app/?session=2026-09-05"""

TARGET_PAGES = ["大台南策展中心", "K R養生廚房", "海餅乾俱樂部", "跨界美.術.管"]

with open("fb_automation/page_tokens_2026-08-27.json", encoding="utf-8") as f:
    data = json.load(f)

results = []
for page in data["pages"]:
    if page["name"] not in TARGET_PAGES:
        continue
    url = f"https://graph.facebook.com/v20.0/{page['id']}/feed"
    payload = urllib.parse.urlencode({
        "message": MESSAGE,
        "access_token": page["access_token"],
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            results.append((page["name"], "OK", body.get("id")))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        results.append((page["name"], "FAIL", err_body))

for name, status, info in results:
    print(f"{name} | {status} | {info}")
