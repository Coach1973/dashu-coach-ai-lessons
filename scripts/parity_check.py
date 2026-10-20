#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""照抄對照器（2026-10-21，my-tools 改 11 版的教訓）

教練說「跟 X 一模一樣」＝照抄 X。這支程式把標準答案 X 的「操作」機械式列出來
（按鈕字、提示字、確認視窗、拖曳手把、點文字直接改…），再逐項到目標頁的原始碼裡找，
列出目標頁缺哪幾項。不靠 AI 記得、不靠 AI 自己判斷「差不多」。

用法：
  python3 parity_check.py <標準答案.html> <目標頁.html 或資料夾>
  目標倉庫可放 .parity-allow（一行一個字串）＝教練明說可以不一樣的項目
結束碼：0＝一項不缺；1＝有缺（Stop 鎖看這個）
"""
import re, sys, os, html

def src_of(path):
    if os.path.isdir(path):
        out = []
        for root, _, files in os.walk(path):
            if '.git' in root:
                continue
            for f in files:
                if f.endswith(('.html', '.js')):
                    out.append(open(os.path.join(root, f), encoding='utf-8', errors='ignore').read())
        return '\n'.join(out)
    return open(path, encoding='utf-8', errors='ignore').read()

def norm(s):
    s = html.unescape(s)
    s = re.sub(r'[\U0001F000-\U0001FFFF☀-➿️]', '', s)   # 去表情符號
    return re.sub(r'[\s「」『』（）()：:，,。.!！?？\'"+\-—／/…]+', '', s)

def features(src):
    """回傳 [(類別, 原字串)]：只抓『操作』，不抓資料內容"""
    feats = []
    for m in re.finditer(r'<button\b[^>]*>(.*?)</button>', src, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if t:
            feats.append(('按鈕', t))
    for attr in ('title', 'placeholder', 'aria-label'):
        for m in re.finditer(attr + r'="([^"]{2,40})"', src):
            feats.append(('提示字', m.group(1)))
    for fn in ('confirm', 'toast', 'alert'):
        for m in re.finditer(fn + r"\(\s*'([^']{3,})'", src):
            feats.append((fn == 'confirm' and '確認視窗' or '提示訊息', m.group(1)))
    marks = {
        'contenteditable="true"': '點文字直接改（contenteditable）',
        'drag-handle': '拖曳手把 ⠿',
        'section-drag-handle': '分類拖曳排序',
        'bulk-checkbox': '批量勾選框',
        'sendBeacon': '點擊計次（熱門排行）',
        'navigator.clipboard': '複製到剪貼簿',
    }
    for k, label in marks.items():
        if k in src:
            feats.append(('結構', label))
    seen, out = set(), []
    for cat, t in feats:
        key = (cat, norm(t))
        if key[1] and key not in seen:
            seen.add(key)
            out.append((cat, t))
    return out

STRUCT_PROBE = {
    '點文字直接改（contenteditable）': ['contenteditable'],
    '拖曳手把 ⠿': ['⠿'],
    '分類拖曳排序': ['section-drag', 'secDrag', 'dragSec'],
    '批量勾選框': ['bulk-checkbox', 'bulk'],
    '點擊計次（熱門排行）': ['sendBeacon', '/click'],
    '複製到剪貼簿': ['navigator.clipboard'],
}

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    ref, tgt = sys.argv[1], sys.argv[2]
    rsrc, tsrc = src_of(ref), src_of(tgt)
    tnorm = norm(tsrc)
    allow_file = os.path.join(tgt if os.path.isdir(tgt) else os.path.dirname(tgt), '.parity-allow')
    allow = set()
    if os.path.isfile(allow_file):
        allow = {norm(l) for l in open(allow_file, encoding='utf-8') if l.strip() and not l.startswith('#')}
    missing, ok = [], 0
    for cat, t in features(rsrc):
        if norm(t) in allow:
            continue
        if cat == '結構':
            hit = any(p in tsrc for p in STRUCT_PROBE.get(t, []))
        else:
            hit = norm(t)[:12] in tnorm
        if hit:
            ok += 1
        else:
            missing.append((cat, t))
    print('照抄對照：標準答案 %s → 目標 %s' % (ref, tgt))
    print('一樣 %d 項，缺 %d 項' % (ok, len(missing)))
    for cat, t in missing:
        print('  ❌ [%s] %s' % (cat, t))
    sys.exit(1 if missing else 0)

if __name__ == '__main__':
    main()
