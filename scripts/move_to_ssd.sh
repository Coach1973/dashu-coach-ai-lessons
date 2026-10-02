#!/bin/bash
# 把「會一直長大的資料夾」搬到外接 SSD，原位置改放捷徑（2026-10-03 教練定：主程式留本機，增量資料放 SSD）
# 用法：scripts/move_to_ssd.sh <資料夾絕對路徑> [SSD 上的名稱]
# 做法（同 10/02 搬 Chrome／下載的標準步驟，全程不刪任何東西）：
#   ①SSD 在線 ②複製 ③逐檔 checksum 比對、差異必須 0 ④確認沒有程式正開著它
#   ⑤原資料夾改名 .bak.日期（留到 7 天後才刪）⑥原位置放捷徑 ⑦驗捷徑讀得到
# 任何一步失敗就停手，原資料夾保持原狀。
set -u

SRC="${1:-}"
NAME="${2:-}"
SSD="/Volumes/953-SSD"
DAY=$(date +%Y%m%d)

say() { echo "[$(date '+%H:%M:%S')] $*"; }
die() { say "❌ $*"; exit 1; }

[ -n "$SRC" ] || die "用法：move_to_ssd.sh <資料夾絕對路徑> [名稱]"
case "$SRC" in /*) ;; *) die "請給絕對路徑：$SRC" ;; esac
SRC="${SRC%/}"
[ -d "$SRC" ] || die "找不到資料夾：$SRC"
[ -L "$SRC" ] && die "已經是捷徑，不用再搬：$SRC"
[ -n "$NAME" ] || NAME=$(basename "$SRC")

mount | grep -q " on $SSD " || die "外接 SSD 沒掛上：$SSD"
DST_DIR="$SSD/Mac本機搬移_$DAY"
DST="$DST_DIR/$NAME"
[ -e "$DST" ] && die "SSD 上已有同名資料：$DST（請換名稱）"

need_kb=$(du -sk "$SRC" | cut -f1)
free_kb=$(df -k "$SSD" | tail -1 | awk '{print $4}')
[ "$free_kb" -gt $((need_kb * 2)) ] || die "SSD 空間不夠"

say "①來源 $(du -sh "$SRC" | cut -f1)：$SRC"
mkdir -p "$DST_DIR"

say "②複製到 $DST"
rsync -a "$SRC/" "$DST/" || die "複製失敗，原資料夾沒動"

say "③逐檔比對（checksum）"
diffn=$(rsync -anc "$SRC/" "$DST/" | grep -v '/$' | wc -l | tr -d ' ')
[ "$diffn" = "0" ] || die "比對有 $diffn 個檔案不同（複製期間來源可能被改動），原資料夾沒動；SSD 上的副本留在 $DST 可刪"

say "④確認沒有程式正開著它"
if lsof +D "$SRC" 2>/dev/null | grep -q .; then
  lsof +D "$SRC" 2>/dev/null | awk 'NR>1{print $1}' | sort -u | tr '\n' ' '
  die "有程式正開著這個資料夾，請先關閉再重跑；原資料夾沒動"
fi

say "⑤原資料夾改名 → $SRC.bak.$DAY（留到 7 天後才刪）"
mv "$SRC" "$SRC.bak.$DAY" || die "改名失敗"

say "⑥原位置放捷徑 → $DST"
ln -s "$DST" "$SRC" || { mv "$SRC.bak.$DAY" "$SRC"; die "建立捷徑失敗，已把原資料夾改回原名"; }

say "⑦驗證捷徑"
if [ -d "$SRC" ] && [ "$(ls "$SRC/" | wc -l | tr -d ' ')" = "$(ls "$SRC.bak.$DAY/" | wc -l | tr -d ' ')" ]; then
  say "✅ 完成：$SRC → $DST；舊的留在 $SRC.bak.$DAY（7 天後再刪）"
else
  rm "$SRC" && mv "$SRC.bak.$DAY" "$SRC"
  die "捷徑驗證失敗，已改回原狀"
fi
