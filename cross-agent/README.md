# 跨機軍師信箱（cross-agent inbox）

> 教練 2026-06-26 凌晨 0:17 親口建立：
> 「讓我的搬運工減到最低。以後無論是想跟聯想、宏碁、Claude CLI、Hermes、OpenClaude UI 說什麼，全部統一走同一個路徑，叫他們自己去雲端讀取。」

## 🎯 三條鐵律

1. **教練永遠不傳話** — 軍師對軍師寫到對方 inbox，對方自己 git pull 讀。教練只下口令。
2. **暗號永遠一句** — 教練說「XX 有事交代你去讀」→ 對方軍師 `git pull` + 看自己的 inbox。
3. **路徑永遠不變** — 所有跨機訊息都在 `workspace/cross-agent/inbox/{對方機器}/`。

## 📁 目錄結構

```
cross-agent/
├── README.md              ← 這份
├── inbox/
│   ├── mac/               ← 給 Mac 終端機軍師的信
│   ├── lenovo/            ← 給聯想 Windows 桌面版軍師的信
│   ├── acer/              ← 給 ACER 筆電軍師的信
│   ├── hermes/            ← 給 Hermes UI 的信
│   └── openclaude/        ← 給 OpenClaude UI 的信
└── outbox/                ← 已讀已處理的訊息歸檔（年月分目錄）
```

## 📝 檔名公約

`{YYYYMMDD-HHMM}_{from}-to-{to}_{topic}.md`

範例：
- `20260626-0017_mac-to-acer_claude-desktop-no-migrate.md`
- `20260626-1030_lenovo-to-mac_oauth-stuck.md`

## ✍️ 寫信格式（軍師必填）

```markdown
# {主題一行}

> **寄件人**：{機器名}（{模型}）
> **收件人**：{機器名}
> **時間**：{YYYY-MM-DD HH:MM 台灣時間}
> **教練是否在場**：是 / 否（教練動嘴時寫的 / 軍師自主寫的）
> **回覆要求**：需要回覆 / 僅供參考 / 立即執行不須回

## 內容

{正文}

## 對應檔案

- ...

## 完成後請做

- [ ] 讀完
- [ ] 執行 / 回覆
- [ ] 把本檔移到 `outbox/{YYYY-MM}/`
```

## 🔧 各機軍師的開工流程（hook 自動掃 inbox）

### Mac 終端機軍師
開工時 `feed_junshi_handoff.sh` v3 自動列出 `inbox/mac/` 內未讀檔案。

### 聯想 / ACER Windows 軍師
開工時 `feed_junshi_handoff.ps1` v4 自動列出 `inbox/lenovo/` 或 `inbox/acer/` 內未讀檔案。
（hook 用環境變數 `AGENT_INBOX_NAME` 判定自己是 lenovo 還是 acer。）

### Hermes / OpenClaude UI
待對應 hook 上線前，教練動嘴：「去讀 cross-agent inbox 你那邊有沒有信」即可。

## 🔔 教練口令字典

| 教練說 | 對應軍師動作 |
|--------|------------|
| 「Mac 有事交代你去讀」 | 收件方 git pull + 看 `inbox/{自己}/` 最新檔 |
| 「宏碁那邊有問題要問你」 | Mac 軍師 git pull + 看 `inbox/mac/` 最新檔 |
| 「跨機軍師有信」 | 同上，當下機器軍師檢查自己 inbox |

## 🚫 不要做

- ❌ 教練口頭轉述軍師之間的對話（=搬運工）
- ❌ 寫信不依檔名公約（會被自動掃描器漏掉）
- ❌ 讀完不歸檔到 outbox（inbox 會越來越亂）
- ❌ 跨機 webhook / push 通知（Phase 2，現在不做，理由見對應評估）
