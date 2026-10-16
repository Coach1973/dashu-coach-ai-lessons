---
name: image-archive-github
description: 教練說「下載」「打包」「一次性下載」「不想一張一張抓」+ 剛跑完 batch 出圖任務（tava-ai-batch / character-illustration-batch / infographic-lk888） → 不要 Telegram 一張一張抓，建 `coach1973/<slug>-archive` **私庫**一次推齊，附 MANIFEST.md（每張圖的章節/用途/reference 對照）+ PROMPTS.md（prompt 摘要）+ README.md，coach 從 GitHub 按「Code → Download ZIP」一鍵打包帶走。MANIFEST 是這條路的核心 — 讓任何 AI（Claude / ChatGPT / Gemini）讀 zip 時 100% 知道每張圖對應到提案哪一頁、是哪種類型（retouch 或純文字）。
---

# 觸發判斷

教練訊息包含以下任一特徵：

- 「下載」「打包」「一次性下載」「不想一張一張抓」「怎麼打包」
- 「怎麼給 AI 看」「丟給 AI」「讓 AI 知道每張對應到哪」
- 出圖任務完成後立刻問「現在怎麼拿到全部」

**典型情境**：
- tava-ai-batch 跑完 8+ 張（例：2026-10-12 約瑟布 42 張 v1+v2 視覺包）→ 教練想下載全部
- character-illustration-batch 跑完 20+ panels → 教練想存檔備份
- infographic-lk888 跑完多版本（例：3 個 size） → 教練想打包帶走

**不是這個 skill**：
- 教練說「上架」「給網址」「公開」「給約瑟看」→ 走 `character-illustration-batch/publishing.md`（策展 SOP）
- 教練要單張 → 直接用 `message` 工具發
- 教練說「推到 Telegram 給我」→ 走原 batch skill 的 push 步驟（例：tava-ai-batch 步驟 7「推 Telegram 拆 4+4」）

# 程序

## 1. 撈圖（從 workspace data/ 撈最新一份進 archive 工作目錄）

```bash
WORK=/tmp/<slug>-archive
mkdir -p $WORK/images
# 範例：撈 v1 + vN 兩批（檔名規則依原 batch script 寫法）
for n in 01 02 03 04 05 06 07 08; do
  src=$(ls -t /Users/bymyway/.openclaw/workspace/data/joseph_cloth_${n}_*.png 2>/dev/null | head -1)
  [ -n "$src" ] && cp "$src" "$WORK/images/v1_${n}_$(basename $src | sed 's/^joseph_cloth_[0-9]*_//;s/_lk888-[0-9-]*\.png$//').png"
done
# 檢查張數
ls $WORK/images/ | wc -l
```

⚠️ **不刪 `$WORK`**（觸發 21GB 安全鎖見 `character-illustration-batch/pitfalls.md` 條目「`rm -rf panels/` 觸發 21GB 安全鎖」）。新檔案直接覆蓋。

⚠️ 進 archive 前一律**重命名成乾淨檔名**（例：`v1_01_hero_facade.png`），不要把 raw timestamp (`_lk888-20261012-021040.png`) 帶進 zip。

## 2. 寫 MANIFEST.md（**核心** — 讓 AI 讀圖時 100% 知道用途）

完整模板見 `manifest-template.md`。必要欄位：

- **結構總覽表**（區塊 / 張數 / 檔名前綴 / 內容性質 / 生成方式）
- **完整對照表**（檔名 / 章節 / 用途 / 比例 / Telegram 訊息 ID）
- **Reference 對照**（哪些原圖用在哪些輸出）— 必加，否則 AI 看到 6 張看起來像的圖無法分辨 retouch 哪張對哪張
- **提案 PDF 配圖建議順序**（給約瑟看時的章節順序）

## 3. 寫 PROMPTS.md（精簡版 prompt 摘要）

每張圖一行 subject 摘要 + 共通風格指令。完整 prompt 在原始 batch script。

> 例：v2_07 的 subject = "borderless entrepreneur partnership network connecting regions through collaborative resources"（從 TAVA 原文 prompt 提煉）。

## 4. 寫 README.md（使用說明）

```markdown
# <任務> 視覺包

📦 N 張
📅 產出：YYYY-MM-DD
🎨 模型：OpenAI gpt-image-2

## 快速使用
1. **看對照表**：打開 `MANIFEST.md`（含每張圖的章節、用途、prompt 摘要、reference 對照）
2. **一次性下載**：點 GitHub 右上「Code → Download ZIP」打包帶走
3. **AI 助理讀圖**：把整包丟給 Claude / ChatGPT / Gemini / NotebookLM，AI 讀 `MANIFEST.md` 後 100% 知道每張圖的用途

## 兩種 AI 生成方式
- **Retouch**（v1_01-06 + vN_34-38）：用約瑟提供的原圖當 reference，AI 重新生成乾淨版
- **純文字生成**（其餘）：只有 prompt，AI 從零生成
```

## 5. git init + commit + 建私庫 + push

```bash
cd $WORK
git init -q
git config user.email "joseph-cloth-archive@coach1973.local"
git config user.name "小龍蝦"

cat > .gitignore <<'EOF'
.DS_Store
EOF

git add MANIFEST.md README.md PROMPTS.md .gitignore images/
git commit -m "<任務> 視覺包：N 張完整版 + MANIFEST"

# 一次建庫 + push
gh repo create <slug>-archive \
  --private \
  --description "<任務> 視覺包：N 張完整版 + MANIFEST" \
  --source=. \
  --remote=origin \
  --push
```

⚠️ `gh` CLI 必須已登入 `Coach1973` 帳號（`gh auth status` 確認），否則 `gh repo create` 會報 auth 失敗。

## 6. 驗證 push 成功

```bash
gh api repos/Coach1973/<slug>-archive/contents/images --jq '. | length'
# 應該 = N
```

## 7. 回報教練

```
✅ GitHub 私庫已建好 + N 張全部推送完成
🔗 https://github.com/Coach1973/<slug>-archive
📦 教練直接點網址 → 按「Code」 → 選「Download ZIP」→ 一鍵打包帶走
📋 裡面有：
- MANIFEST.md（N 張完整對照表）
- PROMPTS.md（每張圖 prompt 摘要）
- README.md（使用說明）
- images/（N 張 PNG，乾淨檔名）
```

# 已知陷阱

| 陷阱 | 解法 |
|------|------|
| `rm -rf $WORK` 觸發 21GB 安全鎖 | `mkdir -p` 不刪目錄，新檔案直接覆蓋 |
| `gh repo create --push` 跑大檔超時（>500MB）| 100MB 內 OK；超大檔考慮 `git lfs track` 或拆成多個 archive repo |
| MANIFEST.md 漏寫「Reference 對照」段 → AI 看到 6 張看起來像的 retouch 無法分辨 | 必加「Reference 對照」段，列出每張原圖用在哪些輸出（例：「原圖 75 → v1_01 + vN_37」）|
| 教練說「上傳」「上架」誤觸發此 skill（其實是要上架公開）| 「上架」「給網址」「公開」走 `character-illustration-batch/publishing.md`；只有「下載」「打包」「私庫」走這個 |
| 檔名帶 raw timestamp (`_lk888-20261012-021040.png`) 進 zip | 進 archive 前一律重命名成乾淨檔名（`v1_01_topic.png`）|
| 教練丟 zip 給其他 AI → AI 不知道哪張對哪 | MANIFEST.md 必填「Reference 對照」+「提案 PDF 配圖建議順序」兩段，AI 才能定位 |
| 私庫建成後教練說「公開」 | `gh repo edit --visibility public` 即可（仍受 100MB GitHub Pages 上限 → 改走 publishing.md 的策展 SOP）|

# 參考

- 來源案例：2026-10-12 約瑟布 42 張 v1+v2 視覺包（教練訊息「人呢？」+「怎麼一次性下載」+「丟給 AI 怎麼知道對應到哪」3 個問題促成）
- GitHub repo URL pattern：`https://github.com/Coach1973/<slug>-archive`
- gh CLI 認證：`gh auth status` 確認 Coach1973 帳號
- 觸發源 skill：tava-ai-batch / character-illustration-batch / infographic-lk888 完成後
- 區別於上架：`character-illustration-batch/publishing.md`（公開策展 SOP，會插 tainan-shangquan 卡片）
