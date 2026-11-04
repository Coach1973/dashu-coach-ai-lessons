#!/usr/bin/env python3
"""LINE 多張照片合成一則回覆（2026-11-04 教練同意，賈維斯體檢建議 2）。

問題：會員一張一張傳照片（沒有被 LINE 標成同一本相簿），小龍蝦每張各回一次，
後面幾則超過免費回覆時效，改走扣額度的推播 → 被推播禁令擋下，會員收不到。
做法：LINE 外掛本來就會把「同一本相簿」的照片等 4 秒合成一輪；這個補丁讓
沒有相簿標記的單張照片也算進「同一人、同一聊天室的散裝相簿」，4 秒內陸續到的照片合成一輪、用一個免費回覆。
用法：python3 line_loose_image_merge_patch.py [apply|check|revert]（預設 apply；可重複執行）
"""
import glob, os, shutil, sys

PROJECTS = os.path.expanduser("~/.openclaw/npm/projects")
MARK = "// LINE_LOOSE_IMAGE_MERGE_V1"
ANCHOR = "\t} : void 0;\n}\nfunction createLineWebhookSpool(options) {"
NEW = ("\t} : { setId: \"loose\", senderKey: senderKeyFor(event), messageId: event.message.id }; " + MARK + "\n"
       "}\nfunction createLineWebhookSpool(options) {")
BAK = ".bak-before-loose-image-merge-20261104"


def targets():
    base = os.path.join(PROJECTS, "openclaw-line-*", "node_modules", "@openclaw", "line", "dist", ".setup")
    return [f for f in sorted(glob.glob(os.path.join(base, "monitor-*.mjs")))
            if "function resolveLineInboundImageSet(event)" in open(f, encoding="utf-8").read()]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "apply"
    files = targets()
    if not files:
        print("❌ 找不到 LINE 外掛的 monitor-*.mjs（外掛版本改了，要人看）")
        return 1
    bad = 0
    for f in files:
        t = open(f, encoding="utf-8").read()
        if mode == "check":
            ok = MARK in t
            bad += 0 if ok else 1
            print(("✅ 已套 " if ok else "🔴 沒套 ") + f)
        elif mode == "revert":
            if os.path.exists(f + BAK):
                shutil.copy2(f + BAK, f); print("已還原 " + f)
        else:
            if MARK in t:
                print("已套過 " + f); continue
            if ANCHOR not in t:
                bad += 1; print("🔴 找不到錨點（外掛寫法改了，要人看）" + f); continue
            if not os.path.exists(f + BAK):
                shutil.copy2(f, f + BAK)
            tmp = f + ".tmp-loose"
            open(tmp, "w", encoding="utf-8").write(t.replace(ANCHOR, NEW, 1))
            os.replace(tmp, f)
            print("✅ 已套用 " + f)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
