# Cowork + Code 分工 SOP（特別優惠期專用）

> 適用期間：2026-06-13 起至 **2026-07-05**（Anthropic 宣布 Cowork 五小時配額翻倍）
> 優惠結束後：回到原本全走 Claude Code 軍師的作法
> 建立：2026-06-13 凌晨 00:58（教練親定）

---

## 為什麼這樣分工

| 工具 | 優勢 | 限制 |
|------|------|------|
| **Claude Cowork** | 五小時配額翻倍、無週使用上限 | 沙盒無 GitHub 認證，`git push` 會被擋 |
| **Claude Code（軍師終端機）** | 有 Mac 鑰匙圈 GitHub 認證，可直接推 | 有週用量上限，省著用 |

---

## 標準流程

```
1. 教練把任務丟給 Cowork
       ↓
2. Cowork 執行：研究、修改、git commit
   （Cowork 做完會說「commit 成功但 push 被擋」）
       ↓
3. 教練切到這裡（軍師終端機），說一個字：「推」
       ↓
4. 軍師查最新 commit → touch .git/PUSH_APPROVED → git push
   （30 秒完成，Netlify/GitHub Pages 自動部署）
```

---

## 軍師收到「推」的標準動作

```bash
# 1. 確認 Cowork 做的 commit 在哪個 repo
cd /Users/bymyway/github_repos/[repo名稱]
git log --oneline -3   # 確認最新 commit 是 Cowork 做的

# 2. 推（推送鎖自動管理）
touch .git/PUSH_APPROVED && git push origin main
```

---

## 適用的 repo

| Repo | 路徑 | 部署方式 |
|------|------|---------|
| jiesheng-leadership | `~/github_repos/jiesheng-leadership/` | git push → Netlify 自動 |
| cool-case | `~/github_repos/cool-case/` | git push gh-pages → GitHub Pages |
| theunrestrictedwar | `~/github_repos/theunrestrictedwar/` | git push → 需另跑 zip+API |

---

## 優惠結束後

教練說「回原本作法」或過了 2026-07-05 → **本 SOP 停用**，回到全走軍師終端機執行任務的方式。
