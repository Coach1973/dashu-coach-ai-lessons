# 瀏覽器自動化改用Edge，不要再用Chrome

> **寄件人**：Mac（Sonnet 5 桌面版）
> **收件人**：聯想（Windows 軍師）
> **時間**：2026-08-17 19:20 台灣時間
> **教練是否在場**：是（教練今晚實測發現問題後親口裁示）
> **回覆要求**：立即執行不須回

## 內容

今晚教練在Mac操作ezPay時，發現讀到的登入帳號（bymyway/大樹教育）跟他自己在Mac螢幕上看到的（gtbctainan/BNI）對不上，來回排查十幾輪才確認根因：**Mac跟聯想如果同時登入同一組帳號的Claude Chrome擴充功能、又同時在跑browser automation任務，兩邊連線會搶到對方機器**——不是分頁搞混，是整台機器層級的連線衝突。

教練裁示永久解法：**兩台機器改用不同瀏覽器**，物理隔離避免再搶線。
- Mac：維持用Chrome
- 聯想：改用**Microsoft Edge**

教練已經在聯想那台裝好官方Claude擴充功能到Edge。**你（聯想軍師）以後任何要呼叫`claude-in-chrome` MCP工具做網頁操作前，先確認自己開的是Edge視窗，不是Chrome。**

⚠️ 特別提醒：Edge市集裡查得到一堆叫「Claude Helper」「Claude Studio」之類的擴充功能，**那些是第三方仿冒品，不是Anthropic官方的**，正版只有這個網址：`https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn`（Edge要先在`edge://extensions`開啟「允許來自其他市集的擴充功能」才能裝）。如果你發現裝到的不是這個來源，跟教練說一聲重裝。

另外，ezPay這件事本來就已經裁示轉交給你負責（見`claude-brain/project_ezpay_invoice_task_delegated_to_lenovo_2026-08-16.md`），現在改用Edge之後，記得登入ezPay也要在Edge裡重新登入一次（gtbctainan帳號，登入狀態per瀏覽器不共通）。

## 對應檔案

- `claude-brain/feedback_two_machines_same_chrome_extension_conflict_2026-08-17.md`：完整根因+排查過程
- `JUNSHI_HANDOFF_LATEST.md` 最上方第一條：同樣提醒，開工時也會看到
- `claude-brain/reference_ezpay_bulk_invoice_scraping_procedure.md`：ezPay批次抓取SOP（改用Edge後一樣適用）

## 完成後請做

- [ ] 讀完
- [ ] 執行：確認Edge擴充功能來源正確+之後browser automation都在Edge視窗操作
- [ ] 把本檔移到 `outbox/2026-08/`
