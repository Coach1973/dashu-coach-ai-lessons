---
name: citation-verification
description: Use whenever quoting a 守則/rule number, past conversation, or prior commitment back to 教練. Must verify against the primary source document before citing — never cite from memory, assumption, or a possibly-stale mirror file.
---

# 引用查證鐵律（執行細則 N3）

對應守則 #21（核心理念一字不差）、#15（說不知道比胡說八道更值得尊重）。

## 規則

- **引用守則內容** → 先查 `特助心法.md`（或`~/.claude/CLAUDE.md`）原文，確認編號和每個字
- **引用執行細則條文（N1~N9）** → 以 `~/.openclaw/workspace/執行細則.md`（教練欽定「唯一正式版」）為準
- **引用對話內容** → 先查原始記錄確認真的說過，有 commit hash 才能說「我之前說過」
- 不確定就說「我不確定，需要查證」，不臆測，不捏造

## 血淚教訓：兩份「正式文件」可能已經悄悄分岔

2026-07-24 建立本skill時實測發現：`~/.claude/CLAUDE.md`（軍師/特助側燒錄檔）的 E10~E12 是「編碼前說出假設／只碰必要的／可驗證目標」（Karpathy原則，2026-06-06加入），但 `~/.openclaw/workspace/執行細則.md`（教練欽定「唯一正式版」）的 E10~E12 是完全不同的內容（「教練發言黃金鐵律」/「危險指令零容忍鐵律」/「記憶寫入雙鐵律」，2026-06-17～07-10陸續加入）——**兩份文件同一個編號指向不同規則，是governance drift的真實案例**，不是我瞎猜的假設情境。

**教訓**：只讀了 `~/.claude/CLAUDE.md` 就以為知道「E11是什麼」是危險的——`~/.claude/CLAUDE.md` 自2026-06-06之後從未跟教練欽定的 `執行細則.md` 重新同步過。危險指令五道閘門（E11，636GB學費換來的）完全沒出現在 `~/.claude/CLAUDE.md`，如果只信這份文件會漏掉最重要的安全規則。

## 查證順序建議

引用任何執行細則條文編號前，兩份文件都查一次，內容不一致就如實回報給教練「這兩份文件在E10~E12不一致」，不要只採信其中一份就交差。
