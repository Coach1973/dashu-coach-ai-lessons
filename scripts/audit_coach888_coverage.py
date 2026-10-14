#!/usr/bin/env python3
"""coach888收錄完整度稽核（2026-09-06教練第N次質問「為什麼一直忘記」後建立）。

跟stop_rules_master.py規則L/L2不一樣的地方：那兩條規則靠「commit訊息裡有沒有
出現特定中文措辭」去猜這輪對話是不是交付了新頁面——這種方法從根本上不可靠，
因為自然語言的寫法千變萬化，今晚已經連續踩到兩次(「後台管理頁」的「頁」
不在原本詞尾清單/heredoc把整段命令跳過)，未來一定還會有新的漏網之魚。

這支腳本改成直接讀程式碼本身：掃`event-signup/app.py`裡所有看起來是「給人看
的網頁」的Flask路由(GET、非API、非動態子頁面)，逐一比對coach888的「大樹常用」
「後臺系統」這兩個教練實際會看的分類有沒有收錄對應網址。跟教練打字措辭完全
無關，看的是「這個網站真的存在的網頁」跟「教練清單上寫的網頁」兩份清單本身
對不對得起來。

用法：
    python3 scripts/audit_coach888_coverage.py          # 只列出結果
    python3 scripts/audit_coach888_coverage.py --strict  # 有漏收錄就exit 1(給Stop hook用)
"""
import json
import re
import sys
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
APP_PY = WORKSPACE / "event-signup" / "app.py"
COACH888_HTML = Path.home() / "github_repos" / "coach888" / "index.html"
BASELINE_PATH = WORKSPACE / "scripts" / "coach888_audit_baseline.txt"
VISIBLE_SECTIONS = ("changyong", "houtai", "bymyway")

# 排除規則：這些路由不是「教練會自己點開看的獨立網頁」，收錄了反而是雜訊
EXCLUDE_PATTERNS = [
    r"^/api/",                          # 純資料端點，不是網頁
    r"^/admin/",                        # 大樹小講後台的子頁面，「後台」本身已收錄一次即可
    r"login$", r"logout$",              # 登入/登出動作，不是獨立網頁
    r"oauth",                            # OAuth技術端點，不是網頁
    r"<",                                # 含動態參數(如<int:id>)的通常是單筆操作，不是入口頁
    r"\.(csv|png|json)$",               # 檔案下載/圖片產生端點
    r"^/curated/",                      # 策展店家網站各自獨立，不進coach888(進tainan-shangquan)
    r"^/KR/", r"^/cica/",                # 掛在event-signup底下的客戶案靜態網站，同上
]


def extract_page_routes(app_py_text: str) -> list[str]:
    routes = []
    # 比對「@app.route("/xxx")」或「@app.route("/xxx", methods=[...])」，
    # 排除methods裡只有POST、沒有GET的動作型端點
    for m in re.finditer(r'@app\.route\(\s*["\']([^"\']+)["\']\s*(?:,\s*methods\s*=\s*\[([^\]]*)\])?\s*\)', app_py_text):
        path, methods = m.group(1), m.group(2) or ""
        if methods and "GET" not in methods and '"GET"' not in methods and "'GET'" not in methods:
            continue
        if any(re.search(p, path) for p in EXCLUDE_PATTERNS):
            continue
        routes.append(path)
    return sorted(set(routes))


def extract_visible_section_html(full_html: str) -> str:
    chunks = []
    for section_id in VISIBLE_SECTIONS:
        start = f'<div class="grid" data-section="{section_id}">'
        end = f'<button class="btn-add-item" data-section="{section_id}">'
        s, e = full_html.find(start), full_html.find(end)
        if s != -1 and e != -1 and e > s:
            chunks.append(full_html[s:e])
    return "\n".join(chunks)


def server_visible_urls() -> str:
    """coach888 實際顯示的內容在伺服器狀態（event.bymyway.com/api/coach888/state），
    coach888_register_admin.py 也是寫那裡；只讀 git 靜態 HTML 會把用正式工具登記的新網址誤報成漏收錄
    （2026-10-14 /tut/team 已登記仍被擋）。連不上伺服器就只看靜態 HTML，不讓稽核本身卡住收工。"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from coach888_register_admin import _get
        layout = json.loads(_get()["coach888_layout"])
    except Exception:  # noqa: BLE001
        return ""
    return "\n".join(u for s in VISIBLE_SECTIONS for u in layout.get(s, []))


def main():
    if not APP_PY.is_file() or not COACH888_HTML.is_file():
        # 雲端工作頁只sparse-checkout main分支的scripts/knowledges/cloud_sync等目錄，
        # 不含event-signup、也沒有~/github_repos/coach888(見.claude/cloud_bootstrap.sh)，
        # 這裡讀不到來源檔是環境限制，不代表教練真的漏收錄了什麼——照
        # stop_rules_master.py呼叫端的既有原則「稽核腳本本身故障不該擋住教練收工」，
        # 安靜跳過，不當成新缺漏擋Stop。2026-09-27雲端v253診斷，09-30軍師審批套用。
        missing = APP_PY if not APP_PY.is_file() else COACH888_HTML
        print(f"⚠️ 找不到 {missing}（本環境無此checkout，跳過此稽核，不代表有漏收錄）")
        return
    app_text = APP_PY.read_text(encoding="utf-8")
    coach888_text = COACH888_HTML.read_text(encoding="utf-8")
    visible = extract_visible_section_html(coach888_text) + "\n" + server_visible_urls()

    routes = extract_page_routes(app_text)

    # 2026-09-05教練拍板：教練朋友/客戶的一次性網站統一收錄進tainan-shangquan
    # 店家名冊，不進coach888——這些路由已經在別的清單追蹤，不算coach888的漏收錄
    tainan_shangquan_path = Path.home() / "github_repos" / "tainan-shangquan" / "index.html"
    tainan_shangquan_text = tainan_shangquan_path.read_text(encoding="utf-8") if tainan_shangquan_path.is_file() else ""

    missing = [
        r for r in routes
        if r not in visible and f"event.bymyway.com{r}" not in visible
        and r.strip("/") not in tainan_shangquan_text
    ]

    baseline = set()
    if BASELINE_PATH.is_file():
        baseline = {
            line.strip() for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
    new_missing = [r for r in missing if r not in baseline]

    print(f"event-signup/app.py 共掃到 {len(routes)} 個像網頁的路由（已排除API/子頁面/動態參數）")
    if missing:
        print(f"\n❌ 以下 {len(missing)} 個在coach888「大樹常用」/「後臺系統」/「bymyway自架版」查不到：")
        for r in missing:
            tag = "（已知舊帳，見baseline）" if r in baseline else "🔴新缺漏"
            print(f"  • event.bymyway.com{r} {tag}")
    else:
        print("✅ 全部都在coach888可見範圍內找得到")

    if "--strict" in sys.argv and new_missing:
        print(f"\n🔴 有 {len(new_missing)} 個不在baseline裡的新缺漏，視為這次對話忘記收錄")
        sys.exit(1)


if __name__ == "__main__":
    main()
