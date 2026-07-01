---
name: project-vps-local-embedding-fix-2026-07-02
description: VPS長期記憶語意搜尋修復成功——根因是env var把OPENAI_API_KEY接到NVIDIA金鑰造成embeddings 401，改用local模式(embeddinggemma-300m)後實測2.5個月前內容(4/20 n8n課程)能被正確撈回，最高分0.714
metadata: 
  node_type: memory
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-02凌晨，教練要求實測VPS小龍蝦的長期記憶能力（能不能記得兩個月前的事），並在發現故障後，指示比照Mac已驗證有效的方式修復——只測教練自己的main帳號，其他8位用戶不動。

**故障根因**：容器環境變數 `OPENAI_API_KEY` 被設成一組教練申請的NVIDIA萬用金鑰（nvapi-...），`OPENAI_BASE_URL` 指向NVIDIA API——這組金鑰本身有效（測`/v1/models`回200），但NVIDIA的embeddings端點路徑跟OpenClaw預設呼叫的不相容（回404），導致`openclaw memory search`直接401失敗，「No matches」不是真的沒有相關記憶，是引擎根本連不上。這個env var設定至少從5月就存在，一直默默壞著沒人發現。

**評估與OPE查證**：
- 教練質疑「VPS是雲端伺服器，local模式是不是不適用」——查證後確認local模式指的是「在同一台機器跑小型嵌入模型」，VPS本身就是完整機器，跟本機一樣適用，跟雲端/地端無關。
- OPE找到官方社群教學明確推薦：1 vCPU低資源VPS就該用`provider:"local"`+輕量模型（`embeddinggemma-300m-qat-Q8_0.gguf`約0.6GB），零外部依賴、零額外費用。
- 查MiniMax是否可當embeddings備案：MiniMax確實有`embo-01`嵌入模型，但OpenClaw官方GitHub上還是一個未實作的功能請求（Issue #62065），沒有原生整合，风险高於local模式。
- 結論：教練提出的「local優先、不行才考慮MiniMax」判斷完全正確，local路線勝出。

**執行**（僅限main agent，其餘8位trial用戶完全未動）：
1. VPS主機建2GB swap（原本0 swap，只有1.6GB閒置RAM，社群建議的保險措施）
2. 安裝官方外掛 `clawhub:@openclaw/llama-cpp-provider`
3. 只在`agents.list`裡main那筆entry加 `memorySearch:{enabled:true, provider:"local"}`，用python逐一比對確認8個trial agent的memorySearch欄位仍是False
4. 重啟容器、跑 `openclaw memory index --force --agent main`

**踩坑與教訓（誠實記錄，不美化）**：
- 第一次跑索引時，SSH連線本身斷線（"Connection reset by peer"），導致軍師誤判「輸出0行=卡住」，把仍在正常運算中的PID 64直接kill -9殺掉——**這是誤殺，浪費了約30分鐘已經在進行的真實進度**。事後查docker logs才確認是連線層問題，不是程式問題。
- 教訓：CPU/RSS持續變動 = 進程活著，缺乏「輸出」不代表「卡死」，尤其SSH+docker exec這種疊兩層管線的組合，連線本身就可能斷但容器內程序繼續跑。下次判斷「是否卡住」要先查連線本身是否還活著，不要只看本地看到的輸出。
- 第二次改用`nohup ... &`背景執行寫進VPS主機檔案，不受SSH斷線影響，最終順利跑完，全程約1小時28分鐘（177+個記憶檔案在1 vCPU上跑embedding，比預期慢很多，但這是一次性成本，之後只需增量索引新內容）。

**驗證結果（真實測試，非理論宣稱）**：
用 `openclaw memory search "n8n 課程 工作流程自動化" --agent main` 實測，最高分結果（0.714，遠高於次高分約0.37的雜訊）精準命中 `memory/2026-04-20-n8n-course-outline.md`——2026年4月20日教練與Wayne老闆討論n8n課程規劃的原始對話。**語意搜尋修復確認成功**，教練「記住兩個月前的事」這個要求，在main帳號上已經驗證做到。

**How to apply**：
1. 8位trial用戶目前仍是壞的embeddings設定（沿用預設沒被我改動）——教練這次只想先驗證單一帳號，若滿意效果，下一步是把同樣的`memorySearch:local`設定複製到8個trial agent，並各自跑一次`memory index --force --agent trial-{id}`（同樣預期在1 vCPU上會很慢，需要有耐心，且8個人依序做會疊加更久的總時間，可考慮排到教練不急的時段）。
2. 判斷「背景程序是否卡住」的通用做法：先確認連線層本身健康（單獨echo測試），再看CPU/記憶體是否持續變動，兩者都正常才叫「活著只是慢」；貿然kill掉還在動的進程等於浪費已完成的進度，這條也該收進試金石。

Related: [[project_vps_health_check_2026-07-01]], [[project_vps_multiagent_rollout_2026-07-02]], [[reference_vps_provision_script]]
