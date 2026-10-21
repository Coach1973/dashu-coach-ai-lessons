from PIL import Image, ImageDraw, ImageFont
import numpy as np, math, sys
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB"); a = np.array(im).astype(float)
HEI = "/System/Library/Fonts/STHeiti Medium.ttc"; ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
S = 4
CX, CY, RI = 122, 143, 85     # 左上標誌：圓心、紅色內圈半徑（以像素量測）
def text(cx, cy, s, size, color, font=HEI, stroke=0):
    f = ImageFont.truetype(font, size*S, index=0) if font==HEI else ImageFont.truetype(font, size*S)
    l = Image.new("RGBA", (400*S, 60*S), (0,0,0,0)); d = ImageDraw.Draw(l)
    b = d.textbbox((0,0), s, font=f); w,h = b[2]-b[0], b[3]-b[1]
    d.text((200*S - w/2 - b[0], 30*S - h/2 - b[1]), s, font=f, fill=color+(255,), stroke_width=stroke, stroke_fill=color+(255,))
    l = l.resize((400,60), Image.LANCZOS); im.paste(l, (int(cx-200), int(cy-30)), l)
# 清掉標誌文字區：每列以左右紅色邊緣（圈內 3 像素）的顏色做漸層；上緣羽化 4 列
orig = a.copy()
for y in range(155, 212):
    dy = y-CY; hw = int(math.sqrt(max(RI*RI-dy*dy,1)))-1
    ys = min(y, 196); hws = int(math.sqrt(RI*RI-(ys-CY)**2))-1
    l = orig[ys-4:ys+5, CX-hws+4:CX-hws+10].reshape(-1,3).mean(0); r = orig[ys-4:ys+5, CX+hws-9:CX+hws-3].reshape(-1,3).mean(0)
    alpha = min(1.0, (y-155+1)/4.0)
    for x in range(CX-hw, CX+hw+1):
        t = (x-(CX-hw))/max(2*hw,1)
        new = (1-t)*l + t*r
        old = orig[y, x]
        im.putpixel((x,y), tuple(int(v) for v in (1-alpha)*old + alpha*new))
text(CX+2, 165, "中華新媒體", 17, (255,255,255), stroke=1)
text(CX+2, 178, "CHINESE NEW MEDIA", 6, (255,255,255), font=ARIAL)
text(CX+2, 193, "影音發展協會", 17, (255,255,255), stroke=1)
text(CX+2, 206, "AUDIOVISUAL DEVELOPMENT ASSOCIATION", 5, (255,255,255), font=ARIAL)
im.save(dst)
im.crop((30,40,230,240)).resize((800,800), Image.LANCZOS).save("/tmp/poster_portrait/z_logo_fixed.png")
