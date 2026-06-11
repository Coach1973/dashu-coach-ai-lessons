// ============================================================
// 🔒 Safety Locks 外掛（小龍蝦端三鎖之二，2026-06-11 軍師建立，教練拍板）
//
// 起因：終端機端已有刪檔鎖/截圖鎖（PreToolUse hook），但小龍蝦
//       （OpenClaw gateway）走的是自己的 exec 工具，hook 管不到。
//       本外掛用官方 before_tool_call 把同一套鎖裝到小龍蝦身上。
//
// 通行證跟終端機共用同一個檔案（教練同意一次，兩邊都認）：
//   刪除：~/.openclaw/workspace/state/DELETE_APPROVED（10 分鐘）
//   截圖：~/.openclaw/workspace/state/SCREENSHOT_APPROVED（10 分鐘）
//
// 推送鎖不在此處——git pre-push 是倉庫層的鎖，任何人（含小龍蝦）
// 從那些資料夾 push 都會被攔，天生全覆蓋。
// ============================================================
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const STATE = path.join(os.homedir(), ".openclaw/workspace/state");
const TOKEN_DELETE = path.join(STATE, "DELETE_APPROVED");
const TOKEN_SHOT = path.join(STATE, "SCREENSHOT_APPROVED");
const MAX_AGE_MS = 10 * 60 * 1000;

function tokenValid(p) {
  try {
    const st = fs.statSync(p);
    if (Date.now() - st.mtimeMs <= MAX_AGE_MS) return true;
    fs.unlinkSync(p);
  } catch {}
  return false;
}

// 與終端機 delete_guard.sh 同一套特徵（兩邊必須同步維護）
const DANGER = [
  /\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\b|--recursive)/,
  /\bfind\b.*-delete\b/,
  /\bfind\b.*-exec\s+rm\b/,
  /\bgit\s+clean\b.*-[a-zA-Z]*f/,
  /\brsync\b.*--delete/,
  /\bshred\b/,
];
const SAFE_TARGETS =
  /\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+("|')?(\/tmp\/|\/private\/tmp\/|\$TMPDIR|node_modules\b)/;

// 案例 F 教訓：剝掉 heredoc 與引號內的字面文字再判斷
function stripLiterals(cmd) {
  let s = cmd.replace(
    /<<-?\s*['"]?([A-Za-z_][A-Za-z0-9_]*)['"]?[\s\S]*?\n\1(?=\s|$)/g,
    " HEREDOC ",
  );
  return s.replace(/"[^"]*"/g, '""').replace(/'[^']*'/g, "''");
}

export default {
  id: "safety-locks",
  name: "Safety Locks",
  register(api) {
    console.log("[safety-locks] 外掛已註冊 before_tool_call 攔截");
    api.on(
      "before_tool_call",
      (event) => {
        console.log("[safety-locks] 偵測工具呼叫:", event.toolName);
        if (event.toolName !== "exec") return;
        const cmd = String(event.params?.command ?? "");
        if (!cmd) return;
        const stripped = stripLiterals(cmd);

        // 📷 截圖鎖（案例 4：未經同意截圖）
        if (/\bscreencapture\b/.test(stripped) && !tokenValid(TOKEN_SHOT)) {
          return {
            block: true,
            blockReason:
              "📷🔒 截圖鎖：教練明令未經同意不可截圖。請先問教練；教練同意後執行 touch ~/.openclaw/workspace/state/SCREENSHOT_APPROVED 再重試（10 分鐘有效）。",
          };
        }

        // 🗑️ 刪檔鎖（案例 23：21GB 蒸發）
        if (DANGER.some((re) => re.test(stripped)) && !SAFE_TARGETS.test(cmd)) {
          if (tokenValid(TOKEN_DELETE)) return;
          return {
            block: true,
            blockReason:
              "🗑️🔒 刪檔鎖（案例23，21GB血淚）：珍貴資料只搬不刪；搬移後必須 du -sh 比對一致才能刪源頭。請改用搬到存檔區，或先取得教練同意後執行 touch ~/.openclaw/workspace/state/DELETE_APPROVED 再重試（10 分鐘有效）。",
          };
        }
      },
      { priority: 100 },
    );
  },
};
