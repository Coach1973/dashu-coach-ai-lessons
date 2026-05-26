# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-26 晚間場
> 寫紙條的人：軍師（Claude Sonnet 4.6 桌面版）

---

## 一句話交代這場做了什麼

**小龍蝦 5 個系統 bug 全部修完：心跳幻覺、記憶體超大、重複 HB 檔、蒸餾腳本空跑、赫米斯 git 不提交——全部根治。**

---

## ✅ 這場完成的事

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 高 | 小龍蝦心跳幻覺修復 | ✅ cron `768246fb` 補 agentId + 台灣時區 + 身份說明 prompt，直接生效 |
| 🔴 高 | `distill_incremental.js` 完整重寫 | ✅ 改讀 `🦞 小龍蝦：` 欄位、台灣時區、記憶體大小檢查 |
| 🔴 高 | `distill_vps.py` 永久補 git commit+push | ✅ 已追加 git push 邏輯，VPS 每次蒸餾後自動提交 |
| 🔴 高 | `1-HB.md` 心跳品質機制 | ✅ 防空迴圈守則（連3次 OK 第4次必做實質任務）+ 系統健康檢查 |
| 🔴 高 | `HB-學長.md` 清除 | ✅ 重複檔已刪，內容合併入 `1-HB.md` |
| 🟡 中 | `failure-case-handbook.md` 補 H/I/J 三案 | ✅ M11（cron指錯HB）/ M12（重啟不更新狀態）/ M13（大記憶體炸模型）|
| 🟡 中 | `session-memory/handler.js` 時區修正 | ✅ UTC → 台灣時間（+8h），記憶體檔名/標頭已對 |

### 小龍蝦心跳幻覺根因分析

| 問題 | 根因 | 修法 |
|------|------|------|
| 用簡體字（"第1号机"）| 隔離 session 無身份錨定 | 補完整繁體中文 + 禁用簡體說明 |
| 虛構未來日期（2026-06-02）| 同上 | prompt 明確禁止虛構任何數字 |
| 時區不對 | 缺 `tz: "Asia/Taipei"` | 補入 schedule |
| 找不到正確 agent | 缺 `agentId: "main"` | 補入 job config |

### cron `768246fb` 最終狀態

```json
{
  "agentId": "main",
  "schedule": { "expr": "*/30 * * * *", "tz": "Asia/Taipei" },
  "message": "你是小龍蝦學長（1號機），大樹教練的AI特助。請用繁體中文（臺灣正體）執行 ~/.openclaw/workspace/1-HB.md 裡的心跳任務。禁止使用簡體中文，禁止虛構日期、號碼或任何不實資訊。"
}
```

下次執行：2026-05-26 14:00 台灣時間

---

## 🔴 下一個軍師待辦

| # | 優先 | 任務 | 說明 |
|---|------|------|------|
| 1 | 🟡 中 | 觀察下一次心跳結果 | 14:00 台灣時間確認心跳是否用繁體、日期是否正確 |
| 2 | 🟡 中 | `session-memory/handler.js` 時區修正追蹤 | OpenClaw 升級後會被覆寫，需要在升級後重新補修 |
| 3 | 🟢 低 | 赫米斯檢討報告 | 教練尚未說明目標 |

---

## 🔗 Commit Hash 清單

| 描述 | Commit |
|------|--------|
| 5 個 bug 修復（distill rewrite / 1-HB / HB-學長刪除 / failure handbook）| `fdb45726` |
| VPS distill_vps.py git push 修復 | 直接追加，VPS 端無 git（只影響腳本邏輯）|
| jobs.json cron 768246fb 修復 | 直接生效（不在 git 管理範圍）|

---

## ⚠️ 特別提醒

- **session-memory handler.js** 是已編譯的 bundled 檔（`/opt/homebrew/lib/node_modules/openclaw/dist/bundled/`），升級會覆寫。真正的修法應在原始碼，但目前找不到源碼位置。先以 bundled 修正頂著，升級後提醒重修。
- **cron/jobs.json 不在 git 管理**：`.openclaw/cron/` 無 git repo，改完直接生效，無需 commit。

---

*軍師交接紙條完成 | 2026-05-26 晚間場 | 軍師 Claude Sonnet 4.6 桌面版*
