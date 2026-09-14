import os
from PIL import Image

ASSETS = os.path.dirname(os.path.abspath(__file__))
OUT_BRAND = os.path.join(ASSETS, "brand")
OUT_ILL = os.path.join(ASSETS, "illustrations")
OUT_PACK = os.path.join(ASSETS, "packaging")
for d in (OUT_BRAND, OUT_ILL, OUT_PACK):
    os.makedirs(d, exist_ok=True)

BROWN = (54, 10, 9)      # #360A08 - matches sampled ink color exactly
CREAM = (242, 240, 236)  # #F2F0EC

def linework_to_transparent(src_path, out_path, fill_rgb):
    """Convert monochrome line-art-on-white JPG into an anti-aliased transparent PNG.
    Alpha is derived from luminance (white bg -> alpha 0, dark ink -> alpha 255),
    then the ink is recolored to fill_rgb. This preserves the original artwork's
    exact shapes/edges; it only changes background transparency and ink color,
    matching the brand kit's own brown/cream file variants.
    """
    im = Image.open(src_path).convert("RGB")
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    opx = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = (0.299 * r + 0.587 * g + 0.114 * b)
            # white (lum ~255) -> alpha 0 ; ink (lum ~24) -> alpha 255
            alpha = max(0, min(255, int((255 - lum) * (255 / (255 - 24)))))
            if alpha > 0:
                opx[x, y] = (fill_rgb[0], fill_rgb[1], fill_rgb[2], alpha)
    out.save(out_path)
    print("wrote", out_path)

linework_to_transparent(os.path.join(ASSETS, "01-logotipo.jpg"), os.path.join(OUT_BRAND, "logo-full-brown.png"), BROWN)
linework_to_transparent(os.path.join(ASSETS, "01-logotipo.jpg"), os.path.join(OUT_BRAND, "logo-full-cream.png"), CREAM)
linework_to_transparent(os.path.join(ASSETS, "09-simbolo.jpg"), os.path.join(OUT_BRAND, "symbol-brown.png"), BROWN)
linework_to_transparent(os.path.join(ASSETS, "09-simbolo.jpg"), os.path.join(OUT_BRAND, "symbol-cream.png"), CREAM)

# --- crop the 3-panel illustration sheet (Da Roca / Gourmet / Especial) ---
ill = Image.open(os.path.join(ASSETS, "11-ilustracao.jpg")).convert("RGB")
w, h = ill.size
# find near-white vertical gutter columns to split panels precisely
def is_gutter_col(x):
    sample_ys = range(0, h, max(1, h // 50))
    whites = 0
    total = 0
    for y in sample_ys:
        r, g, b = ill.getpixel((x, y))
        total += 1
        if r > 235 and g > 235 and b > 235:
            whites += 1
    return whites / total > 0.9

gutters = [x for x in range(w) if is_gutter_col(x)]
print("gutter cols sample:", gutters[:20], "..." if len(gutters) > 20 else "", "count:", len(gutters))
