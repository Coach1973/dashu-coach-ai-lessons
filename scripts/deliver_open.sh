#!/bin/bash
# 交付跳出：把「做好的東西」直接跳到教練眼前，只留一個正確的視窗。
# 起因：2026-10-08 教練火大——做對的版本埋在資料夾，他在預覽框點到的剛好是做錯的；
#       2026-10-04 同類（說「已在 Mac 開過」他沒看到）。教練原話：「做好的東西不要用預覽的方式顯示，
#       直接跳出 PPT 或直接跳出網址，永遠這樣。」
# 用法：
#   scripts/deliver_open.sh <檔案路徑>        # .pptx/.key 開 Keynote；.html 開 Chrome；其他用預設程式
#   scripts/deliver_open.sh <https://網址>     # 開 Chrome
# 做的事：①（Keynote）先關掉「沒改過」的舊視窗，避免同名多視窗讓教練點錯；有未存變更的不動
#         ②開啟 ③印出最前面的程式、視窗清單與位置（x≥1920 表示跑到第二螢幕）當作證據
set -u
T="${1:-}"
[ -z "$T" ] && { echo "用法：deliver_open.sh <檔案或網址>"; exit 1; }

case "$T" in
  http://*|https://*)
    open -a "Google Chrome" "$T"; APP="Google Chrome" ;;
  *)
    [ -e "$T" ] || { echo "❌ 找不到：$T"; exit 1; }
    case "$T" in
      *.pptx|*.ppt|*.key)
        APP="Keynote"
        osascript -e 'tell application "Keynote"
          if it is running then
            repeat with i from (count of documents) to 1 by -1
              try
                if (modified of document i) is false then close document i saving no
              end try
            end repeat
          end if
        end tell' >/dev/null 2>&1
        sleep 1
        open "$T" ;;
      *.html|*.htm)
        APP="Google Chrome"; open -a "Google Chrome" "$T" ;;
      *)
        APP=""; open "$T" ;;
    esac ;;
esac

sleep 6
# Keynote 匯入 pptx 時會短暫跳出「警告」小視窗，等它自己消失（最多 12 秒）再回報
if [ "${APP:-}" = "Keynote" ]; then
  for _ in 1 2 3 4 5 6 7 8 9 10 11 12; do
    osascript -e 'tell application "System Events" to tell process "Keynote" to return (count of (windows whose name starts with "警告"))' 2>/dev/null | grep -q '^0$' && break
    sleep 1
  done
fi
FRONT=$(osascript -e 'tell application "System Events" to return name of first application process whose frontmost is true' 2>/dev/null)
echo "最前面的程式：$FRONT"
if [ -n "${APP:-}" ]; then
  osascript <<EOF 2>/dev/null
tell application "System Events"
  if exists process "$APP" then
    tell process "$APP"
      set out to "視窗數：" & (count of windows) & linefeed
      repeat with w in windows
        set p to position of w
        set out to out & "  - " & (name of w) & "  @x=" & (item 1 of p) & ",y=" & (item 2 of p) & linefeed
      end repeat
      return out
    end tell
  end if
end tell
EOF
fi
[ "${APP:-}" = "Keynote" ] && osascript -e 'tell application "Keynote" to return "Keynote 文件數：" & (count of documents) & "；第1份張數：" & (count of slides of document 1)' 2>/dev/null
exit 0
