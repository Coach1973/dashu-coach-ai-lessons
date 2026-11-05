#!/usr/bin/env python3
"""開工補登記：把「不是 Mac 本機發佈」的 Artifact 補收進大樹作品集「大樹常用」（2026-11-05 案例148）

起因：雲端/網頁版做的 Artifact（例：大樹模組總表 54 項）沒經過 Mac 的 auto_register_artifact.py，
      沒登記也沒交接，桌面版被問找不到。
用法：開工時 AI 先呼叫 Artifact list（scope mine，limit 30），把「url<TAB>標題」每行一筆丟進 stdin：
      printf '%s\t%s\n' ... | python3 artifact_sweep_register.py
規則：已在作品集的略過；曾經掃過的（state/artifact_sweep_seen.json）不再補，教練刪掉的不會又冒出來；
      只印一行結果；失敗不擋工作。
"""
import json, re, sys
from datetime import datetime
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
SEEN = WS / "state" / "artifact_sweep_seen.json"
LOG = WS / "state" / "auto_register_artifact.log"
URL = re.compile(r"https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+")


def main() -> None:
    items = []
    for line in sys.stdin.read().splitlines():
        m = URL.search(line)
        if m:
            title = re.sub(r"\s+", " ", line.replace(m.group(0), "")).strip(" \t|-—:") or "（未命名）"
            items.append((m.group(0), title))
    try:
        seen = set(json.loads(SEEN.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        seen = set()
    added, skipped = [], 0
    try:
        import coach888_register_admin as reg
        layout = json.loads(reg._get()["coach888_layout"])
        for url, title in items:
            if url in seen or any(url in v for v in layout.values()):
                skipped += 1
            else:
                reg.register(url, title, "changyong", "報告")
                added.append(title)
                with LOG.open("a", encoding="utf-8") as f:
                    f.write(f"{datetime.now():%F %T} {url} 開工補登記：{title}\n")
            seen.add(url)
        SEEN.write_text(json.dumps(sorted(seen), ensure_ascii=False), encoding="utf-8")
    except BaseException as e:
        print(f"補登記失敗（不擋工作）：{type(e).__name__}: {e}")
        return
    print(f"Artifact 補登記：新增 {len(added)} 筆、略過 {skipped} 筆" + ("：" + "、".join(added) if added else ""))


if __name__ == "__main__":
    main()
