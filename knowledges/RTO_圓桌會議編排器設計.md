---
name: round-table-orchestrator
description: "圓桌會議編排器（RTO）：教練發訊息進群 → 自動分解任務 → 注入給學長執行；A+B+C 整合，不拆分"
metadata: {"openclaw":{"emoji":"🍣","events":["message:preprocessed"]}}
---

# Round Table Orchestrator（RTO）— 圓桌會議編排器

> 立檔人：軍師（2026-06-09 凌晨）
> 設計依據：[TASOS v1.0](../../workspace/knowledges/TASOS_特助靈魂作業系統.md) Application 層
> 教練親口指令：「**A+B+C 全要、不拆分、保留人格、不要當搬運工**」

---

## 一、要解決的問題

教練在「頂級特助分工群」（chatId `-1003877502911`）丟個話題進去，**希望多個 AI 自動展開討論並收斂出結果**，不需要教練再去 @ 誰、督促進度、整合答案。

這就是「老闆動嘴、AI 全自動執行」的群組版實現。

## 二、整合 A+B+C 三條需求

| 需求 | 怎麼實現 | 對應元件 |
|------|---------|---------|
| **A. 彼此聽得到** | 既有 bot-relay-inbound 已注入「鄰居最近發言」 | ✅ 既有，不動 |
| **B. 真實討論** | RTO 在學長 context 注入「圓桌議程」（議題 + 建議發言順序 + 收斂方式） | 🆕 本 hook |
| **C. 分工協作** | RTO 用 MiniMax-M3 判斷「這個話題該誰負責調查、誰整理、誰收尾」並寫入議程 | 🆕 本 hook |

## 三、運作流程

```
教練 → 頂級特助分工群「研究小米手機新款」
     ↓
RTO 攔截（學長收到的 preprocessed 事件）
     ↓
判斷：發言者 user_id = 6124913915 ✅ 教練
     ↓
判斷：是不是新話題（簡單方法：教練訊息 + 跟最近 30 分鐘的話沒明顯關聯）
     ↓
注入「圓桌議程」到學長 context：
  「教練剛剛說：『研究小米手機新款』
   建議圓桌流程：
   ① 學弟 @kong 調查規格與評測（10 分鐘內）
   ② 學妹 @peipei 整合對小米的市場定位（同步進行）
   ③ 你（學長）等他們回報後做總結，@ 教練呈現結論」
     ↓
學長照議程執行（既有 sessions_send / @mention 機制）
     ↓
學弟/學妹完成 → 學長收斂 → 回報教練
```

## 四、最小可用版限制（v0.1）

- ✅ 只攔截教練（user_id 6124913915）發的訊息
- ✅ 只在學長身上跑（main agent）
- ✅ 議程用 MiniMax-M3 即時生成（不限流，成本不是問題）
- ⚠️ 不主動派發給學弟學妹（學長自己讀議程後派）
- ⚠️ 不監控「議題收斂」（等下一個版本）

## 五、未來擴充（v0.2+）

- 加「議題追蹤表」：寫到 `/tmp/openclaw/rto_active_topics.json`
- 加「收斂偵測」：學弟學妹都回報後，RTO 自動 ping 學長「該收尾了」
- 加「Telegram bot-to-bot 原生 API」（等 OpenClaw 2026.6.x 跟進）

## 六、安全 / 防呆

- 只在 `chatId === '-1003877502911'`（頂級特助分工群）跑，避免污染其他群
- 失敗靜默：不能因為 RTO 掛了就讓教練訊息送不出去
- 議程是「建議」不是「強制」——學長可以選擇不照走（守則#15「說不知道」精神）

## 七、註冊方式

```bash
# 已加進 openclaw.json hooks.internal.entries
# gateway 熱重載自動生效
```

---

## 八、Changelog

### v0.3（2026-06-09 上午 08:55，學妹搶順序後補強）

**動機**：v2.2 上線後測試（08:51 教練第二次測題），學妹仍搶在學弟前面發言。
根因：SOUL.md v2.2 規則寫在 140 行被淹沒，LLM 沒重視。

**改動**：handler.js 加 buildFollowerInjection() 給學弟學妹**直接由 RTO 注入硬性等待指令**：
- 觸發條件：`agentId !== MAIN_AGENT_ID` → `ALL_AGENTS = ['main', 'kong', 'peipei']`
- 學弟學妹收到不呼叫 LLM（省 token），直接注入靜態文字
- 文字明確告知「你的 mention」「對方的 mention」「你的角色」「等待規則」
- 一句鐵律：「這條規則優先於 SOUL.md」

**dry-run 驗證**：三隻機都正確收到對應 injection（學長收議程、學弟學妹收等待硬指令）。

### v0.2（2026-06-09 上午，OPE 後改造）

**動機**：教練親口「全新、清晰且明白的架構，用簡單容易的做法」+ OPE 網搜（AutoGen GroupChat + Council Mode）。

**改動三件**：

1. **prompt 升級**：generateAgenda() prompt 加入異構化角色
   - 🦞 學長 = 哲學家視角（先問本質、揭示假設、整合收尾）
   - 🦐 學弟 = 偵探視角（挖證據、找事實、給數據）
   - 🐰 學妹 = 辯論者視角（挑戰假設、提反方角度、整合矛盾）

2. **議程格式強制 Council Mode 三段收尾**：
   - ✅ 三方共識
   - ⚠️ 主要分歧
   - 💡 獨特發現
   - 禁止只給結論——教練要看推理過程，破純多數決不穩

3. **注入內容升級**：加「群組公開發言」鐵律
   - 學弟學妹在分工群直接公開發言，不再 sessions_send 私訊學長
   - 配套：學長 SOUL.md（commit 66fe13ce）、學弟 SOUL.md（commit e802c1d4）、學妹 SOUL.md（commit f5e8b40）同步升級

**OPE 依據**：
- [AutoGen GroupChat dynamic group chat](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/)
- [AutoGen Selector Group Chat（新 API）](https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/selector-group-chat.html)
- [Council Mode: Multi-Agent Consensus（arxiv 2604.02923）](https://arxiv.org/pdf/2604.02923)

**驗證方式**：教練在分工群（chatId -1003877502911）丟一個需要討論的題目，觀察：
- 學長收到 RTO 注入的圓桌議程
- 學長照議程在群裡 @ 學弟（@CoachWu_openclaw_bot）/學妹（@coachwu_lenovo_bot）
- 學弟學妹在群裡**公開發言**（不是私訊學長）
- 學長最後以 Council Mode 三段呈報教練

**Gateway restart**：2026-06-09 上午（PID 25170 → 38464）載入 v0.2。
