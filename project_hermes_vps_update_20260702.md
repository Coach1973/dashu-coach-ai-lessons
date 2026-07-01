---
name: project-hermes-vps-update-20260702
description: Hermes VPS（113.29.232.178）從 v0.13.0 更新到 v0.17.0，完整過程與驗證紀錄
metadata:
  type: project
  updated: 2026-07-02
---

# Hermes VPS 更新紀錄（2026-07-02）

> 執行者：聯想軍師 Sonnet 5
> 教練口令：「只要長期有好處、沒有壞處，那就做」

## 更新前後版本

| 項目 | 更新前 | 更新後 |
|------|--------|--------|
| 版本 | v0.13.0 | v0.17.0「The Reach Release」 |
| 映像檔時間 | 2026-05-13 | 2026-07-02（最新 latest） |

## 執行步驟（全程過閘門，可逆）

1. 備份 `/root/.hermes`（839M）到 `/root/.hermes.bak.20260702-update`，確認大小一致
2. `docker pull nousresearch/hermes-agent:latest` 拉新版
3. 停用舊容器 + 改名保留 `hermes-old-v0.13.0`（未刪除，可隨時回滾）
4. 用相同掛載（`/root/.hermes:/opt/data`）、相同 port（8642/9119）、相同 env 建新容器
5. 驗證：容器穩定運行 5+ 分鐘無重啟、版本確認 0.17.0、主程式進程活著
6. Telegram 連線行為與更新前比對——舊版本身就有 timeout/reconnect 現象，新版沒有更糟

## 新版重點功能（v0.14→v0.17 累積）

- pip 安裝方式、Windows 支援、開機加速
- 核心程式碼精簡 76%、多代理協作平台成熟
- 獨立桌面版 App（Mac/Linux/Windows）
- iMessage 串接、網頁後台管理面板（含記憶管理）、團隊部署支援
- **新增安全機制**：Dashboard 預設拒絕未認證的公開綁定（0.0.0.0），必須設密碼或 OAuth 才能對外開放——這是安全性提升，非 bug

## 回滾方式（若日後發現問題）

```
docker stop hermes && docker rm hermes
docker rename hermes-old-v0.13.0 hermes
docker start hermes
```

## 待清理（7 天後，遵守備份保留鐵律）

- `/root/.hermes.bak.20260702-update` 保留至 2026-07-09
- `hermes-old-v0.13.0` 容器保留至 2026-07-09 後可 `docker rm`
