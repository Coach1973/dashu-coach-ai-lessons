#!/usr/bin/env python3
"""Hook：UserPromptSubmit（只在 Windows 聯想用）—— 盯「NtFC 核心記憶體漏洞」。

起因（2026-10-15 教練）：記憶體從 50% 以下變 70~80%，查出核心非分頁集區 pool tag「NtFC」(ntfs.sys)
卡了 15GB、1.2 億筆沒釋放，工作管理員看不到。教練：「重開之後，幫我查查」。

原理（事件觸發，不輪詢）：教練每說一句話才量一次（NtQuerySystemInformation class 22，
不需管理員，幾十毫秒）。正常時完全不輸出；只有三種情況才出聲：
  ① 偵測到重新啟動（開機時間變了，或 NtFC 掉到上次一半以下）→ 記新基準，提醒一次
  ② NtFC 跨過 1GB／2GB／4GB／8GB 某條線（同一次開機每條線只提醒一次）
  ③ 第一次執行時已經很大 → 靜默記下，不吵（教練 10/15 已知情）

注意：快速啟動開著，「關機再開」核心記憶體不會清，要「重新啟動」才會。
狀態檔：E:/Claude-Data/.claude/state/ntfc_watch.json
"""
import ctypes
import json
import os
import sys
import time
from pathlib import Path

if os.name != "nt":
    sys.exit(0)

STATE = Path(os.environ.get("NTFC_WATCH_STATE") or r"E:/Claude-Data/.claude/state/ntfc_watch.json")
LEVELS_MB = (1024, 2048, 4096, 8192)
TAG = os.environ.get("NTFC_WATCH_TAG") or "NtFC"


def pool_tags():
    ntdll = ctypes.WinDLL("ntdll")
    size = 0x100000
    while True:
        buf = ctypes.create_string_buffer(size)
        ret = ctypes.c_ulong(0)
        st = ntdll.NtQuerySystemInformation(22, buf, size, ctypes.byref(ret)) & 0xFFFFFFFF
        if st == 0xC0000004:  # STATUS_INFO_LENGTH_MISMATCH
            size = ret.value + 0x10000
            continue
        if st != 0:
            return {}
        break
    raw = buf.raw
    n = int.from_bytes(raw[0:4], "little")
    out = {}
    for i in range(n):
        o = 8 + i * 40
        tag = raw[o:o + 4].decode("latin-1")
        allocs = int.from_bytes(raw[o + 24:o + 28], "little")
        frees = int.from_bytes(raw[o + 28:o + 32], "little")
        used = int.from_bytes(raw[o + 32:o + 40], "little")
        out[tag] = (used, (allocs - frees) & 0xFFFFFFFF)
    return out


def boot_time():
    k32 = ctypes.WinDLL("kernel32")
    k32.GetTickCount64.restype = ctypes.c_ulonglong
    return int(time.time() - k32.GetTickCount64() / 1000)


def fmt(ts):
    return time.strftime("%m/%d %H:%M", time.localtime(ts))


def main():
    tags = pool_tags()
    if not tags:
        return
    mb = tags.get(TAG, (0, 0))[0] / 1048576
    now = int(time.time())
    boot = boot_time()
    try:
        st = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        st = None

    msgs = []
    if st is None:
        # 第一次執行：教練已知道目前的狀況，靜默記下
        st = {"boot": boot, "base_mb": mb, "base_ts": now, "warned": [lv for lv in LEVELS_MB if mb >= lv]}
    elif abs(boot - st["boot"]) > 120 or mb < st.get("last_mb", mb) * 0.5:
        prev = st.get("last_mb", 0)
        if mb < 1024:
            msgs.append(
                f"🧠 記憶體漏洞追蹤（教練 10/15 交辦「重開之後幫我查查」）：偵測到電腦已重新啟動（開機 {fmt(boot)}），"
                f"漏洞那塊（{TAG}）從上次的 {prev:,.0f} MB 降成 {mb:,.0f} MB，已記為新起點。"
                f"👉 請在這一則回覆最前面用一句白話告訴教練：重開後那 15GB 已放掉，我會繼續盯，漲超過 1GB 就會跟您說。"
            )
        else:
            msgs.append(
                f"🧠 記憶體漏洞追蹤（教練 10/15 交辦）：開機時間變了（{fmt(boot)}），但漏洞那塊（{TAG}）還有 {mb:,.0f} MB 沒放掉"
                f"（上次 {prev:,.0f} MB）。快速啟動開著，「關機再開」不會清核心記憶體。"
                f"👉 請用一句白話告訴教練：要按「重新啟動」才會放掉。"
            )
        st = {"boot": boot, "base_mb": mb, "base_ts": now, "warned": [lv for lv in LEVELS_MB if mb >= lv]}
    else:
        hit = [lv for lv in LEVELS_MB if mb >= lv and lv not in st.get("warned", [])]
        if hit:
            hours = max((now - st["base_ts"]) / 3600, 0.01)
            rate = (mb - st["base_mb"]) / hours
            top = sorted(tags.items(), key=lambda kv: kv[1][0], reverse=True)[:3]
            top_s = "、".join(f"{t}={u / 1048576:,.0f}MB" for t, (u, _) in top)
            msgs.append(
                f"🧠 記憶體漏洞又在漲（教練 10/15 交辦）：{TAG} 已 {mb:,.0f} MB（剛跨過 {max(hit) // 1024}GB），"
                f"從 {fmt(st['base_ts'])} 起算平均每小時 +{rate:,.0f} MB；核心記憶體前三名：{top_s}。"
                f"👉 請先用一句白話告訴教練，再追查是誰造成的：嫌疑 NordVPN ThreatProtection（mshield.sys，"
                f"唯一第三方硬碟過濾驅動），可請教練暫停它觀察是否停漲；要更準可用管理員權限跑 wpr 抓 Pool 追蹤。"
                f"背景見記憶 reference_lenovo_memory_ntfs_nonpaged_pool_leak_2026-10-15。"
            )
            st["warned"] = sorted(set(st.get("warned", [])) | set(hit))
    st["last_mb"] = mb
    st["last_ts"] = now
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    if msgs:
        sys.stdout.reconfigure(encoding="utf-8")
        print("\n".join(msgs))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
