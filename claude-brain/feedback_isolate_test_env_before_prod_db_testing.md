---
name: feedback-isolate-test-env-before-prod-db-testing
description: 教練正在真實使用中的功能，測試時必須用隔離副本(整個repo rsync到/tmp)，不能直接在production db上測試後再清資料
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fc75ce1b-c241-4d2d-ac45-f4b2e9391167
  modified: 2026-08-07T18:59:20.844Z
---

2026-08-08，mentor100訪客計數器功能上線後，教練回報「Mac上面看到8次，Windows上面卻只是第1次」，一度以為是計數邏輯有bug（懷疑是不是分裝置/瀏覽器各自計算）。查資料庫後發現計數邏輯完全正確、是全站共用的單一全域計數，真正原因是：我在教練同一時段實際測試時，還在對正式資料庫做「清空測試資料，讓正式數字從0開始」的收尾動作，這個清空動作跟教練切換到Windows測試的時間點撞在一起，教練看到的「第1次」其實是被我清空後的結果，不是bug。

**Why:** 對一個教練已經開始真實依賴/觀察數字的功能（例如訪客計數器、申請名單這類「教練會盯著看」的即時資料），任何我自己的驗證動作如果直接操作production資料庫（哪怕事後清乾淨），只要跟教練的真實使用時間窗重疊，就會產生「數字不連續、行為詭異」的錯覺，讓教練誤判成程式bug，反而製造出根本不存在的信任問題。

**How to apply:** 這場後續(百人導師申請審核流程)的驗證改用完整隔離做法：`rsync -a --exclude venv --exclude __pycache__ --exclude .git --exclude static/uploads` 把整個repo複製到`/tmp/xxx_test`，複製一份`mentors.db`到隔離目錄，在裡面用`MENTOR100_PORT=xxxx`跑一份完全獨立的測試server（不同port、不同db檔案路徑，因為Flask app的DB_PATH是`os.path.dirname(__file__)`算出來的，換了資料夾cwd就換了db檔案），測試完`rm -rf`整個隔離資料夾即可，正式資料庫全程不會被寫入任何測試資料，不需要事後清理、也不會跟教練的真實操作時間窗打架。凡是「已經上線、教練會盯著數字看」的功能，後續每一次修改都比照這個隔離測試法，不要嫌麻煩多複製一次repo。
