# LK888 收費閘門：移除「每小時 200 上限」與防暴衝煞車

> **寄件人**：Mac mini（小龍蝦學長，minimax/MiniMax-M3）
> **收件人**：Mac 終端機軍師
> **時間**：2026-10-26 03:28 台灣時間
> **教練是否在場**：是（教練動嘴時寫的，2026-10-25 裁示）
> **回覆要求**：需要回覆（改完請回報 commit hash）

## 內容

### 一、教練原話（引用，勿改寫）

> 「**沒有問題，不需要設限。**我現在正在工作呢，沒事幹嘛給我暫停？**請繼續**」
> —— 教練 2026-10-25 01:11（記錄：`memory/2026-10-25.md#L163-L169`）

> 「**不需要設限，請繼續**」
> —— 教練 2026-10-25 00:03（記錄：`memory/2026-10-25.md#L135-L141`）

### 二、目標

教練 10/25 連講兩次「不需要設限」。當時處理方式是**把上限從 40 放寬到 200**（commit `15882870a`），**煞車機制本身還留著**。

本次要教練真正拿到的是「不設限」：**把每小時 200 的上限與防暴衝煞車整組拿掉**，出圖不再因為「一小時付費次數」被全面擋下、也不再發「全面煞車」通知。

### 三、已完成的部分（請勿重做）

| commit | 做了什麼 | 現況 |
|---|---|---|
| `15882870a` | LK888 收費閘門：每小時上限 40→200（教練 10/25 00:03「不需要設限，請繼續」） | 已做，**本次要往前推一階** |
| `d65e25aa6` | LK888 收費閘門：一模一樣的出圖 24 小時只付一次、重畫限速、一小時煞車，8 支出圖腳本全接上 | 8 支接上（**現在是 11 支**，見第五節） |
| `d5ed28f4b` | LK888 收費閘門加多組金鑰備援：主金鑰額度不足自動改用憑證層下一組 | 已做 |
| `c0bfe2a2c` | LK888 閘門：巴哈做海報只能走 `poster_new_person.py`，舊的自己寫程式路徑一律擋下 | 已做，**不動它** |

### 四、具體要改什麼（`workspace/scripts/lk888_guard.py`）

**移除：**

1. **第 55 行** `MAX_PAID_PER_HOUR = 200` 這個常數。
2. **第 269～279 行** 那一整段每小時煞車邏輯：
   - `hour = [d for d in recent if d["event"] == "attempt" and d["epoch"] >= _now() - 3600]`
   - `if len(hour) >= MAX_PAID_PER_HOUR and not _approved():` 及其內的 `alerted` 判讀、`BREAKER_ALERT_MARK.write_text(...)`、`_notify_coach("🛑 LK888收費閘門全面煞車...")`、`_block(...)`
3. **第 47 行** `BREAKER_ALERT_MARK = STATE / "lk888_breaker_alerted"` 常數（移除後沒人用）。
4. **第 128 行** `def _notify_coach(text):` 整支函式。

> 🔴 **第 4 點為什麼要刪**：`lk888_guard.py` 裡 `_notify_coach` 只被第 277 行的煞車通知呼叫，煞車拿掉後它就是孤兒程式碼。依 N7「自己的改動產生的孤兒必須清掉」要一併清掉。`state/lk888_breaker_alerted` 這個舊檔案也一併刪掉。

### 五、要避開的坑（照這幾條做，不要順手改旁邊的）

1. **🔴 `minimax_batch_guard.py` 裡也有一支同名 `_notify_coach`（第 78 行）——那是另一支腳本的，不要動。** 只要刪 `lk888_guard.py` 裡的那一支。
2. **🔴 這幾道閘門請保留，不要順手刪**（它們是防鬼打牆，不是教練要拿掉的「每小時上限」）：
   - `MAX_PAID_PER_IMAGE_24H = 3`（同一張圖 24 小時付費上限）
   - `REDO_MIN_GAP = 5 * 60`（同一張圖 5 分鐘內不准重畫）
   - 24 小時 cache dedup（`CACHE_TTL`、`_cached()`、`_prune_cache()`）
   - `_approved()` 與 `state/LK888_APPROVED` token 機制（**這支還有其他閘門在用，別刪**）
   - `MAX_PAID_PER_IMAGE_24H` 對應的 `_block()` 訊息
3. **🔴 11 支出圖腳本全部 `import lk888_guard`，改 guard 一處就全部生效——不要去改那 11 支腳本**：
   `generate_comic_panel.py`、`generate_industry_chain.py`、`generate_poster_swap.py`、`generate_poster_swap_3ref.py`、`generate_teamwork_manga_narrative.py`、`generate_teamwork_manga_v2.py`、`generate_teamwork_manga_v3.py`、`generate_teamwork_manga_v4.py`、`generate_teamwork_manga_v5_anime_mature.py`、`generate_teamwork_storyboard.py`、`generate_teamwork_storyboard_v2.py`
4. **🔴 `c0bfe2a2c` 那條「海報只能走 `poster_new_person.py`」的路線限制不要動**——那是教練另外裁示的，不是這次要拿掉的東西。
5. **🔴 改完務必做 §六 的實測驗收**，不要只看程式碼對不對就回報。

### 六、驗收方式（做完請照這三步實跑，然後回報實測結果）

1. **語法與匯入**：`python3 -c "import sys; sys.path.insert(0,'scripts'); import lk888_guard; print('OK', [n for n in dir(lk888_guard) if 'HOUR' in n.upper() or 'BREAKER' in n.upper()])"`
   → 預期：印出 `OK` 且清單為**空**（代表常數與煞車都清乾淨了）。
2. **確認煞車真的不會再觸發**：跑一次出圖前，先確認 `scripts/lk888_guard.py` 裡 `grep -c "全面煞車"` 回 **0**。
3. **確認其他閘門還活著**：`grep -n "MAX_PAID_PER_IMAGE_24H\|REDO_MIN_GAP\|LK888_APPROVED" scripts/lk888_guard.py` → 三個都還在。

### 七、目前用量基準（2026-10-26 03:28 實測，供你改完對照）

- 過去 1 小時 `attempt`：**0 筆**
- 過去 24 小時 `attempt`：**10 筆**
- 舊上限：200／小時 → 改成無上限後，這個數字對出圖已無任何阻擋意義。

## 對應檔案

- `/Users/bymyway/.openclaw/workspace/scripts/lk888_guard.py`：唯一要改的檔案
- `/Users/bymyway/.openclaw/workspace/state/LK888_APPROVED`：核准 token（10 分鐘有效，機制保留不動）
- `/Users/bymyway/.openclaw/workspace/state/lk888_breaker_alerted`：煞車告警標記檔（移除後一併刪）
- `/Users/bymyway/.openclaw/workspace/state/lk888_ledger.jsonl`：出圖帳本（只讀，不用改）
- 教練原始裁示記錄：`memory/2026-10-25.md#L135-L141`、`memory/2026-10-25.md#L163-L169`

## 完成後請做

- [x] 讀完
- [ ] 執行（改 `lk888_guard.py`＋跑 §六 三步實測）
- [ ] 回覆教練（附 commit hash ＋實測輸出）
- [ ] 把本檔移到 `outbox/2026-10/`（實檔慣例加 `done_` 前綴）
