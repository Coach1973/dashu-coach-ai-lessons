# capability-evolver 首次完整跑結果（2026-06-05）

> 跑時間：2026-06-05 04:53
> Log 完整：`/tmp/evolver_run.log`（810 行，46KB）
> 環境：`EVOLVER_USE_PARENT_GIT=true EVOMAP_PROXY=0 node index.js`

---

## 一、6 個自動偵測信號

| # | 信號 | 類型 | 意義 |
|---|------|------|------|
| 1 | `user_improvement_suggestion` | score-only | 教練說「主動學習」等改進需求 |
| 2 | `recurring_error` | score-only | 重複犯錯模式被抓到 |
| 3 | `perf_bottleneck` | confirmed | 確認的效能瓶頸 |
| 4 | `repeated_tool_usage:exec` | score-only | 重複用 exec 工具 |
| 5 | `tool_bypass` | score-only | 繞過工具的行為 |
| 6 | `evolution_stagnation_detected` | score-only | 停滯警告 |

**它抓到「教練說的主動學習」了 ✅**

---

## 二、自動選的 Gene

**已選**：`gene_gep_repair_from_errors`（priority 0.667，針對重複錯誤修復）

**候選 3 個**：
1. `gene_gep_repair_from_errors`（已選，repair）
2. `gene_gep_optimize_prompt_and_assets`（optimize）
3. `gene_tool_integrity`（repair，防 tool_bypass）

**選擇路徑**：`score_ranked`，`memory_preference_followed: true`

---

## 三、警告與系統狀態

- `recent_error_count: 0`
- `stability: stable`
- `recommended_intent: optimize`
- ⚠️ **偵測到停滯**，建議下一輪走 `INNOVATE` 路線
- ⚠️ `Self-modification causes instability and is blocked by solidify` — 自我修改被擋住（安全機制）
- 要開自我修改：`EVOLVE_ALLOW_SELF_MODIFY=true`（NOT recommended）

---

## 四、capability-evolver 實際讀的素材來源

| 來源 | 大小 | 用途 |
|------|------|------|
| `MEMORY.md` | 3773 bytes | 主索引 |
| `memory_graph` | 26128 bytes | 索引 |

**它沒自動掃**：試金石 8 檔、Top 30、cool_case 21 案例、failure-case-handbook

**餵法**：把素材精華摘要寫進 `MEMORY.md`，下次跑才讀得到。

---

## 五、下一步計畫

1. 把試金石 8 檔前 200 字摘要 + 守則經典場景 21 條標題 → 寫進 MEMORY.md
2. 再跑一次 evolver
3. 對比前後 6 信號變化
