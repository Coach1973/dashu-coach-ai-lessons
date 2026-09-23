#!/usr/bin/env python3
"""
產業鏈節點名稱查核工具：比對候選節點名稱是否真的存在於BNI 905項標準分類詞庫
(namecard-db/taxonomy.json)，區分「AI推理出來、聽起來合理但無實際案例」跟
「BNI體系裡真的有人用這個專業類別加入過」，後者可信度更高（教練2026-09-23親定）。

用法：
  python3 check_industry_chain_names.py --names "珠寶鑑定師,金工修復師,AI顧問"
  python3 check_industry_chain_names.py --names-file candidates.txt

輸出每個候選名稱：
  ✅ 完全命中taxonomy.json裡的真實名稱
  🟡 taxonomy.json裡有相似但不完全一樣的名稱（列出最接近的幾個，可能是措辭差異）
  ❌ 完全查無，屬於AI自己想的，沒有BNI真實案例佐證
"""
import argparse
import difflib
import json
from pathlib import Path

TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "namecard-db" / "taxonomy.json"


def load_names() -> list[str]:
    data = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    return data["unique_names"]


def check_one(name: str, names: list[str]) -> tuple[str, list[str]]:
    name = name.strip()
    if name in names:
        return "exact", [name]
    close = difflib.get_close_matches(name, names, n=3, cutoff=0.55)
    if close:
        return "close", close
    return "none", []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--names", help="逗號分隔的候選節點名稱")
    parser.add_argument("--names-file", help="每行一個候選名稱的文字檔")
    args = parser.parse_args()

    if args.names:
        candidates = [n.strip() for n in args.names.split(",") if n.strip()]
    elif args.names_file:
        candidates = [
            line.strip()
            for line in Path(args.names_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        parser.error("要用 --names 或 --names-file 其中一個")

    names = load_names()
    exact_count = close_count = none_count = 0

    for cand in candidates:
        status, matches = check_one(cand, names)
        if status == "exact":
            exact_count += 1
            print(f"✅ {cand}")
        elif status == "close":
            close_count += 1
            print(f"🟡 {cand}  →  相似真實類別：{'、'.join(matches)}")
        else:
            none_count += 1
            print(f"❌ {cand}  （taxonomy裡查無，屬AI自行推理，無BNI真實案例佐證）")

    print(f"\n共{len(candidates)}個候選：{exact_count}個完全命中、{close_count}個有相似真實類別、{none_count}個完全查無")
    if none_count > 0:
        print("建議把❌的項目換成✅/🟡裡的真實類別，可信度更高。")


if __name__ == "__main__":
    main()
