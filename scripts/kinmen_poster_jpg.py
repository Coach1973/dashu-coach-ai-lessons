from PIL import Image, ImageDraw, ImageFont
import sys
REPO = "/Users/bymyway/github_repos/kinmen-kitchen-1205"
SRC = f"{REPO}/images/ph-IMG-001.webp"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_L = "/System/Library/Fonts/STHeiti Light.ttc"
INK=(22,17,14); CREAM=(244,234,216); MUTED=(205,189,165); RED=(179,50,42); AMBER=(211,155,69)

def f(size, light=False):
    return ImageFont.truetype(FONT_L if light else FONT, size)

def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def text_block(d, x, y, maxw, scale=1.0):
    rows = []
    rows.append(("eyebrow", "金門私廚 × AI 餐桌", f(int(34*scale)), AMBER))
    rows.append(("title", "秋瑩姐的金門私廚", f(int(78*scale)), CREAM))
    rows.append(("gap", None, None, None))
    rows.append(("big", "12/5（六）11:30–14:30", f(int(56*scale)), CREAM))
    rows.append(("kv", ("地點", "台南 KR 養生廚房"), f(int(40*scale)), CREAM))
    rows.append(("kv", ("費用", "每位 1,500 元，限 20 位"), f(int(40*scale)), CREAM))
    rows.append(("gap", None, None, None))
    rows.append(("line", None, None, None))
    rows.append(("eyebrow", "匯款報名", f(int(34*scale)), AMBER))
    rows.append(("kv", ("銀行", "將來銀行（代碼 823）"), f(int(40*scale)), CREAM))
    rows.append(("kv", ("帳號", "88660901056777"), f(int(44*scale)), CREAM))
    rows.append(("kv", ("專線", "0988-585-279"), f(int(40*scale)), CREAM))
    rows.append(("gap", None, None, None))
    rows.append(("small", "道地金門人秋瑩姐掌廚，餐前餐後有茶席，邊吃邊聊手機 AI", f(int(28*scale), True), MUTED))
    for kind, val, font, color in rows:
        if kind == "gap":
            y += int(18*scale); continue
        if kind == "line":
            d.line((x, y + 6, x + maxw, y + 6), fill=(211,193,161), width=2); y += int(26*scale); continue
        if kind == "kv":
            k, v = val
            d.text((x, y), k, font=f(int(30*scale), True), fill=AMBER)
            d.text((x + int(130*scale), y), v, font=font, fill=color)
            y += int(font.size * 1.55); continue
        d.text((x, y), val, font=font, fill=color)
        y += int(font.size * 1.5)
    return y

src = Image.open(SRC).convert("RGB")

# 直式 1080x1350（LINE／限動）
W, H = 1080, 1350
canvas = Image.new("RGB", (W, H), INK)
top = cover(src, W, 600)
canvas.paste(top, (0, 0))
grad = Image.new("L", (W, 200))
for yy in range(200):
    grad.putpixel((0, yy), 0)
gd = ImageDraw.Draw(grad)
for yy in range(200):
    gd.line((0, yy, W, yy), fill=int(255 * yy / 199))
canvas.paste(Image.new("RGB", (W, 200), INK), (0, 400), grad)
d = ImageDraw.Draw(canvas)
text_block(d, 70, 640, W - 140, scale=0.92)
canvas.save(f"{REPO}/images/edm-portrait.jpg", "JPEG", quality=80, optimize=True, progressive=True)

# 橫式 1600x900（臉書）
W2, H2 = 1600, 900
c2 = Image.new("RGB", (W2, H2), INK)
left = cover(src, 800, 900)
c2.paste(left, (0, 0))
d2 = ImageDraw.Draw(c2)
text_block(d2, 860, 170, 680, scale=0.82)
c2.save(f"{REPO}/images/edm-landscape.jpg", "JPEG", quality=80, optimize=True, progressive=True)
print("saved")
