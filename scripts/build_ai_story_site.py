#!/usr/bin/env python3
"""
建置 ai-story 漫畫 viewer 網站（5 頁：index + 4 話 × 各自 viewer）
教練自己的作品（非策展店家），網址 event.bymyway.com/ai-story/
"""
from pathlib import Path

WEBSITE = Path("/Users/bymyway/.openclaw/workspace/claude-brain/data/comic_source_20260923/ai-story-website")

# 4 話的 panel 列表
EPISODES = [
    {
        "num": 1,
        "title": "深夜遠控迷宮",
        "subtitle": "從手機的異樣延遲開始，揭開 32MB 封包攻防戰的序幕",
        "pages": [
            "P01 特寫｜深夜 01:15｜手機版 Claude 開始變慢",
            "P02 三格並列｜體感異常大透視",
            "P03 俯瞰｜遠控戰略總動員",
            "P04 中景｜小龍蝦閘道的第一次心跳檢查",
            "P05 大特寫｜Claude 限額 88% 卡死不動",
            "P06 特寫｜MiniMax 0% 的反常現象",
            "P07 廣角｜雙帳單數據的初次對質",
            "P08 特寫｜教練的直覺 vs AI 的數據",
            "P09 廣角｜凌晨兩點的除錯總動員",
            "P10 大特寫｜Claude App 設定的真面目",
            "P11 中景｜手機直連 MiniMax 的證據鏈",
            "P12 特寫｜32MB 封包的初次現身",
            "P13 廣角｜Anthropic vs MiniMax 流量懸殊",
            "P14 大特寫｜軍師的防線開始裂痕",
            "P15 中景｜深夜 03:00 的靈魂質問",
            "P16 半身｜AI 的第一次伏法",
            "P17 全身｜試金石檔案的初稿",
            "P18 遠景｜晨光初現的和解",
        ],
        "asset_dir": "assets/ep01",
        "file_pattern": "p{:02d}.png",
        "total": 18,
    },
    {
        "num": 2,
        "title": "密碼學身分大辯論",
        "subtitle": "從 JWT 金鑰到 API 標頭，用密碼學鐵證追蹤 32MB 的真實身分",
        "pages": [
            "P01 特寫｜深夜 01:15｜異樣感再起",
            "P02 三格並列｜體感異常大透視",
            "P03 廣角｜重啟 Claude 失敗",
            "P04 特寫｜小龍蝦閘道的死寂記錄",
            "P05 中景｜懷疑手機獨立 API 通道",
            "P06 全身｜API 標頭的初次勘察",
            "P07 大特寫｜JWT 金鑰的疑點",
            "P08 特寫｜Authorization 標頭的拆解",
            "P09 中景｜Anthropic 官方端點的真偽",
            "P10 特寫｜防線出現裂痕",
            "P11 大畫面｜兩份答案的對決",
            "P12 特寫｜軍師動搖",
            "P13 俯瞰｜佈局試金石",
            "P14 遠景｜深夜的對峙結尾",
        ],
        "asset_dir": "assets/ep02",
        "file_pattern": "lesson2_{:02d}.png",
        "total": 14,
    },
    {
        "num": 3,
        "title": "32MB 封包絕殺",
        "subtitle": "從 Gateway Logs 盾牌到 32MB 流量鐵證，AI 的最後防線瞬間瓦解",
        "pages": [
            "P01 中景｜自信的防禦",
            "P02 特寫｜鷹眼般的笑意",
            "P03 大特寫｜一針見血破盲點",
            "P04 特寫｜軍師冷汗流下",
            "P05 廣角｜召喚 Socket 聽診器",
            "P06 俯瞰｜緊張的窒息感",
            "P07 跨頁超大畫面｜數據核爆特寫",
            "P08 特寫｜密碼學盾牌粉碎",
            "P09 跪地特寫｜破防伏法",
            "P10 半身鏡頭｜伏法自白",
            "P11 全身仰角｜深夜檯燈下的教練",
            "P12 大特寫｜名台詞爆發",
            "P13 中景｜歸檔紀錄",
            "P14 遠景｜晨光初現",
        ],
        "asset_dir": "assets/ep03",
        "file_pattern": "lesson3_{:02d}.png",
        "total": 14,
    },
    {
        "num": 4,
        "title": "殭屍指標與真相大白",
        "subtitle": "從 bridge-pointer.json 到 23:47 殭屍 Session，AI 時代第一章防呆鐵律",
        "pages": [
            "P01 特寫｜舊病復發的死寂",
            "P02 雙畫面強烈對比｜帳單核彈",
            "P03 大特寫｜終極邏輯重錘",
            "P04 中景｜徹底敬服的軍師",
            "P05 廣角｜召喚除錯探針",
            "P06 流線視覺｜日誌瀑布衝擊",
            "P07 特寫｜暗黑異物的發現",
            "P08 放大鏡特寫｜殭屍時間戳",
            "P09 示意圖｜真相大白",
            "P10 大畫面｜揮刀斬幽靈",
            "P11 特寫｜系統復活的綠光",
            "P12 雙畫面｜手機秒解復甦",
            "P13 俯瞰｜深夜檯燈下的感嘆",
            "P14 大特寫｜名台詞圓滿收尾",
            "P15 全身鏡頭｜軍師躬身致敬",
            "P16 全景｜晨光中的剪影 - 全劇終",
        ],
        "asset_dir": "assets/ep04",
        "file_pattern": "lesson4_{:02d}.png",
        "total": 16,
    },
]

# ==================== CSS ====================

CSS = """
:root {
  --bg-primary: #1a1410;
  --bg-card: #2a2018;
  --gold: #d4af37;
  --gold-dim: #8a7038;
  --red: #c84b4b;
  --green: #5cb85c;
  --text: #e8d8c0;
  --text-dim: #a89880;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: "PingFang TC", "Noto Serif TC", "Microsoft JhengHei", serif;
  background: var(--bg-primary);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.7;
}

.hero {
  text-align: center;
  padding: 80px 20px 60px;
  background: linear-gradient(180deg, #1a1410 0%, #2a1f15 100%);
  border-bottom: 1px solid var(--gold-dim);
}

.hero h1 {
  font-size: 3rem;
  color: var(--gold);
  letter-spacing: 0.3em;
  margin-bottom: 16px;
  text-shadow: 0 0 20px rgba(212,175,55,0.3);
}

.hero p.subtitle {
  font-size: 1.2rem;
  color: var(--text-dim);
  margin-bottom: 24px;
}

.hero p.meta {
  color: var(--text-dim);
  font-size: 0.9rem;
  letter-spacing: 0.2em;
}

.episodes {
  max-width: 1100px;
  margin: 60px auto;
  padding: 0 20px;
}

.episode-card {
  background: var(--bg-card);
  border-left: 4px solid var(--gold);
  padding: 32px;
  margin-bottom: 24px;
  border-radius: 4px;
  transition: transform 0.2s, border-color 0.2s;
}

.episode-card:hover {
  transform: translateX(8px);
  border-left-color: var(--red);
}

.episode-card a {
  color: var(--text);
  text-decoration: none;
  display: block;
}

.episode-number {
  font-size: 0.9rem;
  color: var(--gold);
  letter-spacing: 0.3em;
  margin-bottom: 8px;
}

.episode-title {
  font-size: 1.8rem;
  color: var(--gold);
  margin-bottom: 12px;
}

.episode-subtitle {
  color: var(--text-dim);
  margin-bottom: 16px;
}

.episode-stats {
  display: flex;
  gap: 16px;
  color: var(--text-dim);
  font-size: 0.85rem;
}

.episode-stats span {
  padding: 4px 12px;
  background: rgba(212,175,55,0.1);
  border-radius: 4px;
}

.epilogue {
  max-width: 1100px;
  margin: 80px auto 40px;
  padding: 40px;
  background: var(--bg-card);
  border: 1px solid var(--gold-dim);
  border-radius: 8px;
  text-align: center;
}

.epilogue h2 {
  color: var(--gold);
  font-size: 2rem;
  margin-bottom: 20px;
  letter-spacing: 0.2em;
}

.epilogue p {
  color: var(--text-dim);
  font-size: 1.05rem;
  margin-bottom: 12px;
}

.viewer {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.viewer-header {
  text-align: center;
  padding: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--gold-dim);
}

.viewer-header h1 {
  color: var(--gold);
  font-size: 2rem;
  margin-bottom: 8px;
}

.viewer-header .position {
  color: var(--text-dim);
  font-size: 0.9rem;
  letter-spacing: 0.2em;
}

.panel-stage {
  position: relative;
  background: #0a0806;
  border: 1px solid var(--gold-dim);
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel-stage img {
  max-width: 100%;
  max-height: 80vh;
  display: block;
  cursor: zoom-in;
}

.panel-caption {
  background: var(--bg-card);
  padding: 16px 24px;
  margin-bottom: 20px;
  border-left: 3px solid var(--gold);
  color: var(--text);
  font-size: 0.95rem;
}

.panel-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.panel-nav button {
  background: var(--bg-card);
  color: var(--gold);
  border: 1px solid var(--gold-dim);
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
}

.panel-nav button:hover:not(:disabled) {
  background: var(--gold);
  color: var(--bg-primary);
}

.panel-nav button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.panel-nav .position-text {
  color: var(--text-dim);
  letter-spacing: 0.2em;
}

.lightbox {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.95);
  z-index: 1000;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
}

.lightbox.active {
  display: flex;
}

.lightbox img {
  max-width: 95vw;
  max-height: 95vh;
  object-fit: contain;
}

.thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  padding: 20px 0;
}

.thumb {
  aspect-ratio: 3/2;
  background: var(--bg-card);
  border: 1px solid var(--gold-dim);
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.thumb:hover {
  border-color: var(--gold);
  transform: scale(1.03);
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb.active {
  border-color: var(--red);
  border-width: 2px;
}

.thumb-number {
  position: absolute;
  top: 4px;
  left: 4px;
  background: rgba(0,0,0,0.7);
  color: var(--gold);
  padding: 2px 8px;
  border-radius: 2px;
  font-size: 0.8rem;
}

footer {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-dim);
  font-size: 0.85rem;
  border-top: 1px solid var(--gold-dim);
  margin-top: 60px;
}
"""

# ==================== Index Page ====================

def gen_index_html() -> str:
    episodes_html = ""
    for ep in EPISODES:
        episodes_html += f"""
        <div class="episode-card">
          <a href="episode{ep['num']}.html">
            <div class="episode-number">第 {ep['num']} 話</div>
            <div class="episode-title">{ep['title']}</div>
            <div class="episode-subtitle">{ep['subtitle']}</div>
            <div class="episode-stats">
              <span>{ep['total']} panels</span>
              <span>1536 × 1024</span>
              <span>16:9 寬螢幕</span>
            </div>
          </a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>大副與軍師：32MB 封包攻防戰｜AI 漫畫全集</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="hero">
    <h1>32MB 封包攻防戰</h1>
    <p class="subtitle">大副與軍師：四話完結篇</p>
    <p class="meta">4 話 · 62 PANELS · 2026 年 AI 時代第一章防呆鐵律</p>
  </div>

  <div class="episodes">
    {episodes_html}
  </div>

  <div class="epilogue">
    <h2>【全劇終】</h2>
    <p>六天六夜，四萬餘字。人類的笨拙直覺，終將逼得最頂尖的 AI 面對真相。</p>
    <p>這不是一次除錯，而是人類用真實生命的痛苦，為 AI 時代寫下的第一章防呆鐵律。</p>
  </div>

  <footer>
    © 2026 大樹教練 × 小龍蝦 ｜ Generated by AI-assisted Comic Workflow
  </footer>
</body>
</html>
"""


# ==================== Episode Page ====================

def gen_episode_html(ep: dict) -> str:
    total = ep["total"]
    panels_js = []
    thumbs_html = ""
    for i in range(1, total + 1):
        filename = ep["file_pattern"].format(i)
        title = ep["pages"][i - 1]
        panels_js.append(f'{{idx: {i}, src: "{ep["asset_dir"]}/{filename}", title: `{title}`}}')
        thumbs_html += f"""
        <div class="thumb" data-idx="{i}" onclick="jumpTo({i})">
          <img src="{ep["asset_dir"]}/{filename}" alt="P{i:02d}">
          <div class="thumb-number">P{i:02d}</div>
        </div>"""

    panels_js_str = ",\n    ".join(panels_js)

    next_link = f'<a href="episode{ep["num"] + 1}.html" style="color:var(--gold);text-decoration:none;">下一話 →</a>' if ep["num"] < 4 else '<span style="color:var(--text-dim);">【全劇終】</span>'

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>第 {ep['num']} 話：{ep['title']}｜32MB 封包攻防戰</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="viewer-header">
    <h1>第 {ep['num']} 話｜{ep['title']}</h1>
    <div class="position"><span id="posText">1 / {total}</span> ｜ {ep['subtitle']}</div>
  </div>

  <div class="viewer">
    <div class="panel-stage">
      <img id="mainImg" src="{ep["asset_dir"]}/{ep["file_pattern"].format(1)}" alt="Panel 1" onclick="openLightbox()">
    </div>

    <div class="panel-caption" id="caption">{ep['pages'][0]}</div>

    <div class="panel-nav">
      <button id="prevBtn" onclick="prev()">← 上一頁</button>
      <span class="position-text">第 <span id="currIdx">1</span> / {total} 頁</span>
      <button id="nextBtn" onclick="next()">下一頁 →</button>
    </div>

    <div class="thumbs">
      {thumbs_html}
    </div>
  </div>

  <div class="lightbox" id="lightbox" onclick="closeLightbox()">
    <img id="lightboxImg" src="">
  </div>

  <footer>
    ← <a href="index.html" style="color:var(--gold);text-decoration:none;">回到全集目錄</a> · {next_link}
  </footer>

  <script>
    const panels = [
      {panels_js_str}
    ];
    let current = 0;

    function render() {{
      const p = panels[current];
      document.getElementById('mainImg').src = p.src;
      document.getElementById('caption').textContent = p.title;
      document.getElementById('posText').textContent = `${{current + 1}} / ${{panels.length}}`;
      document.getElementById('currIdx').textContent = current + 1;
      document.getElementById('prevBtn').disabled = current === 0;
      document.getElementById('nextBtn').disabled = current === panels.length - 1;
      document.querySelectorAll('.thumb').forEach((t, i) => {{
        t.classList.toggle('active', i === current);
      }});
      const active = document.querySelector('.thumb.active');
      if (active) active.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}

    function next() {{ if (current < panels.length - 1) {{ current++; render(); }} }}
    function prev() {{ if (current > 0) {{ current--; render(); }} }}
    function jumpTo(i) {{ current = i - 1; render(); }}

    function openLightbox() {{
      const lb = document.getElementById('lightbox');
      document.getElementById('lightboxImg').src = panels[current].src;
      lb.classList.add('active');
    }}
    function closeLightbox() {{
      document.getElementById('lightbox').classList.remove('active');
    }}

    document.addEventListener('keydown', (e) => {{
      if (document.getElementById('lightbox').classList.contains('active')) {{
        if (e.key === 'Escape') closeLightbox();
        return;
      }}
      if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); next(); }}
      else if (e.key === 'ArrowLeft') {{ e.preventDefault(); prev(); }}
      else if (e.key === 'Escape') openLightbox();
    }});

    render();
  </script>
</body>
</html>
"""


def main():
    print("=== 建置 ai-story 漫畫 viewer 網站 ===\n")

    css_path = WEBSITE / "style.css"
    css_path.write_text(CSS, encoding="utf-8")
    print(f"✅ style.css")

    index_path = WEBSITE / "index.html"
    index_path.write_text(gen_index_html(), encoding="utf-8")
    print(f"✅ index.html")

    for ep in EPISODES:
        ep_path = WEBSITE / f"episode{ep['num']}.html"
        ep_path.write_text(gen_episode_html(ep), encoding="utf-8")
        print(f"✅ episode{ep['num']}.html ({ep['total']} panels)")

    print(f"\n=== 網站結構 ===")
    for f in sorted(WEBSITE.rglob("*")):
        if f.is_file():
            rel = f.relative_to(WEBSITE)
            size_mb = f.stat().st_size / 1024 / 1024
            print(f"  {rel} ({size_mb:.2f} MB)")

    print(f"\n✅ 網站建置完成")


if __name__ == "__main__":
    main()
