#!/usr/bin/env python3
"""all_works_refresh.py 與 all-works 頁面的自動驗證（不連網、不碰正式資料、不推 GitHub）。

驗證：
  1. canon() 網址正規化：Python 與頁面 JS 兩邊對同一批網址結果必須一模一樣（去重靠它）
  2. 稱呼別名：曾志雄博士 → 曾博士；不產生「任教授」這種假稱呼
  3. build()：倉庫＋名冊合併、路徑對照（/DIY3 ↔ diy-studio-workshop）、封存副本、已下架、私有倉庫不外洩描述
  4. 頁面 JS（用 node 在假瀏覽器環境跑）：作品一覽合併、四種狀態、搜尋「曾博士」「Scott」找得到 scott-dr

執行：python3 scripts/test_all_works_refresh.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import all_works_refresh as m  # noqa: E402

PAGE = Path.home() / "github_repos" / "all-works" / "index.html"
FAILS = []


def check(name, cond, extra=""):
    print(("✅ " if cond else "❌ ") + name + (f"  {extra}" if extra and not cond else ""))
    if not cond:
        FAILS.append(name)


# ── 1. canon：Python vs 頁面 JS ─────────────────────────────────────
URLS = [
    "https://event.bymyway.com/curated/scott-dr/",
    "https://event.bymyway.com/curated/scott-dr/index.html",
    "https://Coach1973.github.io/BNI-Training/",
    "https://event.bymyway.com/curated/rongtree/invite.html?to=%E7%8E%8B&from=x#top",
    "https://theunrestrictedwar.netlify.app",
    "https://northern-tw.netlify.app/",
    "https://chapters.bymyway.com/admin",
    "https://claude.ai/artifact/ThW2E2kT2W9xk5PJUtmoQa",
    "https://event.bymyway.com/admin/login?next=/admin",
]
py = [m.canon(u) for u in URLS]
check("canon：去尾斜線與 index.html 後同網址", m.canon(URLS[0]) == m.canon(URLS[1]) == "event.bymyway.com/curated/scott-dr")
check("canon：大小寫與參數不影響", py[2] == "coach1973.github.io/bni-training" and py[3] == "event.bymyway.com/curated/rongtree/invite.html")
node = shutil.which("node")
if node and PAGE.exists():
    html = PAGE.read_text(encoding="utf-8")
    fn = re.search(r"function canon\(u\)\{.*?\n\}", html, re.S).group(0)
    out = subprocess.run([node, "-e", fn + f"\nconsole.log(JSON.stringify({json.dumps(URLS)}.map(canon)))"],
                         capture_output=True, text=True, timeout=20)
    check("canon：Python 與頁面 JS 結果一致", json.loads(out.stdout or "[]") == py, out.stderr[:200])
else:
    print("⚠️ 沒有 node 或頁面檔，略過 JS 對照")

# ── 2. 稱呼別名 ────────────────────────────────────────────────────
check("別名：曾志雄博士 → 曾博士", "曾博士" in m.aliases_for("曾志雄博士 Dr. Scott｜成大資工博士"))
check("別名：不切出「任教授」", "任教授" not in m.aliases_for("曾志雄博士（Dr. Scott），兼任助理教授"))

# ── 3. build() ────────────────────────────────────────────────────
def repo(name, private=False, pages=False, desc="", pushed="2026-10-01T00:00:00Z", archived=False):
    return {"name": name, "private": private, "has_pages": pages, "description": desc, "pushed_at": pushed,
            "html_url": f"https://github.com/Coach1973/{name}", "archived": archived}


repos = [repo("scott-dr", pages=True, pushed="2026-10-13T11:03:44Z"),
         repo("diy-studio-workshop", private=True, desc="秘密描述不可外洩"),
         repo("_archived_nmda"), repo("northern411", pages=True), repo("shihmin", pages=True),
         repo("lonely", pages=False)]
registry = {"sites": [
    {"slug": "scott-dr", "title": "曾志雄博士 Dr. Scott｜成大資工博士", "category": "食", "repo": "Coach1973/scott-dr",
     "event_url": "https://event.bymyway.com/curated/scott-dr/", "uploaded_at": "2026-10-13 11:43", "description": "曾志雄博士（Dr. Scott）"},
    {"slug": "shihmin", "title": "林士民", "category": "育", "repo": "Coach1973/shihmin", "listed": False,
     "unlisted_at": "2026-10-07 00:19", "event_url": "https://event.bymyway.com/curated/shihmin/", "uploaded_at": "2026-10-04 22:59"},
    {"slug": "ghost", "title": "倉庫改過名的站", "category": "樂", "event_url": "https://event.bymyway.com/curated/ghost/",
     "uploaded_at": "2026-09-01 10:00"}],
    "redirects": {"scott-old": "scott-dr"}}
pages = {"scott-dr": "https://coach1973.github.io/scott-dr/", "northern411": "https://coach1973.github.io/northern411/",
         "shihmin": "https://coach1973.github.io/shihmin/"}
data = m.build(repos, pages, registry, {"diy-studio-workshop": "event.bymyway.com/DIY3"})
by = {i["id"]: i for i in data["items"]}
check("build：6 個倉庫 + 1 個名冊獨有 = 7 筆", len(data["items"]) == 7, str(len(data["items"])))
check("build：策展網址優先當主網址", by["scott-dr"]["url"] == "https://event.bymyway.com/curated/scott-dr/")
check("build：更新日取較新的（倉庫 10/13 vs 名冊 10/13）", by["scott-dr"]["updated"] == "2026-10-13")
check("build：舊短網址轉址也算同一個作品", "event.bymyway.com/curated/scott-old" in by["scott-dr"]["keys"])
check("build：路徑對照 /DIY3", by["diy-studio-workshop"]["url"] == "https://event.bymyway.com/DIY3/"
      and "event.bymyway.com/diy3" in by["diy-studio-workshop"]["keys"])
check("build：私有倉庫不放描述", by["diy-studio-workshop"]["desc"] == "" and "秘密" not in json.dumps(by["diy-studio-workshop"], ensure_ascii=False))
check("build：封存副本標已下架", by["_archived_nmda"]["delisted"] and by["_archived_nmda"]["cat"] == "封存副本")
check("build：名冊 listed:false → 已下架", by["shihmin"]["delisted"] and by["shihmin"]["unlistedAt"] == "2026-10-07 00:19")
check("build：northern411 對照 northern-tw.netlify.app", "northern-tw.netlify.app" in by["northern411"]["keys"])
check("build：名冊獨有（找不到倉庫）也列出", "reg:ghost" in by and by["reg:ghost"]["inRegistry"])
check("build：沒網頁的倉庫分類＝程式／內部倉庫", by["lonely"]["cat"] == "程式／內部倉庫")
check("build：曾博士別名進資料", "曾博士" in by["scott-dr"]["aliases"])

# ── 4. 頁面 JS 在假瀏覽器裡跑（用真實 data.json 與一份假的作品一覽狀態）──────────
REAL = Path.home() / "github_repos" / "all-works" / "data.json"
if node and PAGE.exists() and REAL.exists():
    harness = r"""
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[1],'utf8');
const script=html.match(/<script>([\s\S]*)<\/script>/)[1];
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const items=JSON.parse(JSON.stringify(data.items));
const sc=items.find(i=>i.id==='scott-dr');
const state={
  coach888_layout:JSON.stringify({changyong:[sc.url, 'https://coach1973.github.io/ai-go/status.html','https://claude.ai/artifact/AAA'],recentlydeleted:['https://northern-tw.netlify.app/']}),
  coach888_names:JSON.stringify({[sc.url]:'曾志雄博士 Dr. Scott（作品集名）'}),
  coach888_items:JSON.stringify({'https://claude.ai/artifact/AAA':{name:'某份報告',badge:'報告'}}),
  coach888_badges:'{}',coach888_titles:JSON.stringify({changyong:'大樹常用',recentlydeleted:'最近刪除'})};
const els={};
const el=id=>els[id]||(els[id]={id,innerHTML:'',textContent:'',value:'',addEventListener(){},setAttribute(){},hasAttribute(){return false}});
const ctx={console,URL,Date,Map,Promise,Math,JSON,Object,Array,String,setTimeout,URLSearchParams,
  navigator:{},location:{search:''},window:{},
  document:{getElementById:el,addEventListener(){}},
  fetch:(u)=>{
    if(u.startsWith('data.json'))return Promise.resolve({ok:true,json:()=>Promise.resolve({generated:'2026-10-15T00:00:00Z',items})});
    if(u.includes('coach888'))return Promise.resolve({ok:true,json:()=>Promise.resolve(state)});
    return Promise.resolve({ok:true,json:()=>Promise.resolve([])});
  }};
ctx.window=ctx;vm.createContext(ctx);vm.runInContext(script,ctx);
setTimeout(()=>{
  const W=ctx.__allWorks,S=W.state;
  const find=id=>S.items.find(i=>i.id===id);
  const q=t=>{S.q=t;S.status='';S.src='';S.cat='';S.webOnly=false;return W.visible().map(i=>i.id)};
  const byStatus={};S.items.forEach(i=>byStatus[i.status]=(byStatus[i.status]||0)+1);
  console.log(JSON.stringify({total:S.items.length,byStatus,
    scStatus:find('scott-dr').status,scTitle:find('scott-dr').title,
    aigoKids:(find('ai-go')||{}).kids,aigoStatus:(find('ai-go')||{}).status,
    nortStatus:find('northern411').status,
    artifact:S.items.filter(i=>i.fromC888).map(i=>[i.title,i.category]),
    q1:q('曾博士').slice(0,5),q2:q('Scott').slice(0,5),q3:q('scott-dr'),q4:q('  SCOTT  博士 ').slice(0,5),q5:q('不存在的名字xyz')}));
},50);
"""
    out = subprocess.run([node, "-e", harness, str(PAGE), str(REAL)], capture_output=True, text=True, timeout=60)
    try:
        r = json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        r = {}
        print(out.stdout[-500:], out.stderr[-800:])
    check("頁面：能跑完並合併出項目", r.get("total", 0) >= 160, str(r.get("total")))
    check("頁面：scott-dr 有在作品一覽 → 已收進作品一覽", r.get("scStatus") == "works")
    check("頁面：顯示名稱用作品集裡的名字", "作品集名" in (r.get("scTitle") or ""))
    check("頁面：子頁面算到母站（ai-go 有子頁 → 已收進）", r.get("aigoStatus") == "works" and (r.get("aigoKids") or 0) >= 1, str(r.get("aigoKids")))
    check("頁面：被丟進「最近刪除」的 → 已下架", r.get("nortStatus") == "off", str(r.get("nortStatus")))
    check("頁面：作品一覽獨有的項目（claude.ai 報告）另列一筆", ["某份報告", "大樹常用"] in (r.get("artifact") or []), str(r.get("artifact")))
    check("搜尋「曾博士」找得到 scott-dr", "scott-dr" in (r.get("q1") or []), str(r.get("q1")))
    check("搜尋「Scott」找得到 scott-dr", "scott-dr" in (r.get("q2") or []), str(r.get("q2")))
    check("搜尋倉庫名「scott-dr」找得到", "scott-dr" in (r.get("q3") or []))
    check("搜尋多詞（大小寫、空白不拘）「SCOTT 博士」", "scott-dr" in (r.get("q4") or []), str(r.get("q4")))
    check("搜尋找不到的字回空", r.get("q5") == [], str(r.get("q5")))
    print("   狀態分布（假作品一覽）：", r.get("byStatus"))
else:
    print("⚠️ 略過頁面 JS 測試（缺 node、頁面或 data.json）")

print("\n結果：", "全部通過" if not FAILS else f"{len(FAILS)} 項失敗：{FAILS}")
sys.exit(1 if FAILS else 0)
