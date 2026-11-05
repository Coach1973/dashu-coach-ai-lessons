#!/usr/bin/env python3
"""把新做的「管理／編輯／刪除」網址登記進教練的「大樹作品集」(coach888)，教練只能靠那裡找到這些網址。

規則（執行細則 N10，教練 2026-10-10）：AI 只要做出新的後台、管理頁、編輯連結、刪除入口，同一輪就要跑這支登記，
不准等教練提醒。教練記不住那一長串網址，大樹作品集是他唯一找得到的地方。

用法：
  python3 scripts/coach888_register_admin.py <網址> <顯示名稱> [--section baoliu] [--badge 後臺]
  python3 scripts/coach888_register_admin.py --list          看「活動後台」現有項目
  （預設同時登記進 event.bymyway.com/vault 憑證總覽頁；有帳密的後台加 --no-vault，帳密自己補進 /vault 的表）
預設放進「活動後台」(baoliu)、標籤「後臺」。同一個網址重複登記只會更新名稱與位置，不會重複。
寫入前先備份整份狀態到 state/，寫完重新讀回核對。
"""
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

API = "https://event.bymyway.com/api/coach888/state"
HEADERS = {"User-Agent": "Mozilla/5.0", "Origin": "https://coach1973.github.io", "Content-Type": "application/json"}
BACKUP_DIR = Path(__file__).resolve().parent.parent / "state"


def _get() -> dict:
    return json.loads(urllib.request.urlopen(urllib.request.Request(API, headers=HEADERS), timeout=15).read())


def _post(layout: dict, items: dict) -> None:
    body = json.dumps({"coach888_layout": json.dumps(layout, ensure_ascii=False),
                       "coach888_items": json.dumps(items, ensure_ascii=False)}).encode("utf-8")
    urllib.request.urlopen(urllib.request.Request(API, data=body, method="POST", headers=HEADERS), timeout=15)


VAULT_EXTRA = Path(__file__).resolve().parent.parent / "event-signup" / "vault_extra.json"


def register_vault(url: str, name: str, user: str = "（不需要帳密，網址本身就是通行證）", password: str = "—") -> str:
    """同時登記進 event.bymyway.com/vault（憑證總覽頁，教練另一個找後台的地方）。同網址重複登記只更新。
    event-signup 的 /vault 每次開頁都會讀這個檔，不用重啟。"""
    try:
        rows = json.loads(VAULT_EXTRA.read_text(encoding="utf-8")) if VAULT_EXTRA.exists() else []
    except ValueError:
        rows = []
    rows = [r for r in rows if r.get("url") != url] + [{"name": name, "url": url, "user": user, "password": password}]
    VAULT_EXTRA.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"；已同步到 /vault（共 {len(rows)} 筆額外項目）"


PINNED = Path(__file__).resolve().parent.parent / "event-signup" / "coach888_pinned_recent.json"


def _pin_recent(url: str, name: str, section: str, badge: str) -> None:
    """另存一份「最近登記」，伺服器端被舊頁面蓋掉時 72 小時內會補回（案例149）。"""
    try:
        rows = json.loads(PINNED.read_text(encoding="utf-8")) if PINNED.exists() else []
    except ValueError:
        rows = []
    cutoff = (datetime.now().timestamp() - 7 * 86400)
    rows = [r for r in rows if r.get("url") != url and datetime.strptime(r["at"], "%Y-%m-%d %H:%M").timestamp() > cutoff]
    rows.append({"url": url, "section": section, "name": name, "badge": badge, "at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    PINNED.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def register(url: str, name: str, section: str = "baoliu", badge: str = "後臺") -> str:
    if not url.startswith("https://"):
        raise SystemExit("網址要用 https:// 開頭")
    state = _get()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    (BACKUP_DIR / f"coach888_state_backup_{stamp}_before_admin_register.json").write_text(
        json.dumps(state, ensure_ascii=False), encoding="utf-8")
    layout, items = json.loads(state["coach888_layout"]), json.loads(state.get("coach888_items") or "{}")
    if section not in layout:
        raise SystemExit(f"找不到分類 {section}（現有：{', '.join(layout)}）")
    before = {k: len(v) for k, v in layout.items()}
    already = any(url in v for v in layout.values())
    for v in layout.values():
        if url in v:
            v.remove(url)
    layout[section].append(url)          # 放在該分類最後一項，不去動教練排好的順序
    items[url] = {"name": name, "badge": badge}
    _post(layout, items)
    chk = _get()
    l2, i2 = json.loads(chk["coach888_layout"]), json.loads(chk["coach888_items"])
    if url not in l2.get(section, []) or i2.get(url, {}).get("name") != name:
        raise SystemExit("寫入後核對不符，請人工檢查 coach888 狀態（備份在 state/）")
    _pin_recent(url, name, section, badge)
    after = {k: len(v) for k, v in l2.items()}
    moved = {k: (before[k], after[k]) for k in before if before[k] != after.get(k)}
    return f"{'已更新' if already else '已登記'}：{name}（{section}，共 {len(l2[section])} 項；數量變動 {moved or '無'}）"


def main(argv):
    if argv[:1] == ["--list"]:
        st = _get()
        layout, items = json.loads(st["coach888_layout"]), json.loads(st["coach888_items"])
        names = json.loads(st.get("coach888_names") or "{}")
        for u in layout.get("baoliu", []):
            print(f"- {(items.get(u) or {}).get('name') or names.get(u) or '?'} | {u}")
        return 0
    args = [a for a in argv if not a.startswith("--")]
    opt = {argv[i]: argv[i + 1] for i in range(len(argv) - 1) if argv[i] in ("--section", "--badge")}
    pos = [a for a in args if a not in opt.values()]
    if len(pos) != 2:
        print(__doc__)
        return 2
    if len(pos[0]) > 60:   # 教練 2026-10-10：「只要是這種長網址的一律都變短址」。先做短網址再登記；這裡只提醒不擋。
        print(f"⚠️ 這個網址有 {len(pos[0])} 個字，太長了。教練要求後台／管理網址一律做成短網址"
              "（參考信任遊戲後台 /game/a/<12字>、策展上傳 /u/<10字>：用金鑰算固定短代碼，舊長連結照樣有效）。")
    msg = register(pos[0], pos[1], opt.get("--section", "baoliu"), opt.get("--badge", "後臺"))
    if "--no-vault" not in argv:   # 預設也登記進 /vault（憑證總覽頁）；密碼型後台請加 --no-vault 自己手動補帳密
        msg += register_vault(pos[0], pos[1])
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
