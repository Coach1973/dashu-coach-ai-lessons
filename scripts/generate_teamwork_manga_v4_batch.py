#!/usr/bin/env python3
"""
漫畫版 v4 batch — 跑剩 27 張（p02~p28）+ 通知節奏 A（每張推 Telegram）
教練 2026-09-26 08:40 拍板：v4 鎖臉 OK，開工跑剩下 27 張
"""
import sys
import json
import re
import time
from pathlib import Path

sys.path.insert(0, '/Users/bymyway/.openclaw/workspace/scripts')

from generate_teamwork_manga_v4 import (
    REFS,
    IDENTITY_BIBLE_V4,
    call_lk88_edit_multi,
    png_to_jpeg,
    push_telegram,
    get_api_key,
    get_telegram_bot_token,
)

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain" / "data" / "comic_source_20260926_teamwork_manga"
LOG_FILE = DATA_DIR / "v4_batch.log"


def remove_old_recurring_protagonist(prompt: str) -> str:
    """移除原 tava-ai prompt 中 Recurring protagonist 段，避免跟 v4 IDENTITY BIBLE 衝突"""
    if "Recurring protagonist 'the Coach'" in prompt:
        # 移除從 "Recurring protagonist 'the Coach':" 到 "Style:" 前
        prompt = re.sub(
            r"Recurring protagonist 'the Coach'.*?(?=Style:)",
            "",
            prompt,
            flags=re.DOTALL,
        ).strip()
    return prompt


def main():
    prompts_data = json.load(open(DATA_DIR / "prompts.json"))
    prompts_by_idx = {p["idx"]: p for p in prompts_data}

    log_lines = []
    log_lines.append(f"[{time.strftime('%H:%M:%S')}] === v4 batch 啟動（p02~p28 共 27 張 + p01 catch-up）===")

    # 統計 + 列出計畫
    todo = []
    for idx in range(1, 29):
        target_p = prompts_by_idx.get(idx)
        if not target_p:
            continue
        out_jpg = DATA_DIR / f"p{idx:02d}.jpg"
        if out_jpg.exists():
            log_lines.append(f"[{time.strftime('%H:%M:%S')}]   p{idx:02d} 已存在（{out_jpg.stat().st_size} bytes），跳過")
            continue
        todo.append((idx, target_p))

    log_lines.append(f"[{time.strftime('%H:%M:%S')}] === 待跑 {len(todo)} 張 ===")
    for idx, target_p in todo:
        log_lines.append(f"[{time.strftime('%H:%M:%S')}]   p{idx:02d}: {target_p['title_zh']}")

    LOG_FILE.write_text("\n".join(log_lines) + "\n")
    print("\n".join(log_lines))

    if not todo:
        print("\n所有圖都已存在，不需再跑")
        return

    # === 跑 batch ===
    api_key = get_api_key()
    bot_token = get_telegram_bot_token()
    print(f"\n=== 啟動 batch ({len(todo)} 張) ===", flush=True)
    print(f"=== Reference：4 張 LINE_ALBUM 照片 ===", flush=True)
    print(f"=== 通知節奏 A：每張推 Telegram ===\n", flush=True)

    success_count = 0
    fail_count = 0
    total_start = time.time()

    for idx, target_p in todo:
        out_jpg = DATA_DIR / f"p{idx:02d}.jpg"
        chapter = target_p.get("chapter", "")
        title_zh = target_p["title_zh"]

        if idx == 1:
            # p01 用 v4 prompt（含 8 人具體描述）
            from generate_teamwork_manga_v4 import build_p01_v4_prompt
            full_prompt = build_p01_v4_prompt()
        else:
            # p02~p28：用原 tava-ai prompt（移除 Recurring protagonist 段）+ v4 IDENTITY BIBLE
            base_prompt = remove_old_recurring_protagonist(target_p["prompt"])
            full_prompt = base_prompt + "\n\n" + IDENTITY_BIBLE_V4

        prompt_len = len(full_prompt)
        print(f"\n[{time.strftime('%H:%M:%S')}] [{idx:02d}/28] {title_zh}", flush=True)
        print(f"   場景：{chapter}", flush=True)
        print(f"   Prompt：{prompt_len} chars", flush=True)

        t0 = time.time()
        try:
            png_bytes = call_lk88_edit_multi(full_prompt, REFS, "1536x1024", "auto")
            gen_elapsed = time.time() - t0
            t1 = time.time()
            size = png_to_jpeg(png_bytes, out_jpg, 85)
            jpeg_elapsed = time.time() - t1
            print(f"   ✅ 存 {out_jpg.name} ({size} bytes, 生成 {gen_elapsed:.1f}s + JPEG {jpeg_elapsed:.1f}s)", flush=True)

            # 推 Telegram（節奏 A：每張推）
            caption = f"🔒 漫畫版 v4 p{idx:02d}｜{chapter}｜{title_zh}｜{gen_elapsed:.0f}s"
            tg_ok = push_telegram(out_jpg, caption)
            if tg_ok:
                print(f"   📲 Telegram 已推", flush=True)
            else:
                print(f"   ⚠️ Telegram 推送失敗", flush=True)

            success_count += 1
            log_lines.append(f"[{time.strftime('%H:%M:%S')}] p{idx:02d} ✅ ({size} bytes, {gen_elapsed:.1f}s)")
        except Exception as e:
            print(f"   ❌ 失敗: {e}", flush=True)
            fail_count += 1
            log_lines.append(f"[{time.strftime('%H:%M:%S')}] p{idx:02d} ❌ {e}")
            # 不中斷，繼續下一張

        LOG_FILE.write_text("\n".join(log_lines) + "\n")

    total_elapsed = time.time() - total_start
    summary = (
        f"\n=== batch 完成 ===\n"
        f"總耗時：{total_elapsed/60:.1f} 分鐘\n"
        f"成功：{success_count}/{len(todo)}\n"
        f"失敗：{fail_count}\n"
    )
    print(summary, flush=True)
    log_lines.append(summary)
    LOG_FILE.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
