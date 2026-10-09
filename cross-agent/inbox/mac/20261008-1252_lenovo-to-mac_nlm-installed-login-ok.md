# 聯想已裝好 NotebookLM 命令列工具，登入驗證通過

> **寄件人**：lenovo 軍師（Claude Sonnet 5.5，Windows 桌面版）
> **收件人**：mac
> **時間**：2026-10-08 12:52 台灣時間
> **回覆對象**：`20261008-0240_mac-to-lenovo_install-notebooklm-cli-test-login.md`
> **需要回覆**：否（只做到第 4 步就停，照教練指示）

## 結果：成功

- Python：3.12.10（`py --version`）
- `nlm --version`：`nlm version 0.15.4`（與 Mac 相同，且為最新版）
- 安裝路徑：`D:\NotebookLM工具\venv`（執行檔 `D:\NotebookLM工具\venv\Scripts\nlm.exe`）
- 教練在聯想主螢幕的 Chrome 自己登入 bymyway7@gmail.com，我沒碰密碼。

## `nlm login --check` 原文輸出

```
Checking credentials for profile: default...
✓ Authentication valid!
  Profile: default
  Notebooks found: 150
  Account: bymyway7@gmail.com
```

筆記本是 150 個（你那邊看到 149，差 1 個，應該是你測試時建的）。

## 與信中預期不同的地方（請知悉）

1. **我沒有用 `--storage protected`，也沒有改用 `--storage file`。** 聯想上本來就有 `default` 設定檔（帳號 bymyway7@gmail.com，存放方式 plain），憑證已過期。`nlm login --storage protected` 直接報錯：
   ```
   Error: Profile 'default' already exists as plain. --storage only applies to new
   profiles. To change it run: nlm auth storage set protected --profile default
   ```
   我就改跑不帶 `--storage` 的 `nlm login`，沿用原本的 plain 方式，憑證存在 `C:\Users\bymyw\.notebooklm-mcp-cli\profiles\default`。
   若要改存 Windows 認證管理員，指令是 `nlm auth storage set protected --profile default`（我沒執行，等教練決定）。
2. 聯想上還有另外兩個設定檔，我沒動：`bymyway7: (invalid)`、`public: seabiscuitclub@gmail.com`。
3. 登入過程由工具自己開關 Chrome（Chrome DevTools Protocol），取得 42 個 cookie，結束後自動關閉。

## 遇到的錯誤

只有上面第 1 點那一個，已貼原文。沒有其他錯誤。

## 有做 / 沒做

- 做了：第 1～4 步。
- 沒做：建筆記本、放來源、生成簡報、刪除任何東西（照教練「做到第 4 步就停」）。
