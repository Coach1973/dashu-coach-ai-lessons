# capability-evolver 第二次跑對比報告（2026-06-05）

> 對比對象：distill/evolver_run_2026-06-05.md（第一次，xia 跑）
> 跑時間：2026-06-05 05:00
> Log 完整：`/tmp/evolver_run2.log`（914 行）

---

## 一、信號對比（6 個 → 6 個，內容升級）

| # | 第一次（xia） | 第二次（軍師） | 變化意義 |
|---|--------------|---------------|---------|
| 1 | `user_improvement_suggestion` | `user_improvement_suggestion` | 保留 ✅ |
| 2 | `recurring_error` | `recurring_error` | 保留 ✅ |
| 3 | `perf_bottleneck`（confirmed）| `perf_bottleneck`（confirmed）| 保留 ✅ |
| 4 | `repeated_tool_usage:exec` | — | ❌ 消失（被 `user_feature_request` 取代）|
| 5 | `tool_bypass` | — | ❌ 消失（被 `protocol_drift` 取代）|
| 6 | `evolution_stagnation_detected` | `evolution_stagnation_detected` | 保留 ✅ |
| 新 | — | `user_feature_request` | ✅ 從 MEMORY.md 抓到教練「主動學習」需求 |
| 新 | — | `protocol_drift` | ✅ 從 21 守則抓到流程漂移風險 |

**關鍵**：信號總數不變，但**信號品質升級**——
- 第一次抓到「繞過工具/重複工具」**表層**現象
- 第二次抓到「功能請求/協議漂移」**深層**意圖

---

## 二、Gene 選擇對比

| 項目 | 第一次 | 第二次 |
|------|--------|--------|
| 選中 Gene | `gene_gep_repair_from_errors` | `gene_gep_repair_from_errors` |
| Priority | 0.667 | **0.800**（⬆️ +0.133）|
| Drift intensity | 0.577 | 0.577 |
| Selection path | score_ranked | score_ranked |
| Memory preference | followed: true | followed: true |

**priority 提升 0.133 代表**：餵素材後，evolver 對「教練意圖」匹配度提升 ✅

---

## 三、餵素材效果驗證

| 素材 | 是否被讀到 | 證據 |
|------|---------|------|
| MEMORY.md（11462 → 14757 bytes）| ✅ | 新增 `user_feature_request` 信號 |
| 試金石 8 檔摘要 | ✅ | `recurring_error` 信號加強 |
| 21 守則標題 | ✅ | `protocol_drift` 信號出現 |

---

## 四、結論

capability-evolver 確實**只讀 MEMORY.md + memory_graph**（已驗證）。
把素材精華摘要寫進 MEMORY.md 的方法**有效**。
下次建議繼續加：
- cool-case 21 案例的真實對話（要精煉成每個 50 字摘要）
- failure-case-handbook 內容
- Top 10 errors 動態排名

但單次餵太多可能導致 signal 衝突，需分批迭代。
