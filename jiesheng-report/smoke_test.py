"""
自我檢測腳本：模擬工作人員完整操作流程，驗證登入/新增/勾選繳費/統計/刪除全部正確。
用法：JIESHENG_TEST_BASE=http://127.0.0.1:5061 JIESHENG_TEST_USER=staff JIESHENG_TEST_PASS=xxx python smoke_test.py
本機開發用預設值：base=http://127.0.0.1:5061, user=staff, pass=test1234（跟本機測試環境一致）
部署到 Mac 後也可以用這支腳本對 https://jiesheng-report.bymyway.com 跑一次，確認上線沒壞掉。
"""
import http.cookiejar
import os
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.environ.get("JIESHENG_TEST_BASE", "http://127.0.0.1:5061")
USER = os.environ.get("JIESHENG_TEST_USER", "staff")
PASS = os.environ.get("JIESHENG_TEST_PASS", "test1234")

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def req(method, path, data=None):
    url = BASE + urllib.parse.quote(path, safe="/?=&")
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    with opener.open(r) as resp:
        return resp.status, resp.read().decode("utf-8")


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    if not cond:
        raise SystemExit(1)


# 1. 登入
status, html = req("POST", "/admin/login", {"username": USER, "password": PASS})
check("登入成功", status == 200 and "戰報" in html)

# 2. 台南新增一位測試報名者
status, html = req("POST", "/admin/add", {
    "workshop": "台南", "name": "煙霧測試小明", "phone": "0912345678",
    "register_date": "2026-07-26", "note": "smoke_test自動產生",
})
check("新增報名者未出錯", status == 200)

status, html = req("GET", "/admin?workshop=台南")
check("台南名單看得到剛新增的人", "煙霧測試小明" in html)
m = re.search(r'/admin/update/(\d+)"[^>]*>.*?name="name" value="煙霧測試小明"', html, re.S)
if not m:
    m = re.search(r'id="save-(\d+)"[^>]*action="/admin/update/\d+"', html)
    m2 = re.search(r'煙霧測試小明.*?name="save-(\d+)"', html, re.S)
reg_id = None
for mm in re.finditer(r'id="save-(\d+)"', html):
    reg_id = mm.group(1)  # 抓最新一筆（新增的會排在最前面，DESC排序）
    break
check("抓到新報名者的 id", reg_id is not None)

# 3. 統計數字：報名1、已繳0、未繳1
row = re.search(r'台南.*?報名<b>(\d+)</b>.*?已繳<b>(\d+)</b>.*?未繳<b>(\d+)</b>', html, re.S)
check("新增後統計正確(報名1/已繳0/未繳1)", row and row.group(1) == "1" and row.group(2) == "0" and row.group(3) == "1")

# 4. 勾選已繳費
status, html = req("POST", f"/admin/update/{reg_id}", {
    "name": "煙霧測試小明", "phone": "0912345678", "register_date": "2026-07-26",
    "note": "smoke_test自動產生", "paid_method": "ATM", "amount": "1000", "paid": "on",
})
check("勾選繳費未出錯", status == 200)

status, html = req("GET", "/admin?workshop=台南")
check("勾選後名單顯示已繳費", "已繳費" in html and "煙霧測試小明" in html)
row = re.search(r'台南.*?報名<b>(\d+)</b>.*?已繳<b>(\d+)</b>.*?未繳<b>(\d+)</b>', html, re.S)
check("繳費後統計正確(報名1/已繳1/未繳0)", row and row.group(1) == "1" and row.group(2) == "1" and row.group(3) == "0")

# 5. 台中/台北也能各自新增，互不干擾
req("POST", "/admin/add", {"workshop": "台中", "name": "煙霧測試台中", "register_date": "2026-07-26"})
req("POST", "/admin/add", {"workshop": "台北", "name": "煙霧測試台北", "register_date": "2026-07-26"})
status, html = req("GET", "/admin?workshop=台中")
check("台中名單只看到台中的人、看不到台南的人", "煙霧測試台中" in html and "煙霧測試小明" not in html)
status, html = req("GET", "/admin?workshop=台北")
check("台北名單只看到台北的人", "煙霧測試台北" in html and "煙霧測試小明" not in html)

# 6. 清理測試資料（刪除三筆測試資料）
status, html = req("GET", "/admin?workshop=台南")
for mm in re.finditer(r'id="del-(\d+)"', html):
    req("POST", f"/admin/delete/{mm.group(1)}")
status, html = req("GET", "/admin?workshop=台中")
for mm in re.finditer(r'id="del-(\d+)"', html):
    req("POST", f"/admin/delete/{mm.group(1)}")
status, html = req("GET", "/admin?workshop=台北")
for mm in re.finditer(r'id="del-(\d+)"', html):
    req("POST", f"/admin/delete/{mm.group(1)}")

status, html = req("GET", "/admin?workshop=台南")
check("刪除後台南名單清空、統計歸零", "煙霧測試小明" not in html and "目前還沒有報名者" in html)

print("\n全部通過：登入／新增／勾選繳費／統計即時反映／三城市互不干擾／編輯／刪除，全流程正常。")
