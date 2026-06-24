---
name: feedback-modal-selector-remove-pitfall
description: 🔴🔴 modal class 用 .fixed.inset-0.bg-black/60 時，禁止用該 selector 做 remove() 否則會把 modal 自己清掉
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c69b6a3e-279f-496c-b431-48b479cca56a
---

任何「點 anchor / 點 menu / 收起 mobile drawer」的 code 裡，如果用 `document.querySelectorAll('.fixed.inset-0.bg-black/60').forEach(m => m.remove())` 來清半透黑底 overlay → **會連 modal 自己一起 remove**，因為 modal class 也包含 `fixed inset-0 bg-black/60`。

**Why:** 2026-06-21 凌晨 government-grow 報名按鈕：教練回報「第一次按沒反應，要 F5 才有反應；切換 menu 後又壞」。我繞了 3 次（cache-buster meta、addEventListener 硬化、preview viewport=1 diag），全沒解。真根因是 `initSmoothScroll` 內每點 anchor link 就 `mobileMenus.forEach(m => m.remove())`，把 modal 從 DOM 清掉 → 後續 `getElementById('registerModal')` 拿到 null → showRegisterModal throw → 按鈕「沒反應」。F5 才 DOM 重建。

**How to apply:**
- 看到 modal class 含 `fixed inset-0 bg-black/60` + 有 mobile menu overlay code → **立刻 grep `querySelectorAll('.fixed.inset-0.bg-black')`**，把所有 remove call 加上 `:not(#registerModal):not(#successModal):not(任何 modal id)` 排除。
- 治本：mobile menu overlay 應該掛專屬 class（如 `.mobile-menu-overlay`），不要跟 modal 共用 selector。
- 教練反覆說「F5 才有反應」+「點 menu 後又壞」這兩個訊號同時出現 → 99% 是 DOM 元素被誤 remove，不是 cache、不是 timing。

**診斷捷徑：** 在 console 跑 `Element.prototype.remove = (orig => function(){console.trace('remove',this.id||this.className);return orig.apply(this,arguments);})(Element.prototype.remove)`，重現 bug → 看誰 remove 了 modal。

相關記憶：[[feedback-compare-before-diagnose]]、[[feedback-do-everything-for-user]]
