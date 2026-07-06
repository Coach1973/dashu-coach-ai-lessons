#!/usr/bin/env python3
"""產生大樹教練GitHub作品一頁式總覽頁（純資料轉HTML，不需要深度判斷）"""
import json
from pathlib import Path
from datetime import datetime

# 教練親口確認：只要「有意義命名」的真實創作，4/6同一天建立的netlify測試批次不算
PROJECTS = [
    {"name": "bigtree", "url": "https://coach1973.github.io/bigtree/", "title": "2026/7/1 創業×政府×AI主題講座", "updated": "2026-07-06"},
    {"name": "jiesheng-leadership", "url": "https://coach1973.github.io/jiesheng-leadership/", "title": "結繩領導學｜現場座談會×實體工作坊", "updated": "2026-07-05"},
    {"name": "cool-case", "url": "https://coach1973.github.io/cool-case/", "title": "頂級特助的心法實踐（AI特助案例庫）", "updated": "2026-07-01"},
    {"name": "consultant", "url": "https://coach1973.github.io/consultant/", "title": "創業路上的坑，她替你踩過了（謝扉榆講座）", "updated": "2026-06-25"},
    {"name": "ai-go", "url": "https://coach1973.github.io/ai-go/", "title": "大樹教練AI特助心法—一鍵注入任何AI", "updated": "2026-06-23"},
    {"name": "government-grow", "url": "https://coach1973.github.io/government-grow/", "title": "中小微企業多元發展貸款說明會（台南場）", "updated": "2026-06-20"},
    {"name": "government-subsidies", "url": "https://coach1973.github.io/government-subsidies/", "title": "中小微企業多元發展實戰說明會（經濟部）", "updated": "2026-06-20"},
    {"name": "tainan-calender", "url": "https://coach1973.github.io/tainan-calender/", "title": "2026全年度行事曆", "updated": "2026-06-20"},
    {"name": "bni-dna", "url": "https://coach1973.github.io/bni-dna/", "title": "大台南南區DnA團隊戰情儀表板", "updated": "2026-06-18"},
    {"name": "gold-excellence", "url": "https://coach1973.github.io/gold-excellence/", "title": "好同學暨好夥伴專屬聚會｜金卓獎2026（已推Netlify：gold-excellence.netlify.app）", "updated": "2026-06-17"},
    {"name": "northern411", "url": "https://coach1973.github.io/northern411/", "title": "智匯健康｜失智防治與逆齡醫學論壇", "updated": "2026-06-17"},
    {"name": "bymyway-website", "url": "https://coach1973.github.io/bymyway-website/", "title": "大樹教練 吳大樹｜有效溝通就是無價之寶（正式網域：bymyway.com）", "updated": "2026-06-17"},
    {"name": "theunrestrictedwar", "url": "https://coach1973.github.io/theunrestrictedwar/", "title": "超限戰 The Unrestricted War 電影站", "updated": "2026-06-17"},
    {"name": "vip-club", "url": "https://coach1973.github.io/vip-club/", "title": "頂級特助俱樂部・特助心法（教練詮釋版）", "updated": "2026-05-28"},
    {"name": "coach-vip-club", "url": "https://coach1973.github.io/coach-vip-club/", "title": "頂級特助俱樂部・特助心法（純淨版）", "updated": "2026-05-28"},
    {"name": "coach-case4", "url": "https://coach1973.github.io/coach-case4/", "title": "特助心法實踐故事第四部", "updated": "2026-05-27"},
    {"name": "coach-case3", "url": "https://coach1973.github.io/coach-case3/", "title": "特助守則實踐故事第三部", "updated": "2026-05-26"},
    {"name": "coach-case2", "url": "https://coach1973.github.io/coach-case2/", "title": "特助守則實踐故事（AI特助成長記錄）", "updated": "2026-05-26"},
    {"name": "coach-case", "url": "https://coach1973.github.io/coach-case/", "title": "特助心法實踐演示", "updated": "2026-05-26"},
]

PROJECTS.sort(key=lambda p: p["updated"], reverse=True)

cards_html = "\n".join(f"""
      <a class="card" href="{p['url']}" target="_blank" rel="noopener">
        <div class="card-date">最後更新 {p['updated']}</div>
        <div class="card-title">{p['title']}</div>
        <div class="card-url">{p['url']}</div>
      </a>""" for p in PROJECTS)

html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大樹教練 · GitHub 作品總覽</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 40px 20px;
    font-family: -apple-system, "PingFang TC", "Noto Sans TC", sans-serif;
    background: #f5f5f2; color: #1a1a1a;
  }}
  h1 {{ text-align: center; font-size: 28px; margin-bottom: 6px; }}
  .subtitle {{ text-align: center; color: #777; margin-bottom: 36px; font-size: 14px; }}
  .grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 18px; max-width: 1200px; margin: 0 auto;
  }}
  .card {{
    display: block; background: #fff; border-radius: 12px; padding: 18px 20px;
    text-decoration: none; color: inherit; border: 1px solid #e5e5e0;
    transition: transform .15s, box-shadow .15s;
  }}
  .card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,.08); }}
  .card-date {{ font-size: 12px; color: #999; margin-bottom: 8px; }}
  .card-title {{ font-size: 16px; font-weight: 600; line-height: 1.5; margin-bottom: 10px; }}
  .card-url {{ font-size: 12px; color: #2563eb; word-break: break-all; }}
  footer {{ text-align: center; margin-top: 40px; font-size: 12px; color: #aaa; }}
</style>
</head>
<body>
  <h1>大樹教練 · GitHub 作品總覽</h1>
  <div class="subtitle">共 {len(PROJECTS)} 個正式創作 · 產生時間 {datetime.now().strftime('%Y-%m-%d')}</div>
  <div class="grid">{cards_html}
  </div>
  <footer>資料來源：gh repo list Coach1973（GitHub官方API）· 已排除4/6批次netlify測試專案</footer>
</body>
</html>
"""

out_path = Path(__file__).resolve().parent.parent / "作品總覽.html"
out_path.write_text(html, encoding="utf-8")
print(f"已產生：{out_path}")
print(f"共 {len(PROJECTS)} 個作品卡片")
