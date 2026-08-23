---
name: project_hook_orphans_never_registered_2026-08-24
description: 三支 hook（bni-member-directory-map／line-delivery-fallback／line-url-typo-guard）接力棒記載「已完成驗證」但從未註冊進 openclaw.json，一天都沒跑過，等教練決定是否啟用
metadata: 
  node_type: memory
  type: project
  originSessionId: c0394d00-7e60-4062-8d89-8edafcf326b1
  modified: 2026-08-23T20:05:21.682Z
---

2026-08-24 全系統稽核時，把 `~/.openclaw/hooks/` 21 個目錄逐一比對 `openclaw.json`，
發現這 3 支**檔案齊全、HOOK.md 也有、但從來沒被註冊**，等於寫好之後一天都沒運作過：

| hook | 原本要做什麼 | 建立日 |
|---|---|---|
| `bni-member-directory-map` | 新 LINE user ID 進來時自動查顯示名稱、比對通訊錄猜真實姓名，讓教練在後台看得懂是誰 | 2026-07-26 |
| `line-delivery-fallback` | bni_tainan 回覆送出失敗（reply token 過期）時自動改用 Push API 補送，避免訊息默默消失 | 2026-07-24 |
| `line-url-typo-guard` | 送出前校正回覆裡的網址錯字，避免會員點到 404；累計 3 次自動通知教練 | 2026-07-24 |

**跟接力棒記載矛盾**：`JUNSHI_HANDOFF_LATEST.md` v80 那段寫「三個 hook 都已經重啟驗證+commit」。
查 `git log -S` 確認 `openclaw.json` 從來沒出現過這幾個名字——所以「已驗證」這句話當時就不成立。

**為什麼 2026-08-24 沒有自行啟用**：其中 `line-delivery-fallback` 跟 `line-url-typo-guard`
會改動 BNI 大台南南區 LINE 公開帳號的**對外回覆行為**，那是真實會員在用的服務。
凌晨教練睡覺時，把三支從未在正式環境跑過的 hook 一次打開，出事會直接讓會員看到，
且教練當下無法反應——所以只回報不自行開啟，等教練一句話決定。

**要啟用的話**（教練說了再做）：
```bash
python3 - <<'EOF'
import json, collections
p='/Users/bymyway/.openclaw/openclaw.json'
d=json.load(open(p), object_pairs_hook=collections.OrderedDict)
for n in ['bni-member-directory-map','line-delivery-fallback','line-url-typo-guard']:
    d['hooks']['internal']['entries'][n]={'enabled':True,'path':f'~/.openclaw/hooks/{n}/handler.js'}
json.dump(d, open(p,'w'), ensure_ascii=False, indent=2)
EOF
openclaw gateway restart
```
啟用後**務必**用 [[reference_openclaw_hook_requires_hookmd_metadata]] 的方法核對
gateway log 的 loaded 數字有沒有從 16 變成 19，不能只看設定檔改好了就當作生效。

Related: [[reference_openclaw_hook_requires_hookmd_metadata]]、[[feedback_verify_activity_via_git_log_not_relay_file]]
