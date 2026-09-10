# -*- coding: utf-8 -*-
"""
BNI培訓紀錄 - 內部後台（私有，不對外公開）

⚠️ 這支腳本產生的 bni_training_admin.html 含會員統編/個人載具/email/電話/應收金額/
   歷史發票比對，僅供教練開發票時查用。只放在這個私有大腦repo(mac-openclaw-workflows，
   GitHub上是private)，絕對不能複製進 github_repos/BNI-Training(那個是公開GitHub Pages)。

公開版(姓名/分會/出席)在 github_repos/BNI-Training/build_data.py，
兩邊的出席資料本體(PEOPLE_RAW)要同步一致，改一邊記得也改另一邊。

來源：
  knowledges/2026-08-17_培訓出席原始資料_教練提供.md（出席+累計應收金額）
  D:\\Users\\Desktop\\會員發票統編.docx（統編/載具對照，2026-06-16版）
  claude-brain/data/damushu_jiaoyu_invoices_1year_2026-08-17.csv（ezPay培訓費發票，店代337643900/344031309）
  ⚠️注意：不要跟 ezpay_invoices_2024-01-01_to_2026-08-17.csv(店代337391376/BNI台南南區入會續約費)搞混，
  那份都是$24,000~$39,800的入會/續約費，跟培訓場次$300~$1800完全是不同類別，不能拿來比對培訓應收。

更新資料：改下面 PEOPLE_RAW(跟公開版共用同一份出席事實)/TAX_INFO/PHONE/INVOICES，重跑
    python build_bni_training_admin.py
再 commit 到這個私有 repo 即可，教練任何一台機器 git pull 後直接開 bni_training_admin.html 查用。
"""
import io

SESSIONS = [
    {"id": "0413", "label": "4/13 進階MSP", "fee": 300},
    {"id": "0511", "label": "5/11 初階MSP", "fee": 300},
    {"id": "0611", "label": "6/11 主題培訓", "fee": 600},
    {"id": "0615", "label": "6/15 進階MSP", "fee": 300},
    {"id": "0720", "label": "7/20 初階MSP", "fee": 300},
    {"id": "0817", "label": "8/17 主題培訓", "fee": 300},
    {"id": "0907", "label": "9/7 初階MSP", "fee": 300},
    {"id": "0910", "label": "9/10 主題培訓", "fee": 600},
]
SID = [s["id"] for s in SESSIONS]

P, A, T, N = "present", "absent", "teacher0", "nodata"
SH = "share0"


def row(vals):
    return dict(zip(SID, vals))


# ---- 出席+應收金額（66人，跟公開版PEOPLE_RAW同一份事實，多帶金額）----
PEOPLE_RAW = {
    "連晧宇": ("真鑫", [A, P, P, P, P, P, P, P], 2700),
    "張騰文": ("真鑽", [P, P, P, P, A, P, P, P], 2700),
    "康文彬": ("真鑽", [A, P, A, P, A, P, N, N], 900),
    "陳淑玲": ("真鑽", [A, A, A, A, P, P, N, N], 600),
    "蔡珮彤": ("真鑫", [A, A, A, A, P, P, P, N], 900),
    "陳佳玲": ("真鑽", [A, A, A, A, A, P, N, N], 300),

    "買駿航": (None, [A, P, P, P, P, N, P, P], 2400),
    "柯朝陽": (None, [P, P, P, P, A, N, A, N], 1500),
    "吳亞平": (None, [A, P, P, P, P, N, N, N], 1500),
    "古禹澤": (None, [P, A, P, P, A, N, N, N], 1200),
    "李美花": (None, [P, A, P, P, A, N, P, N], 1500),
    "黃一恭": (None, [P, P, P, A, A, N, N, N], 1200),
    "張敬雍": (None, [P, A, P, P, T, N, N, P], 1800),
    "張晴晴": (None, [A, P, P, A, A, N, N, N], 900),
    "陳佩君": (None, [P, SH, P, T, T, T, T, SH], 900),
    "楊在珍": (None, [P, P, T, T, T, N, N, N], 600),
    "林佳伶": (None, [A, SH, P, T, T, N, N, N], 600),
    "杜亞洛": (None, [A, P, A, P, A, N, N, N], 600),
    "劉彥彬": (None, [A, P, A, P, A, N, N, N], 600),
    "許朝竣": ("真鑽", [P, A, A, P, P, N, N, N], 600),  # 7/20原缺席，跟同人重複記錄(曾誤植「許超尊」)核對後改出席
    "蔡瑞穠": (None, [A, A, A, P, P, N, N, N], 600),
    "莊政川": (None, [A, P, A, A, P, N, N, P], 1200),
    "楊博丞": (None, [A, P, A, A, P, N, N, N], 600),
    "陳俊源": (None, [A, P, A, A, P, N, A, N], 600),
    "林佳慧": (None, [A, P, A, A, P, N, N, N], 600),
    "陳欣佑": (None, [A, A, P, A, A, N, N, N], 600),  # 2026-08-18教練告知已離會，但他有真實發票紀錄(承恕法律事務所$1200已開立)，離會不影響已發生的金流，保留此筆供對帳
    "楊智帆": (None, [A, A, P, A, A, N, N, P], 1200),
    "邱南寅": (None, [A, A, P, A, A, N, N, P], 600),

    "宋映璇": (None, [P, N, N, N, N, N, N, N], 300),
    "郭展鴻": (None, [P, N, N, N, N, N, N, N], 300),
    "葉建葳": (None, [P, N, N, N, N, N, N, N], 300),
    "陳新典": (None, [P, N, N, N, N, N, N, N], 300),
    "顏淳峯": (None, [P, N, N, N, N, N, N, N], 300),
    "楊仁豪": (None, [P, A, A, T, T, T, N, P], 900),  # 教練2026-08-18提供4-8月開票總清冊：6/15、7/20、8/17皆擔任講師

    "王聖凱": (None, [N, P, N, N, N, N, N, P], 900),
    "吳玫萱": (None, [N, P, N, N, N, N, N, N], 300),
    "黃鑫豊": (None, [N, P, N, N, N, N, N, N], 300),
    "吳志煒": (None, [N, P, N, N, N, N, A, P], 900),
    "林尹渟": ("真鑫", [N, P, N, N, N, N, N, P], 900),
    "楊尚儒": (None, [A, P, A, T, A, A, P, P], 1200),  # 教練2026-08-18提供4-8月開票總清冊：6/15擔任講師
    "謝盛峰": ("真鑫", [N, P, N, N, N, N, N, N], 300),
    "范郁琪": ("真鑫", [N, P, N, N, N, N, N, N], 300),  # 教練更正原「范郁斌」姓名有誤

    "葉彤黎": ("真鑽", [N, N, N, P, N, N, N, P], 900),
    "伍芬群": ("真鑽", [N, N, N, P, N, N, N, N], 300),
    "吳三貴": ("真鑽", [N, N, N, P, N, N, N, P], 900),
    "林宜宏": (None, [N, N, N, P, N, N, P, N], 600),
    "徐偉倫": ("真鑫", [N, N, N, P, N, N, N, N], 300),
    "柯炫任": (None, [N, N, N, P, N, N, N, N], 300),
    "楊凱為": ("真鑫", [N, N, N, P, N, N, N, N], 300),

    "薛如媛": (None, [N, N, N, N, P, N, N, N], 300),
    "柯宗佑": (None, [N, N, N, N, P, N, N, P], 900),
    "林富郎": (None, [N, N, N, N, P, N, N, N], 300),
    "陳穗青": (None, [N, N, N, N, P, N, N, N], 300),
    "洪嘉妘": (None, [N, N, N, N, P, N, N, N], 300),
    "傅恩平": (None, [N, N, N, N, P, N, T, P], 900),
    "杜泱峻": ("真鑽", [N, N, N, N, P, N, P, P], 1200),  # 教練2026-08-18更正：原「杜泱畯」姓名有誤
    "郭馨文": (None, [N, N, N, N, P, N, N, P], 900),

    # 教練2026-08-18提供4-8月開票總清冊，這兩人MSP名單原本完全沒有，全程0元免收費(講師/分享人)
    "王彤": ("真誠", [T, SH, N, T, T, T, T, N], 0),
    "張羽家": ("真誠", [N, N, N, T, N, T, N, N], 0),
    "郭政輝": ("真鑽", [N, N, N, N, N, N, P, N], 300),
    "張育慈": ("真誠", [N, N, N, N, N, N, P, N], 300),  # 2026-09-10新會員，教練口頭確認要開票，統編待查(ezPay查無入會發票紀錄)
    "鄭樫峯": ("真鑽", [N, N, N, N, N, N, N, P], 600),
    "李孟哲": ("真鑽", [N, N, N, N, N, N, N, P], 600),
    "黃智宏": ("真鑽", [N, N, N, N, N, N, N, P], 600),
}

# ---- 統編/載具（來源：會員發票統編.docx，2026-06-16版，目前僅11人有資料）----
TAX_INFO = {
    "張騰文": {"type": "carrier", "label": "個人載具", "code": "LKZTH3E"},
    "張敬雍": {"type": "company", "label": "雍証豚畜產行", "taxid": "00434234"},
    "康文彬": {"type": "carrier", "label": "個人載具", "code": "B3BU7PV"},
    "許朝竣": {"type": "company", "label": "毫丞工業社", "taxid": "47805197"},
    "陳欣佑": {"type": "company", "label": "承恕法律事務所", "taxid": "09819116"},
    "楊智帆": {"type": "company", "label": "鴻羽網路有限公司", "taxid": "54082268"},
    "陳佳玲": {"type": "company", "label": "億生多有限公司", "taxid": "90636756"},
    "顏淳峯": {"type": "company", "label": "峰越企業有限公司", "taxid": "94007890"},
    "林宜宏": {"type": "company", "label": "明林股份有限公司", "taxid": "69291307"},
    "傅恩平": {"type": "personal", "label": "傳統二聯發票", "email": "fuenping@gmail.com"},
    "陳穗青": {"type": "carrier", "label": "個人載具", "code": "AMU2DXY"},
    "郭政輝": {"type": "company", "label": "展鑫精密實業社", "taxid": "99287483"},
    "鄭樫峯": {"type": "company", "label": "古鎰統包工程有限公司", "taxid": "00220958"},
    "李孟哲": {"type": "company", "label": "歐格企業社", "taxid": "40864451"},
}

# ---- 電話/Email（來源：BNI Connect官方「地區會員培訓報告」2026-08-17教練提供，跟61人MSP名單比對姓名后
#      45人有對到，16人查無(可能是還沒登記在BNI Connect或名字有出入)，剩下的16人維持待補）----
PHONE = {
    "張騰文": ("0925978176", "janjan0210@gmail.com"),
    "買駿航": ("0916071122", "hankmai@hotmail.com"),
    "柯朝陽": ("0916252199", "ted0916252199@gmail.com"),
    "吳亞平": ("0938276282", "aaeee81@yahoo.com.tw"),
    "古禹澤": ("0911402529", "kudyun123@gmail.com"),
    "李美花": ("0910-388-096", "l0910388096@gmail.com"),
    "黃一恭": ("0933274338", "golden463310@gmail.com"),
    "張敬雍": ("0909071516", "aa7661403@gmail.com"),
    "康文彬": ("062995666", "kboris002@yahoo.com.tw"),
    "張晴晴": ("+886922119111", "Forching.zhang@gmail.com"),
    "陳佩君": ("0988004118", "johnpeggy0706@gmail.com"),
    "陳淑玲": ("0927-808352", "c58suelin@gmail.com"),
    "楊在珍": ("0912181212", "a0912181212@gmail.com"),
    "林佳伶": ("+886 982156945", "lavisiontw@gmail.com"),
    "杜亞洛": ("062988090", "kingsman12330@gmail.com"),
    "劉彥彬": ("0980225525", "liujerry68@gmail.com"),
    "許朝竣": ("063565711", "lovepooh0212@gmail.com"),
    "蔡瑞穠": ("0933334570", "golife99@gmail.com"),
    "莊政川": ("0981897696", "j3939558569z39@gmail.com"),
    "楊博丞": ("0978001089", "jeff56381@gmail.com"),
    "陳俊源": ("0926916809", "chunyuan0410@gmail.com"),
    "林佳慧": ("0901174279", "a0983072095@gmail.com"),
    "楊智帆": ("0987511503", "me26cc@yahoo.com.tw"),
    "邱南寅": ("0913958599", "asionthree@yahoo.com.tw"),
    "陳佳玲": ("+886975628217", "wanli2300192@gmail.com"),
    "宋映璇": ("0905005303", "z0933408418@gmail.com"),
    "郭展鴻": ("0918989150", "chin.kwok2014@gmail.com"),
    "葉建葳": ("0923-711-725", "x52042001@gmail.com"),
    "陳新典": ("0900370777", "xin84513@gmail.com"),
    "顏淳峯": ("0900156339", "yanmusen27@gmail.com"),
    "楊仁豪": ("062566418", "sb930311@ms31.hinet.net"),
    "王聖凱": ("0929380309", "z2463412@gmail.com"),
    "吳玫萱": ("0966876261", "a50301201@gmail.com"),
    "黃鑫豊": ("0982107225", "a0982107225note5@gmail.com"),
    "吳志煒": ("0987895531", "koutianwuinteriordesign@gmail.com"),
    "楊尚儒": ("0909131345", "shangjyang@gmail.com"),
    "林宜宏": ("06 261 1181", "n41352007@gmail.com"),
    "柯炫任": ("0981947772", "iooming6180@yahoo.com.tw"),
    "薛如媛": ("062996630", "lyrhsueh@gmail.com"),
    "柯宗佑": ("0925285919", "a0925285919@gmail.com"),
    "林富郎": ("06-2996630", "frankzoy@yahoo.com.tw"),
    "洪嘉妘": ("0918891283", "c0918891283@gmail.com"),
    "傅恩平": ("0955467226", "fuenping@gmail.com"),
    "郭馨文": ("0919991131", "aa0963631151@gmail.com"),
    "陳穗青": ("0913729828", "julia660127@gmail.com"),
}

# ---- ezPay培訓費發票比對（來源：damushu_jiaoyu_invoices_1year_2026-08-17.csv，店代337643900/344031309）----
# 注意：跟BNI入會/續約費(店代337391376)是完全不同的發票類別，不可混用，本表只收培訓費金額量級($300~$3000)的紀錄。
INVOICES = {
    "張騰文": [{"date": "2026-03-18", "no": "ZK67264311", "amount": 900, "status": "已開立"}],
    "張敬雍": [
        {"date": "2026-03-18", "no": "ZK67264314", "amount": 1200, "status": "已開立"},
        {"date": "2026-06-30", "no": "BN78971203", "amount": 1200, "status": "已開立"},
    ],
    "康文彬": [{"date": "2026-03-18", "no": "ZK67264301", "amount": 900, "status": "已開立"}],
    "陳欣佑": [{"date": "2026-03-18", "no": "ZK67264307", "amount": 1200, "status": "已開立"}],
    "楊智帆": [
        {"date": "2025-11-07", "no": "VJ79571750", "amount": 600, "status": "已開立"},
        {"date": "2026-03-18", "no": "ZK67264313", "amount": 1200, "status": "已開立"},
    ],
    "陳佳玲": [{"date": "2026-03-20", "no": "ZK67264321", "amount": 600, "status": "已開立"}],
    "林宜宏": [{"date": "2026-03-18", "no": "ZK67264315", "amount": 300, "status": "已開立"}],
    "傅恩平": [{"date": "2026-03-18", "no": "ZK67264316", "amount": 900, "status": "已開立"}],
    "陳穗青": [{"date": "2026-03-19", "no": "ZK67264319", "amount": 600, "status": "已開立"}],
    "李美花": [{"date": "2026-03-18", "no": "ZK67264312", "amount": 600, "status": "已開立"}],
    "郭展鴻": [{"date": "2026-03-18", "no": "ZK67264303", "amount": 1200, "status": "已開立"}],
    "郭政輝": [{"date": "2026-09-10", "no": "FT00098555", "amount": 300, "status": "已開立"}],
    "李美花": [{"date": "2026-09-10", "no": "FT00098550", "amount": 300, "status": "已開立"}],
    "張騰文": [{"date": "2026-09-10", "no": "FT00098551", "amount": 300, "status": "已開立"}],
    "蔡珮彤": [{"date": "2026-09-10", "no": "FT00098553", "amount": 300, "status": "已開立"}],
    "林宜宏": [{"date": "2026-09-10", "no": "FT00098556", "amount": 300, "status": "已開立"}],
    "杜泱峻": [{"date": "2026-09-10", "no": "自訂091008", "amount": 900, "status": "已開立"}],
    "連晧宇": [{"date": "2026-09-10", "no": "自訂091009", "amount": 900, "status": "已開立"}, {"date": "2026-09-10", "no": "自訂091025(疑重複)", "amount": 600, "status": "已開立"}],
    "買駿航": [{"date": "2026-09-10", "no": "自訂091010", "amount": 900, "status": "已開立"}],
    "張敬雍": [{"date": "2026-09-10", "no": "自訂091011", "amount": 600, "status": "已開立"}],
    "傅恩平": [{"date": "2026-09-10", "no": "自訂091012", "amount": 600, "status": "已開立"}],
    "楊智帆": [{"date": "2026-09-10", "no": "自訂091013", "amount": 600, "status": "已開立"}],
    "黃智宏": [{"date": "2026-09-10", "no": "自訂091014", "amount": 600, "status": "已開立"}],
    "葉彤黎": [{"date": "2026-09-10", "no": "自訂091015", "amount": 600, "status": "已開立"}],
    "吳三貴": [{"date": "2026-09-10", "no": "自訂091016", "amount": 600, "status": "已開立"}],
    "李孟哲": [{"date": "2026-09-10", "no": "自訂091017", "amount": 600, "status": "已開立"}],
    "楊仁豪": [{"date": "2026-09-10", "no": "自訂091018", "amount": 600, "status": "已開立"}],
    "郭馨文": [{"date": "2026-09-10", "no": "自訂091019", "amount": 600, "status": "已開立"}],
    "林尹渟": [{"date": "2026-09-10", "no": "自訂091020", "amount": 600, "status": "已開立"}],
    "王聖凱": [{"date": "2026-09-10", "no": "自訂091021", "amount": 600, "status": "已開立"}],
    "莊政川": [{"date": "2026-09-10", "no": "自訂091022", "amount": 600, "status": "已開立"}],
    "吳志煒": [{"date": "2026-09-10", "no": "自訂091023", "amount": 600, "status": "已開立"}],
    "柯宗佑": [{"date": "2026-09-10", "no": "自訂091024(1200兩位待釐清)", "amount": 600, "status": "已開立"}],
    "鄭樫峯": [{"date": "2026-09-10", "no": "自訂091026", "amount": 600, "status": "已開立"}],
}

INVOICE_TYPE = {}


def tax_cell(info):
    if not info:
        return '<span class="missing">⚠️待補</span>'
    if info["type"] == "company":
        return '<span class="taxid">%s</span><br><span class="taxid-no">統編 %s</span>' % (info["label"], info["taxid"])
    if info["type"] == "carrier":
        return '<span class="taxid">個人載具</span><br><span class="taxid-no">%s</span>' % info["code"]
    if info["type"] == "personal":
        return '<span class="taxid">%s</span><br><span class="taxid-no">%s</span>' % (info["label"], info["email"])
    return '<span class="missing">⚠️待補</span>'


STATUS_MAP = {
    "present": ("present", "出席"),
    "absent": ("absent", "缺席"),
    "nodata": ("nodata", "-"),
    "teacher0": ("special", "🎤講師0元"),
    "share0": ("special", "🎤分享0元"),
}


def render_row(rank, name, chapter, att, due, tax_info, phone, invoices, invoice_type):
    invoiced_total = sum(i["amount"] for i in invoices if i["status"] == "已開立")
    if not invoices:
        inv_status, inv_cls = "未查到", "inv-none"
    elif invoiced_total >= due:
        inv_status, inv_cls = "已開立", "inv-ok"
    else:
        inv_status, inv_cls = "部分/待核對", "inv-partial"

    cells = ['<td class="rank">%d</td>' % rank, '<td class="name">%s</td>' % name,
             '<td class="chapter">%s</td>' % (chapter or '<span class="nodata">-</span>')]
    for sid in SID:
        cls, label = STATUS_MAP[att[sid]]
        cells.append('<td class="%s">%s</td>' % (cls, label))
    cells.append('<td class="total-score">$%s</td>' % format(due, ","))
    cells.append('<td class="taxcell">%s</td>' % tax_cell(tax_info))
    if phone:
        phone_html = '%s<br><span class="taxid-no">%s</span>' % (phone[0], phone[1])
    else:
        phone_html = '<span class="missing">⚠️待補</span>'
    cells.append('<td class="phonecell">%s</td>' % phone_html)
    if invoices:
        detail = "<br>".join("%s $%s (%s)" % (i["date"], format(i["amount"], ","), i["status"]) for i in invoices)
        inv_html = '<span class="%s">%s</span><br><span class="inv-amt">%s</span>' % (inv_cls, inv_status, detail)
    else:
        inv_html = '<span class="%s">%s</span>' % (inv_cls, inv_status)
    cells.append('<td class="invcell">%s</td>' % inv_html)
    cells.append('<td class="typecell">%s</td>' % (invoice_type or '<span class="missing">待勾選</span>'))
    has_tax = "1" if tax_info else "0"
    return '<tr class="data-row" data-name="%s" data-hastax="%s">%s</tr>' % (name, has_tax, "".join(cells))


def main():
    people = []
    for name, (chapter, att, due) in PEOPLE_RAW.items():
        people.append((name, chapter, row(att), due))
    people.sort(key=lambda x: (-x[3], x[0]))

    total_people = len(people)
    total_due = sum(p[3] for p in people)
    total_invoiced = sum(sum(i["amount"] for i in INVOICES.get(p[0], []) if i["status"] == "已開立") for p in people)
    with_tax = sum(1 for p in people if TAX_INFO.get(p[0]))
    with_invoice = sum(1 for p in people if INVOICES.get(p[0]))
    with_phone = sum(1 for p in people if PHONE.get(p[0]))
    missing_tax = total_people - with_tax

    header_ths = "".join('<th>%s</th>' % s["label"] for s in SESSIONS)
    rows_html = "\n".join(
        render_row(i + 1, name, chapter, att, due, TAX_INFO.get(name), PHONE.get(name),
                   INVOICES.get(name, []), INVOICE_TYPE.get(name))
        for i, (name, chapter, att, due) in enumerate(people)
    )

    html = HTML_TEMPLATE.format(
        header_ths=header_ths, rows_html=rows_html, total_people=total_people,
        total_due="{:,}".format(total_due), total_invoiced="{:,}".format(total_invoiced),
        with_tax=with_tax, with_invoice=with_invoice, with_phone=with_phone, missing_tax=missing_tax,
    )
    with io.open("bni_training_admin.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("bni_training_admin.html done, %d people" % total_people)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>【內部後台/勿外流】BNI培訓開票查詢表</title>
<style>
:root {{
    --bg-color: #0b0f19; --panel-bg: #1a2333; --text-main: #e2e8f0; --text-muted: #64748b;
    --neon-blue: #00f0ff; --neon-green: #10b981; --neon-red: #ff2a2a; --neon-gold: #f59e0b;
}}
body {{ background: var(--bg-color); color: var(--text-main); font-family: 'Helvetica Neue','PingFang TC','Microsoft JhengHei',sans-serif;
    margin: 0; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; }}
.warn-banner {{ width: 100%; max-width: 1300px; background: #3a1414; border: 1px solid var(--neon-red); color: #ffb4b4;
    border-radius: 8px; padding: 10px 18px; margin-bottom: 20px; font-size: .88rem; text-align: center; }}
.header-container {{ text-align: center; margin-bottom: 28px; }}
h1 {{ color: var(--neon-blue); font-size: 2rem; letter-spacing: 2px; margin: 0; text-shadow: 0 0 15px rgba(0,240,255,.5); }}
p.subtitle {{ color: var(--text-muted); font-size: 1rem; margin-top: 10px; }}
.stats-row {{ display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; width: 100%; max-width: 1300px; margin-bottom: 24px; }}
.stat-card {{ background: var(--panel-bg); border: 1px solid #2d3748; border-radius: 10px; padding: 16px 22px; min-width: 150px; text-align: center; }}
.stat-card .num {{ font-size: 1.6rem; font-weight: bold; color: var(--neon-blue); }}
.stat-card .num.gold {{ color: var(--neon-gold); }}
.stat-card .num.red {{ color: var(--neon-red); }}
.stat-card .lbl {{ font-size: .78rem; color: var(--text-muted); margin-top: 4px; }}
.controls {{ width: 100%; max-width: 1300px; display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }}
.controls input[type=text] {{ flex: 1; min-width: 200px; background: var(--panel-bg); border: 1px solid #2d3748;
    color: var(--text-main); padding: 10px 14px; border-radius: 8px; font-size: 1rem; }}
.controls button {{ background: var(--panel-bg); border: 1px solid #2d3748; color: var(--text-muted);
    padding: 10px 16px; border-radius: 8px; cursor: pointer; font-size: .9rem; }}
.controls button.active {{ color: var(--neon-blue); border-color: var(--neon-blue); }}
.table-wrapper {{ width: 100%; max-width: 1300px; background: var(--panel-bg); border-radius: 12px;
    overflow-x: auto; border: 1px solid #2d3748; }}
.table-wrapper table {{ min-width: 1550px; }}
table {{ width: 100%; border-collapse: collapse; text-align: center; }}
thead {{ background: #0f172a; border-bottom: 2px solid var(--neon-blue); }}
th {{ padding: 12px 8px; color: var(--neon-blue); font-weight: 600; white-space: nowrap; font-size: .82rem; }}
td {{ padding: 10px 8px; border-bottom: 1px solid #2d3748; font-size: .88rem; }}
tbody tr:hover {{ background: rgba(0,240,255,.05); }}
.present {{ color: var(--neon-green); font-weight: bold; }}
.absent {{ color: var(--neon-red); font-weight: bold; }}
.nodata {{ color: #475569; }}
.special {{ color: var(--neon-gold); font-weight: bold; font-size: .78rem; }}
.rank {{ color: #94a3b8; font-weight: bold; }}
.name {{ font-weight: bold; color: #fff; text-align: left; padding-left: 14px; white-space: nowrap; }}
.chapter {{ color: #94a3b8; font-size: .82rem; }}
.total-score {{ color: var(--neon-gold); font-weight: bold; }}
.taxcell, .invcell, .phonecell {{ font-size: .78rem; line-height: 1.5; white-space: nowrap; }}
.taxid {{ color: var(--text-main); }}
.taxid-no {{ color: var(--text-muted); font-size: .72rem; }}
.missing {{ color: var(--neon-red); font-size: .75rem; }}
.inv-ok {{ color: var(--neon-green); font-weight: bold; }}
.inv-partial {{ color: var(--neon-gold); font-weight: bold; }}
.inv-none {{ color: var(--text-muted); }}
.inv-amt {{ color: var(--text-muted); font-size: .7rem; }}
.typecell {{ font-size: .78rem; color: var(--text-muted); }}
.note-panel {{ width: 100%; max-width: 1300px; margin-top: 32px; background: #1a2333; border-radius: 12px;
    border: 1px solid #2d3748; padding: 24px 30px; box-sizing: border-box; }}
.note-panel h2 {{ color: var(--neon-gold); font-size: 1rem; margin: 0 0 14px 0; border-bottom: 1px dashed #475569; padding-bottom: 10px; }}
.note-panel ul {{ color: #e2e8f0; line-height: 1.9; margin: 0; padding-left: 22px; font-size: .88rem; }}
</style>
</head>
<body>
<div class="warn-banner">⚠️ 內部後台，含會員統編/個人載具/email/電話等個資，僅供教練開發票查用，不要外傳或公開連結</div>
<div class="header-container">
    <h1>BNI培訓開票查詢表</h1>
    <p class="subtitle">姓名 → 統編/載具/電話/應收金額/歷史發票比對　私有版，不會出現在公開網站</p>
</div>
<div class="stats-row">
    <div class="stat-card"><div class="num">{total_people}</div><div class="lbl">出席人次總計</div></div>
    <div class="stat-card"><div class="num gold">${total_due}</div><div class="lbl">累計應收金額</div></div>
    <div class="stat-card"><div class="num">{with_tax}</div><div class="lbl">已有統編/載具</div></div>
    <div class="stat-card"><div class="num red">{missing_tax}</div><div class="lbl">⚠️尚無統編對照</div></div>
    <div class="stat-card"><div class="num gold">{with_phone}</div><div class="lbl">已有電話/Email</div></div>
    <div class="stat-card"><div class="num">{with_invoice}</div><div class="lbl">已比對到歷史發票</div></div>
</div>
<div class="controls">
    <input type="text" id="searchBox" placeholder="搜尋姓名...">
    <button class="filter-btn active" data-filter="all">全部</button>
    <button class="filter-btn" data-filter="missing">⚠️尚無統編</button>
    <button class="filter-btn" data-filter="hastax">已有統編/載具</button>
</div>
<div class="table-wrapper">
<table>
<thead><tr>
    <th>排名</th><th style="text-align:left;padding-left:14px;">姓名</th><th>分會</th>
    {header_ths}
    <th>累計應收</th><th>統編/載具</th><th>電話/Email</th><th>歷史發票比對</th><th>發票類型</th>
</tr></thead>
<tbody id="tbody">
{rows_html}
</tbody>
</table>
</div>
<div class="note-panel">
<h2>📋 使用說明</h2>
<ul>
<li>這是給教練自己開ezPay發票時查用的內部頁面，資料來源跟公開版(BNI-Training)共用同一份出席事實，多帶了統編/電話/email/金額。</li>
<li>電話欄位目前完全沒有資料來源，教練口述提供後改<code>build_bni_training_admin.py</code>的<code>PHONE</code>字典重新產生即可。</li>
<li>「歷史發票比對」只比對 damushu_jiaoyu 培訓費CSV(店代337643900/344031309)，跟BNI入會/續約費(店代337391376，金額都是$24,000起跳)是不同類別，不會混在一起。多數比對到的日期早於本輪培訓(4/13)起點，僅供核對「這個人是否開過培訓票」的參考基準，不是本輪自動勾稽。</li>
<li>資料落差：本輪整理時多找到「陳穗青」1人(原60人名單漏收)，另外「李美花」「郭展鴻」統編對照表雖未填但ezPay已有個人姓名發票記錄，一併標記。</li>
</ul>
</div>
<script>
const searchBox = document.getElementById('searchBox');
const rows = Array.from(document.querySelectorAll('.data-row'));
let currentFilter = 'all';
function applyFilters() {{
    const q = searchBox.value.trim();
    rows.forEach(r => {{
        const nameMatch = !q || r.dataset.name.includes(q);
        let filterMatch = true;
        if (currentFilter === 'missing') filterMatch = r.dataset.hastax === '0';
        if (currentFilter === 'hastax') filterMatch = r.dataset.hastax === '1';
        r.style.display = (nameMatch && filterMatch) ? '' : 'none';
    }});
}}
searchBox.addEventListener('input', applyFilters);
document.querySelectorAll('.filter-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        applyFilters();
    }});
}});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
