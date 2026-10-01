// Mac 小螢幕(id1)鏡像到大螢幕(id2)。執行：swiftc 本檔 -o /tmp/mir && /tmp/mir ；還原兩個獨立螢幕：/tmp/mir off
import CoreGraphics
var cfg: CGDisplayConfigRef? = nil
CGBeginDisplayConfiguration(&cfg)
let off = CommandLine.arguments.count > 1 && CommandLine.arguments[1] == "off"
CGConfigureDisplayMirrorOfDisplay(cfg, 1, off ? kCGNullDirectDisplay : 2)
let r = CGCompleteDisplayConfiguration(cfg, .permanently)
print("result", r.rawValue)
