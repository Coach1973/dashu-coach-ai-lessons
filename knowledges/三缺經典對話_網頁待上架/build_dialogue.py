import html, re, sys
SRC = "/Users/bymyway/github_repos/bni-chapters/docs/classic_dialogue_three_lacks_2026-10-06.md"
OUT = sys.argv[1]
lines = open(SRC, encoding="utf-8").read().split("\n")

def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

out = []
title = lines[0].lstrip("# ").strip()
i = 1
section_open = False
para_buf = []
item_buf = None
in_table = False
table_rows = []

def flush_para():
    global para_buf
    if para_buf:
        out.append('<p class="verbatim">' + "<br>".join(inline(x) for x in para_buf) + "</p>")
        para_buf = []

def flush_item():
    global item_buf
    if item_buf:
        out.append('<p class="verbatim item">' + "<br>".join(inline(x) for x in item_buf) + "</p>")
        item_buf = None

def flush_table():
    global table_rows
    if table_rows:
        head, body = table_rows[0], table_rows[2:]
        t = '<div class="tbl"><table><thead><tr>' + "".join(f"<th>{inline(c.strip())}</th>" for c in head.strip("|").split("|")) + "</tr></thead><tbody>"
        for r in body:
            t += "<tr>" + "".join(f"<td>{inline(c.strip())}</td>" for c in r.strip("|").split("|")) + "</tr>"
        out.append(t + "</tbody></table></div>")
        table_rows = []

quote_buf = []
def flush_quote():
    global quote_buf
    if not quote_buf:
        return
    body = []
    lst = []
    for q in quote_buf:
        if q.startswith("- "):
            lst.append(q[2:])
        else:
            if lst:
                body.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ul>"); lst = []
            if q.strip():
                body.append(f"<p>{inline(q)}</p>")
    if lst:
        body.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ul>")
    out.append('<aside class="note"><span class="tag">雲端軍師註（非教練原話）</span>' + "".join(body) + "</aside>")
    quote_buf = []

for ln in lines[1:]:
    s = ln.rstrip()
    if s.startswith(">"):
        flush_para(); flush_item(); flush_table()
        quote_buf.append(s[1:].lstrip())
        continue
    flush_quote()
    if s.startswith("|"):
        flush_para(); flush_item()
        table_rows.append(s); continue
    flush_table()
    if s.startswith("## "):
        flush_para(); flush_item()
        out.append(f"<h2>{inline(s[3:])}</h2>")
        continue
    if re.match(r"^\d+\. ", s):
        flush_para(); flush_item()
        item_buf = [re.sub(r"^\d+\. ", "", s)]
        continue
    if s == "":
        flush_para(); flush_item()
        continue
    if item_buf is not None:
        item_buf.append(s); continue
    para_buf.append(s)

flush_para(); flush_item(); flush_quote(); flush_table()

# 檔頭（雲端寫給教練看的說明）與結尾表格都保留
doc = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>大樹教練與雲端克勞德軍師｜經典對話：商務市場最缺三件事</title>
<style>
body{{margin:0;background:#f4f1ea;color:#222;font-family:-apple-system,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;line-height:1.85;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:22px 16px 70px}}
h1{{font-size:26px;line-height:1.4;margin:8px 0 6px}}
h2{{font-size:21px;margin:40px 0 12px;padding-bottom:6px;border-bottom:2px solid #2f6b4f;color:#2f6b4f}}
.intro{{font-size:15px;color:#555;background:#fff;border-left:5px solid #2f6b4f;padding:12px 16px;border-radius:6px}}
.intro p{{margin:6px 0}}
.verbatim{{background:#fff;border-radius:10px;padding:16px 18px;margin:14px 0;font-size:18px;box-shadow:0 1px 4px rgba(0,0,0,.08);white-space:normal}}
.verbatim.item{{margin-left:6px}}
.note{{font-size:15px;color:#4a3a22;background:#fbf3e3;border-radius:8px;padding:12px 16px;margin:16px 0;border-left:4px solid #b5651d}}
.note p,.note ul{{margin:6px 0}}
.note .tag{{display:inline-block;font-size:13px;color:#8a5a1a;font-weight:700;margin-bottom:4px}}
.tbl{{overflow-x:auto;margin:14px 0}}
table{{border-collapse:collapse;width:100%;font-size:15px;background:#fff}}
th,td{{border:1px solid #ddd;padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:#e9f0eb}}
.foot{{font-size:13px;color:#777;margin-top:44px;border-top:1px dashed #bbb;padding-top:12px}}
</style></head>
<body><div class="wrap">
<h1>{inline(title)}</h1>
<div class="intro">
{"".join("<p>" + inline(x.lstrip("> ").rstrip()) + "</p>" for x in lines[2:9] if x.startswith(">") and x.strip(">").strip())}
</div>
{chr(10).join(out)}
<p class="foot">教練原話逐字保留（含語音輸入的口語與標點）；雲端軍師註另以淡黃底標示，不是教練說的話。數字為教練口述，尚未查證。</p>
</div></body></html>
"""
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, len(doc))
