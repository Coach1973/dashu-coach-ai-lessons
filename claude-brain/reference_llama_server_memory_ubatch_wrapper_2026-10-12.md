---
name: reference-llama-server-memory-ubatch-wrapper-2026-10-12
description: 小龍蝦記憶搜尋的 llama-server 吃 2.1GB 的原因是 ubatch-size 2048（外掛寫死），已用包裝腳本壓成 1024（約0.66GB）；外掛更新或 command 被重設會失效
metadata:
  node_type: memory
  type: reference
  originSessionId: d2f1840b-1c75-4eb2-bd6d-77e9cb276c66
  modified: 2026-10-12T10:43:27.048Z
---

小龍蝦「記憶搜尋」（embeddinggemma-300m 小模型）的 `llama-server` 子程序常駐可長到 2.1GB。原因不是模型（0.3GB），是 `ubatch-size 2048` 的運算暫存區。外掛 `@openclaw/llama-cpp-provider` 原始碼把 2048 寫死，每次啟動都會把預設檔 `tools/llama.cpp/models-*.ini` 改回 2048（只改 ini 一次不會留住，會被改回）。

**怎麼壓的（2026-10-12）：** `openclaw.json` 的 `llama-cpp` provider `localService.command` 改指向包裝腳本 `tools/llama.cpp/llama-server-lite.sh`，它在 exec 真正的 llama-server 前，把 ini 裡的 `ubatch-size = 2048` 改成 1024。實測：2048＝1.8~2.1GB、1024＝0.66GB；實際記憶塊最長 758 tokens（metrics `n_tokens_max`），1024 夠用，超過 1024 tokens 的單筆輸入會被拒絕（"input too large"）。

**Why:** 教練 10/12 問「能否設計在 1G 左右」，並強調不要關掉記憶搜尋（釋放只關 RustDesk 等，不碰小龍蝦；release_all_memory.sh／rustdesk_free_memory.sh 已查證沒碰 llama-server）。

**How to apply:** 外掛升級後若 llama-server 又長到 2GB，先檢查 `openclaw.json` 的 command 是否被重設回原路徑 `.../b10809/darwin-arm64/llama-server`（版本號可能變）。要驗證：開子程序用 `ps -o command= -p <pid>` 看 `--ubatch-size`，`footprint <pid>` 看 phys_footprint。原本 ini 備份 `models-*.ini.bak-20261012-ubatch2048`，openclaw.json 備份 `openclaw.json.bak-20261012-llama-lite`。
