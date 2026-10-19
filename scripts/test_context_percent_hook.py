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
    check("2. 同一場同一條線不重複「跨線提醒」（過 30% 改為每句定期報告，教練 2026-10-17）", rc == 0 and "跨過 30%" not in out and "定期報告" in out, out)
    tp.write_text(tp.read_text(encoding="utf-8").replace('"cache_read_input_tokens": 318900', '"cache_read_input_tokens": 518900'), encoding="utf-8")
    rc, out, _ = run({"session_id": sid, "transcript_path": str(tp)}, m1)
    check("3. 一次跳過 35/40/45/50 只提醒最高的 50", "跨過 50%" in out and "已過一半" in out, out)

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


    # 定期報告：每 5 句報一次（跨線那句也算報過，重新數）
    m4 = tempfile.mkdtemp(dir=d)
    sid3 = "test-session-3"
    tp3 = fake_transcript(d, sid3, 120000)
    outs = [run({"session_id": sid3, "transcript_path": str(tp3)}, m4)[1] for _ in range(10)]
    check("8. 12% 第 1~4 句不出聲、第 5 句定期報告", all(o == "" for o in outs[:4]) and "定期報告" in outs[4] and "約 12%" in outs[4], outs[:5])
    check("9. 第 10 句再報一次", outs[9].count("定期報告") == 1 and all(o == "" for o in outs[5:9]), outs[5:10])
    m5 = tempfile.mkdtemp(dir=d)
    tp4 = fake_transcript(d, "test-session-4", 460000)
    rc, out, _ = run({"session_id": "test-session-4", "transcript_path": str(tp4)}, m5)
    check("10. 46% 跨 45 線（45 已加回）", "跨過 45%" in out, out)

    # 過 30% 之後每一句都報（教練 2026-10-17）：先跨線（第 1 句），之後 3 句每句都有定期報告
    m6 = tempfile.mkdtemp(dir=d)
    tp5 = fake_transcript(d, "test-session-5", 330000)
    outs = [run({"session_id": "test-session-5", "transcript_path": str(tp5)}, m6)[1] for _ in range(4)]
    check("11b. 過 30% 的跨線與定期報告都叫 AI 把容量放最後一句", "最後一句" in outs[0] and all("最後一句" in o for o in outs[1:]), outs)
    check("11. 33% 第 1 句跨線提醒、第 2~4 句每句都有定期報告（含額度提示）",
          "跨過 30%" in outs[0] and all("定期報告" in o and "約 33%" in o and "get_usage" in o for o in outs[1:]), outs)
    m7 = tempfile.mkdtemp(dir=d)
    tp6 = fake_transcript(d, "test-session-6", 290000)
    outs = [run({"session_id": "test-session-6", "transcript_path": str(tp6)}, m7)[1] for _ in range(5)]
    check("12. 29% 還是每 5 句才報（沒過線不加密）", all(o == "" for o in outs[:4]) and "定期報告" in outs[4] and "get_usage" not in outs[4], outs)
    check("12b. 30% 以下的定期報告維持放第一行（默契只針對過 30%）", "第一行" in outs[4] and "最後一句" not in outs[4], outs[4])

    # 教練 2026-10-19 默契：問「對話百分比剩多少」就直接給數字（12% 沒過線也要給）；平常話不出聲
    m8 = tempfile.mkdtemp(dir=d)
    tp7 = fake_transcript(d, "test-session-7", 120000)
    rc, out, _ = run({"session_id": "test-session-7", "transcript_path": str(tp7), "prompt": "對話百分比剩多少"}, m8)
    check("13. 12% 時問「對話百分比剩多少」→ 直接給：已用約 12%、剩約 88%", "約 12%" in out and "剩約 88%" in out, out)
    check("13d. 關鍵字回覆也叫 AI 放最後一句", "最後一句" in out, out)
    rc, out, _ = run({"session_id": "test-session-7", "transcript_path": str(tp7), "prompt": "目前對話1M的百分比是多少？"}, m8)
    check("13b. 另一種問法「目前對話1M的百分比是多少」也認得", "剩約 88%" in out, out)
    rc, out, _ = run({"session_id": "test-session-7", "transcript_path": str(tp7), "prompt": "幫我查一下預約頁"}, m8)
    check("13c. 平常的話（12%、非第 5 句）不出聲", out == "", out)

print("全部通過" if ok else "有失敗")
sys.exit(0 if ok else 1)
