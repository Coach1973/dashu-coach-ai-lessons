# 鼠鬚管（Squirrel）移除與重新安裝經驗

> 任務日期：2026-06-03
> 軍師：Claude Opus 4.6

---

## 問題現象

教練反應：
- 鼠鬚管輸入法會自己不斷新增
- 本來只有 1 個，變成 4 個
- 刪掉之後又自動出現

---

## 根因分析

**不是「刪了又出現」，是 macOS 自動復原：**

1. Squirrel.app 雖然已被刪除
2. 但 macOS 在 `com.apple.HIToolbox.plist`（Input Sources）中仍保有輸入法註冊
3. 每次 macOS 偵測到「輸入法不存在」，就自動從 plist 復原
4. 這是 macOS 輸入法的保護機制，不是 bug

**為什麼會新增變 4 個：**
- 每一次「安裝失敗」或「偵測到不存在」就會寫入新的 registry
- 累積下來就變成 4 個重複的 Squirrel 輸入來源

---

## 解決方案

### 1. 先移除 Input Sources 註冊（根因治療）

```python
import plistlib

# 備份
cp ~/Library/Preferences/com.apple.HIToolbox.plist ~/Library/Preferences/com.apple.HIToolbox.plist.backup

# 讀取
with open('~/Library/Preferences/com.apple.HIToolbox.plist', 'rb') as f:
    data = plistlib.load(f)

# 過濾掉 squirrel
clean_sources = [src for src in data['AppleEnabledInputSources'] 
               if 'squirrel' not in str(src.get('Bundle ID')).lower()]

# 寫回
data['AppleEnabledInputSources'] = clean_sources
```

### 2. 移除殘留檔案

```bash
rm -f ~/Library/Preferences/im.rime.inputmethod.Squirrel.plist
rm -rf ~/Library/HTTPStorages/im.rime.inputmethod.Squirrel
```

### 3. 重新安裝 Squirrel

- 下載 `Squirrel-1.1.2.pkg`（不是 zip）
- 用 GUI 安裝（`open Squirrel-1.1.2.pkg`）
- 安裝完後**登出再登入**（觸發 Input Sources 更新）

### 4. 設定無蝦米（Rime + Liur）

```bash
# clone 無蝦米字根表
git clone --depth 1 https://github.com/hsuanyi-chou/rime-liur.git /tmp/rime-liur

# 複製到 Rime 目錄
mkdir -p ~/Library/Rime
cp /tmp/rime-liur/Rime/* ~/Library/Rime/

# 設定預設輸入法
cat > ~/Library/Rime/default.custom.yaml << 'YAML'
patch:
  schema_list:
    - schema: liur
YAML

# 觸發部署
open /Library/Input\ Methods/Squirrel.app
```

### 5. 設定 Ctrl+Space 快速切換

```bash
# 方法 1：GUI（推薦）
# 系統設定 → 鍵盤 → 快速鍵 → 輸入選單 → 設定為 Control+Space

# 方法 2：CLI（不一定有效）
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 60 "{ enabled = 1; value = <00000000 01000000 00000020 00000000 00000000>; }"
```

---

## 學到的經驗

1. **Input Sources（HIToolbox.plist）是獨立的** — 刪 App 不會自動清除輸入法註冊
2. **先用 plist 修改，再刪 App** — 順序很重要
3. **安裝後要登出再登入** — 這一步不能省略
4. **用 GUI 安裝 .pkg** — 比 CLI 更穩定
5. **Squirrel 安裝在 `/Library/Input Methods/`** — 不是 `/Applications/`

---

## 相關檔案位置

| 用途 | 路徑 |
|------|------|
| Squirrel.app | `/Library/Input Methods/Squirrel.app` |
| Rime 設定 | `~/Library/Rime/` |
| Rime build | `~/Library/Rime/build/` |
| Input Sources | `~/Library/Preferences/com.apple.HIToolbox.plist` |
| 無蝦米字根 | `rime-liur/Rime/` (GitHub) |

