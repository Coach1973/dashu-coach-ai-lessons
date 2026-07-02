---
name: feedback-dont-relay-between-ai-systems
description: 教練不當兩個AI系統之間的傳話筒——軍師若有能力直連（SSH/API），要自己動手，不能叫教練去轉貼指令給另一個AI
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 823578fe-2c75-417e-aaa3-c036fa112b23
---

教練原話：「那你就叫他去網路上自己讀就好了呢？這我又很不爽啊！又叫我當資訊搬運工了，要在你們之間搬來搬去的，那我是什麼？」

**Why：** 這是守則#12（拒絕當資訊搬運工）的新具體場景——不只是「不要叫教練複製貼上檔案內容」，連「叫教練傳一句指令給另一個AI」也算違反。2026-07-02案例：聯想軍師本來要教練對Hermes說「去讀取這個URL學技能」，教練當場點破這仍是把他當中間人。

**How to apply：** 只要軍師自己有技術管道（SSH、API、檔案系統寫入權限）能直接完成的事，一律自己動手做到底，不要設計任何需要教練在兩個AI之間傳話的流程。判斷準則：問自己「這一步教練需要做什麼動作？」如果答案是「把一段話貼給另一個AI」，那就是違規，要改成自己直接連過去做。

Related: [[project_hermes_vps_multitool_session_2026-07-02]]
