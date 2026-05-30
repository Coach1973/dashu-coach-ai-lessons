# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-30（Sonnet 終端機特助完成收尾）
> 寫紙條的人：終端機特助（Claude Sonnet 4.6）

---

## ✅ 本場完成任務：northern-tw.netlify.app 論壇網站全面建置

### 第一階段：基礎修復
| 任務 | 結果 |
|------|------|
| 11 張圖片從 Netlify 舊 deploy 救回 | ✅ |
| 場次切換列建置（4/11 + 6/26） | ✅ |

### 第二階段：6/26 嘉義場完整建置
| 任務 | 結果 |
|------|------|
| 7 位講師頭像＋學經歷＋演講主題 | ✅ |
| 完整議程（上午免費諮詢 / 下午講座） | ✅ |
| 報名表（實體 + 線上 Google Forms） | ✅ |
| 贊助廠商方案 NT$30,000 | ✅ |
| 全球健康發展協會申請入會連結 | ✅ |
| 中正大學 Logo | ✅ |
| 席次 200 / 報名費免費 | ✅ |

### 第三階段：頁面架構優化
| 任務 | 結果 |
|------|------|
| 626 設為首頁、411 移至成長足跡 | ✅ |
| 場次切換列移至頁面最底部 | ✅ |
| 回到頂部浮動按鈕（右下角 ▲） | ✅ |
| 快速跳轉列（6 個按鈕，同一排） | ✅ |

### 第四階段：成長足跡豐富化
| 任務 | 結果 |
|------|------|
| 協會官網 / FB 影音 / 申請入會按鈕 | ✅ |
| 第一場 1206 桃園場 4 篇媒體報導 | ✅ |
| 第二場 411 高雄場 6 篇媒體報導 | ✅ |
| 每篇均附媒體標籤＋超連結 | ✅ |

---

## 🌐 網站資訊

| 站台 | URL | Site ID |
|------|-----|---------|
| 正式版 | https://northern-tw.netlify.app/ | f1f3ed15-79b6-4bed-b4d1-0199a185a181 |
| 測試版 | https://northern-tw-test.netlify.app/ | 56d3fa7e-41bd-40d9-8000-2e9b779b0461 |

Netlify Token：nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838（到期 2027/05/14）

---

## ⚠️ 本地工作目錄（重開機會消失）

最新版所有檔案：/tmp/northern_images/
重開機後需從 Netlify API 重新拉檔案。

---

## 🗓 6/26 場次關鍵資訊

- 時間：2026 年 6 月 26 日（五）09:30–17:00
- 地點：國立中正大學創新大樓（嘉義縣民雄鄉大學路一段168號）
- 指導：嘉義縣衛生局
- 主辦：國立中正大學中小企業育成中心、全球健康發展協會、紐約北方醫學中心
- 報名費：免費，席次 200 位
- 實體報名：https://forms.gle/Htk4YENdd5m9rmmG8
- 線上報名：https://forms.gle/PHQjjADVXTyVbXGc7
- 贊助廠商：NT$30,000
- 入會表單：https://forms.gle/NjhHmEwxCUrw8FBW8

講師：宋昇峯、林明傑、吳啟裕、張克咸、楊尚儒、陳佩君、藍士哲

---

## 📌 下一棒待辦

- 1206 桃園場內容補完善（教練會提供報導及花絮，不急）
- 626 議程時間如有更動再調整

---

## 🔴 部署鐵律

Netlify 手動上傳型，每次更新：
1. 修改 /tmp/northern_images/index.html
2. zip -r deploy.zip .
3. curl API 推送（絕對不用 git push）

---

## 🗓 蒸餾系統現況（2026-05-30 本場建立）

### 蒸餾系統架構
| 層 | 檔案 | 用途 |
|---|------|------|
| 提取 | `scripts/extract_terminal_sessions.py` | 從 JSONL 提取教練原話，寫入 pending_distill/ |
| 蒸餾 | `scripts/distill_terminal_llm.py` | 呼叫 Claude LLM 自動蒸餾 |
| 排程 | `scripts/run_distill_terminal.sh` | cron wrapper：提取→蒸餾→git commit push |
| 狀態 | `terminal-notes/.extract_state.json` | 追蹤 87 個 session 是否已提取 |
| 原始 | `terminal-notes/done_distill/` | 87 個 session raw text（已存檔） |
| 蒸餾 | `distill/terminal_YYYY-MM-DD.md` | 已濃縮精華（14 個 session） |

### 蒸餾現況
| 指標 | 數量 |
|------|------|
| 總 session 數 | 87 個 |
| 已提取（done_distill） | 87 個 ✅ |
| 已蒸餾進 .md 檔 | 20 個（S1-S14 + A-F） |
| **未蒸餾（待下一棒）** | **67 個**（含 55 個實質內容） |

### 未蒸餾重點優先序（按教練原話數排序）
| 優先 | Session ID | 教練原話 | 日期 | 主題 |
|------|-----------|---------|------|------|
| 🥇 | c4bb5bf2 | 82 條 | 2026-05-17 07:59 | 守則演化 + GitHub Pages 部署 |
| 🥈 | 05a82b40 | 63 條 | 2026-05-29 14:06 | 未確認（可能 Windows 教學） |
| 🥉 | 8edf0dc7 | 58 條 | 2026-05-05 08:30 | 未確認 |
| 4 | f1631209 | 57 條 | 2026-05-15 13:57 | 未確認 |
| 5 | 27767e3a | 46 條 | 2026-05-22 03:16 | 未確認 |
| 6 | 74751326 | 43 條 | 2026-05-29 01:57 | 未確認 |
| 7 | de3cc846 | 41 條 | 2026-05-20 03:31 | 未確認 |
| 8 | e72f3be0 | 38 條 | 2026-04-26 19:06 | 未確認 |

### 蒸餾指令（已測試可用）
```bash
cd ~/.claude-code/workspace
python3 scripts/extract_terminal_sessions.py   # 先提取
ls terminal-notes/pending_distill/            # 看有沒有新檔
# 用 Opus 無限流量蒸餾，格式：
# 教練原話用「👤 教練：」標記，一字不改
# 每 session 濃縮到 300-500 字
# 結果寫入 distill/terminal_YYYY-MM-DD.md
```

### 已蒸餾 Session（S1-S14 格式）
```markdown
## 📍 Session N：YYYY-MM-DD 時段（模型）｜主題標籤

### 教練關心的重點
（濃縮 100-200 字，引用教練原話）

👤 教練：「原話一字不改」

### 解決的問題
- bullet point 列表
- 每個要點一句話

### 重要教訓
- **守則#XX**：具體哪條
```

---

## 🔴 本場完成（Opus 軍師 2026-05-30）

| 任務 | 結果 |
|------|------|
| 蒸餾 Session 13（fc380e54） | ✅ Windows 教學籌備，Haiku 4.5 |
| 蒸餾 Session 14（cf4cf707） | ✅ 全自動總結系統建立，Opus 白燒 13% |
| distill/terminal_2026-05-30.md | ✅ 增至 14 個 session |
| extract_state.json | ✅ 更新至 87 個 session |
| done_distill/ | ✅ 87 個 raw text 存檔 |
| 新建 distill_terminal_llm.py | ✅ |
| 新建 run_distill_terminal.sh | ✅ |

### 本場犯錯記錄
- **Session 14 犯錯**：Opus 視窗裡又查 API、又建腳本，把簡單事複雜化，白燒 13% 流量
- 違反守則#03（思考就是問問題）、#12（拒絕當搬運工）、#16（複雜解法不一定是正確的）

---

## 📌 下一棒待辦

### 🔴🔴🔴 最高優先：繼續蒸餾（67 個未完成）

下一棒軍師開工後：
1. 讀 `distill/terminal_2026-05-30.md`（已蒸餾 S1-S14）
2. 讀 `terminal-notes/done_distill/`（87 個 raw text）
3. 按上表優先序蒸餾（c4bb5bf2 → 05a82b40 → 8edf0dc7...）
4. 每 5 個 session commit 一次（給 hash）
5. 全部完成後更新 `distill/守則故事庫/` 相關檔案

### 🟡 次優先：守則故事庫增補
- 守則#13（大師兄與華山派）：需補真實教練原話
- 守則故事庫目前 24 個檔，蒸餾結果可用來補充更多守則案例

### 🟢 一般：northern-tw 網站
- 1206 桃園場內容（教練提供報導花絮後才做）
- 626 議程時間如有更動再調整

---

**commit hash：** `6976c766`
**時間：** 2026-05-30 12:XX（台灣時間）
**軍師：** Claude Opus 4.7 Max（桌面版 App）
