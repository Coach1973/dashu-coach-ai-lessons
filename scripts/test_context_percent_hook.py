#!/usr/bin/env python3
"""context_percent_hook.py 回歸測試：用假對話檔（不碰真的），各種情況跑一次。
執行：python scripts/test_context_percent_hook.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).with_name("context_percent_hook.py")
ok = True


def fake_transcript(d, sid, tokens):
    p = Path(d) / "projects" / "proj" / (sid + ".jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        {"type": "user", "message": {"content": "hi"}},
        {"type": "assistant", "message": {"model": "x", "usage": {"input_tokens": 5, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}},
        {"type": "assistant", "message": {"model": "x", "usage": {"input_tokens": 100, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": tokens - 1100}}},
        {"type": "assistant", "message": {"model": "<synthetic>", "usage": {"input_tokens": 1}}},
        "not json line",
    ]
    p.write_text("\n".join(x if isinstance(x, str) else json.dumps(x) for x in lines), encoding="utf-8")
    return p


def run(payload, marker, config_dir=None, window=None):
    env = {**os.environ, "CONTEXT_MARKER_DIR": marker, "PYTHONIOENCODING": "utf-8"}
    env.pop("CONTEXT_WINDOW", None)
    if window:
        env["CONTEXT_WINDOW"] = str(window)
    if config_dir:
        env["CLAUDE_CONFIG_DIR"] = config_dir
    data = payload if isinstance(payload, str) else json.dumps(payload)
    r = subprocess.run([sys.executable, str(HOOK)], input=data.encode("utf-8"), capture_output=True, env=env)
    return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("✅ " if cond else "❌ ") + name + ("" if cond else f"  → {detail}"))


with tempfile.TemporaryDirectory() as d:
    sid = "test-session-1"
    tp = fake_transcript(d, sid, 320000)  # 100 萬視窗下 32%
    m1 = tempfile.mkdtemp(dir=d)
    rc, out, err = run({"session_id": sid, "transcript_path": str(tp)}, m1)
    check("1. 32% 跨 30 線會提醒", rc == 0 and "跨過 30%" in out and "約 32%" in out, out + err)
    rc, out, _ = run({"session_id": sid, "transcript_path": str(tp)}, m1)
    check("2. 同一場同一條線不重複提醒", rc == 0 and out == "", out)
    tp.write_text(tp.read_text(encoding="utf-8").replace('"cache_read_input_tokens": 318900', '"cache_read_input_tokens": 518900'), encoding="utf-8")
    rc, out, _ = run({"session_id": sid, "transcript_path": str(tp)}, m1)
    check("3. 一次跳過 35/40/50 只提醒最高的 50", "跨過 50%" in out and "已過一半" in out, out)

    m2 = tempfile.mkdtemp(dir=d)
    rc, out, _ = run({"session_id": sid}, m2, config_dir=d)
    check("4. 沒給 transcript_path，靠 session_id 找到檔案", "跨過 50%" in out, out)

    m3 = tempfile.mkdtemp(dir=d)
    sid2 = "test-session-2"
    tp2 = fake_transcript(d, sid2, 120000)
    rc, out, _ = run({"session_id": sid2, "transcript_path": str(tp2)}, m3)
    check("5. 12% 不提醒", rc == 0 and out == "", out)
    rc, out, _ = run({"session_id": sid2, "transcript_path": str(tp2)}, m3, window=200000)
    check("6. CONTEXT_WINDOW 可覆寫（20 萬視窗下 60%）", "約 60%" in out and "視窗 20 萬" in out, out)

    for i, bad in enumerate(["", "not json", "{}", json.dumps({"session_id": "nope"})], 1):
        rc, out, err = run(bad, m3)
        check(f"7.{i} 壞輸入／找不到檔不出錯也不輸出", rc == 0 and out == "", out + err)

print("全部通過" if ok else "有失敗")
sys.exit(0 if ok else 1)
