---
name: reference-openclaw-hook-inject-format
description: "⛔已過時（2026-10-02）：inject 不管字串或物件都到不了模型，改看 feedback_openclaw_hook_fire_and_forget"
metadata: 
  node_type: memory
  type: reference
  originSessionId: cdae7e71-8e47-47bc-bf18-e9dbfee6ced3
---

# ⛔ 已過時：OpenClaw Hook inject 格式

**2026-10-02 更正**：這份原本說「`event.context.inject` 改成 `{role,content}` 物件就會生效」——**錯的**。查 2026.9.4 原始碼：`message:preprocessed` 的 context 是當場新建、用完就丟，沒有任何地方讀 `inject`；`agent:bootstrap` 只認 `bootstrapFiles`。不管字串還是物件，都到不了模型。

當初 RTO v0.1~v0.3「trajectory 裡 0 次出現」的真正原因就是這個，不是格式。

正確做法與受影響清單：[[feedback_openclaw_hook_fire_and_forget]]
