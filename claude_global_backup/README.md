# ~/.claude 全域配置備份

> 建立：2026-05-27 軍師
> 起因：`feed_junshi_handoff.sh` 曾憑空消失（settings.json 還引用、檔案卻不見），
>       根因是 `~/.claude/` 不在任何 git repo，關鍵配置一旦被覆蓋就無從恢復。
> 守則#07：不要在同一個地方跌倒兩次。

---

## 📦 備份了什麼

| 檔案 | 對應 | 說明 |
|------|------|------|
| `CLAUDE.global.md` | `~/.claude/CLAUDE.md` | 全域燒錄版心法（Claude Code 每次必讀）|
| `settings_hooks_only.json` | `~/.claude/settings.json` 的 hooks + permissions 區塊 | ⚠️ **刻意排除 env**（含 ANTHROPIC_AUTH_TOKEN，不可進 git）|

## 🔧 恢復方法

```bash
# 恢復全域 CLAUDE.md
cp ~/.openclaw/workspace/claude_global_backup/CLAUDE.global.md ~/.claude/CLAUDE.md

# 恢復 hooks（手動把 settings_hooks_only.json 的 hooks 區塊貼回 ~/.claude/settings.json）
# ⚠️ env 區塊（ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN）要另外從教練處取得，不在此備份
```

## ⚠️ 安全紅線

`~/.claude/settings.json` 的 `env` 含教練的 API token，**永遠不備份進 git、不 push 到 GitHub**。
此目錄只存「結構」與「無 secret 的配置」，供重建參考。

## 🔄 何時要更新此備份

每次修改 `~/.claude/CLAUDE.md` 或 `~/.claude/settings.json` 的 hooks 後，重跑：

```bash
cp ~/.claude/CLAUDE.md ~/.openclaw/workspace/claude_global_backup/CLAUDE.global.md
python3 -c "import json; d=json.load(open('/Users/bymyway/.claude/settings.json')); json.dump({'hooks':d.get('hooks',{}),'permissions':d.get('permissions',{})}, open('/Users/bymyway/.openclaw/workspace/claude_global_backup/settings_hooks_only.json','w'), ensure_ascii=False, indent=2)"
```
