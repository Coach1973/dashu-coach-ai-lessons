# 提煉：2026-03-02 C槽瘦身 Cowork Session

> 來源：D:\Claude-Data\Claude-Roaming\local-agent-mode-sessions（已於 2026-06-25 刪除）
> 提煉日期：2026-06-25
> 提煉者：聯想機軍師 Claude Sonnet 4.6
> 原始大小：~900KB jsonl

---

## 🎯 一句話總結

教練的宏碁 Windows 筆電 C 槽 100GB 幾乎全滿（88GB 已用），Cowork AI 從 Mac 遠端協助，透過教練手動執行 PowerShell 腳本，最終釋放近 20GB。

---

## 📖 三幕劇

**第一幕（困境）：**
C 槽 100GB 只剩 12GB，教練說「很奇怪，照理說不會滿」。AI 請教練安裝 WizTree 掃描，但 AI 自己在 Mac 上，無法直接控制 Windows 電腦——雙方各自在不同機器，這是本場最大的限制。

**第二幕（反轉 × 3）：**
1. AI 試圖幫教練把 .bat 清理腳本存到桌面，一直失敗——因為教練的桌面（Desktop）和下載（Downloads）都在 **D 碟**，而 Cowork 系統只能存取 C 碟，存不進去。
2. 改用記事本手動貼上腳本，又因為中文字編碼（Encoding）問題導致執行就閃退。
3. 最終改走 PowerShell 逐行輸入指令，才成功跑完清理。

**第三幕（頓悟）：**
清掉的主要空間：休眠檔（hiberfil.sys，約 6-8GB）+ WinSxS 系統清理（約 5-8GB）= **釋放近 20GB**，C 槽從 88GB 降至 68GB，剩餘從 12GB 回到 **23GB**。

---

## 🔑 關鍵線索（與未來高度相關）

| 線索 | 說明 |
|------|------|
| **教練的 Desktop/Downloads 在 D 碟** | 這是非標準設定，是日後所有「捷徑找不到」「存檔失敗」的根源 |
| **C 槽反覆滿** | 2026-03 滿過一次，2026-06-25 再次滿（觸發今天的搬移災難） |
| **Cowork 跨機限制** | Cowork AI 在 Mac，無法直接控制 Windows，必須靠教練手動執行 |
| **中文 .bat 腳本容易炸** | 編碼問題，PowerShell 直接執行比 .bat 可靠 |

---

## 📐 正確做法（C槽快速瘦身三板斧）

```powershell
# 1. 刪休眠檔（省 6-8GB）
powercfg -h off

# 2. WinSxS 清理（省 3-8GB）
Dism.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase

# 3. 磁碟清理（省 1-3GB）
cleanmgr /sagerun:1
```

---

## 🔗 與今天（2026-06-25）的關聯

今天教練為了解決「C 槽又滿了」，要求把 App 資料搬到 D 碟，引發四小時災難（見試金石案例 I）。

**根源是同一個問題：C 槽空間長期不足。**

根本解法建議（未執行）：
1. 定期跑上面三板斧（每季一次）
2. 考慮為 C 槽擴容，而不是搬移 App 資料（搬移風險遠大於效益）

---

*提煉完成，原始 jsonl 已刪除。*
