#!/bin/bash
# 把落在副螢幕上的所有視窗搬回主螢幕（教練的副螢幕是擴充塢附的，從不使用）。
# 用法：move_windows_to_main_display.sh [--dry-run]
DRY="${1:-}"
/usr/bin/osascript -l JavaScript - "$DRY" <<'JXA' 2>/dev/null
ObjC.import("AppKit");
function run(argv) {
  var dry = argv[0] === "--dry-run";
  var main = $.NSScreen.screens.objectAtIndex(0).frame;
  var W = main.size.width, H = main.size.height;
  var se = Application("System Events");
  var procs = se.processes.whose({ backgroundOnly: false })();
  var moved = [];
  procs.forEach(function (p) {
    var wins;
    try { wins = p.windows(); } catch (e) { return; }
    wins.forEach(function (w) {
      try {
        var pos = w.position(), size = w.size();
        var cx = pos[0] + size[0] / 2, cy = pos[1] + size[1] / 2;
        if (cx >= 0 && cx < W && cy >= 0 && cy < H) return;
        var nx = Math.max(0, Math.min(100, W - size[0]));
        var ny = Math.max(25, Math.min(100, H - size[1]));
        if (!dry) w.position = [nx, ny];
        moved.push(p.name() + "「" + (w.name() || "") + "」 " + pos[0] + "," + pos[1] + " → " + nx + "," + ny);
      } catch (e) {}
    });
  });
  return (dry ? "[試跑] " : "") + "副螢幕視窗 " + moved.length + " 個" + (moved.length ? "\n" + moved.join("\n") : "");
}
JXA
