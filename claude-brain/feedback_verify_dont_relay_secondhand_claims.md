---
name: feedback-verify-dont-relay-secondhand-claims
description: 教練不接受「另一個AI寫的記憶檔案」當證據——要親自查證（跑指令/讀原始log），不能只轉述別人的報告
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 823578fe-2c75-417e-aaa3-c036fa112b23
---

教練原話：「你轉述的證據鏈我相信它可能是真的，但『你轉述』跟『我親自看到』是兩回事。在沒親自驗到之前，我不動手——這不是卡你，是保護你（守則#04、#15）。」

**背景：** 2026-07-02，聯想軍師一開始只讀Mac軍師寫的記憶檔案（`reference_vps_provision_script.md`）就直接引用「腳本已測試通過」的說法給教練用。教練要求三項親自查證：①GitHub commit是否真的存在 ②VPS上的腳本檔案是否真的存在 ③原始逐字稿是否真的支持這個說法。三項都親自跑指令驗證後才過關。

**Why：** 記憶檔案是「別人事後寫的摘要」，可能過時、可能誇大、可能有遺漏（這場另一個真實案例：Mac軍師報告「開通全自動」，教練親自糾正說其實有核准關卡）。摘要沒有一手證據的可信度。

**How to apply：** 任何要教練「照著做/開工」的關鍵判斷，如果證據來源是「另一台機器的記憶檔案/報告」而非自己親眼驗證，動手前先花時間跑一次原始查證（SSH進去看、git log確認、讀raw session log），不要因為記憶檔案寫得完整、有條理就直接信任。這條比一般的「先查證」更嚴格——連「別的AI已經查證過」都不算數，要自己重跑一次。

Related: [[project_hermes_vps_multitool_session_2026-07-02]], [[feedback_verify_via_real_transcript_not_case_count]]
