---
name: VPS 更新 SOP（關鍵字觸發）
description: 教練說「VPS 更新」「VPS 有更新」「VPS 升級」立刻照 SOP 跑，不問、不試錯、不繞坑
type: feedback
originSessionId: cae9559f-fcf7-4f7a-9a7e-2a47efa14c03
---
# 🔴 關鍵字觸發 SOP — 「VPS 更新」

> ⛔ **2026-09-24 查證：下面四步驟更新錯對象，不要再照做。** VPS 的小龍蝦跑在 Docker 容器裡，實際服務的是映像檔內 `/app` 那份程式（2026-09-24 仍是 **2026.5.27**，容器建於 5/28）；`openclaw update` 只更新容器裡另一份指令工具（`/usr/local/lib/node_modules/openclaw`，顯示 2026.6.34），**從來沒升級到正式服務**，而且容器一重建就消失。查真正版本：`docker exec openclaw sh -c "grep -m1 version /app/package.json"`。
>
> **正確升級方式**＝換映像檔：①`docker tag` 另存舊映像當退路 ②備份 `/root/openclaw/data`（含 SQLite 資料庫，跨 2.0 會單向遷移）③`docker pull ghcr.io/openclaw/openclaw:<指定版本>`（不要用 latest）④改 `/root/openclaw/docker-compose.yml` 的 image 後 `docker-compose up -d` ⑤驗證 `/app/package.json` 版本＋`/health`＋機器人收訊。
>
> **2026-09-24 評估結論**：9.6 剛發布即有多個 P0 升級災情，暫不升；VPS 若要升，優先考慮官方長期穩定版 `ghcr.io/openclaw/openclaw:2026.7.35`（extended-stable＝LTS，不經 2.0 資料遷移）。當天已另存 `openclaw-rollback:2026.5.27` 並備份 `/root/openclaw/backup/data-pre-upgrade-20260924`（4.5G），正式服務未變動。詳見 `knowledges/2026-09-24_團隊協作全面體檢報告.md` 第六節。

**觸發詞（任一命中即啟動 SOP）：**
- 「VPS 更新」「VPS 有更新」「VPS 可用更新」「VPS 升級」
- 「openclaw 更新」配合 VPS / 雲端 / 遠端語境
- 教練貼出「v 版本號A (執行中版本 v 版本號B). 立即更新」這種版本對照句

**Why：** 2026-05-18 教練親定。第一次跑的時候我繞了 sshpass 跟 docker 容器權限兩個坑才成功，教練要求把這變成肌肉記憶，下次零思考執行。

**How to apply：** 命中觸發詞 → **直接跑下面四步**，不要問教練「要更新嗎」「從哪更新」「密碼是多少」「在哪台機器」。守則 08：花時間討論就是為了執行。

---

## SOP 四步驟（命中觸發詞立刻照跑）

```bash
# 1. 預檢版本
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw --version"

# 2. dry-run 看計畫
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw update --dry-run 2>&1 | tail -20"

# 3. 真正執行（必須 -u root，預設 user 是 node 沒權限）
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec -u root openclaw openclaw update 2>&1 | tail -30"

# 4. 驗證新版本
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw --version"
```

## 必踩的兩個坑（不照做必失敗）

1. **必須 `sshpass -p '9kdxvQN2'`**：純 `ssh` 直連會 Permission denied（密碼互動模式被擋）。本機 sshpass 路徑：`/opt/homebrew/bin/sshpass`。
2. **必須 `docker exec -u root`**：容器預設 user 是 `node`，無權限寫 `/usr/local/lib/node_modules`，會噴 `EACCES`。

## 回報模板（更新完成後給教練看的）

```
教練，VPS 更新完成 ✅
更新前：vXXXX → 更新後：vXXXX
總耗時：XX 秒
gateway 重啟：容器內無系統服務（正常 skip）
```

## 環境資訊

- IP：43.245.60.200
- 密碼：9kdxvQN2（2026-05-18 仍有效）
- 容器名稱：openclaw
- openclaw 安裝路徑：/usr/local/lib/node_modules/openclaw

## 戰史

- 2026-05-18：v2026.5.7 → v2026.5.12，全程 55 秒，這次教練親自下令把流程定為 SOP。
