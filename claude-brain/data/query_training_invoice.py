# -*- coding: utf-8 -*-
"""
查詢BNI培訓費開票資料，給教練問「XX開過票沒/是哪種發票」時直接查用，
不用每次都重新問教練是二聯還是三聯——統編/手機條碼/Email一旦記錄過就在這裡查得到。

用法：
    python3 query_training_invoice.py <姓名關鍵字>

資料來源：build_bni_training_admin.py 的 TAX_INFO/PHONE/INVOICES/PEOPLE_RAW
（跟教練開票查詢用的 bni_training_admin.html 同一份資料，這支只是給LINE/Telegram/
Hermes這類沒有瀏覽器介面的管道用文字輸出同一份事實）
"""
import sys

import build_bni_training_admin as db


TYPE_LABEL = {
    "company": "三聯(公司統編)",
    "carrier": "二聯(手機條碼/載具)",
    "personal": "二聯(Email，無載具)",
}


def search(keyword: str) -> list[str]:
    blocks = []
    for name, (chapter, att) in {n: (c, a) for n, (c, a, *_ ) in db.PEOPLE_RAW.items()}.items():
        if keyword not in name:
            continue
        due = db.PEOPLE_RAW[name][2]
        tax_info = db.TAX_INFO.get(name)
        phone = db.PHONE.get(name)
        invoices = db.INVOICES.get(name, [])
        invoiced_total = sum(i["amount"] for i in invoices if i["status"] == "已開立")

        lines = [f"👤 {name}" + (f"（{chapter}）" if chapter else "")]
        if tax_info:
            label = TYPE_LABEL.get(tax_info["type"], tax_info["type"])
            if tax_info["type"] == "company":
                lines.append(f"🧾 發票類型：{label} — {tax_info['label']}（統編{tax_info['taxid']}）")
            elif tax_info["type"] == "carrier":
                lines.append(f"🧾 發票類型：{label} — {tax_info['label']} {tax_info['code']}")
            elif tax_info["type"] == "personal":
                lines.append(f"🧾 發票類型：{label} — {tax_info['label']}（{tax_info['email']}）")
        else:
            lines.append("🧾 發票類型：⚠️尚無記錄，開票前需向教練確認")
        if phone:
            lines.append(f"📱 {phone[0]}　✉️ {phone[1]}")
        lines.append(f"💰 累計應收 ${due:,}　已開立 ${invoiced_total:,}"
                      + ("　✅已結清" if invoiced_total >= due else "　⚠️尚有差額"))
        if invoices:
            lines.append("📋 開票紀錄：")
            for i in sorted(invoices, key=lambda x: x["date"]):
                lines.append(f"　{i['date']}　{i['no']}　${i['amount']:,}　{i['status']}")
        else:
            lines.append("📋 開票紀錄：無")
        blocks.append("\n".join(lines))
    return blocks


def main() -> None:
    if len(sys.argv) < 2:
        print("用法：python3 query_training_invoice.py <姓名關鍵字>")
        raise SystemExit(1)
    keyword = " ".join(sys.argv[1:])
    blocks = search(keyword)
    if not blocks:
        print(f"查無「{keyword}」的培訓開票記錄")
        return
    print(f"共找到 {len(blocks)} 筆：\n\n" + "\n\n".join(blocks))


if __name__ == "__main__":
    main()
