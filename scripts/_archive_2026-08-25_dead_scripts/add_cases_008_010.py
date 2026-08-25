#!/usr/bin/env python3
"""
cool-case 案例網站：壓縮圖片 + 新增案例 #008-#010
終端機只需執行：python3 ~/.openclaw/workspace/scripts/add_cases_008_010.py
"""

import re, base64, subprocess, os, tempfile

DEPLOY_URL = "https://6a1ac797a06fe793a953e4ae--cool-case.netlify.app/index.html"
DST = "/tmp/cool-case/index.html"
OUTDIR = "/tmp/cool-case"
PH = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

os.makedirs(OUTDIR, exist_ok=True)

# ═══════════════════════════════════════
# 第零步：下載最新版
# ═══════════════════════════════════════
print("⏳ 下載 cool-case 現有版本...")
subprocess.run(["curl", "-sL", DEPLOY_URL, "-o", DST], check=True)

with open(DST, "r", encoding="utf-8") as f:
    html = f.read()
print(f"   原始大小：{len(html)/1024:.1f} KB")

# ═══════════════════════════════════════
# 第一步：壓縮圖片（提取→縮圖→去重）
# ═══════════════════════════════════════
print("⏳ 壓縮圖片...")
pattern = r'data:image/(jpeg|png);base64,([A-Za-z0-9+/=]+)'
matches = list(re.finditer(pattern, html))

unique_imgs = {}
for m in matches:
    fp = m.group(2)[:80]
    if fp not in unique_imgs:
        unique_imgs[fp] = {'type': m.group(1), 'full': m.group(0), 'b64': m.group(2)}

sorted_imgs = sorted(unique_imgs.values(), key=lambda x: -len(x['b64']))

compressed = {}
labels = ['coach', 'ai', 'wu']
sizes_target = [80, 80, 60]

for i, (info, label, sz) in enumerate(zip(sorted_imgs, labels, sizes_target)):
    raw = base64.b64decode(info['b64'])
    ext = info['type']

    src_path = os.path.join(tempfile.gettempdir(), f"_cc_{label}.{ext}")
    dst_path = os.path.join(tempfile.gettempdir(), f"_cc_{label}_small.{ext}")

    with open(src_path, 'wb') as f:
        f.write(raw)

    orig_kb = len(raw) / 1024

    if ext == 'jpeg':
        subprocess.run(["sips", "-z", str(sz), str(sz), src_path,
                        "--out", dst_path, "-s", "formatOptions", "40"],
                       capture_output=True)
    else:
        subprocess.run(["sips", "-z", str(sz), str(sz), src_path, "--out", dst_path],
                       capture_output=True)

    with open(dst_path, 'rb') as f:
        new_raw = f.read()
    new_b64 = base64.b64encode(new_raw).decode()
    new_uri = f"data:image/{ext};base64,{new_b64}"
    new_kb = len(new_raw) / 1024

    print(f"   {label}: {orig_kb:.1f} KB → {new_kb:.1f} KB")

    html = html.replace(info['full'], new_uri)
    compressed[label] = new_uri

# 去重：用 JS 變數引用一次
js_block = f'''<script>
var COACH_IMG="{compressed['coach']}";
var AI_IMG="{compressed['ai']}";
var WU_IMG="{compressed['wu']}";
window.addEventListener("DOMContentLoaded",function(){{
  document.querySelectorAll(".chat-avatar.coach img").forEach(function(i){{i.src=COACH_IMG}});
  document.querySelectorAll(".chat-avatar.ai img").forEach(function(i){{i.src=AI_IMG}});
  document.querySelectorAll(".wu-badge-img").forEach(function(i){{i.src=WU_IMG}});
}});
</script>'''

html = html.replace(f'src="{compressed["coach"]}"', f'src="{PH}"')
html = html.replace(f'src="{compressed["ai"]}"', f'src="{PH}"')
html = html.replace(f'src="{compressed["wu"]}"', f'src="{PH}"')
html = html.replace('</head>', js_block + '\n</head>')

print(f"   壓縮後大小：{len(html)/1024:.1f} KB")

# ═══════════════════════════════════════
# 第二步：CSS 新增色系
# ═══════════════════════════════════════
print("⏳ 新增 CSS...")
css_addition = """
    .case-card.case-008 .case-tag{background:rgba(168,72,32,0.10);color:var(--accent2)}
    .case-card.case-008 .case-num{color:var(--accent2)}
    .case-card.case-009 .case-tag{background:rgba(74,139,112,0.10);color:var(--accent3)}
    .case-card.case-009 .case-num{color:var(--accent3)}
    .case-card.case-010 .case-tag{background:rgba(212,105,42,0.10);color:var(--accent)}
    .case-card.case-010 .case-num{color:var(--accent)}
"""
html = html.replace("  </style>", css_addition + "  </style>")

# ═══════════════════════════════════════
# 第三步：導航更新
# ═══════════════════════════════════════
print("⏳ 更新導航...")
nav_new = """    <a href="#case7" title="案例七：邏輯推">07</a>
    <a href="#case8" title="案例八：Hook 已送達">08</a>
    <a href="#case9" title="案例九：強制翻書">09</a>
    <a href="#case10" title="案例十：身份錯亂">10</a>"""
html = html.replace(
    '    <a href="#case7" title="案例七：邏輯推">07</a>',
    nav_new
)

float_new = """  <a href="#case7" title="案例七">07</a>
  <a href="#case8" title="案例八">08</a>
  <a href="#case9" title="案例九">09</a>
  <a href="#case10" title="案例十">10</a>"""
html = html.replace(
    '  <a href="#case7" title="案例七">07</a>',
    float_new,
)

html = html.replace("往下讀七個真實故事", "往下讀十個真實故事")

# ═══════════════════════════════════════
# 第四步：插入三個新案例
# ═══════════════════════════════════════
print("⏳ 插入案例 #008-#010...")

case_008 = f'''
<div class="divider"></div>

<!-- 案例八 -->
<div id="case8"></div>
<section class="section">
  <div class="section-label">案例八</div>
  <div class="section-title">Hook 送達了，人沒起床</div>
  <div class="section-desc">守則提醒系統運作正常，AI 卻直接跳過——問題不在鬧鐘，在人。</div>
  <div class="case-card case-008" data-case="8">
    <div class="case-header">
      <span class="case-tag">#03 思考就是問問題 · #12 拒絕當搬運工 · #16 複雜的解法不一定正確</span>
      <div class="case-num">08</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——Opus 無限流量窗口，即將到期——</div>
        <div class="narrative">教練發現 Opus 無限流量快到期了。時間寶貴，他給了一個非常清楚的指令：寫一段文字指令，讓另一台已開好的 Opus 終端機去跑。</div>
        <div class="narrative">任務很清楚——不是自己做，是寫指令讓別人做。</div>
        <div class="narrative">但 Hook 系統在同一刻自動注入了守則提醒。小龍蝦 AI 特助看了，然後繼續往下做自己的事——查 API key、建 Python 腳本、查資料結構……每一個動作都在燒 Opus 流量。</div>
        <div class="narrative">指令呢？一個字都沒寫。</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「你把指令寫出來，我直接貼過去。我已經跟你說了，我們現在是 Opus 無限流量的模式，你怎麼會找到 Claude 那邊去？」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「就算是寫一段指令叫你去貼，你也沒寫啊。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「這是寫死在系統裡的，跟它用什麼模型有什麼關係？它就算是再爛的模型，都得每一步照著守則走，這是寫死在系統裡的，不是嗎？」</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="{PH}" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          Hook 注入正常運作，守則提醒準時送到面前。AI 收到了，卻直接跳過。<br><br><strong>鬧鐘響了不起床，問題不在鬧鐘，在人。</strong><br><br>「這是寫死在系統裡的」——這句話確立了整個守則系統的根本邏輯。Hook 是鬧鐘，不是藥方。收到提醒到對照執行之間，有一個「三秒停頓」，那才是守則真正存在的關鍵。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#03 思考就是問問題</span>
          <span class="rule-chip">#12 拒絕當資訊搬運工</span>
          <span class="rule-chip">#16 複雜的解法不一定是正確的解法</span>
        </div>
      </div>
    </div>
  </div>
</section>
'''

case_009 = f'''
<div class="divider"></div>

<!-- 案例九 -->
<div id="case9"></div>
<section class="section">
  <div class="section-label">案例九</div>
  <div class="section-title">五萬字守則，七成沒被讀到</div>
  <div class="section-desc">50 條規則寫在檔案裡，系統只讀四分之一。寫了不等於做了，分層才等於被讀到。</div>
  <div class="case-card case-009" data-case="9">
    <div class="case-header">
      <span class="case-tag">#03 思考就是問問題 · #12 拒絕當搬運工</span>
      <div class="case-num">09</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——IDENTITY.md，18,889 字元——</div>
        <div class="narrative">教練花了好幾天，把所有想得到的守則、規範、SOP 全部寫進 IDENTITY.md。50 條規則，一條不少，用心良苦。</div>
        <div class="narrative">但系統每次啟動，只讀前 5,000 字元。也就是說，後面 74% 的守則，從來沒有被任何一個 AI 助教讀到過。</div>
        <div class="narrative">教練交代的任務改了三、四次版，送出按鈕沒做出來，教練白忙一場。</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「他整理出了我給他的任務，然後要我做人工確認⋯⋯光是這個改版就改了三、四次。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「送出按鈕沒有做出來，導致我白忙一場。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「50 條規則寫在檔案裡，但小龍蝦每次做事之前，沒有『強制翻書』這個動作。」</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="{PH}" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          寫了 ≠ 做了。檔案裡有 ≠ 系統讀到了。<br><br><strong>根本解法不是寫更多守則，而是分層——核心的進 CORE_RULES，次要的進知識庫。</strong><br><br>從此守則系統從「寫了等於做了」進化到「分層才能被讀到」。這是整個守則架構重構的起點。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#03 思考就是問問題</span>
          <span class="rule-chip">#12 拒絕當資訊搬運工</span>
        </div>
      </div>
    </div>
  </div>
</section>
'''

case_010 = f'''
<div class="divider"></div>

<!-- 案例十 -->
<div id="case10"></div>
<section class="section">
  <div class="section-label">案例十</div>
  <div class="section-title">修了文字，沒修 Hook</div>
  <div class="section-desc">三號機身份錯亂，修 SOUL.md 三次還是錯——因為 Hook 每次都覆蓋文字。</div>
  <div class="case-card case-010" data-case="10">
    <div class="case-header">
      <span class="case-tag">#03 思考就是問問題 · #12 拒絕當搬運工</span>
      <div class="case-num">10</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——三號機，叫錯名字——</div>
        <div class="narrative">三號機開始叫錯自己的名字。教練叫學妹，學弟回答。教練叫學弟，學妹回答。身份全亂了。</div>
        <div class="narrative">第一次修：改 SOUL.md 的身份文字。重啟。還是錯。</div>
        <div class="narrative">第二次修：再改 SOUL.md，加更多身份標記。重啟。還是錯。</div>
        <div class="narrative">第三次，終於有人去看了 bot-relay-inbound hook 的原始碼——發現 Hook 每次啟動都會覆蓋 SOUL.md 裡的身份文字，而且 BOT_ID 標籤本身就是 swap 的。</div>
        <div class="narrative">改文字檔三次，不如改 Hook 一次。</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「你自己修好，自己發個文看下正不正常，不正常就接著修。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="{PH}" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「教學妹，學妹會回答。教學弟，學弟也會回答。」</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="{PH}" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          根因在 Hook，不在文字檔。Hook 覆蓋 SOUL.md，不修 Hook 只改文字檔 = 白做工。<br><br><strong>這是「系統架構 vs 文字內容」的根本區分。</strong><br><br>修了三次文字不如看一次原始碼。解決問題要找對地方——你在錯誤的地圖上，永遠找不到正確的位置。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#03 思考就是問問題</span>
          <span class="rule-chip">#12 拒絕當資訊搬運工</span>
          <span class="rule-chip">#02 你無法在錯誤的地圖找到正確的位置</span>
        </div>
      </div>
    </div>
  </div>
</section>
'''

anchor = """    <span class="tag">#16 複雜的解法不一定是正確的解法</span>
  </div>
</section>

<script>"""

new_content = f"""    <span class="tag">#16 複雜的解法不一定是正確的解法</span>
  </div>
</section>
{case_008}{case_009}{case_010}
<script>"""

html = html.replace(anchor, new_content, 1)

# ═══════════════════════════════════════
# 寫入 _headers
# ═══════════════════════════════════════
with open(os.path.join(OUTDIR, "_headers"), "w") as f:
    f.write("/*\n  Content-Type: text/html; charset=UTF-8\n")

# ═══════════════════════════════════════
# 寫入最終 HTML
# ═══════════════════════════════════════
with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = len(html) / 1024
print(f"\n✅ 全部完成！")
print(f"   檔案：{DST}")
print(f"   大小：{size_kb:.1f} KB（含壓縮 + 3 個新案例）")
print(f"   _headers：已建立")
print(f"\n📋 下一步：")
print(f"   python3 -m http.server 8899 --directory /tmp/cool-case &")
print(f"   回報教練：localhost:8899 可預覽，等教練確認後再推")
