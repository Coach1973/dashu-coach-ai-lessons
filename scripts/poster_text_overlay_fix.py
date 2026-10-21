from PIL import Image, ImageDraw, ImageFont
import numpy as np
src, dst = "/tmp/poster_swap_test2.png", "/tmp/poster_swap_test3.png"
im = Image.open(src).convert("RGB"); a = np.array(im)
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
S = 4
def mean(x0,y0,x1,y1): return tuple(int(v) for v in a[y0:y1, x0:x1].reshape(-1,3).mean(0))
def vfill(x0,y0,x1,y1,ya,yb):
    top = a[ya-2:ya+1, x0:x1].mean(0); bot = a[yb:yb+3, x0:x1].mean(0)
    for y in range(y0,y1):
        t = (y-y0+0.5)/(y1-y0)
        im.paste(Image.fromarray(((1-t)*top+t*bot).astype("uint8")[None,:,:]), (x0,y))
def fill(box, color): ImageDraw.Draw(im).rectangle(box, fill=color)
def text(cx, cy, s, size, color):
    f = ImageFont.truetype(FONT, size*S, index=0)
    l = Image.new("RGBA", (400*S, 80*S), (0,0,0,0)); d = ImageDraw.Draw(l)
    b = d.textbbox((0,0), s, font=f); w,h = b[2]-b[0], b[3]-b[1]
    d.text((200*S - w/2 - b[0], 40*S - h/2 - b[1]), s, font=f, fill=color+(255,), stroke_width=2, stroke_fill=color+(255,))
    l = l.resize((400,80), Image.LANCZOS)
    im.paste(l, (int(cx-200), int(cy-40)), l)
black1 = mean(1385,358,1400,378); black2 = mean(1347,633,1370,643)
gold = (236,190,72); print("sample", black1, black2)
# 獎座立牌：清掉亂字，補「創作者」
vfill(1336,262,1447,322,259,324); text(1391, 285, "創作者", 17, gold)
# 獎座底座：乾淨世界
fill((1327,601,1437,630), black2); text(1382, 615, "乾淨世界", 23, gold)
# 左上標誌：整行重寫「中華新媒體」
for y in range(127,149):
    l = a[y,50:54].mean(0); r = a[y,168:172].mean(0)
    for x in range(64,160):
        t=(x-64)/96; im.putpixel((x,y), tuple(int(v) for v in (1-t)*l+t*r))
text(111, 137, "中華新媒體", 17, (255,255,255))
im.save(dst)
im.crop((1260,180,1480,680)).resize((660,1500)).save("/tmp/z3_trophy.png")
im.crop((10,20,210,220)).resize((800,800)).save("/tmp/z3_logo.png")
