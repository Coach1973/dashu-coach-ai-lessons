# TOOLS.md - Local Notes

## 環境架構
- **主機**：Mac mini（吳大樹的Mac mini）
- **位置**：所有 Bot（1號機、2號機、3號機）都在同一臺 Mac mini 上，不在 VPS
- **主機名稱**：wudashudeMac-mini.local

## ⚠️ Git 推送驗證鐵律（2026-08-05 GitHub 5xx 學到）

`git push` 收到 `Internal Server Error` / 任何 5xx 時，**commit 本身仍然在本地建好，但遠端實際沒收**。本場 23:09 第一次推 `三機每日總結 2026-08-05` 就遇到 GitHub 回 `Internal Server Error`（Request ID D31C:286443:28C59C:2FC541:6A735218），重試一次才成功。

**鐵律**：
1. push 收到 5xx 一定要重試一次。
2. 重試後用 `git ls-remote origin <branch>` 確認 commit hash 真的出現在遠端，才算「推過了」。
3. commit ≠ push：「本地 commit 已就位」不等於「教練能看到」。

---

## ⚠️ 長命令的 exec 階段會被回收 → 結果一律寫檔再用 read 取（2026-10-26 實測）

2026-10-26 連續 10+ 次遇到：`exec` 階段在 10～20 秒後被回收（session 直接消失，只剩 `(no new output)`），命令其實被中斷，stdout 拿不到；同一時間 `process poll` 也會掉線。

**鐵律**：
1. 任何預計超過 ~15 秒的命令，**一律把輸出寫進 `/tmp/xxx.txt`**（`{ ... } > "$OUT" 2>&1`），再用 `read` 工具讀檔；**不要依賴 exec 階段的 stdout**。
2. `process poll` 拿不到輸出時不要一直 poll——改用寫檔＋`read`。
3. 推完 commit/push 一定要用 `git ls-remote` 驗（見上方鐵律）；這個命令快且可靠，適合單獨跑。
4. inline python heredoc 不要留半套 helper（例如呼叫沒定義的 `_try_alive`）——寧可拆成兩段，或直接用 `ps`／`lsof` 這類現成指令取代。

---

## ⚠️ 關鍵路徑（cron 環境 PATH 不含 /opt/homebrew/bin）

| 工具 | 絕對路徑 |
|------|---------|
| node | `/opt/homebrew/bin/node` |
| python3 | `/opt/homebrew/bin/python3` |
| claude-code CLI（軍師） | `/Users/bymyway/.local/bin/claude` |
| openclaw CLI（**排程用這支**） | `/Users/bymyway/.openclaw/tmp/agent-cli/openclaw` |

**原則**：任何 cron wrapper 腳本一律使用絕對路徑，不依賴 PATH。

> 🔴 2026-10-27 實測修正：`/opt/homebrew/bin/claude-code` 與 `/opt/homebrew/bin/claude` **都不存在**（command not found）。軍師 CLI 真正的執行檔是 `/Users/bymyway/.local/bin/claude`（symlink 到 `~/.local/share/claude/versions/<ver>`）。

## ⚠️ openclaw CLI 有三支，版本不一致 → 舊版會讀不了新設定（2026-10-27 實測）

`which -a openclaw` 會列出三支，版本差很多：

| 路徑 | 版本 | 能不能用 |
|------|------|---------|
| `/opt/homebrew/bin/openclaw` | 2026.6.34 | ❌ **不能用**：解析不了現在的 `openclaw.json`，`cron list` 直接噴 `Invalid config at .../openclaw.json`（`meta`、`browser.profiles.imported.color`、`agents.defaults.heartbeat`… 全部 Invalid input） |
| `/Users/bymyway/.nvm/versions/node/v24.21.0/bin/openclaw` | 2026.9.4 | ⚠️ 版本對但要靠 `openclaw: Retrying with .../node` 重試才跑得起來，輸出會混雜 Node 警告 |
| `/Users/bymyway/.openclaw/tmp/agent-cli/openclaw` | 2026.9.4 | ✅ **首選**：乾淨、秒回、輸出可直接解析 |

**鐵律**：要下排程指令（`cron add/list/rm`）一律用 `/Users/bymyway/.openclaw/tmp/agent-cli/openclaw`。
看到 `Invalid config` 先別懷疑設定壞掉——**先確認自己跑的是哪一支 CLI**。

**建立一次性提醒的可用寫法（2026-10-27 實測成功）**：

```bash
CLI=/Users/bymyway/.openclaw/tmp/agent-cli/openclaw
$CLI cron add \
  --at "2026-10-27T19:00:00" \
  --tz "Asia/Taipei" \
  --name "提醒發LRP戰報-2026-10-27-19:00" \
  --message "⏰ 教練，19:00 到了——該發 LRP 戰報了。" \
  --announce --channel telegram --to 6124913915 \
  --agent main --session isolated --json
```

- `--at` 給「無時區的 ISO」時，靠 `--tz` 決定時區；存檔會轉成 UTC（`2026-10-27T19:00 Asia/Taipei` → `at: 2026-10-27T11:00:00.000Z`），**驗收時要用 Asia/Taipei 換算回來看**，不要直接看 UTC 字串。
- 投遞教練本人用 `--to 6124913915`（DM），群組是 `-5115910257`，兩者不可混用。
- `--announce` 讓 agent 的最終回覆直接推到該 chat。
- 建完一定要用 `cron list --json` 驗 `nextRunAtMs` 換算後是不是正確的當下時間。

## 模型驗證

- **驗證腳本**：`~/.claude-code/workspace/scripts/validate-models.sh`（舊路徑 `~/.claude-code/scripts/` 已停用，2026-06-04 更新）
- **當前 Primary**：`claude/Claude Sonnet`
- **備用**：`google/gemini-3.1-pro-preview`

## 常用腳本（小龍蝦專用）

| 腳本 | 用途 | cron 頻率 |
|------|------|----------|
| `~/.claude-code/workspace/scripts/run_distill.sh` | 增量蒸餾今日對話 | 每 2 小時 |
| `~/.claude-code/workspace/scripts/run_relay_poll.sh` | 學弟妹讀取學長 RELAY_QUEUE | 每分鐘 |
| `~/.claude-code/workspace/scripts/sync_handoff_to_claudemd.sh` | 接力棒鏡像到 CLAUDE.md | 每 5 分鐘 |
| `~/.claude-code/workspace/scripts/heartbeat_audit.sh` | 心跳品質審查 | 每天 23:50 |

> ⚠️ 所有腳本路徑已統一移至 `~/.claude-code/workspace/scripts/`（2026-06-04 更新）

### 📋 報名人數／報名名單（2026-10-14，10/13 臨時 awk 把「4人以上」算成 1 人）
教練問「X 日報名人數」「列出報名同行的人」→ 一律跑 `python3 ~/.openclaw/workspace/scripts/registration_report.py <日期或場次，例如 1017>`，整段輸出直接回給教練（含「含同行至少 N 人」與完整名單）。不准自己用 awk／sqlite 臨時算。總覽：不帶參數。

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 🚀 軍師任務橋——讓小龍蝦呼叫軍師執行任務（2026-06-13 教練親定）

**觸發時機**：教練要推 git、或要軍師執行複雜任務時

### 推 git（教練說「推 XX」）

```bash
python3 -c "
import json, datetime
task = {
    'id': datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
    'type': 'push',
    'repo': 'REPO名稱',   # jiesheng-leadership / cool-case / theunrestrictedwar
    'branch': 'main',      # cool-case 要改成 gh-pages
    'requestedBy': '小龍蝦',
    'ts': datetime.datetime.now().astimezone().isoformat()
}
with open('/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_QUEUE', 'w') as f:
    f.write(json.dumps(task, ensure_ascii=False) + '\n')
print('✅ 已派任務給軍師')
"
```

### 叫軍師跑複雜任務（教練說「叫軍師做 XX」）

```bash
python3 -c "
import json, datetime
task = {
    'id': datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
    'type': 'task',
    'prompt': '教練要做的事情描述',
    'requestedBy': '小龍蝦',
    'ts': datetime.datetime.now().astimezone().isoformat()
}
with open('/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_QUEUE', 'w') as f:
    f.write(json.dumps(task, ensure_ascii=False) + '\n')
print('✅ 已派任務給軍師')
"
```

### 讀取軍師回報結果

```bash
cat /Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_RESULT 2>/dev/null
```

**注意**：
- 軍師會自動 Telegram 通知教練結果，小龍蝦也可以主動讀結果
- push 類型：軍師自動建通行證（PUSH_APPROVED）→ 推送 → 通知
- task 類型：軍師用 `claude -p` 執行 → 結果回寫 → 通知
- Repo 路徑一律在 `/Users/bymyway/github_repos/`

### 🔴 卡關規則（2026-10-01 教練親定）：口頭講完就去做，不准跟教練說「這個不行、那個不行」

教練的目標：**動嘴講完，小龍蝦就直接去執行。**
1. 自己能做的，直接做完，回報結果。
2. 自己做不到或被擋住（沒權限、沒工具、不確定誰管）：**不要對教練說「不行」「做不到」「卡住了」**。立刻用上面「叫軍師跑複雜任務」寫一封信給軍師，信裡寫清楚：①教練要什麼結果 ②你試過什麼 ③卡在哪一句錯誤訊息。
3. 寫完信，只對教練說一句：「已交給軍師處理，結果出來我回報您。」不要列出一堆障礙、不要叫教練去點任何東西。
4. 軍師收到信就想辦法解決，並回報結果；教練只需要聽結果。
5. 例外：花錢、不可逆操作、代表教練對外發言，才先問教練。

---

## 🔎 查話工具（recall）——記住教練每一句話的入口（2026-06-11 軍師建立，教練拍板）

**觸發時機**：教練問「我之前說過X嗎」「我什麼時候講過X」「幫我查X那件事」「我們之前討論過的X」——任何要找舊話的時候，**不要靠記憶猜，直接查**：

```bash
python3 ~/.openclaw/workspace/scripts/recall.py 關鍵詞
```

- 結果自帶台灣時間＋出處（小龍蝦群/峰哥群/佩佩群/終端機/每日摘要）
- 多關鍵詞 = 任一命中：`recall.py 早鳥 金流`
- 要更多筆：`recall.py --limit 20 關鍵詞`
- 同義詞自動展開（查「傘繩」自動連「散繩/閃神」一起查），同義詞表：`state/recall_synonyms.json`，發現新的語音諧音就補進去
- **Context 紀律**：只把搜尋結果（幾百字）帶進對話，禁止為了找話去讀大型 memory 檔
