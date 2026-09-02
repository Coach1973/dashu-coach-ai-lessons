# -*- coding: utf-8 -*-
"""
BNI入會/續約發票 - 內部後台（私有，不對外公開）

⚠️ 這支腳本產生的 bni_membership_admin.html 含會員統編/個人載具/email/電話/歷史發票，
   僅供教練開發票時查用。只放在這個私有大腦repo(mac-openclaw-workflows，GitHub上是private)。

跟「培訓費」(build_bni_training_admin.py，店代337643900/344031309)是完全獨立的系統：
這支是「聚寶盆」商業顧問有限公司(店代337391376)開立的BNI入會/續約發票，金額$24,000起跳，
一年一次；培訓費是大樹教育開立，金額$300~$1800，每月都有。兩邊資料不互相比對，教練親口
2026-09-03交代：這是兩個獨立系統，不能混為一談。

來源：
  claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv（238筆，2年完整歷史原始匯出）
  claude-brain/data/ezpay_invoice_remarks_108taxid_2026-08-17.csv（108個統編→分會+姓名備註對照）
  claude-brain/data/ezpay_bni_membership_invoices_2026-08-24_12張完成清單.json（入會12張）
  claude-brain/data/ezpay_bni_renewal_invoices_2026-08-24_6張完成清單.json（續約6張）
  namecard-db/namecards.db 的 cards 表（電話/Email，用姓名比對，去空格後聯合查詢避免
  「姓 空格 名」格式跟cards表本身重複列造成的fan-out——用子查詢取一筆，不用JOIN）

比對邏輯：
  買受人統編 == "-" 的CSV列＝個人發票，買受人名稱本身就是會員姓名，可直接用。
  買受人統編 != "-" 的CSV列＝公司發票，姓名要查remarks CSV的「發票備註」欄(格式
  「OO分會-姓名」或「OO-姓名」不一致，用regex兩種都吃)才知道是誰；備註如果寫的是
  業務描述而非人名(如「真鑽-浪板工程」)，比對不到會員名單就先擱著，不會硬猜。

更新資料：改下面 COMPLETION_FILES 加入新一批完成清單json，或重新匯出2年CSV後改
  CSV_2YEAR/REMARKS_CSV路徑，重跑 python3 build_bni_membership_admin.py 再commit即可。
"""
import csv
import json
import re
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent
CSV_2YEAR = DATA_DIR / "ezpay_invoices_2024-01-01_to_2026-08-17.csv"
REMARKS_CSV = DATA_DIR / "ezpay_invoice_remarks_108taxid_2026-08-17.csv"
COMPLETION_FILES = [
    (DATA_DIR / "ezpay_bni_membership_invoices_2026-08-24_12張完成清單.json", "2026-08-24"),
    (DATA_DIR / "ezpay_bni_renewal_invoices_2026-08-24_6張完成清單.json", "2026-08-24"),
]
NAMECARD_DB = DATA_DIR.parent.parent / "namecard-db" / "namecards.db"
OUT_HTML = DATA_DIR / "bni_membership_admin.html"

REMARK_RE = re.compile(r"^(.+?)(?:分會)?-(.+)$")


def norm(s):
    return (s or "").replace(" ", "").replace("　", "").strip()


def load_remarks():
    """統編 -> (分會, 姓名候選)。姓名候選不保證是人名，後面比對時才驗證。"""
    out = {}
    with open(REMARKS_CSV, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            taxid = r["買受人統編"].strip()
            note = r["發票備註"].strip()
            m = REMARK_RE.match(note)
            if m:
                out[taxid] = (m.group(1).strip(), m.group(2).strip())
    return out


def load_csv_invoices(remarks):
    records = []
    with open(CSV_2YEAR, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            taxid = r["買受人統編"].strip()
            buyer = r["買受人名稱"].strip()
            amount_str = r["發票金額"].replace("$", "").replace("TWD", "").replace(",", "").strip()
            try:
                amount = int(amount_str)
            except ValueError:
                amount = None
            name, chapter = None, None
            if taxid == "-":
                name = buyer
            else:
                hint = remarks.get(taxid)
                if hint:
                    chapter, name = hint
            records.append({
                "date": r["開立日期"].strip(), "invoice_no": r["發票號碼"].strip(),
                "amount": amount, "name": name, "chapter": chapter,
                "buyer": buyer, "taxid_or_carrier": taxid, "item": None,
            })
    return records


def load_completion_records():
    records = []
    for path, batch_date in COMPLETION_FILES:
        data = json.load(open(path, encoding="utf-8"))
        for d in data:
            records.append({
                "date": batch_date, "invoice_no": d.get("invoice_number"),
                "amount": d.get("amount"), "name": d.get("name"), "chapter": None,
                "buyer": d.get("buyer"), "taxid_or_carrier": d.get("ubn") or d.get("carrier") or "-",
                "item": d.get("item"),
            })
    return records


def load_phone_email(names):
    """姓名(去空格) -> (電話, email)。cards表對同一人常有多筆重複掃描紀錄，
    用子查詢取任一筆即可(電話/Email實測一致)，不用JOIN避免笛卡兒積。"""
    out = {}
    if not NAMECARD_DB.exists():
        return out
    conn = sqlite3.connect(NAMECARD_DB)
    conn.row_factory = sqlite3.Row
    for n in names:
        row = conn.execute(
            "SELECT mobile, email FROM cards WHERE REPLACE(name,' ','') = ? "
            "ORDER BY (bni_status='bni_member') DESC, id LIMIT 1",
            (n,),
        ).fetchone()
        if row:
            out[n] = (row["mobile"] or "", row["email"] or "")
    conn.close()
    return out


def build():
    remarks = load_remarks()
    all_records = load_csv_invoices(remarks) + load_completion_records()

    by_name = {}
    unresolved = []
    for rec in all_records:
        if not rec["name"]:
            unresolved.append(rec)
            continue
        key = norm(rec["name"])
        by_name.setdefault(key, {"display_name": rec["name"], "chapter": rec["chapter"], "invoices": []})
        if rec["chapter"] and not by_name[key]["chapter"]:
            by_name[key]["chapter"] = rec["chapter"]
        by_name[key]["invoices"].append(rec)

    phone_email = load_phone_email(by_name.keys())

    people = []
    for key, info in by_name.items():
        invoices = sorted(info["invoices"], key=lambda r: r["date"], reverse=True)
        phone, email = phone_email.get(key, ("", ""))
        people.append({
            "name": info["display_name"], "chapter": info["chapter"] or "未知",
            "phone": phone, "email": email, "invoices": invoices,
            "latest": invoices[0], "count": len(invoices),
        })
    people.sort(key=lambda p: p["latest"]["date"], reverse=True)

    total_people = len(people)
    with_phone = sum(1 for p in people if p["phone"] or p["email"])
    total_invoices = len(all_records)
    unresolved_count = len(unresolved)

    rows_html = []
    for i, p in enumerate(people, 1):
        latest = p["latest"]
        history_html = "<br>".join(
            f'{inv["date"]} {inv.get("item") or ""} ${inv["amount"]:,} ({inv["invoice_no"]})' if inv["amount"] else
            f'{inv["date"]} {inv.get("item") or ""} ({inv["invoice_no"]})'
            for inv in p["invoices"]
        )
        contact = "<br>".join(x for x in [p["phone"], p["email"]] if x) or '<span class="missing">⚠️待補</span>'
        amount_disp = f'${latest["amount"]:,}' if latest["amount"] else "-"
        rows_html.append(
            f'<tr class="data-row" data-name="{p["name"]}" data-chapter="{p["chapter"]}">'
            f'<td class="rank">{i}</td>'
            f'<td class="name">{p["name"]}</td>'
            f'<td class="chapter">{p["chapter"]}</td>'
            f'<td class="phonecell">{contact}</td>'
            f'<td class="total-score">{amount_disp}</td>'
            f'<td class="invcell">{history_html}</td>'
            f'<td class="countcell">{p["count"]}筆</td>'
            f'</tr>'
        )

    unresolved_html = "".join(
        f'<li>{r["date"]} {r["buyer"]}（統編{r["taxid_or_carrier"]}）${r["amount"]:,} 發票{r["invoice_no"]} '
        f'—— 備註未能對應到具體會員姓名，需人工核對</li>'
        for r in unresolved if r["amount"]
    )

    html = TEMPLATE.format(
        total_people=total_people, total_invoices=total_invoices,
        with_phone=with_phone, unresolved_count=unresolved_count,
        rows_html="\n".join(rows_html), unresolved_html=unresolved_html or "<li>（無）</li>",
    )
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"寫入 {OUT_HTML}：{total_people} 位會員、{total_invoices} 筆發票紀錄、"
          f"{unresolved_count} 筆無法比對姓名")


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>【內部後台/勿外流】BNI入會續約發票查詢表</title>
<style>
:root {{
    --bg-color: #0b0f19; --panel-bg: #1a2333; --text-main: #e2e8f0; --text-muted: #64748b;
    --neon-blue: #00f0ff; --neon-green: #10b981; --neon-red: #ff2a2a; --neon-gold: #f59e0b;
}}
body {{ background: var(--bg-color); color: var(--text-main); font-family: 'Helvetica Neue','PingFang TC','Microsoft JhengHei',sans-serif;
    margin: 0; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; }}
.warn-banner {{ width: 100%; max-width: 1200px; background: #3a1414; border: 1px solid var(--neon-red); color: #ffb4b4;
    border-radius: 8px; padding: 10px 18px; margin-bottom: 20px; font-size: .88rem; text-align: center; }}
.header-container {{ text-align: center; margin-bottom: 28px; }}
h1 {{ color: var(--neon-blue); font-size: 2rem; letter-spacing: 2px; margin: 0; text-shadow: 0 0 15px rgba(0,240,255,.5); }}
p.subtitle {{ color: var(--text-muted); font-size: 1rem; margin-top: 10px; }}
.stats-row {{ display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; width: 100%; max-width: 1200px; margin-bottom: 24px; }}
.stat-card {{ background: var(--panel-bg); border: 1px solid #2d3748; border-radius: 10px; padding: 16px 22px; min-width: 150px; text-align: center; }}
.stat-card .num {{ font-size: 1.6rem; font-weight: bold; color: var(--neon-blue); }}
.stat-card .num.gold {{ color: var(--neon-gold); }}
.stat-card .num.red {{ color: var(--neon-red); }}
.stat-card .lbl {{ font-size: .78rem; color: var(--text-muted); margin-top: 4px; }}
.controls {{ width: 100%; max-width: 1200px; display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }}
.controls input[type=text] {{ flex: 1; min-width: 200px; background: var(--panel-bg); border: 1px solid #2d3748;
    color: var(--text-main); padding: 10px 14px; border-radius: 8px; font-size: 1rem; }}
.table-wrapper {{ width: 100%; max-width: 1200px; background: var(--panel-bg); border-radius: 12px;
    overflow-x: auto; border: 1px solid #2d3748; }}
table {{ width: 100%; border-collapse: collapse; text-align: center; min-width: 1100px; }}
thead {{ background: #0f172a; border-bottom: 2px solid var(--neon-blue); }}
th {{ padding: 12px 8px; color: var(--neon-blue); font-weight: 600; white-space: nowrap; font-size: .82rem; }}
td {{ padding: 10px 8px; border-bottom: 1px solid #2d3748; font-size: .88rem; }}
tbody tr:hover {{ background: rgba(0,240,255,.05); }}
.rank {{ color: #94a3b8; font-weight: bold; }}
.name {{ font-weight: bold; color: #fff; text-align: left; padding-left: 14px; white-space: nowrap; }}
.chapter {{ color: #94a3b8; font-size: .82rem; }}
.total-score {{ color: var(--neon-gold); font-weight: bold; white-space: nowrap; }}
.phonecell, .invcell {{ font-size: .78rem; line-height: 1.5; text-align: left; }}
.countcell {{ color: var(--text-muted); font-size: .8rem; }}
.missing {{ color: var(--neon-red); font-size: .75rem; }}
.note-panel {{ width: 100%; max-width: 1200px; margin-top: 32px; background: #1a2333; border-radius: 12px;
    border: 1px solid #2d3748; padding: 24px 30px; box-sizing: border-box; }}
.note-panel h2 {{ color: var(--neon-gold); font-size: 1rem; margin: 0 0 14px 0; border-bottom: 1px dashed #475569; padding-bottom: 10px; }}
.note-panel ul {{ color: #e2e8f0; line-height: 1.9; margin: 0; padding-left: 22px; font-size: .85rem; }}
</style>
</head>
<body>
<div class="warn-banner">⚠️ 內部後台，含會員統編/個人載具/email/電話等個資，僅供教練開發票查用，不要外傳或公開連結</div>
<div class="header-container">
    <h1>BNI入會續約發票查詢表</h1>
    <p class="subtitle">姓名 → 電話/Email/歷史入會續約發票比對　私有版，跟培訓費是完全獨立的系統</p>
</div>
<div class="stats-row">
    <div class="stat-card"><div class="num">{total_people}</div><div class="lbl">已比對到姓名的會員數</div></div>
    <div class="stat-card"><div class="num gold">{total_invoices}</div><div class="lbl">2年歷史發票總筆數</div></div>
    <div class="stat-card"><div class="num">{with_phone}</div><div class="lbl">已有電話/Email</div></div>
    <div class="stat-card"><div class="num red">{unresolved_count}</div><div class="lbl">⚠️備註未能比對到姓名</div></div>
</div>
<div class="controls">
    <input type="text" id="searchBox" placeholder="搜尋姓名...">
</div>
<div class="table-wrapper">
<table>
<thead><tr>
    <th>排名</th><th style="text-align:left;padding-left:14px;">姓名</th><th>分會</th>
    <th>電話/Email</th><th>最近一筆金額</th><th>歷史發票明細</th><th>筆數</th>
</tr></thead>
<tbody id="tbody">
{rows_html}
</tbody>
</table>
</div>
<div class="note-panel">
<h2>📋 使用說明</h2>
<ul>
<li>這是給教練開ezPay入會/續約發票前查用的內部頁面，來源是聚寶盆(店代337391376)2年完整發票匯出(238筆) + 108個統編備註對照 + 2026-08-24最新一批18張完成清單。</li>
<li>「分會」欄若顯示「未知」，代表這筆是個人發票(買受人統編為"-")，remarks對照表裡沒有這個人的分會紀錄，僅供參考，不影響開票判斷。</li>
<li>跟培訓費查詢表(bni_training_admin.html)是完全獨立的兩套系統，教練2026-09-03已明確裁示不互相比對，這裡不會出現培訓費的$300~$1800小額發票。</li>
<li>下方是備註寫的是業務描述而非人名、無法自動比對到具體會員的公司發票，需要人工核對：</li>
<ul>{unresolved_html}</ul>
</ul>
</div>
<script>
const searchBox = document.getElementById('searchBox');
const rows = Array.from(document.querySelectorAll('.data-row'));
searchBox.addEventListener('input', () => {{
    const q = searchBox.value.trim();
    rows.forEach(r => {{
        r.style.display = (!q || r.dataset.name.includes(q)) ? '' : 'none';
    }});
}});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
