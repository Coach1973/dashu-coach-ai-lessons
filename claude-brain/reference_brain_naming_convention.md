---
name: reference-brain-naming-convention
description: 共用大腦（claude-brain）三機通用檔名/frontmatter 命名公約 2026-06-25；任何機器寫記憶都照此格式，避免三機各取各名越長越亂
metadata:
  type: reference
---

# 共用大腦命名公約（claude-brain）

> 緣起：三機共用大腦上線後，聯想軍師寫的檔用了連字號（`feedback_shortcut-fix`）、有的沒前綴（`touchstone`），與 Mac 既有 119 檔不一致。2026-06-25 教練以信念三拍板統一。
> 鐵律：**任何機器（Mac/聯想/ACER）往 claude-brain 寫記憶，一律照此格式。**

## 一、檔名格式

```
<type>_<snake_case 描述>[_YYYY-MM-DD].md
```

- **type（必含，4 選 1）**：`user` / `feedback` / `project` / `reference`
  - `user`：教練是誰、習慣、偏好
  - `feedback`：教練給的做事指導（含糾正與確認），要附 **Why** + **How to apply**
  - `project`：進行中的工作、目標、約束
  - `reference`：外部資源指標（URL、儀表板、票號）或長存事實
- **描述**：全小寫，**詞與詞之間用底線 `_`，不准用連字號 `-`**
- **日期後綴（選用）**：只有日期可用連字號，格式 `_YYYY-MM-DD` 接在最後

✅ 對：`feedback_shortcut_fix.md`、`project_line_moved_to_e.md`、`project_xinfa_final_2026-05-20.md`
❌ 錯：`feedback_shortcut-fix.md`（描述用連字號）、`touchstone.md`（沒 type 前綴）

## 二、frontmatter 格式

```markdown
---
name: <type>-<kebab-case>      # 用連字號，詞同檔名
description: <一行摘要，給 recall 判斷相關性用>
metadata:
  type: user | feedback | project | reference
---
```

- **檔名用底線、`name:` 用連字號**，兩者詞相同（例：檔 `reference_coach_machines_naming.md` ↔ name `reference-coach-machines-naming`）。
- `[[連結]]` 一律連 `name:`（kebab），不連檔名 → 所以**改檔名不影響連結**，改 `name:` 才要同步更新引用。

## 三、其他鐵律

- **一檔一事實**：別把多個主題塞同一檔（原 `touchstone.md` 的反例已拆/改）。
- **每個檔在 MEMORY.md 補一行索引**：`- [標題](檔名.md) — 一句鉤子`。
- **本機限定不上雲**：`daily_*.md` / `.dreams/` / `*.bak`（已由 `.gitignore` 擋）。

## 四、機關（不靠自覺）

- 檢查腳本：`scripts/lint_brain_naming.sh` — 列出所有不合規檔名，回傳非 0 即有違規。
- 用法：寫完記憶、push 前跑一次；未來可掛 pre-commit。

## 相關
- [[project-claude-brain-cloud-sync]] — 共用大腦系統本體
