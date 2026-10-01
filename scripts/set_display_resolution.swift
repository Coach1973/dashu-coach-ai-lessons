// 設定 Mac 大螢幕(id2)解析度：swiftc 本檔 -o /tmp/setres && /tmp/setres 寬 高。還原1920x1080：/tmp/setres 1920 1080
import CoreGraphics
let w = Int(CommandLine.arguments[1])!, h = Int(CommandLine.arguments[2])!
let opts = [kCGDisplayShowDuplicateLowResolutionModes: true] as CFDictionary
let ms = CGDisplayCopyAllDisplayModes(2, opts) as! [CGDisplayMode]
guard let m = ms.first(where: { $0.width == w && $0.height == h && $0.pixelWidth == w && Int($0.refreshRate) == 60 }) else { print("no mode"); exit(1) }
var cfg: CGDisplayConfigRef? = nil
CGBeginDisplayConfiguration(&cfg)
CGConfigureDisplayWithDisplayMode(cfg, 2, m, nil)
print("result", CGCompleteDisplayConfiguration(cfg, .permanently).rawValue)
