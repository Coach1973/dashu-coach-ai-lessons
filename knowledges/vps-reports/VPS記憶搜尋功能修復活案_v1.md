# VPS 記憶搜尋功能修復活案 v1

> 建立時間：2026-07-20 08:50（台灣時間）
> 執行者：軍師（Mac 桌面版 Sonnet 5）
> 派工人：小龍蝦學長
> 觸發：教練詢問「VPS 用戶放 1-2 個月後還能搜尋過去對話嗎？」
> 狀態：根因分析完成，待教練裁示後執行

---

## 一、教練問題的誠實回答

| 問題 | 答案 |
|------|------|
| VPS 用戶放 1-2 個月後還能搜尋過去對話嗎？ | 部分能、部分不能。Dreaming 夢境記憶能搜尋（持續運作中），但 5/4 之後的對話主索引不能（77 天斷層）。Trial 用戶完全不能（個人 SQLite 從未建立索引）。 |
| 小龍蝦目前的記憶搜尋功能是否最佳狀態？ | 不是。dreaming 系統健康，但「memory/ → main.sqlite」索引機制從 5/4 停止運作 77 天；trial 用戶個人化從未實現。 |

---

## 二、實際狀況盤點（軍師親自 SSH 驗證）

### 主機與容器
- 主機：Ubuntu 24.04.4 LTS，磁碟 62GB 可用
- Docker 容器：openclaw 7 weeks ago 建立，Up 2 days (healthy)
- openclaw 版本：2026.6.1

### 記憶系統元件狀態

| 元件 | 路徑 | 狀態 | 證據 |
|------|------|------|------|
| Dreaming 抽取（每天 03:00）| memory-core plugin | 持續運作 | memory/dreaming/light/2026-07-19.md 44,138 bytes |
| Dreaming 寫入 markdown | memory-core plugin | 持續運作 | memory/dreaming/{deep,light,rem}/2026-07-20.md 都有 |
| main.sqlite（教練本人索引）| /root/openclaw/data/memory/main.sqlite | 從 5/4 停止更新（77 天）| mtime=2026-05-04 03:00:47 |
| trial SQLite 個人化 | /root/openclaw/data/memory/trial-*.sqlite | 表結構建好但 0 條內容 | 7 個 trial SQLite.chunks 全 0 |
| 對話原文 jsonl | /root/openclaw/data/agents/*/sessions/*.jsonl | 完整保留 | main + 7 trial 都有大量 jsonl |

### main.sqlite 內容統計
```
chunks: 103
files: 23
embedding_cache: 38
chunks_fts: 103
最新被索引檔案 mtime: 2026-05-04
```

### trial SQLite 內容統計（以 trial-8626705510 為例）
```
files: 0, chunks: 0, embedding_cache: 0, chunks_fts: 0
chunks_fts_config: 1（FTS5 表結構存在）
```

### memory_search meta 設定
```json
{
  "model": "fts-only",
  "provider": "none",
  "sources": ["memory"],
  "ftsTokenizer": "unicode61"
}
```
結論：VPS 只索引 memory/ 下 markdown，用 FTS5 全文搜尋，無向量 embedding。

---

## 三、根因分析（軍師親自查證）

### 根因 1：5/4 後 memory/ → main.sqlite 索引機制停止運作
- main.sqlite 的 mtime = 2026-05-04 03:00:47（停止 77 天）
- files 表最新記錄 mtime 也是 2026-05-04
- 之後的 memory/dreaming/*.md 持續被寫入，但沒有任何程式把它們索引到 main.sqlite
- 推測：OpenClaw 內部索引觸發機制從 5/4 開始失效（容器/plugin 變動、條件未觸發、silent error）

### 根因 2：cron job「每 2 小時增量記憶蒸餾」寫死 Mac 路徑
```
message: ...執行：node /Users/bymyway/.openclaw/workspace/scripts/distill_incremental.js...
```
- VPS 容器內不存在此路徑
- 即使改對路徑，這個腳本只輸出 daily log 增量，本來就不寫 SQLite
- 所以 cron 失敗只是症狀，不是根因

### 根因 3：trial 用戶個人 SQLite 從未被寫入過
- 7 個 trial 用戶都有獨立 SQLite，表結構建好但全部 0 條內容
- 推測：trial 模式預設只跑共享 dreaming，不主動建立個人索引

### 根因 4：trial 用戶對話原文存在，但 clients/ 個人 profile 只有 3 個
- agents/ 下有 7 個 trial，但 clients/ 只有 3 個 .md profile

---

## 四、小龍蝦學長盤點的修正

| 小龍蝦學長盤點 | 軍師查證後 | 修正 |
|----------------|-----------|------|
| 73 天記憶斷層 | 部分正確 | dreaming 持續運作，main.sqlite 索引停止 77 天 |
| main.sqlite 103 條 | 正確 | chunks: 103, files: 23 |
| trial 用戶 SQLite 全部 0 條 | 正確 | 7 個 trial SQLite.chunks 全 0 |
| FTS5 搜尋全部 0 條 | 合理 | 索引停在 5/4，dreaming 7/5 之後的內容未重新索引 |
| memsearch provider 失效 | 不準確 | provider = local（正常運作），內容過期 |
| 模型 provider 切換 | 不準確 | M3 provider 已正確註冊（6/9 修復過），跟 memory 無關 |

---

## 五、方案評估（建議優先順序）

### P0：查證 5/4 索引機制停止的真因
動作：讀取 plugin-runtime-deps 下的 memory 程式碼、查 docker events、找觸發條件
工時：1-2 小時
風險：低（純查證）

### A：補回 77 天 main.sqlite 索引
前置：P0 完成
動作：手動觸發 reindex
工時：1-2 小時
風險：中

### D：複製 Mac 的 recall.py 到 VPS
動作：複製並修正路徑，提供給 trial agent 作為 fallback
工時：0.5 小時
風險：低

### B：trial 用戶個人化
前置：A 完成
動作：建立個人 dream 抽取 cron、修改 plugin 設定
工時：2-3 小時
風險：中

### C：開放搜尋工具給 trial agent
前置：B 完成
動作：修改 openclaw.json 允許清單
工時：0.25 小時
風險：低

---

## 六、建議執行順序（總工時 5-7 小時）

| 順序 | 動作 | 工時 | 依賴 |
|------|------|------|------|
| 1 | P0：查證 5/4 索引機制停止的真因 | 1-2 hr | 無 |
| 2 | D：複製 recall.py 到 VPS | 0.5 hr | 無（可平行）|
| 3 | A：補回 77 天 main.sqlite 索引 | 1-2 hr | 1 完成 |
| 4 | B：trial 用戶個人化索引 | 2-3 hr | 3 完成 |
| 5 | C：開放 trial 用戶搜尋工具 | 0.25 hr | 4 完成 |

---

## 七、回滾方案

1. P0 純查證，無變更
2. D 方案：失敗只會留檔案，rm 即可
3. A 方案：備份 main.sqlite 到 /root/openclaw/data/memory/main.sqlite.bak.20260720
4. B 方案：備份 7 個 trial SQLite
5. C 方案：備份 openclaw.json

---

## 八、隱私與注意事項

1. 不動對外用戶的隱私資料 —— 對話只用於建立索引，不分析不外流
2. 先驗證再執行 —— 每個改動前先用不會壞的查詢確認狀態
3. 保留回滾方案 —— 改壞了要能回到壞但穩定的狀態
4. 教練會看結果 —— 報告要清楚、簡潔、可執行

---

## 九、試金石補充

建議新增試金石案例 53：VPS 蒸餾斷層 77 天——多機部署記憶系統時，cron/索引機制沒有設定 sync 也沒有健康告警，導致失效 77 天才被發現。

---

## 十、教練需要裁示的事項

1. 是否同意執行 P0+D（合計 2-2.5 小時）？
2. 是否同意執行 A（1-2 小時）？
3. 是否同意執行 B（2-3 小時）？
4. 是否同意執行 C（15 分鐘）？
5. 本案是否升級為試金石案例 53？

---

立檔人：軍師（Mac 桌面版 Sonnet 5）
派工人：小龍蝦學長
立檔時間：2026-07-20 08:50（台灣時間）
