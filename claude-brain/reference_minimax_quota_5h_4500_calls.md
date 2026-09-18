---
name: reference-minimax-quota-5h-4500-calls
description: 教練的MiniMax方案是「5小時內4500次呼叫」上限，教練已講過30次以上——遇到MiniMax錯誤/429/quota類問題，直接用這個數字比對，不要再問教練額度是多少
metadata: 
  node_type: memory
  type: reference
  originSessionId: 43af4704-419a-42cc-a1f0-d21ff9cd22a2
  modified: 2026-09-17T18:13:59.987Z
---

教練的 MiniMax 方案配額：**5 小時內 4500 次 API 呼叫**。這是教練多次（30次以上）明確講過的固定事實，遇到任何 MiniMax 相關錯誤（429、rate limit、quota 用盡等）時，直接拿這個數字去核對日誌裡的真實呼叫次數再下結論，**不要再回頭問教練「額度是多少」或「是不是用滿了」**——教練對這種重複發問已經明確表達不耐煩。

歷史案例：2026年稍早曾因為BNI相關任務在短時間內打出過多次呼叫，真的把額度用滿過，該事故已記錄在試金石檔案裡，屬於過去已結案事件，不代表現在遇到的每一次MiniMax錯誤都是同樣原因——現在遇到新的429錯誤，要先查真實呼叫次數（log）+ 確認是不是同一組帳號/key被哪個agent耗用，不能直接套用舊案例的結論。

**2026-09-18更新（試金石案例75）：診斷速度教訓**——額度異常暴增時，不要先套理論（歷史累加桶、背景漏洞、顯示器不準），第一步先問「教練最近跟哪個機器人講過話」，直接拉那個機器人最近5~10分鐘的原始log找同一traceId密集重複的爆發訊號，這是機械、廉價的檢查，比繞去算歷史累加快得多。當晚真正查出的兩個根因：小二(test2/OpenClaw 2.0沙盒)有兩種「工具呼叫失敗→無限重試」的bug（NO_REPLY送出被擋、edit工具寫檔失敗），官方GitHub有對應的未關閉issue #122261「Tool retry loops can saturate gateway event loop — propose per-tool circuit breaker」，是整個OpenClaw 2.x線目前已知但未修復的洞。教練最終裁示：test2已停用（gateway process已kill），等該issue真正修復或有測2.0差異化功能需求時才重啟評估，近期不用主動追蹤。

[[feedback_check_shared_resource_before_recommending_revoke_2026-09-13]]
