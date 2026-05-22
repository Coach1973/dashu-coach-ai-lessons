---
name: Claude Code CLI 對話紀錄路徑
description: 終端機（Claude Code CLI）對話 session 的存放位置，可直接讀取 JSONL
type: reference
originSessionId: 8fc287b4-68a6-415b-9454-1df736e9c1fc
---
## 終端機版（Claude Code CLI）— JSONL 格式，可直接讀取

### 主工作目錄（最常用）
```
/Users/bymyway/.claude/projects/-Users-bymyway--openclaw/
```
- 約 32 個 session，每個是一個 `.jsonl` 檔
- 最新 session = `ls -lt *.jsonl | head -1`

### 其他工作目錄
```
/Users/bymyway/.claude/projects/-Users-bymyway--openclaw-workspace/
/Users/bymyway/.claude/projects/-Users-bymyway/
```

### 讀取指令
```bash
# 列出所有 session（按時間排序）
ls -lt /Users/bymyway/.claude/projects/-Users-bymyway--openclaw/*.jsonl

# 讀取指定 session 的對話訊息
python3 -c "
import json
with open('SESSION_FILE.jsonl') as f:
    for line in f:
        d = json.loads(line)
        if d.get('type') == 'message' and d.get('role') in ('user','assistant'):
            print(d['role'][:4], ':', str(d.get('content',''))[:100])
"
```

## 桌面版（Claude.app）— 二進位，不可直接讀取

```
/Users/bymyway/Library/Application Support/Claude/IndexedDB/https_claude.ai_0.indexeddb.leveldb/
```
- LevelDB 二進位格式，需特殊工具解析，**不建議終端機直接讀取**
