import Foundation
import Vision
import CoreImage
import AppKit
let args = CommandLine.arguments
let inURL = URL(fileURLWithPath: args[1])
let outPath = args[2]
guard let ci = CIImage(contentsOf: inURL) else { print("load fail"); exit(1) }
let req = VNGenerateForegroundInstanceMaskRequest()
let h = VNImageRequestHandler(ciImage: ci)
try h.perform([req])
guard let obs = req.results?.first else { print("no mask"); exit(2) }
let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: h, croppedToInstancesExtent: false)
let out = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
try ctx.writePNGRepresentation(of: out, to: URL(fileURLWithPath: outPath), format: CIFormat.RGBA8, colorSpace: cs)
print("ok instances:", obs.allInstances.count)
