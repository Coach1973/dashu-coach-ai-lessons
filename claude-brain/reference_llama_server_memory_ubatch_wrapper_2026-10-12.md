---
name: reference-llama-server-memory-ubatch-wrapper-2026-10-12
description: 小龍蝦記憶搜尋 llama-server 吃 2.1GB＝外掛原始碼寫死 ubatch 2048、每次載入模型把設定檔寫回；10/12 包裝腳本被蓋掉失效，10/29 改外掛原始碼成 1024＋守衛 llama_memory_guard.sh（事件觸發＋每日05:10，超 1.2GB 自動釋放、外掛被更新洗回自動補）
metadata:
  node_type: memory
  type: reference
  originSessionId: d2f1840b-1c75-4eb2-bd6d-77e9cb276c66
  modified: 2026-10-29T02:05:00.000Z
---

小龍蝦「記憶搜尋」（embeddinggemma-300m 小模型）的 `llama-server` 嵌入程序可長到 2.1GB。原因不是模型（0.3GB），是 `ubatch-size 2048` 的運算暫存區。

**根因（10/29 查清，取代 10/12 的判斷）：** 外掛 `@openclaw/llama-cpp-provider`（實際載入的是 `~/.openclaw/npm/projects/openclaw-llama-cpp-provider-*__g-5ecf1d6216a147e6/.../dist/index.js`，2026.9.4）第 530 行 `const LLAMA_CPP_EMBEDDING_UBATCH_SIZE = 2048;`，**每次載入嵌入模型**時若設定檔內容不同就重寫成 2048。所以 10/12 的包裝腳本 `tools/llama.cpp/llama-server-lite.sh`（只在 router 啟動時改一次 ini）會被蓋掉：10/25 19:32 router 啟動改成 1024，19:46:07 外掛寫回 2048、同一秒啟動嵌入程序 → 2164MB 撐了 3 天，教練在活動監視器看到 2.11G。

**現在的做法（10/29，commit 85287938b）：** `workspace/scripts/llama_memory_guard.sh`＋launchd `ai.openclaw.llama-memory-guard`（備份在 ops/launchagents_backup，受 launchagents_guard 保護）：
- 外掛原始碼是 2048 → 改 1024（旁邊留 .bak）並 `launchctl kickstart -k gui/501/ai.openclaw.gateway` 重啟小龍蝦讓它生效
- 設定檔是 2048 → 改 1024
- 嵌入程序 footprint > 1200MB 或還在用 2048 → **連同上層 router 一起結束**；下次記憶搜尋外掛自動重開
- 有動手才通知教練（notify_coach 1 小時節流）
- 觸發：WatchPaths（npm/projects、外掛 index.js、tools/llama.cpp）＋RunAtLoad＋每天 05:10。實測改回 2048 後 6 秒自動修回。

**踩過的坑：**
- 只殺嵌入程序、不殺 router → router 一直回 HTTP 500「model failed to load」，記憶搜尋整個壞掉，要連 router 一起殺才會恢復。
- `/opt/homebrew/bin/openclaw` 是舊版，`gateway restart` 會因「Invalid input」設定檢查拒絕（不影響正在跑的閘道）；小龍蝦實際跑 nvm 那份，重啟一律用 `launchctl kickstart -k`。
- `openclaw capability embedding create --provider local` 是 CLI 自己起一套引擎、跑完就關，看不到閘道那套的常駐程序；要量常駐用量，看 `pgrep -fl "llama-server --embeddings"` 後 `footprint <pid>`。

**實測數字：** 2048＝2164MB；1024＝93MB（短查詢）～約 0.66GB（10/12 真實索引負載）。1024 夠用（記憶塊最長 758 tokens），超過 1024 tokens 的單筆會被拒絕。

**Why:** 教練 10/12 要「1G 左右」、不要關掉記憶搜尋；10/29 要「像 RustDesk 那樣，到一定的量自動釋放，回到正常值」的長久方案。

**How to apply:** 教練又問 llama-server 吃記憶體 → 先看 `workspace/logs/llama_memory_guard.log` 最後幾行與 `launchctl list | grep llama-memory-guard`；外掛換版本資料夾名稱時，plist 裡的 index.js 路徑要更新（npm/projects 監看仍會觸發）。備份：`workspace/state/backup_20261029_llama_ubatch/`。
