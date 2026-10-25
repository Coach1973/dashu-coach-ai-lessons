#!/usr/bin/env python3
"""巴哈（peipei）用 synterolink Claude 的每日花費煞車。
2026-10-26 教練：巴哈預設 Haiku 5.5、最高 Sonnet 5、每天不超過 10 美金。
觸發：launchd WatchPaths 監看巴哈對話資料庫（每次回話都會寫入＝事件觸發，不是輪詢）。
- 今天（台灣時間）synterolink 花費加總 ≥ 上限 → 巴哈改回 MiniMax、私訊教練、留旗標
- 隔天第一次觸發，若旗標是前幾天留的 → 自動換回 Haiku（只還原煞車自己切掉的，不動教練手動改的）
花費＝小龍蝦按 openclaw.json 裡的單價算出的 cost.total（單價用官方長對話價，偏保守）。"""
import json, sqlite3, datetime, urllib.request, urllib.parse, os, sys
CAP = 10.0
CFG = '/Users/bymyway/.openclaw/openclaw.json'
DB = '/Users/bymyway/.openclaw/agents/peipei/agent/openclaw-agent.sqlite'
STATE = '/Users/bymyway/.openclaw/workspace/state/peipei_claude_cap.json'
LOG = '/Users/bymyway/Library/Logs/openclaw/peipei_claude_cap.log'
CLAUDE = 'synterolink/claude-haiku-5-5'
MINIMAX = 'minimax/MiniMax-M3'
COACH = '6124913915'
TPE = datetime.timezone(datetime.timedelta(hours=8))

def log(m):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    open(LOG, 'a').write(f"[{datetime.datetime.now(TPE):%Y-%m-%d %H:%M:%S}] {m}\n")

def notify(text):
    c = json.load(open(CFG))
    tok = c['channels']['telegram']['accounts']['bot_main']['botToken']
    d = urllib.parse.urlencode({'chat_id': COACH, 'text': text}).encode()
    urllib.request.urlopen(urllib.request.Request(f'https://api.telegram.org/bot{tok}/sendMessage', d), timeout=30)

def set_model(m):
    c = json.load(open(CFG))
    c['agents']['entries']['peipei']['model'] = m
    tmp = CFG + '.capguard.tmp'
    json.dump(c, open(tmp, 'w'), ensure_ascii=False, indent=2)
    os.replace(tmp, CFG)

def spent_today():
    start = datetime.datetime.now(TPE).replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000
    db = sqlite3.connect(f'file:{DB}?mode=ro', uri=True, timeout=10)
    total = 0.0
    for (ej,) in db.execute("select event_json from transcript_events where created_at>=? and event_json like '%synterolink%'", (start,)):
        try:
            msg = json.loads(ej).get('message') or {}
        except Exception:
            continue
        if msg.get('provider') == 'synterolink':
            total += float(((msg.get('usage') or {}).get('cost') or {}).get('total') or 0)
    return total

def main():
    today = datetime.datetime.now(TPE).strftime('%Y-%m-%d')
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    cur = json.load(open(CFG))['agents']['entries']['peipei']['model']
    s = spent_today()
    st['last_check'] = datetime.datetime.now(TPE).isoformat(timespec='seconds'); st['spent_today'] = round(s, 4); st['date'] = today
    if cur.startswith('synterolink/') and s >= CAP:
        set_model(MINIMAX); st['capped_on'] = today
        log(f'達上限 ${s:.2f} → 巴哈改回 MiniMax')
        notify(f'【軍師轉達】巴哈今天用 Claude 已花約 ${s:.2f}，達每日上限 ${CAP:.0f}，已自動改回 MiniMax。明天第一次對話會自動換回 Haiku。')
    elif cur == MINIMAX and st.get('capped_on') and st['capped_on'] < today and s < CAP:
        set_model(CLAUDE); st.pop('capped_on', None)
        log('新的一天 → 巴哈換回 Haiku')
        notify('【軍師轉達】新的一天，巴哈已自動換回 Claude Haiku（每日上限 $10）。')
    json.dump(st, open(STATE, 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f'錯誤：{e!r}')
        sys.exit(0)   # 煞車壞了不擋巴哈；錯誤留在 log
