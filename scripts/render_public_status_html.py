#!/usr/bin/env python3
"""
把 status.md 轉成 status.html，讓其他家 AI（ChatGPT/Gemini/Grok...）也讀得到。

真因（2026-09-25 curl 實測查證，不是猜的）：GitHub Pages 對 .md 副檔名的檔案回傳
content-type: text/markdown；同目錄的 index.html 回傳 text/html。人爬蟲(GPTBot等)測試
都是 HTTP 200，不是被 robots.txt 或 Cloudflare 擋——是多數 AI 內建的「讀網頁」工具只
認得 text/html，看到 text/markdown 就回報「讀不到/被封鎖」。

設計：status.md 仍是唯一的手改來源（教練/AI 改這份），這支程式只負責轉換，
每次 publish_public_status.sh 執行時自動重跑，不用雙邊手動維護、不會分岔。
內容整段印進 HTML 原始碼（不靠 JS 才顯示），沒有瀏覽器 JS 引擎的爬蟲/AI 一樣讀得到。
"""
import re
import sys
import html
import markdown

SRC = sys.argv[1] if len(sys.argv) > 1 else "status.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else "status.html"

md_text = open(SRC, encoding="utf-8").read()

# 第一個 H1 當標題與 <title>，其餘全文轉 HTML
lines = md_text.splitlines()
title = "大樹教練工作交接棒"
if lines and lines[0].startswith("# "):
    title = lines[0][2:].strip()

body_html = markdown.markdown(
    md_text,
    extensions=["extra", "sane_lists"],
)
# 純文字網址(沒寫成 [文字](網址) 格式的)也轉成可點連結，方便人眼閱讀；
# 已經在 <a href="...">、href屬性、或標籤內的不重複處理
body_html = re.sub(
    r'(?<!href=")(?<!">)(https?://[^\s<>"]+[^\s<>".,;:)])',
    r'<a href="\1">\1</a>',
    body_html,
)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="貼這個網址給任何 AI，它立刻接手大樹教練目前的工作狀態。">
<style>
:root {{
  --bg: #FFFBF5; --bg-warm: #FFF8EC; --bg-deep: #FFF3DC;
  --surface: #FFFFFF; --border: #F0E4D0; --border-strong: #E0D0B0;
  --primary: #D4692A; --primary-dark: #A84820;
  --green: #4A8B70; --green-dark: #2F6B52;
  --text: #3D2B1F; --text-dim: #7A6A5A; --text-muted: #A89880;
  --shadow-sm: 0 2px 8px rgba(61,43,31,0.06);
  --shadow-md: 0 8px 24px rgba(61,43,31,0.12);
}}
* {{ box-sizing: border-box; }}
body {{
  background: var(--bg); color: var(--text); margin: 0;
  font-family: 'Noto Sans TC','Microsoft JhengHei UI',-apple-system,sans-serif;
  line-height: 1.8; font-size: 17px; font-weight: 450;
}}
.wrap {{ max-width: 760px; margin: 0 auto; padding: 40px 20px 80px; }}
.banner {{
  background: linear-gradient(135deg, var(--green) 0%, var(--green-dark) 100%);
  color: #fff; border-radius: 16px; padding: 20px 24px; margin-bottom: 28px;
  font-size: 15px; box-shadow: var(--shadow-md);
}}
.banner b {{ font-size: 17px; }}
.card {{
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 32px 36px; box-shadow: var(--shadow-sm);
}}
h1 {{ color: var(--primary-dark); font-size: 26px; margin: 0 0 8px; line-height: 1.4; }}
h2 {{ color: var(--green-dark); font-size: 20px; margin: 34px 0 14px; border-bottom: 2px solid var(--border); padding-bottom: 8px; }}
h3 {{ color: var(--text); font-size: 17px; margin: 22px 0 10px; }}
p {{ margin: 0 0 14px; }}
blockquote {{
  background: var(--bg-warm); border-left: 4px solid var(--primary);
  margin: 0 0 14px; padding: 10px 18px; border-radius: 0 8px 8px 0; color: var(--text-dim);
}}
blockquote p {{ margin: 0; }}
code {{ background: var(--bg-deep); padding: 2px 6px; border-radius: 4px; font-family: 'SF Mono',Menlo,monospace; font-size: 0.9em; }}
a {{ color: var(--primary); font-weight: 600; }}
ul, ol {{ padding-left: 22px; margin: 0 0 14px; }}
li {{ margin-bottom: 6px; }}
table {{ width: 100%; border-collapse: collapse; margin: 0 0 18px; font-size: 15px; }}
th, td {{ border: 1px solid var(--border); padding: 8px 12px; text-align: left; }}
th {{ background: var(--bg-warm); color: var(--green-dark); }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 28px 0; }}
.footer {{ text-align: center; color: var(--text-muted); font-size: 13px; margin-top: 32px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="banner">
    <b>🌳 大樹教練公開工作交接棒</b>｜貼這個網址給任何 AI，讀完就掌握目前工作狀態。
  </div>
  <div class="card">
{body}
  </div>
  <div class="footer">
    純文字版（給不能讀 HTML 的工具）：<a href="status.md">status.md</a>
    ・方法論原文：<a href="system-prompt.md">system-prompt.md</a>
  </div>
</div>
</body>
</html>
"""

out = TEMPLATE.format(title=html.escape(title), body=body_html)
open(OUT, "w", encoding="utf-8").write(out)
print(f"✅ 已產生 {OUT}（{len(out)} bytes）")
