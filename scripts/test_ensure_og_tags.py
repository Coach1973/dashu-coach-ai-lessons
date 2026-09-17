#!/usr/bin/env python3
"""ensure_og_tags_absolute 的單元測試（2026-09-18 軍師交辦：寫小測試再 commit）"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import curation_process as cp


def make_index(tmpdir: Path, html: str) -> Path:
    p = tmpdir / "index.html"
    p.write_text(html, encoding="utf-8")
    return p


def test_relative_og_image_to_absolute():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_index(tmp, '''<!DOCTYPE html>
<html><head>
<meta property="og:image" content="img/hero.jpg">
<meta property="og:title" content="測試店">
<meta property="og:description" content="測試描述">
</head><body></body></html>''')
        cp.ensure_og_tags_absolute(tmp, "test-slug")
        result = (tmp / "index.html").read_text(encoding="utf-8")
        assert "https://event.bymyway.com/curated/test-slug/img/hero.jpg" in result, \
            f"❌ og:image 沒改成絕對 URL：\n{result}"
        print("✅ test_relative_og_image_to_absolute")


def test_absolute_og_image_unchanged():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_index(tmp, '''<!DOCTYPE html>
<html><head>
<meta property="og:image" content="https://example.com/hero.jpg">
<meta property="og:title" content="測試店">
</head><body></body></html>''')
        cp.ensure_og_tags_absolute(tmp, "test-slug")
        result = (tmp / "index.html").read_text(encoding="utf-8")
        assert "https://example.com/hero.jpg" in result, "絕對 URL 應該保留"
        # 沒被覆寫成另一個 URL
        assert "https://event.bymyway.com/curated/test-slug/" not in result, \
            f"絕對 og:image 不該被改寫成 event.bymyway.com：\n{result}"
        print("✅ test_absolute_og_image_unchanged")


def test_missing_og_tags_get_filled():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_index(tmp, '''<!DOCTYPE html>
<html><head>
<title>康燕居測試 — 一盞燕窩</title>
<meta name="description" content="燕窩的由來與故事">
</head><body>
<img src="img/hero.jpg" alt="主視覺">
</body></html>''')
        cp.ensure_og_tags_absolute(tmp, "kangyenju-test")
        result = (tmp / "index.html").read_text(encoding="utf-8")
        assert 'property="og:type" content="website"' in result, "沒補 og:type"
        assert 'property="og:title" content="康燕居測試 — 一盞燕窩"' in result, "沒補 og:title"
        assert 'property="og:description" content="燕窩的由來與故事"' in result, "沒補 og:description"
        assert 'property="og:image" content="https://event.bymyway.com/curated/kangyenju-test/img/hero.jpg"' in result, \
            f"沒補 og:image 絕對 URL：\n{result}"
        print("✅ test_missing_og_tags_get_filled")


def test_description_differs_from_title():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_index(tmp, '''<!DOCTYPE html>
<html><head>
<title>康燕居｜一盞燕窞</title>
<meta name="description" content="康燕居｜一盞燕窞">
</head><body>
<img src="img/hero.jpg">
</body></html>''')
        cp.ensure_og_tags_absolute(tmp, "test")
        result = (tmp / "index.html").read_text(encoding="utf-8")
        # description 應該跟 title 有差異（教練抱怨重複的問題）
        import re
        og_title = re.search(r'property="og:title" content="([^"]+)"', result)
        og_desc = re.search(r'property="og:description" content="([^"]+)"', result)
        assert og_title and og_desc, "og:title 或 og:description 沒生成"
        # 正規化後比較
        def norm(s):
            return re.sub(r"[\s\-|\/・—_,，。;;:\"'《》「」()（）]+", "", s).lower()
        assert norm(og_title.group(1)) != norm(og_desc.group(1)), \
            f"❌ og:title 和 og:description 內容重複：title={og_title.group(1)} | desc={og_desc.group(1)}"
        print("✅ test_description_differs_from_title")


def test_idempotent():
    """跑兩次結果應該一樣"""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_index(tmp, '''<!DOCTYPE html>
<html><head>
<meta property="og:image" content="assets/og-card.jpg">
<title>測試</title>
<meta name="description" content="描述內容">
</head><body></body></html>''')
        cp.ensure_og_tags_absolute(tmp, "x")
        first = (tmp / "index.html").read_text(encoding="utf-8")
        cp.ensure_og_tags_absolute(tmp, "x")
        second = (tmp / "index.html").read_text(encoding="utf-8")
        assert first == second, f"❌ 第二次跑改動了內容：\nfirst={first}\nsecond={second}"
        print("✅ test_idempotent")


def main():
    test_relative_og_image_to_absolute()
    test_absolute_og_image_unchanged()
    test_missing_og_tags_get_filled()
    test_description_differs_from_title()
    test_idempotent()
    print("\n=== 全部 5 個測試通過 ===")


if __name__ == '__main__':
    main()
