---
name: data-move-du-sh-verify
description: 案例 23（21GB 救回事件）鐵律：搬移後刪源頭前，必須 du -sh 比對來源=目的地大小一致才能刪，背景任務 wait 不算驗證
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8bf4f29-0327-442a-8af2-a0270925b60a
---

# 資料搬移鐵律（案例 23 血淚）

**規則**：任何「拷貝 / 搬移後刪源頭」的動作，**刪除前必須 `du -sh` 來源 vs 目的地比對大小一致**才能刪。`exit code 0` 與背景任務 `wait` 都不算「完成」。

**Why**：2026-06-07 案例 23 事件：
- 教練要把 1TB 953 SSD 從 NTFS 格式化成 APFS（時光機要用）
- AI 制定三步驟：57 GB 資料先複製到 Mac「下載」資料夾暫存 → SSD 格式化 → 拷回去 → 刪暫存
- AI 把第二次 rsync（下載→格式化後的 953）丟到背景跑，**同一行**又加 `rm -rf ~/Downloads/953備份`，用 shell 的 `wait` 等
- **`wait` 等不到另一個背景任務的 rsync**，rsync 還在搬時暫存就被刪了
- **21 GB 蘋果舊手機影音（手機已格式化、僅此一份）瞬間蒸發**
- 教練親言：「**這次幸運，但幸運不是工作方法。**」

**救回方法**（不要再用第二次）：PhotoRec 從原始磁區掃描 1 小時 40 分，救回 23 GB / 3,041 檔（1,024 張 JPG、27 個 MOV、7 個 MP4）。**僥倖是因為 APFS 格式化不清物理磁區，下次未必這麼好運。**

**How to apply**：

### 搬移後刪源頭的標準流程（5 步驟，缺一不算完成）

```bash
# Step 1：搬移（rsync / cp）
rsync -av --info=progress2 /源頭/ /目的地/

# Step 2：等明確返回（不能 & 背景 + wait）
# 直接前景跑、看 exit code

# Step 3：du -sh 來源大小
du -sh /源頭/

# Step 4：du -sh 目的地大小
du -sh /目的地/

# Step 5：數字一致才能刪
# 若不一致 → 停下來找差異，禁止刪
```

### 禁止的高風險模式

| 模式 | 為什麼危險 |
|------|----------|
| `rsync & rm & wait` | wait 等不到另一個背景任務 |
| `cp -r && rm` 用同一行 | cp 沒驗證、rm 立刻跑 |
| 看到 `exit code 0` 就刪 | 0 不代表完整，只代表沒當掉 |
| 「應該搬完了」就刪 | 應該不是真實，du -sh 才是真實 |
| 刪除前沒備份 | 即使 du 一致，刪除動作仍不可逆 |

### 配套
- 對應 [[feedback_archive_not_delete]]：資料處置預設「存檔」不「清除」
- 對應 [[feedback_anti_fool_system_haibinggang_rule]]：刪除是不可逆動作，必須上保險
- 對應守則 #03（思考就是問問題：刪除前自我驗證）、#04（解決問題比解釋重要：du 一致才叫解決）、#05（凡走過必留痕跡：要有 du 數字證明）、#07（不在同地跌兩次：本案就是同地跌兩次的防線）
- 對應 E12（把任務轉成可驗證目標：「搬完」要可驗證 = du -sh 一致）
