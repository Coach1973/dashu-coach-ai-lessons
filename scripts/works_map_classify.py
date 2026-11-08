#!/usr/bin/env python3
"""大樹作品分類表：把 all-works/data.json 的每個作品分到一個主分類。
用法：python3 works_map_classify.py [--list]   （--list 印出每類清單供檢查）
被 build_works_map.py 引用。分類規則＝明確名單優先，其次關鍵字，最後看有沒有上架。"""
import json, re, sys
from pathlib import Path

HOME = Path.home()
DATA = HOME / "github_repos/all-works/data.json"
SKY = HOME / "github_repos/skyteam/index.html"

CATS = [
    ("course", "1", "課程・活動報名", "講座、工作坊、課程、聚會、邀請信——有日期、要人報名的網頁"),
    ("sky", "2", "顧問師天團・人才軍火庫", "天團總站，以及已進人才軍火庫的專家個人品牌頁"),
    ("tool", "3", "工具・技能・系統", "常用技能表、拆解工具、心法、SOP、分會系統、查詢頁"),
    ("unlisted", "4", "沒有上架的", "只在 GitHub 上、或已下架，沒有放進 event.bymyway.com 作品庫的網頁"),
    ("person", "5", "個人品牌頁（還沒進天團）", "已上架的個人網頁，但還沒收進人才軍火庫"),
    ("shop", "6", "店家・企業品牌網站", "餐飲、工廠、事務所、旅店等商家與公司的網頁"),
    ("org", "7", "協會・公益・社群", "協會、校友會、公益、Podcast 等團體型網頁"),
    ("story", "8", "故事・漫畫・報告書・教材", "漫畫、原話報告書、互動教材、送件包"),
    ("internal", "9", "內部・備份・測試", "程式倉庫、封存副本、測試檔——不是給人看的網頁"),
]

TOOLS = set("""my-tools bigtree-skills ai-go vip-club coach-vip-club reverse-skill rs-demo hero-opening-skill
course-signup-playbook tava-brand-web-playbook creator-survey idea-center cooling-off business-bni rongtree-sop
bni-gusest bni-trust all-works coach888 touchstone-plan bni-chapters team-bymyway team01-guests zhenzuan-guests
zhenxin-guests zhengui-guests zhencheng-guests teamwork-notes tainan-calender line-ti-shi-ce-shi-zhan
web-showcase worklucky-2026 msp-vote""".split())
COURSE = set("""tut-membership ai-image1202 taipeiema1017 ema1017 reemployment hing-sales bigtree-1107 bigtree-1003
bni-workshop 1107-taiwna-tea kr1003 ai-impact newmedia runforfuture 111-wei women-reepmployment superpower
time-secret bigtree consultant gold-excellence government-grow government-subsidies ai-forum-taichung ai-talk
diy-studio-workshop rpl-diy leadership-knot-workshop diy-outdoor-workshop diy-knot-workshop teamwork
peipeievent-411 invitation-leader invitation-peipei bni-training""".split())
STORY = set("""answer answer2 answer-tree ai-story game-1004 ai-team-strategy c-challenge lacks-1006 three-lacks bestteam
yousure submission ai-application-submission-package a-to-b rebreathe zaolin big-plan coach-case coach-case2
coach-case3 coach-case4 theunrestrictedwar tra-taitung""".split())
ORG = set("""nmda social-good social-club mbba rongtree tut-memory tut-alumni champagne-salon""".split())
PERSON = set("zhou-liangdun liu-weihua wei-gen tsai-peiru ohth-at-aj".split())
PERSON_WORDS = re.compile(r"老師|博士|董事長|牧師|執行長|總經理|會長|理事長|創辦人|教練|顧問|講師|社長|導師|作者|設計師|主持人|Dr\.|總監|醫師|長老|律師|師｜|\bCP\b")
COURSE_WORDS = re.compile(r"講座|工作坊|課程|報名|大會|聚會|說明會|培訓|研習|邀請")


def sky_slugs():
    s = SKY.read_text(encoding="utf-8")
    m = re.search(r'<script id="experts-data" type="application/json">(.*?)</script>', s, re.S)
    return {re.sub(r".*/curated/([^/]+)/?.*", r"\1", e["url"]) for e in json.loads(m.group(1)) if "/curated/" in e["url"]}


def classify(x, sky):
    i, name = x["id"], x["name"]
    if x["cat"] in ("程式／內部倉庫", "封存副本") or i.startswith("_archived") or re.search(r"test|backup|archive", i):
        return "internal"
    if i == "skyteam" or i in sky:
        return "sky"
    if x["delisted"]:
        return "unlisted"
    if i in TOOLS:
        return "tool"
    if i in COURSE:
        return "course"
    if i in STORY:
        return "story"
    if i in ORG:
        return "org"
    if i in PERSON:
        return "person"
    if i.startswith("ai-application-submission"):
        return "story"
    if not x["inRegistry"]:
        return "unlisted"
    if COURSE_WORDS.search(name):
        return "course"
    if PERSON_WORDS.search(name):
        return "person"
    return "shop"


def load():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    sky = sky_slugs()
    out = []
    for x in d["items"]:
        c = classify(x, sky)
        tags = []
        if not x["inRegistry"] and c not in ("unlisted", "internal"):
            tags.append("只在 GitHub")
        if x["delisted"]:
            tags.append("已下架")
        if x["private"] and c in ("internal", "unlisted"):
            tags.append("私有")
        out.append(dict(id=x["id"], name=re.sub(r"^【封存副本】", "", x["name"]).strip(), url=x["url"], cat=c,
                        updated=x["updated"], tags=tags, src=x["cat"]))
    return out, d["generated"]


if __name__ == "__main__":
    items, gen = load()
    for key, num, title, _ in CATS:
        g = [x for x in items if x["cat"] == key]
        print(f"\n## {num} {title}  ({len(g)})")
        if "--list" in sys.argv:
            for x in g:
                print("  ", x["id"][:24].ljust(24), x["name"][:36], x["tags"])
