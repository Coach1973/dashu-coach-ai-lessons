# TOOLS.md - Local Notes

## 環境架構
- **主機**：Mac mini（吳大樹的Mac mini）
- **位置**：所有 Bot（1號機、2號機、3號機）都在同一臺 Mac mini 上，不在 VPS
- **主機名稱**：wudashudeMac-mini.local

## ⚠️ 關鍵路徑（cron 環境 PATH 不含 /opt/homebrew/bin）

| 工具 | 絕對路徑 |
|------|---------|
| node | `/opt/homebrew/bin/node` |
| python3 | `/opt/homebrew/bin/python3` |
| claude-code CLI | `/opt/homebrew/bin/claude-code` |

**原則**：任何 cron wrapper 腳本一律使用絕對路徑，不依賴 PATH。

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
