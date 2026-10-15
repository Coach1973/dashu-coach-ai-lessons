#!/usr/bin/env python3
"""optimize_site_assets._rewrite_refs 回歸測試（2026-10-15）：新舊寫法結果必須一樣，且超長內嵌資料不能卡住。
執行：python3 scripts/test_optimize_rewrite_refs.py"""
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import optimize_site_assets as o

fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def old_rewrite(text, old_name, new_name):      # 舊版（會卡）：只用在短文字上比對語意
    count = 0
    pattern = re.compile(r"[^\s\"'()<>,=]*" + re.escape(old_name) + r"(?=[\s\"'()<>,?#;]|$)")

    def repl(m):
        nonlocal count
        tok = m.group(0)
        if tok.startswith(("http://", "https://", "//")):
            return tok
        count += 1
        return tok[: -len(old_name)] + new_name
    return pattern.sub(repl, text), count


samples = [
    '<img src="images/a.png"> <img src=\'a.png\'> url(a.png) url("x/a.png?v=1") <a href="https://cdn.com/a.png">x</a>',
    'a.png a.png,a.png a.png.bak xa.png //cdn/a.png "a.png" srcset="a.png 1x, b/a.png 2x"',
    'background:url(../img/中文 資料夾/a.png) 沒有a.png結尾 a.pngx',
    'no refs here', 'a.png', '/a.png', './a.png"', 'http://x/a.png https://y/z/a.png https://q/a.png.png',
    'a.pnga.png a.png a.png',
]
for i, t in enumerate(samples):
    check(f"語意與舊版相同 #{i}", o._rewrite_refs(t, "a.png", "a.webp") == old_rewrite(t, "a.png", "a.webp"))
random.seed(7)
alphabet = ['a.png', ' ', '"', "'", '(', ')', ',', '=', '<', '>', 'x', '/', 'https://', '//', '中', '\n']   # 不放 ; # ? （舊版遇到連在一起的兩個檔名會漏改，見下方明確案例）
for i in range(300):
    t = "".join(random.choice(alphabet) for _ in range(random.randint(0, 60)))
    if o._rewrite_refs(t, "a.png", "A.webp") != old_rewrite(t, "a.png", "A.webp"):
        check(f"隨機比對 #{i} 不同：{t!r}", False)
        break
else:
    check("300 組隨機文字與舊版結果完全相同", True)

# 舊版缺陷：同一段連續文字裡有兩個檔名（用 ; 或 # 或 ? 接在一起），舊版只改最後一個，前一個會變壞連結。新版兩個都改。
r, c = o._rewrite_refs('x="a.png;a.png#top" y="a.png?v=1"', "a.png", "a.webp")
check("連在一起的多個引用全部改到（舊版會漏）", r == 'x="a.webp;a.webp#top" y="a.webp?v=1"' and c == 3)
r, c = o._rewrite_refs('<a href="https://cdn.com/a.png">x</a> <img src="a.png">', "a.png", "a.webp")
check("外部網址不動、站內引用才改", r == '<a href="https://cdn.com/a.png">x</a> <img src="a.webp">' and c == 1)

blob = "data:image/png;base64," + "QUJD" * 2_500_000      # 10MB、沒有任何空白的內嵌圖片資料
t = f'<img src="{blob}"> <img src="images/hero.png"> url(hero.png)'
t0 = time.time()
res, cnt = o._rewrite_refs(t, "hero.png", "hero.webp")
dt = time.time() - t0
check(f"10MB 內嵌資料 + 兩處引用：{dt:.2f} 秒內完成（舊版 15 分鐘沒跑完）", dt < 5)
check("引用有被正確改掉、內嵌資料沒動", cnt == 2 and "images/hero.webp" in res and "url(hero.webp)" in res and blob in res)
t0 = time.time()
o._rewrite_refs(blob, "hero.png", "x")
check("整段都是內嵌資料、檔名不存在：立刻略過", time.time() - t0 < 1)
print("\n全部通過" if not fails else f"\n失敗 {len(fails)} 項")
raise SystemExit(1 if fails else 0)
