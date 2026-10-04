#!/usr/bin/env python3
"""把《AI企業團隊戰略》舊對話紀錄，做成「教練原話報告書」網頁（形態同 game-1004 原話逐字報告書）。

來源：knowledges/2026-10-04_AI企業團隊戰略_原始對話紀錄.txt（教練 2026-10-04 提供，ChatGPT 對話，Round 01～04）
原則：原話一律用「原始檔第 N 行」直接取出，不經手改字；軍師註另行標示，不混入原話。
教練 vs AI 檔內沒有角色標籤，依格式判斷：教練語音轉文字幾乎沒有標點，AI 回覆有標點與全形符號。
產出：/Users/bymyway/github_repos/game-1004 以外的暫存資料夾 out/index.html，再驗證原話與原始檔逐字相同。
"""
import html
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "knowledges" / "2026-10-04_AI企業團隊戰略_原始對話紀錄.txt"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/strategy_report/index.html")

LINES = SRC.read_text(encoding="utf-8").split("\n")

# (段落標題, 段落說明, [(行號或行號元組, 小標, 軍師註), ...])
STAGES = [
    ("第一輪收尾 → 要整理資料", "第一輪（檔內標示 Round 01｜2026/09/05）談完後，教練的感謝與下一步指示。", [
        (2, "感謝：這是兩三年來最深刻的一次討論", "教練對 AI 的肯定；他說 AI 可以在半夜三更接下任何話題、把人內心最想要的東西挖出來，是目前沒有人類做得到的。AI 此前回應「十五分鐘後見」。"),
        (4, "指示：請把整理的資料給我，準備下一輪", "此後 AI 交出「Round 01 專案接力包」（原檔第 5 行起，是 AI 寫的報告，不收）。"),
    ]),
    ("第二輪：要求封存、約定提醒", "第二輪結尾，教練要求 AI 把這輪對話封存成接力包，並約定怎麼提醒。", [
        (620, "追問：完成的時候你會通知我嗎", "簡體字應是語音轉文字的結果。AI 答：完成後會告訴你。"),
        (622, "提醒：除非我說話，其他聲音（含導航聲）一概不用管", "教練說這裡面有導航的聲音，怕 AI 以為是在跟它說話。"),
        (624, "約定：我每隔兩分鐘問你好了沒，你每次都回答我", "AI 此前答覆：沒辦法在教練沒說話時主動通知。"),
        (626, "下令：非常明確告訴你，請你開始封存", "AI 回「好的」。"),
        (629, "追問：請問已經好了嗎", "第一次問（文字輸入）。"),
        (630, "再問：好了。請問已經好了嗎", "⚠️ 軍師註：此行依「簡體、問句、緊接在教練前一則之後」判斷為教練語音，把握度略低於其他則；原檔沒有角色標籤。"),
    ]),
    ("第三輪：催交接力包（Word／PDF／純文字）", "第三輪結尾，教練催 AI 交出實體檔案。", [
        ((670, 671), "要求：文字檔不用太費勁，Word、PDF、純文字三份都要，要有品質", "這一則是同一次送出的兩行文字。檔內緊接著出現一行系統提示：Data analysis isn't available right now。"),
        (674, "催問：到底整理得怎麼樣？整理好了沒？", "檔內在這則前一行標有「今天 下午2:40」，應是這則的時間。"),
        (706, "宣布：終於我們可以開始第四回合了", "AI 回應：Round 04 要從「他第一次真正理解 BNI 的時候，最先要明白的那一件事」開始。"),
        (708, "回答：是", "回答 AI 上一句的確認。"),
        (710, "先確認：第三回合的報告有沒有包含第一、第二回合的資訊", "AI 答：有放進來，但是壓縮過的戰略地圖，不是逐字合併本。"),
    ]),
    ("第四輪：BNI 到底是什麼？陌生人為什麼要來？", "教練一邊用比喻回答、一邊反問 AI，逼 AI 用「世界級行銷大師」的腦袋想出與眾不同的招募方式（目標：年底新建三個分會）。", [
        (712, "兩個比喻：全球連鎖加盟系統＋企業健身房", "回答 AI：一個陌生又有企圖心的人，第一次接觸 BNI 最先要理解什麼。語音原文「倭軍健身房」，教練 10-04 確認＝World Gym（W-O-R-L-D G-Y-M），原話原樣保留。"),
        (714, "反問：你要贏得客戶的信任該做什麼？——BNI 就是讓你把這些事做到位", "回答 AI：怎麼用一句話讓對方知道這不只是交朋友。"),
        (716, "接續：讓優秀的企業老闆看見，你想讓別人看到什麼樣的品牌", "接續上一則（中間 AI 只回「嗯嗯嗯嗯」）。"),
        (718, "證據很多；但問題是「知道」跟「做到」之間有距離", "回答 AI：接下來最關鍵的具體證據是什麼。用「瘦下來會穿漂亮衣服、知道但做不到」比喻：大家都知道 BNI 有幫助，要讓他們做到才是最大的問題。"),
        (720, "帶團隊的邏輯：強制的東西不會長久，不被信任是最大的懲罰", "回答 AI：這樣的招募方式貼不貼近你。說明自己的信仰與帶區域的文化：創業的人本來就不想被管。"),
        (722, "疑問：為什麼你會問三支團隊呢", "AI 前一句問：你希望三支團隊的核心成員最優先具備什麼特質？教練隨後追問這個問題。"),
        (724, "對啊，那你會再問我什麼問題", "AI 認錯後，教練請它說出下一個問題。"),
        (726, "追問：在 Round 04 你的定位是誰？你用什麼角度來問我？", "AI 答：研究夥伴與反向驗證者。"),
        (728, "我是演講高手；年底要新建三個分會；反問：從沒去過的人為什麼加入健身房", "教練說明討論目的：他今年年底要新建三個全新的分會。並說：若 AI 能回答健身房的問題，BNI 一樣有答案。原話裡的「倭郡健身房」同為 World Gym 的語音諧音（教練 10-04 確認過「倭軍健身房」＝World Gym）。"),
        (730, "再反問：看到健身房招牌或業務員招募，他加入的動機是什麼", "請 AI 用最高智慧自由回答。"),
        (732, "我的答案：想變強、已經不錯但想更好；重點不是告訴別人 BNI 有多好", "教練肯定 AI「是天才」，並說明：重點是對方有沒有意識到事業的瓶頸，意識到溝通就容易。"),
        (734, "更深的挑戰：九千人都在招募；「你來推銷我加入＝BNI 需要我」是最大的誤區", "回答 AI：「這樣的方向有跟你對齊嗎」。提到全台灣 28 個加盟區、9000 多個會員，以及「能開一萬家店」「35 萬的企業家」。"),
        (736, "任務：給你戴高帽子，請你扮演世界級行銷大師，給我讓對方心甘情願的方案", "教練交付 AI 的正式任務。"),
        (739, "要求：更深入、更大膽、另類思考、獨特賣點", "AI 前一句提出「篩選願意成長的人」，教練說「還不錯」但要更勝一籌。"),
        (742, "請求：把這個案子縮到淺顯易懂再說一次", "AI 前一句提出「換遊戲：企業成長診斷」。"),
        (744, "差強人意：全台至少三千人都會這樣說，我還是在紅海裡", "教練從銷售起家，指出「診斷痛點」是每個做銷售的都懂的話術。"),
        (746, "我們的優勢是做培訓：先為他創造價值，再說我們用 BNI 模式", "AI 前一句提出「企業成長診斷教練」的定位。教練說這在第一輪就談過，現在又接上、是「完美的閉環」。"),
        (748, "OkayOkay", "語音附和。"),
        (750, "一部分對，但現實問題在哪裡呢，我舉個例子", "AI 前一句提出「企業家成長平台，先給價值再帶到 BNI」。"),
        (752, "BNI 知名度已經很大，最後一定會發現是 BNI，那種場景機率太低", "教練指出「先不講 BNI」模型的致命弱點。"),
        (754, "對，終於抓到重點：為什麼要選擇我們這個團隊，這才是好問句", "AI 前一句把問題改成「在大家都知道 BNI 的前提下，為什麼值得選擇我們」。"),
        (756, "人是環境的產物：團隊有一群優秀的人，新人自然跟著做", "應是回答自己剛提的好問句「為什麼要選擇我們這個團隊」（原檔沒有明確的提問，屬推測）。用健身房裡肌肉很大的人都做同一個動作的畫面說明環境帶動。語音原文「無化驅動」，語意疑為「文化驅動」，原樣保留。"),
        (758, "插話：音量可不可以再大聲一點，你越講越小聲", "語音對話中的現場要求。"),
        (761, "這才是真正的競爭力：整個文化、整個團隊去驅動，不是個人話術", "回應 AI：把這種文化型的競爭力落地成新分會的日常動作，是值得深挖的題目。"),
        (763, "沒錯，然後呢，哈囉", "催 AI 往下說。"),
        (765, "請求：把選項再送給我聽一下", "AI 前一句提出三個可深入方向。"),
        (767, "三個提問都不好；最遠方是設計初次接觸的美好體驗與流程", "這個流程可以在正式例會、咖啡會議或線上會議，「但這個會議是要經過流程的計畫」。"),
        (769, "附和：對沒錯說的對啊然後呢", "語音附和（開頭「Cheers」「mm-hmm」是語音轉文字的雜訊，原樣保留）。"),
        (771, "請求：再說一次沒聽得懂", "請 AI 重複上一段。"),
        (773, "我想到一個 idea 你可以記錄：我那邊有非常多見證", "AI 剛結論「把第一次接觸流程寫成可複製版本」。"),
        (775, "見證：360 行行行出狀元，100 個以上案例直接攤在他眼前，問他「你是誰？」", "教練說這是他要的殺傷力。語音原文「混臉鴨」語意不明，原樣保留。"),
        (777, "一百個案例就在我的案例資料庫當中", "AI 前一句問要不要從收集一百個案例的架構開始。"),
        (779, "要做到自動化、自動篩選，只剩有意願的人才來找我", "說明為什麼要做這套線上流程：讓對方出現在他面前時，已經知道自己不足、渴望學習、也看過成功案例，只想問還需要具備什麼條件才能加入團隊。"),
        (781, "我已有一套方法：輸入專業 level，AI 立即產生他的「產業服務列」", "語音原文「產業伏變」「產業服務列」，語意不明，疑與「產業鏈」有關，未經教練確認，原樣保留。教練要和 AI 討論的是把它做成具體、可執行的流程。"),
        (783, "談了快一個小時：Windows count 夠嗎？要總結、準備 Round 5 了嗎", "提醒 AI 上下文長度。語音原文「Windows count」，教練 10-04 確認＝context window。"),
        (785, "結束談話；我會用文字至少提醒你三次，盡快生成 PDF 和純文字檔", "原話說「這些都是網會的題材」。語音原文「網會」，教練 10-04 確認＝網頁，原話原樣保留。AI 答：我現在開始準備。"),
        (787, "追問：還需要多久把這次對話整理成第五回合的前置基礎？什麼時候給報告", "教練提到他們已經形成一個完美的閉環。簡體字應是語音轉文字的結果。"),
        (790, "催問：好了嗎？", "檔內在這則前一行標有「今天 下午5:06」，應是這則的時間。AI 答：產檔工具碰到使用量限制，PDF 和文字檔都還沒成功。"),
    ]),
]

THEMES = [
    ("兩個比喻：全球連鎖加盟系統／企業健身房", ["兩個比喻：全球連鎖加盟系統＋企業健身房"]),
    ("贏得信任＝把事情做到位；強制不會長久；不被信任是最大的懲罰", ["反問：你要贏得客戶的信任該做什麼", "帶團隊的邏輯"]),
    ("「知道」不等於「做到」", ["證據很多"]),
    ("最大誤區：「你來推銷我加入＝BNI 需要我」（其實是我需要 BNI）", ["我的答案", "更深的挑戰"]),
    ("九千人都在拉人 → 紅海 → 要換戰場、要與眾不同", ["更深的挑戰", "要求：更深入", "差強人意", "我們的優勢是做培訓", "BNI 知名度已經很大"]),
    ("「為什麼要選擇我們這個團隊」才是好問句", ["對，終於抓到重點"]),
    ("人是環境的產物：文化驅動、團隊驅動", ["人是環境的產物", "這才是真正的競爭力"]),
    ("初次接觸要有經過計畫的美好體驗與流程", ["三個提問都不好"]),
    ("見證與 100 個案例＝證據牆", ["我想到一個 idea", "見證：360", "一百個案例"]),
    ("自動篩選有意願的人＋AI 產業服務列 → 做出可執行流程", ["要做到自動化", "我已有一套方法"]),
    ("目的：年底新建三個全新的分會", ["我是演講高手"]),
    ("跟 AI 的工作約定：封存、提醒、三份檔案要有品質", ["追問：完成的時候", "約定：我每隔兩分鐘", "下令：非常明確", "要求：文字檔", "結束談話"]),
]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def main() -> None:
    cards = []
    n = 0
    for stage_title, stage_desc, items in STAGES:
        for key, title, note in items:
            n += 1
            nums = key if isinstance(key, tuple) else (key,)
            text = "\n".join(LINES[i - 1] for i in nums)
            cards.append(dict(n=n, nums=nums, title=title, note=note, text=text, stage=stage_title, stage_desc=stage_desc))

    total_chars = sum(len(c["text"].replace("\n", "")) for c in cards)
    toc, body, last_stage = [], [], None
    for c in cards:
        if c["stage"] != last_stage:
            last_stage = c["stage"]
            toc.append(f'<li class="stage">{esc(c["stage"])}</li>')
            body.append(f'<h2 class="stage-h" style="font-size:19px">{esc(c["stage"])}</h2><div class="stage-desc">{esc(c["stage_desc"])}</div>')
        line_label = f'原始檔第 {c["nums"][0]} 行' if len(c["nums"]) == 1 else f'原始檔第 {c["nums"][0]}～{c["nums"][-1]} 行'
        toc.append(f'<li><a href="#m{c["n"]}">第 {c["n"]} 則 · {esc(c["title"])}</a></li>')
        body.append(
            f'<section class="card" id="m{c["n"]}">\n'
            f'<div class="meta"><span class="no">第 {c["n"]} 則</span><span class="time">{line_label}</span>'
            f'<span class="cnt">{len(c["text"].replace(chr(10), ""))} 字</span></div>\n'
            f'<div class="note"><b>{esc(c["title"])}</b><br><span>軍師註（非教練原話）：{esc(c["note"])}</span></div>\n'
            f'<div class="verbatim" data-msg="{c["n"]}">{esc(c["text"])}</div>\n</section>'
        )

    theme_li = []
    for theme, keys in THEMES:
        refs = sorted({c["n"] for c in cards for k in keys if c["title"].startswith(k) or k in c["title"]})
        if refs:
            theme_li.append(f'<li>{esc(theme)}：' + "、".join(f'<a href="#m{r}">第 {r} 則</a>' for r in refs) + "</li>")

    low = next(c["n"] for c in cards if 630 in c["nums"])
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>教練原話報告書｜AI 企業團隊戰略（BNI × AI × 教育訓練，Round 01～04）</title>
<style>
body{{margin:0;background:#f4f1ea;color:#222;font-family:-apple-system,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;line-height:1.8;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:18px 14px 60px}}
h1{{font-size:24px;line-height:1.4;margin:6px 0 4px}}
.sub{{color:#666;font-size:14px;margin-bottom:14px}}
.box{{background:#fff;border-left:5px solid #2f6b4f;padding:12px 16px;border-radius:6px;margin:14px 0;font-size:15px}}
.box.warn{{border-left-color:#b5651d}}
.card{{background:#fff;border-radius:10px;padding:14px 16px;margin:18px 0;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
.meta{{display:flex;flex-wrap:wrap;gap:10px;font-size:13px;color:#555;margin-bottom:6px}}
.no{{background:#2f6b4f;color:#fff;border-radius:12px;padding:0 10px}}
.note{{font-size:14px;color:#6b4a1a;background:#fbf3e3;border-radius:6px;padding:6px 10px;margin-bottom:8px}}
.note span{{color:#8a6a3a}}
.verbatim{{white-space:pre-wrap;word-break:break-word;font-size:18px;border-top:1px dashed #ccc;padding-top:10px}}
.stage-desc{{font-size:14px;color:#555;margin:-6px 0 4px}}
ol.toc{{font-size:15px;padding-left:22px}}
ol.toc a{{color:#2f6b4f;text-decoration:none}}
ol.toc li.stage{{list-style:none;margin-left:-22px;margin-top:10px;font-weight:700;color:#444}}
ul.themes{{font-size:15px;padding-left:22px}}
ul.themes a{{color:#2f6b4f;text-decoration:none}}
code{{background:#eee;padding:1px 6px;border-radius:4px}}
</style>
</head>
<body>
<div class="wrap">
<h1>教練原話報告書｜AI 企業團隊戰略</h1>
<div class="sub">主題：BNI × AI × 教育訓練（年底新建三個分會的招募戰略）｜來源：教練 2026-10-04 提供的舊對話紀錄《AI企業團隊戰略》（檔內第一輪標示 2026/09/05，Round 01～04）｜共 {len(cards)} 則教練發言、{total_chars} 字</div>

<div class="box">
<b>這份報告書是做什麼的</b><br>
教練要求：把這份舊的原始資料，做成跟「商務遊戲／AI 百人導師」同形態的「教練原話報告書」。下面每一則「原話」都是從原始檔指定的行直接取出，沒有改寫、沒有刪減、沒有潤飾；每則都標了「原始檔第 N 行」，可以回頭核對。
</div>
<div class="box warn">
<b>給下一個對話框的軍師</b><br>
１．先讀完本檔全部原話。<br>
２．<b>只收教練說的話。</b>原始檔裡 AI（ChatGPT）寫的四份接力包／報告，以及 AI 的回覆，都不收；教練在第一～三輪的完整逐字對話，原檔最後一段寫明保存在各 Round 的原始網頁，這份檔案裡沒有。<br>
３．原始檔沒有「誰說的」標籤，教練與 AI 是依格式判斷：教練的語音轉文字幾乎沒有標點，AI 的回覆有標點。唯一把握度較低的是第 {low} 則，已在軍師註標明。<br>
４．原話是語音輸入，有諧音字、簡體字、英文雜訊（如「Cheers」「mm-hmm」）照原樣保留，不要自行更正。軍師註裡標「教練 10-04 確認」的，是教練事後親口確認過的諧音；標「疑為」或「語意不明」的，是推測，<b>沒有經過教練確認</b>。<br>
５．每則上方「軍師註」是軍師加的導讀，不是教練說的話，已用不同底色區隔。真正的原話只有下方白底大字那一塊。
</div>

<h2 style="font-size:19px">主題索引（軍師整理，非教練原話）</h2>
<ul class="themes">{''.join(theme_li)}</ul>

<h2 style="font-size:19px">目錄</h2>
<ol class="toc">{''.join(toc)}</ol>

<h2 style="font-size:19px">教練原話（依原始檔先後）</h2>
{chr(10).join(body)}
</div>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")

    # 逐字驗證：從做好的網頁把每則原話抽出來，要跟原始檔指定行完全相同
    built = OUT.read_text(encoding="utf-8")
    bad = 0
    for c in cards:
        m = re.search(rf'<div class="verbatim" data-msg="{c["n"]}">(.*?)</div>\n</section>', built, flags=re.S)
        got = html.unescape(m.group(1))
        want = "\n".join(LINES[i - 1] for i in c["nums"])
        if got != want:
            bad += 1
            print("❌ 不一致：第", c["n"], "則")
    print(f"共 {len(cards)} 則、{total_chars} 字；逐字比對不一致：{bad}；輸出 {OUT}")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
