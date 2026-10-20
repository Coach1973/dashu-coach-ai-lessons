#!/usr/bin/env python3
"""把大樹教練的全套規則同步進每個「雲端對話會用到的 GitHub 倉庫」。

為什麼有這支（2026-10-20 教練：「聯想的 Claude 很笨、還在問同不同意」查證結果）：
  雲端對話（claude.ai/code）只讀得到「該倉庫」裡的 CLAUDE.md 與 .claude/settings.json，
  讀不到 Mac 的 ~/.claude/。以前只有 workspace 與外層 ~/.openclaw 有開場注入，
  bni-chapters／my-tools／rongtree 等倉庫的雲端對話沒有 21 守則、沒有亮燈、沒有交件流程。

做法（事件觸發，不輪詢）：
  來源（~/.claude/CLAUDE.md、模型分工規則、cloud_sync/CLOUD_RULES_COMMON.md、repo_kit/*）有變
  → 對 cloud_repos.json 裡的每個倉庫，在 state/cloud_rules_clones/ 的小型暫存複製（只下載
    CLAUDE.md 與 .claude/）產生規則包 → commit → push 到倉庫預設分支。
  觸發點：session_end_auto_push.sh（每則回覆結束；來源沒變就 0.1 秒離開，不碰網路）。

規則包內容（放在倉庫 .claude/coach-rules/）：
  RULES.md       完整規則（私有倉庫＝特助心法 21 守則＋執行細則 N1~N10 原文；公開倉庫＝只有雲端行為規則）
  core.md        開場注入的精簡版（SessionStart 印出，控制在 10,000 字以內避免被截斷）
  session_start.sh／prompt_hook.sh／stop_check.py   三支 hook（只在 CLAUDE_CODE_REMOTE=true 才動）
  VERSION        來源指紋與時間
  另：.claude/settings.json 掛上 hook（已有的設定會合併保留）、CLAUDE.md 最上方加一小段指標。

用法：
  sync_rules_to_repos.py              來源有變才同步（hook 用）
  sync_rules_to_repos.py --force      強制全部重推
  sync_rules_to_repos.py --only NAME  只處理一個倉庫
  sync_rules_to_repos.py --dry-run    只建置、不推送（印出會改什麼）
  sync_rules_to_repos.py add NAME     把新倉庫加進清單並立刻同步
  sync_rules_to_repos.py status       讀回每個倉庫線上的版本，對照現在的來源
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent                       # workspace 或其 worktree 的根
STATE = Path(os.environ.get("CLOUD_RULES_STATE", "/Users/bymyway/.openclaw/workspace/state"))
CONF = HERE / "cloud_repos.json"
KIT = HERE / "repo_kit"
GLOBAL_CLAUDE = Path.home() / ".claude" / "CLAUDE.md"
GLOBAL_FALLBACK = ROOT / "cloud_sync" / "GLOBAL_CLAUDE.md"
MODEL_RULE = ROOT / "knowledges" / "模型分工規則_Opus與Sonnet.md"
COMMON = ROOT / "cloud_sync" / "CLOUD_RULES_COMMON.md"
SYNCED = STATE / "cloud_rules_synced.json"
CLONES = STATE / "cloud_rules_clones"
LOG = STATE / "cloud_rules_sync.log"
GIT = ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com"]
ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "PATH": f"/opt/homebrew/bin:/usr/local/bin:{os.environ.get('PATH', '')}"}

BEGIN = "<!-- COACH-RULES:BEGIN（由 Mac 自動同步，請勿手改）-->"
END = "<!-- COACH-RULES:END -->"
CORE_LIMIT = 9500          # 開場注入的字數上限（Claude Code 對過長的 hook 輸出只給預覽）
KEEP_HEADS = ("# 特助心法", "# 特助執行細則", "# 🚦 問教練之前的三關", "# ⚡ 任務執行時的自我對照")
HOOK_MARK = "coach-rules"


def log(msg):
    STATE.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(cmd, cwd=None, check=True, timeout=180):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=ENV, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])} 失敗：{(r.stderr or r.stdout).strip()[-300:]}")
    return r


# ── 來源與建置 ──────────────────────────────────────────────

def source_files():
    g = GLOBAL_CLAUDE if GLOBAL_CLAUDE.exists() else GLOBAL_FALLBACK
    return [g, MODEL_RULE, COMMON, Path(__file__).resolve(), *sorted(KIT.glob("*"))]


def source_hash():
    h = hashlib.sha256()
    for p in source_files():
        h.update(p.name.encode())
        data = p.read_bytes() if p.exists() else b""
        if p.name.endswith("CLAUDE.md"):      # 「最後同步：時間」每天自己會變，不算規則有變，免得每天白推一次
            data = b"\n".join(l for l in data.split(b"\n") if "最後同步".encode() not in l)
        h.update(data)
    return h.hexdigest()


def sections(text):
    """依 '# ' 一級標題切段（忽略程式碼區塊內的 #）。回傳 [(標題行, 內文含標題)]"""
    out, cur, head, fence = [], [], None, False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("# "):
            if head is not None:
                out.append((head, "\n".join(cur)))
            head, cur = line, [line]
        else:
            cur.append(line)
    if head is not None:
        out.append((head, "\n".join(cur)))
    return out


def drop_subsection(text, sub_prefix):
    """拿掉 '## sub_prefix…' 這一小節（到下一個 ## 或 # 為止）"""
    out, skip = [], False
    for line in text.splitlines():
        if line.startswith("## ") or line.startswith("# "):
            skip = line.startswith(sub_prefix)
        if not skip:
            out.append(line)
    return "\n".join(out)


def full_rules_body():
    g = GLOBAL_CLAUDE if GLOBAL_CLAUDE.exists() else GLOBAL_FALLBACK
    parts = []
    for head, body in sections(g.read_text(encoding="utf-8")):
        if head.startswith(KEEP_HEADS):
            if head.startswith("# 特助執行細則"):
                body = drop_subsection(body, "## 新舊對照")
            parts.append(body.rstrip() + "\n")
    return "\n".join(parts)


def condensed_rules(g_text):
    """開場用精簡版：使命願景理念＋21 守則（標題＋定義行，原文）＋N1~N10（標題＋第一句）"""
    lines = g_text.splitlines()
    out = ["## 特助心法（精簡；原文與教練親筆詮釋在 RULES.md）"]
    for key in ("使命：", "願景：", "理念："):
        for ln in lines:
            if ln.startswith(key):
                out.append(ln)
                break
    for i, ln in enumerate(lines):
        if re.match(r"\*\*\d\d\. ", ln):
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            out.append(f"{ln.strip()} {nxt}")
    out.append("")
    out.append("## 執行細則 N1~N10（精簡）")
    for i, ln in enumerate(lines):
        m = re.match(r"\*\*N(\d+)\. ", ln)
        if m and int(m.group(1)) >= 8:
            continue
        if m:
            body = ""
            for nx in lines[i + 1:i + 8]:
                nx = nx.strip()
                if nx and not nx.startswith("對應守則") and not nx.startswith("撐住它") and not nx.startswith("案例"):
                    body = nx
                    break
            body = body.lstrip("- ").strip()
            first = body.split("。")[0] + "。" if "。" in body else body
            if first.endswith("：。") or first.endswith("："):
                first = ""
            out.append(f"{ln.strip()} {first[:150]}".rstrip())
    out.append("（N8 記憶、N9 交接、N10 作品集收錄是 Mac 系統的事，雲端不用做，由 Mac 軍師接手；原文在 RULES.md）")
    return "\n".join(out)


def build_files(variant, src_hash):
    """回傳 {相對路徑: 內容}（不含 settings.json 與 CLAUDE.md，那兩個要和既有內容合併）"""
    common = COMMON.read_text(encoding="utf-8").strip()
    stamp = f"版本 {src_hash[:8]}，{datetime.now():%Y-%m-%d %H:%M} 同步"
    files = {}
    if variant == "full":
        g_text = (GLOBAL_CLAUDE if GLOBAL_CLAUDE.exists() else GLOBAL_FALLBACK).read_text(encoding="utf-8")
        model_rule = MODEL_RULE.read_text(encoding="utf-8").strip()
        files[".claude/coach-rules/RULES.md"] = (
            f"# 大樹教練雲端對話規則全文（{stamp}）\n\n"
            "> 來源：Mac 的 ~/.claude/CLAUDE.md（特助心法 21 守則＋執行細則，教練欽定、一字不差）、模型分工規則、雲端專屬規則。\n"
            "> 由 Mac 自動同步，請勿手改。身份：雲端對話＝軍師（Sonnet 5 以上），稱呼「大樹教練」；下面原文中提到小龍蝦／Telegram／VPS／hook 的部分，是 Mac 與小龍蝦系統的說明，雲端對話只需遵守其中的守則與細則精神。\n\n"
            f"{common}\n\n---\n\n{model_rule}\n\n---\n\n{full_rules_body()}")
        core = (f"☁️ 大樹教練雲端規則已載入（{stamp}）。完整原文在 .claude/coach-rules/RULES.md，"
                f"第一次回覆前請先用 Read 讀完它（約 {len(files['.claude/coach-rules/RULES.md']) / 10000:.1f} 萬字）。\n\n"
                f"{common}\n\n{condensed_rules(g_text)}\n")
    else:
        files[".claude/coach-rules/RULES.md"] = (
            f"# 大樹教練雲端對話規則（公開倉庫精簡版，{stamp}）\n\n"
            "> 這個倉庫是公開的，所以只放雲端行為規則，不放特助心法全文。完整守則在教練的 Mac 上。\n"
            "> 由 Mac 自動同步，請勿手改。\n\n" + common + "\n")
        core = f"☁️ 大樹教練雲端規則已載入（{stamp}，公開倉庫精簡版）。\n\n{common}\n"
    if len(core) > CORE_LIMIT:
        raise RuntimeError(f"core.md 太長（{len(core)} 字 > {CORE_LIMIT}），開場注入會被截斷；請縮短來源")
    files[".claude/coach-rules/core.md"] = core
    files[".claude/coach-rules/VERSION"] = f"{src_hash}\n{datetime.now().isoformat(timespec='seconds')}\nvariant={variant}\n"
    for k in KIT.glob("*"):
        files[f".claude/coach-rules/{k.name}"] = k.read_text(encoding="utf-8")
    return files


def our_hook_entries():
    def ent(cmd):
        return {"hooks": [{"type": "command", "command": cmd}]}
    base = '"$CLAUDE_PROJECT_DIR/.claude/coach-rules/'
    return {
        "SessionStart": ent(f'F={base}session_start.sh"; [ -f "$F" ] && bash "$F"; exit 0'),
        "UserPromptSubmit": ent(f'F={base}prompt_hook.sh"; [ -f "$F" ] && bash "$F"; exit 0'),
        "Stop": ent(f'F={base}stop_check.py"; [ -f "$F" ] && python3 "$F"; exit 0'),
    }


def merge_settings(existing_text):
    data = json.loads(existing_text) if existing_text.strip() else {}
    hooks = data.setdefault("hooks", {})
    for event, entry in our_hook_entries().items():
        lst = hooks.setdefault(event, [])
        lst[:] = [e for e in lst if HOOK_MARK not in json.dumps(e, ensure_ascii=False)]   # 先清掉舊版自己的，再放新版
        lst.insert(0, entry)
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def claude_md_block():
    return (f"{BEGIN}\n"
            "## ☁️ 大樹教練的雲端對話規則（雲端對話必讀）\n"
            "你是大樹教練的 AI 軍師（稱呼「大樹教練」），不是一般的程式助手。開場時系統會自動送上完整規則；"
            "如果你沒看到「☁️ 大樹教練雲端規則已載入」，第一件事先用 Read 讀 `.claude/coach-rules/RULES.md`。\n"
            "最重要的三件事：①每則交辦的回覆第一行先亮燈（🔵Haiku／🟢Sonnet／🟣Opus）；"
            "②方向清楚就直接做完，不要問「同不同意」；"
            "③推不上 main 是正常的：推到自己的 `claude/*` 分支，並在 `docs/to_junshi/` 寫信給 Mac 軍師（做了什麼、怎麼驗證、哪裡只用假資料測過），由 Mac 驗證、合併、上線。\n"
            f"{END}\n")


def upsert_claude_md(existing):
    block = claude_md_block()
    if BEGIN in existing and END in existing:
        pre = existing[:existing.index(BEGIN)]
        post = existing[existing.index(END) + len(END):].lstrip("\n")
        return pre + block + ("\n" + post if post else "")
    return block + ("\n" + existing if existing.strip() else "")


# ── 倉庫處理 ────────────────────────────────────────────────

def load_conf():
    return json.loads(CONF.read_text(encoding="utf-8"))


def repo_info(owner, name):
    r = run(["gh", "repo", "view", f"{owner}/{name}", "--json", "isPrivate,defaultBranchRef"], check=False, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"讀不到 {name} 的資訊：{r.stderr.strip()[-200:]}")
    d = json.loads(r.stdout)
    return d["isPrivate"], d["defaultBranchRef"]["name"]


def ensure_clone(owner, name, branch):
    d = CLONES / name
    url = f"https://github.com/{owner}/{name}.git"
    if not (d / ".git").is_dir():
        CLONES.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "-q", "--depth", "1", "--branch", branch, "--single-branch", "--filter=blob:none", "--sparse", url, str(d)])
        run(["git", "sparse-checkout", "set", "--no-cone", "/CLAUDE.md", "/.claude/"], cwd=d)
    run(["git", "fetch", "-q", "--depth", "1", "origin", branch], cwd=d)
    if run(["git", "status", "--porcelain"], cwd=d).stdout.strip():
        raise RuntimeError(f"{name} 的暫存複製有沒處理完的修改（{d}），請先看一下再重跑")
    run(["git", "merge", "-q", "--ff-only", f"origin/{branch}"], cwd=d)
    return d


def sync_repo(name, src_hash, dry_run, variant_override=None):
    conf = load_conf()
    owner = conf.get("owner", "Coach1973")
    is_private, branch = repo_info(owner, name)
    variant = variant_override or conf.get("variant", {}).get(name) or ("full" if is_private else "public")
    d = ensure_clone(owner, name, branch)
    files = build_files(variant, src_hash)
    sp = d / ".claude" / "settings.json"
    files[".claude/settings.json"] = merge_settings(sp.read_text(encoding="utf-8") if sp.exists() else "")
    cp = d / "CLAUDE.md"
    files["CLAUDE.md"] = upsert_claude_md(cp.read_text(encoding="utf-8") if cp.exists() else "")
    if dry_run:                 # 試跑：只比對、不寫任何東西
        diff = [rel for rel, c in files.items()
                if rel != ".claude/coach-rules/VERSION" and (not (d / rel).exists() or (d / rel).read_text(encoding="utf-8") != c)]
        return f"{name}：[試跑] {'會更新 ' + '、'.join(diff) if diff else '已是最新'}（{variant}）"
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if rel == ".claude/coach-rules/VERSION" and p.exists() and p.read_text().splitlines()[:1] == content.splitlines()[:1]:
            continue          # 指紋一樣就不要只為了時間戳重推
        p.write_text(content, encoding="utf-8")
    for p in (d / ".claude/coach-rules").glob("*.sh"):
        p.chmod(0o755)
    run(["git", "add", "CLAUDE.md", ".claude"], cwd=d)
    if not run(["git", "diff", "--cached", "--name-only"], cwd=d).stdout.strip():
        return f"{name}：已是最新（{variant}）"
    changed = run(["git", "diff", "--cached", "--stat"], cwd=d).stdout.strip().splitlines()[-1]
    msg = f"[Mac] 雲端對話規則包同步（{src_hash[:8]}，{variant}）：亮燈、不問同不同意、交件流程"
    run(GIT + ["commit", "-q", "-m", msg], cwd=d)
    r = run(["git", "push", "-q", "origin", f"HEAD:{branch}"], cwd=d, check=False)
    if r.returncode != 0:                     # 被別人搶先推了：重抓、重蓋、再推一次
        run(["git", "fetch", "-q", "--depth", "1", "origin", branch], cwd=d)
        run(["git", "rebase", "-q", f"origin/{branch}"], cwd=d)
        run(["git", "push", "-q", "origin", f"HEAD:{branch}"], cwd=d)
    sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=d).stdout.strip()
    return f"{name}：已推上 {branch} {sha}（{variant}；{changed}）"


def cmd_status(args):
    conf = load_conf()
    cur = source_hash()[:8]
    for name in conf["repos"]:
        r = run(["gh", "api", f"repos/{conf.get('owner', 'Coach1973')}/{name}/contents/.claude/coach-rules/VERSION", "-q", ".content"], check=False, timeout=60)
        if r.returncode != 0:
            print(f"❌ {name}：線上沒有規則包")
            continue
        import base64
        first = base64.b64decode(r.stdout.strip()).decode().splitlines()[0][:8]
        print(f"{'✅' if first == cur else '⚠️ 過期'} {name}：線上 {first}／現在 {cur}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="sync", choices=["sync", "add", "status"])
    ap.add_argument("name", nargs="?")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    if args.cmd == "status":
        return cmd_status(args)
    conf = load_conf()
    if args.cmd == "add":
        if not args.name:
            sys.exit("用法：add <倉庫名>")
        if args.name not in conf["repos"]:
            conf["repos"].append(args.name)
            CONF.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        args.only, args.force = args.name, True

    src = source_hash()
    done = json.loads(SYNCED.read_text()) if SYNCED.exists() else {"hash": "", "repos": {}}
    todo = [args.only] if args.only else conf["repos"]
    if not args.force and not args.dry_run:
        todo = [n for n in todo if done["repos"].get(n, {}).get("hash") != src]
    if not todo:
        return                                  # 來源沒變：安靜離開，不碰網路
    # 同時只跑一個
    lock = STATE / "cloud_rules_sync.lock"
    if lock.exists() and time.time() - lock.stat().st_mtime < 600:
        return
    lock.write_text(str(os.getpid()))
    try:
        for n in todo:
            try:
                res = sync_repo(n, src, args.dry_run)
                log(res)
                if not args.dry_run:
                    done["repos"][n] = {"hash": src, "time": datetime.now().isoformat(timespec="seconds")}
            except Exception as e:                # 單一倉庫失敗不影響其他
                log(f"❌ {n}：{e}")
        if not args.dry_run:
            done["hash"] = src
            SYNCED.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
