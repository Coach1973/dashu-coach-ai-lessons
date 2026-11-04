# -*- coding: utf-8 -*-
"""
「不用問的一直問」偵測（執行細則 N2 的程式版）——2026-11-04

起因：教練這週 204 句原話裡，「不用問的事一直問」是重複提醒的第二大類（約 8 次）。
舊的 stop_rules_master.py 規則 F 只提醒、不擋，擋不住。這支負責「高信心」的那一部分：
最終回覆的結尾幾行，用「要不要我／要我…嗎／還是先…？」向教練討許可。

放行條件（都是 N2 第①關「只有教練能做」或方向真的不明）：
  1. 該行出現花錢／對外發言／不可逆／需要教練登入等關鍵字
  2. 該行是「您想要什麼結果」這類真的方向不明的問句
  3. 同一則訊息裡有一行  【只有您能決定：…】  自己說明是哪一關（會被記錄，事後可稽核）

回測（2026-10-28～11-04 的 1,643 輪對話）見 docs 或接力棒；
被擋的訊息要二選一：直接做（交辦範圍內）／不做也不問，寫進接力棒「🔧AI 自己的清單」（範圍外的順手項目）。
"""
import re

GATE_WORDS = re.compile(
    r"付費|花錢|費用|扣(額度|點)|額度|推播|對外|代表(您|你|教練)|發(送|布|佈|出|信|訊息)|寄出|"
    r"刪除|刪掉|清掉|不可逆|覆蓋|force|強制推|reset --hard|密碼|驗證碼|簽章|授權|付款|訂閱|月租|"
    r"升級|重啟|重新啟動|登入|帳號|截圖鎖|批准|同意")
AMBIG = re.compile(r"您想要什麼結果|你想要什麼結果|多種.{0,6}(解讀|方式|方案)|方向(不明|模糊)|不確定您|"
                   r"是不是指|是不是語音輸入|請問您說的是|語音輸入錯誤")   # N3：聽不懂的詞要問；N2：方向不明只問一句
SUMMARY_OK = re.compile(r"要現在總結嗎|要總結嗎|現在總結")   # 教練 10/21 定的收尾框格式
CONDITIONAL = re.compile(r"^\s*[-*]?\s*(如果|假如|若)")        # 「如果您希望我…說一聲」是附帶說明，不是討許可的問句
ONLY_COACH_TAG = re.compile(r"【只有您能決定[：:][^】]{2,}】")

_Q = r"[？?]"
PATTERNS = [
    ("要不要", re.compile(r"要不要(我|把|順手|幫|直接|先|再|繼續).*" + _Q)),
    ("要我嗎", re.compile(r"(需要|要|想要)我.{0,30}(嗎|" + _Q + ")")),
    ("是否需要我", re.compile(r"(是否需要|是否要)我|(您|你)希望我")),
    ("還是先", re.compile(r"還是先.{0,30}" + _Q)),
    ("要現在做嗎", re.compile(r"要(現在|馬上|立刻|繼續|開始|先)[^。，；？?]{0,14}(做|開始|執行|處理|修|改|推|上線|嗎)[^。，；？?]{0,6}" + _Q)),
    ("可以嗎", re.compile(r"(可以|行|好)嗎" + _Q + r"\s*$")),
]


def _strip_quotes(s):
    s = re.sub(r"`[^`]*`", "", s)
    s = re.sub(r"「[^」]*」", "", s)
    s = re.sub(r"『[^』]*』", "", s)
    s = re.sub(r"\"[^\"]*\"", "", s)
    return s


def has_only_coach_tag(text):
    return bool(text and ONLY_COACH_TAG.search(text))


def find_asks(text, tail_lines=8):
    """回傳 [(類型, 該行前70字)]；只看最後 tail_lines 個非空行、跳過程式碼區塊與引號內的句型。"""
    if not text:
        return []
    lines, in_code = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not ln.strip():
            continue
        lines.append(ln)
    hits = []
    for ln in lines[-tail_lines:]:
        if GATE_WORDS.search(ln) or AMBIG.search(ln) or SUMMARY_OK.search(ln) or CONDITIONAL.search(ln):
            continue
        s = _strip_quotes(ln)
        for name, rx in PATTERNS:
            if rx.search(s):
                hits.append((name, ln.strip()[:70]))
                break
    return hits


def should_block(text):
    """True＝這則最終回覆該擋；同時回傳命中清單。"""
    hits = find_asks(text)
    if hits and not has_only_coach_tag(text):
        return True, hits
    return False, hits
