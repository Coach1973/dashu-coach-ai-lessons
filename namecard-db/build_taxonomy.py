"""
整合兩份BNI專業分類原始資料，產出統一的標準分類詞庫 taxonomy.json。

來源：
1. 教練透過AI(Gemini)從BNI官方文件提取的28大類/533項專業清單
   (/Users/bymyway/Downloads/gemini-code-1787668824032.py 裡的 raw_text)
2. 大台南南區AI小幫手既有知識庫 industry_database.md 裡的
   「BNI 682+ 產業全生態戰略總庫」(8大類，含★子分類，台灣本地實戰數據)

輸出格式：扁平化 items 清單，每項保留所屬大類與來源標籤，供:
- extract.py 辨識名片時當作AI可選的category候選池
- 產業鏈媒合邏輯做初步分群依據
不做「完全去重合併成單一階層」，因為兩份資料設計邏輯不同(一份是官方標準分類，
一份是台灣本地實戰精煉版)，保留雙來源反而讓AI判斷時有更完整的參照。

用法：python3 build_taxonomy.py
"""
import json
import re

GEMINI_SRC = "/Users/bymyway/Downloads/gemini-code-1787668824032.py"
BNI_DB_SRC = "/Users/bymyway/.openclaw/agents/bni_tainan/knowledge/industry_database.md"
OUTPUT = "taxonomy.json"


def parse_gemini_533() -> list[dict]:
    """解析28大類/533項清單，格式：N- 大類名 \n 專長: \n - 項目"""
    with open(GEMINI_SRC, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'raw_text\s*=\s*"""(.*?)"""', content, re.S)
    if not m:
        raise RuntimeError("找不到raw_text區塊")
    raw = m.group(1)

    items = []
    current_category = None
    for line in raw.split("\n"):
        line = line.rstrip()
        cat_match = re.match(r"^\d+-\s*(.+)$", line)
        if cat_match and not line.strip().startswith("-"):
            current_category = cat_match.group(1).strip()
            continue
        if line.strip() == "專長:":
            continue
        item_match = re.match(r"^-\s*(.+)$", line.strip())
        if item_match and current_category:
            name = item_match.group(1).strip()
            if name.endswith("(其他)"):
                continue  # "XX(其他)"是萬用兜底項，不列入具體詞庫
            items.append({"category": current_category, "name": name, "source": "bni_official_533"})
    return items


def parse_taiwan_682() -> list[dict]:
    """解析682+產業全生態戰略總庫，格式：### N. 大類 \n ★子分類：項目1、項目2..."""
    with open(BNI_DB_SRC, encoding="utf-8") as f:
        content = f.read()
    m = re.search(
        r"## 【BNI 682\+.*?Master Category Database\)】(.*?)## 【區域團隊介紹",
        content,
        re.S,
    )
    if not m:
        raise RuntimeError("找不到682+產業全生態戰略總庫區塊")
    block = m.group(1)

    items = []
    current_category = None
    for line in block.split("\n"):
        line = line.strip()
        if not line:
            continue
        cat_match = re.match(r"^###\s*\d+\.\s*(.+?)(\s*\(.+\))?$", line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue
        if line.startswith("★") and current_category:
            # ★子分類名稱：項目1、項目2、項目3...
            sub_match = re.match(r"^★\s*([^：]+)：(.+)$", line)
            if not sub_match:
                continue
            sub_name = sub_match.group(1).strip()
            names = re.split(r"[、,，]\s*", sub_match.group(2))
            for name in names:
                name = name.strip().rstrip("。")
                if name:
                    items.append({
                        "category": current_category,
                        "sub_category": sub_name,
                        "name": name,
                        "source": "taiwan_682",
                    })
    return items


def main() -> None:
    items_533 = parse_gemini_533()
    items_682 = parse_taiwan_682()

    all_items = items_533 + items_682
    unique_names = sorted({it["name"] for it in all_items})

    taxonomy = {
        "generated_from": [GEMINI_SRC, BNI_DB_SRC],
        "total_items": len(all_items),
        "unique_item_count": len(unique_names),
        "items": all_items,
        "unique_names": unique_names,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)

    categories_533 = sorted({it["category"] for it in items_533})
    categories_682 = sorted({it["category"] for it in items_682})
    print(f"533清單：{len(categories_533)}大類，{len(items_533)}項")
    print(f"682+清單：{len(categories_682)}大類，{len(items_682)}項")
    print(f"合併後（含重複，不同來源視為不同項）：{len(all_items)}項")
    print(f"去重後不重複專業名稱：{len(unique_names)}項")
    print(f"已寫入 {OUTPUT}")


if __name__ == "__main__":
    main()
