#!/usr/bin/env python3
"""
重排順序：
新 #01 = 舊 #08（誰允許它切回去的？）
新 #02 = 舊 #07（邏輯推就知道要做）
新 #03 = 舊 #01（鬧鐘響了卻沒起床）
新 #04-#08 = 舊 #02-#06（順序維持）
新 #09-#10 = 舊 #09-#10
"""
import re

html_path = "/tmp/cool-case/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 順序映射：新位置 -> 舊編號
order = [8, 7, 1, 2, 3, 4, 5, 6, 9, 10]

CN_NUM = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"七", 8:"八", 9:"九", 10:"十"}

# 找出每個 case 區塊（從 <div id="caseN"></div> 到下一個 case 前的最後一個 divider）
case_blocks = {}
for n in range(1, 11):
    start_marker = f'<div id="case{n}"></div>'
    start = html.find(start_marker)
    if start < 0:
        print(f"WARNING: case{n} not found")
        continue

    # 找下一個 case
    next_start = -1
    for m in range(n+1, 12):
        next_marker = f'<div id="case{m}"></div>'
        ns = html.find(next_marker)
        if ns > 0:
            next_start = ns
            break

    if next_start < 0:
        # 最後一個案例，找 <script> 標籤
        next_start = html.find('<script>', start)

    # 找 next_start 之前的最後一個 divider，把 divider 包含進去
    divider = '<div class="divider"></div>'
    last_divider = html.rfind(divider, start, next_start)
    if last_divider > 0:
        end = last_divider + len(divider) + 1  # 包含 divider 和換行
    else:
        end = next_start

    case_blocks[n] = html[start:end]
    print(f"case{n}: {len(case_blocks[n])} chars")

# 找到第一個 case 之前的 HTML
first_case_start = html.find('<div id="case1"></div>')
header_html = html[:first_case_start]

# 找到最後一個 case 之後的 HTML
last_case_end = -1
for n in range(10, 0, -1):
    if n in case_blocks:
        marker = f'<div id="case{n}"></div>'
        pos = html.find(marker)
        # 找這個 case 後面結束位置
        next_marker_pos = -1
        for m in range(n+1, 12):
            next_marker = f'<div id="case{m}"></div>'
            ns = html.find(next_marker)
            if ns > 0 and ns > pos:
                next_marker_pos = ns
                break
        if next_marker_pos < 0:
            next_marker_pos = html.find('<script>', pos)
        last_case_end = next_marker_pos
        break

# 找最後一個 case 結束位置（包含 divider）
divider = '<div class="divider"></div>'
real_last_case_end = -1
for n in range(10, 0, -1):
    if n in case_blocks:
        marker = f'<div id="case{n}"></div>'
        pos = html.find(marker)
        next_pos = html.find('<script>', pos)
        last_div = html.rfind(divider, pos, next_pos)
        if last_div > 0:
            real_last_case_end = last_div + len(divider) + 1
        else:
            real_last_case_end = next_pos
        break

footer_html = html[real_last_case_end:]

# 對每個 case 區塊重編（id, label, case-num）
def relabel(block_html, old_n, new_n):
    new_num_str = f"{new_n:02d}"
    new_cn = CN_NUM[new_n]

    # 1. id="caseN"
    block_html = block_html.replace(f'id="case{old_n}"', f'id="case{new_n}"', 1)

    # 2. <div class="section-label">案例X</div>
    block_html = re.sub(
        r'(<div class="section-label">案例)[一二三四五六七八九十]+(</div>)',
        rf'\g<1>{new_cn}\g<2>',
        block_html,
        count=1
    )

    # 3. <div class="case-num">XX</div>
    block_html = re.sub(
        r'(<div class="case-num">)\d+(</div>)',
        rf'\g<1>{new_num_str}\g<2>',
        block_html,
        count=1
    )

    # 4. 案例 X 註解（如果有）— 跳過

    return block_html

# 重組
new_cases_html = ""
for new_pos, old_n in enumerate(order, start=1):
    if old_n not in case_blocks:
        continue
    relabeled = relabel(case_blocks[old_n], old_n, new_pos)
    new_cases_html += relabeled
    print(f"新 #{new_pos:02d} ← 舊 #{old_n:02d}")

# 重編浮動 nav
# 原本格式：<a href="#caseN" title="案例X">XX</a>
nav_pattern = re.compile(r'<a href="#case\d+" title="案例[一二三四五六七八九十]+">\d+</a>')
nav_matches = nav_pattern.findall(footer_html)

# 重建 nav 為新順序
new_nav_items = []
for new_n in range(1, len(order)+1):
    new_nav_items.append(f'  <a href="#case{new_n}" title="案例{CN_NUM[new_n]}">{new_n:02d}</a>')

# 替換 footer 裡的 nav
# 找到 nav block 並整段替換
nav_block_pattern = re.compile(r'(<a href="#top"[^>]*>▲</a>\s*\n)((?:\s*<a href="#case\d+"[^>]*>\d+</a>\s*\n)+)')
def replace_nav(m):
    return m.group(1) + '\n'.join(new_nav_items) + '\n'

footer_html = nav_block_pattern.sub(replace_nav, footer_html, count=1)

# 組裝
new_html = header_html + new_cases_html + footer_html

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

import os
print(f"\n完成。新檔案大小: {os.path.getsize(html_path)/1024:.1f} KB")
print(f"新順序: {order}")
