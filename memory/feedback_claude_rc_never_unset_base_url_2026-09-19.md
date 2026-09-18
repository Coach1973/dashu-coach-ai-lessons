---
name: claude-rc-never-unset-base-url
description: claude rc啟動時明確unset ANTHROPIC_BASE_URL/API_KEY/AUTH_TOKEN反而觸發硬性檢查噴錯，正確做法是完全不去動它們
metadata:
  type: feedback
---

`claude rc`（Claude Code Remote Control）啟動時，如果shell命令裡明確寫`unset ANTHROPIC_BASE_URL`（或`env -u ANTHROPIC_BASE_URL`），即使目的是「清空它讓CLI用預設值」，實際會觸發CLI自己的硬性檢查噴錯：

```
Error: Remote Control is only available when using Claude via api.anthropic.com.
ANTHROPIC_BASE_URL is set and does not point at api.anthropic.com,
so this session is using a custom endpoint — unset it (or run in a shell without it) to use Remote Control.
```

錯誤訊息本身要你「unset it」，但你去unset反而觸發同一個錯誤——這是CLI實作上的反直覺行為，推測是它偵測「這個變數是否被顯式unset過」而非單純檢查目前的值是否為空。

**正確做法**：完全不要在啟動`claude rc`的shell命令裡碰`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`這三個變數（既不要export也不要unset），讓它們維持原本從`~/.zshrc`/`~/.claude/settings.json`繼承下來的狀態即可正常連線。只需要unset真正會擋住RC的`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`這一個變數。

- 為什麼重要：2026-09-19查修手機Remote Control時，舊版`scripts/restart_remote_control.sh`用「暫時搬移整份settings.json」這種粗暴解法繞過這個問題，一直沒意識到問題其實只在那三個變數的unset動作本身。新版腳本改成只unset一個key，同時反覆用tmux實測4輪交叉確認「不要主動unset BASE_URL」這個結論站得住腳，才敢寫進正式腳本。
- 怎麼應用：往後任何涉及`claude rc`啟動指令的腳本/alias，凡是要清掉MiniMax路由設定時，只鎖定`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`這個key，其餘BASE_URL/API_KEY/AUTH_TOKEN一律不要碰（無論是想清空還是想帶入自訂值都不要顯式操作，會觸發CLI內建檢查噴錯）。完整技術脈絡見[[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]。
