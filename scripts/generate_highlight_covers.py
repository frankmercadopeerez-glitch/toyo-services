from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "social" / "highlights"
OUT.mkdir(parents=True, exist_ok=True)
SCALE = 4
W, H = 1080, 1920
RED, WHITE, BLACK, GRID = "#f20d2f", "#f5f5f3", "#06080b", "#20242b"

def sc(value):
    if isinstance(value, (tuple, list)):
        out = []
        for item in value:
            if isinstance(item, (tuple, list)):
                out.extend(sc(item))
            else:
                out.append(int(item * SCALE))
        return tuple(out)
    return int(value * SCALE)

def font(size):
    for candidate in (Path("C:/Windows/Fonts/bahnschrift.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), sc(size))
    return ImageFont.load_default()

def centered_text(d, y, text, face, fill, spacing=0):
    widths = [d.textlength(ch, font=face) for ch in text]
    total = sum(widths) + sc(spacing) * max(0, len(text) - 1)
    x = (sc(W) - total) / 2
    for ch, width in zip(text, widths):
        d.text((x, sc(y)), ch, font=face, fill=fill)
        x += width + sc(spacing)

def base():
    im = Image.new("RGB", sc((W, H)), BLACK)
    d = ImageDraw.Draw(im)
    for x in range(-H, W + H, 220):
        d.line(sc((x, 0, x - H, H)), fill=GRID, width=sc(1))
    cx, cy, radius = 540, 710, 276
    d.ellipse(sc((cx-radius, cy-radius, cx+radius, cy+radius)), outline=RED, width=sc(22))
    d.ellipse(sc((cx-radius+40, cy-radius+40, cx+radius-40, cy+radius-40)), outline="#4a111a", width=sc(3))
    return im, d

def label(d, text):
    centered_text(d, 1085, text.upper(), font(72), WHITE, 2)
    centered_text(d, 1208, "TOYO SERVICES", font(30), RED, 4)
    d.line(sc((450, 1295, 630, 1295)), fill=RED, width=sc(7))

def line(d, points, fill=WHITE, width=28):
    d.line(sc(points), fill=fill, width=sc(width), joint="curve")

def services(d):
    # Use the native engineering-symbol glyph for a mechanically balanced gear.
    symbol_font = ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", sc(320))
    symbol = "⚙"
    box = d.textbbox((0, 0), symbol, font=symbol_font)
    x = (sc(W) - (box[2] - box[0])) / 2 - box[0]
    y = sc(705) - (box[3] - box[1]) / 2 - box[1]
    d.text((x, y), symbol, font=symbol_font, fill=WHITE)
    d.ellipse(sc((492, 662, 588, 758)), fill=RED)

def motor(d):
    d.rounded_rectangle(sc((365, 600, 715, 820)), radius=sc(25), outline=WHITE, width=sc(28))
    d.rectangle(sc((440, 540, 640, 605)), outline=WHITE, width=sc(26))
    line(d, (365, 665, 325, 665, 325, 755, 365, 755), RED, 26)
    line(d, (715, 665, 755, 665, 755, 755, 715, 755), RED, 26)
    line(d, (440, 710, 640, 710), RED, 24)
    d.ellipse(sc((505, 675, 575, 745)), outline=RED, width=sc(20))

def protection(d):
    shield = ((540,515),(700,585),(680,770),(620,840),(540,900),(460,840),(400,770),(380,585),(540,515))
    line(d, shield, WHITE, 28)
    line(d, (455,705,515,765,635,625), RED, 30)

def location(d):
    d.ellipse(sc((405,510,675,780)), outline=WHITE, width=sc(28))
    d.polygon(sc(((425,700),(540,900),(655,700))), fill=WHITE)
    d.ellipse(sc((442,547,638,743)), fill=BLACK)
    d.ellipse(sc((490,595,590,695)), fill=RED)

def nosotros(d):
    face = font(155)
    word = "TS"
    box = d.textbbox((0,0), word, font=face)
    d.text(((sc(W)-(box[2]-box[0]))/2, sc(610)), word, font=face, fill=WHITE)
    d.line(sc((425,815,655,815)), fill=RED, width=sc(24))
    d.line(sc((480,855,600,855)), fill=WHITE, width=sc(12))

def save(name, text, painter):
    im, d = base()
    painter(d)
    label(d, text)
    im.resize((W,H), Image.Resampling.LANCZOS).save(OUT / f"highlight-{name}-v2.png", optimize=True)

save("servicios", "Servicios", services)
save("motor", "Motor", motor)
save("proteccion", "Protección", protection)
save("ubicacion", "Ubicación", location)
save("nosotros", "Nosotros", nosotros)
print("\n".join(str(p) for p in sorted(OUT.glob("*-v2.png"))))
