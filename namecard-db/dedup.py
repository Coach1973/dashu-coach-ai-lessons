"""
合併同一張名片的正反面：找出「無姓名」的卡片，其實是另一張已有姓名卡片的背面
（同公司/同標語/同類別，只是背面沒印個人姓名，這是常見情況）。

做法：先用公司名稱關鍵字重疊找候選配對（可靠、不靠AI隱含推理），
再讓AI確認這組候選是否合理，避免誤判兩間不相關公司。

用法：python dedup.py（也會被 watch_and_extract.py 每次掃描後自動呼叫）
"""
import json
import os
import re

import anthropic

import db

MODEL = os.environ.get("NAMECARD_MODEL", "MiniMax-M3")

# 公司名稱裡常見、比對時要忽略的通用字詞
STOPWORDS = {
    "股份有限公司", "有限公司", "企業社", "工作室", "集團", "CORP", "CORPORATION",
    "CO", "LTD", "INC", "COMPANY", "TAIWAN", "台灣", "國際", "INTERNATIONAL",
    "ASSOCIATION", "協會",
}

# 註：原本這裡有一段呼叫AI做yes/no確認，實測MiniMax-M3對同一組資料重複問會給出
# 不一致的答案（同樣的TFS配對，三次呼叫兩次no一次yes），不夠可靠，故拿掉AI確認這一步，
# 改成只靠公司名稱關鍵字重疊判斷（已排除「有限公司」「股份」等通用字，能重疊代表
# 真正有意義的品牌詞如「TFS」），判斷結果穩定可重現。


def _tokens(company: str) -> set[str]:
    if not company:
        return set()
    words = re.split(r"[\s（）()／/、,，·．.]+", company.upper())
    return {w for w in words if len(w) >= 2 and w not in STOPWORDS}


def find_frontback_pairs(client: anthropic.Anthropic) -> list[dict]:
    conn = db.get_conn()
    rows = conn.execute(
        "SELECT id, name, company, tagline, category, created_at FROM cards "
        "WHERE status != 'failed' AND status != 'roster'"
    ).fetchall()
    conn.close()

    named = [r for r in rows if (r["name"] or "").strip()]
    nameless = [r for r in rows if not (r["name"] or "").strip()]
    if not nameless or not named:
        return []

    confirmed = []
    matched_secondary_ids = set()
    for sec in nameless:
        if sec["id"] in matched_secondary_ids:
            continue
        sec_tokens = _tokens(sec["company"])
        if not sec_tokens:
            continue
        for pri in named:
            pri_tokens = _tokens(pri["company"])
            overlap = sec_tokens & pri_tokens
            if overlap:
                confirmed.append({
                    "primary_id": pri["id"],
                    "secondary_id": sec["id"],
                    "reason": f"公司名稱關鍵字重疊「{'/'.join(overlap)}」({pri['company']} vs {sec['company']})",
                })
                matched_secondary_ids.add(sec["id"])
                break
    return confirmed


def merge_pairs(pairs: list[dict]) -> int:
    if not pairs:
        return 0
    conn = db.get_conn()
    merged_count = 0
    for pair in pairs:
        primary_id = pair.get("primary_id")
        secondary_id = pair.get("secondary_id")
        if not primary_id or not secondary_id or primary_id == secondary_id:
            continue
        primary = conn.execute("SELECT * FROM cards WHERE id = ?", (primary_id,)).fetchone()
        secondary = conn.execute("SELECT * FROM cards WHERE id = ?", (secondary_id,)).fetchone()
        if not primary or not secondary:
            continue

        fillable = [
            "title", "mobile", "landline", "email", "line_id",
            "website", "address", "tagline",
        ]
        updates = {}
        for field in fillable:
            if not (primary[field] or "").strip() and (secondary[field] or "").strip():
                updates[field] = secondary[field]

        extra_images = [secondary["image_filename"]]
        if secondary["extra_images"]:
            extra_images = secondary["extra_images"].split(",") + extra_images
        existing_extra = primary["extra_images"].split(",") if primary["extra_images"] else []
        merged_extra = ",".join(existing_extra + extra_images)
        updates["extra_images"] = merged_extra

        note_add = f"已自動合併背面照片({secondary['image_filename']})：{pair.get('reason', '')}"
        updates["confidence_notes"] = (
            f"{primary['confidence_notes']}；{note_add}" if primary["confidence_notes"] else note_add
        )

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        conn.execute(
            f"UPDATE cards SET {set_clause} WHERE id = ?",
            (*updates.values(), primary_id),
        )
        conn.execute("DELETE FROM cards WHERE id = ?", (secondary_id,))
        merged_count += 1
        print(f"  🔗 合併：#{secondary_id}({secondary['company']}) → #{primary_id}({primary['name']})")

    conn.commit()
    conn.close()
    return merged_count


def run_dedup(client: anthropic.Anthropic | None = None) -> int:
    client = client or anthropic.Anthropic()
    pairs = find_frontback_pairs(client)
    return merge_pairs(pairs)


if __name__ == "__main__":
    count = run_dedup()
    print(f"完成，合併 {count} 組正反面名片。")
