import os
import random
import yaml
import drawBot as db


caption = """
A collection of peculiar shapes of the Latin lowercase letter ‘a’ (U+0061), subjectively selected to illustrate that an essential form of ‘a’ (if it exists) must be quite complex. The poster, designed by David Březina, was printed in 333 copies for the Automatic Type Design 3 conference, which took place from 17 to 21 February 2025 in Nancy, France.

all-types-of-a.rosettatype.com
"""
F = {
    "font": "AdapterMonoPEVF-All",
    "fontVariations": {"wght": 700},
    "openTypeFeatures": {"ss12": False},
    "fontSize": 5,
    "lineHeight": 8,
}
F2 = {
    "font": "AdapterMonoPEVF-All",
    "fontVariations": {"wght": 500}, #"slnt": -10, "ital": 1},
    "openTypeFeatures": {"ss12": False},
    "fontSize": 5,
    "lineHeight": 7.5,
}

def logo():
	p = db.BezierPath()
	logo = db.FormattedString("Rosetta", font="AdapterPEVF-All", fontSize=16,
								fontVariations={"wght": 750, "opsz": 10}, align="left")
	p.text(logo, (0, 5))
	tw, _ = db.textSize(logo)
	p.rect(0.7, 0, tw - 1, 2)
	return p

def draw_poster(letters, show_captions=False):
    cols = 7
    rows = len(letters) // cols
    margins = (20, 20, 100, 20)
    
    db.newDrawing()
    w, h = 800, 1190  # narrow A3. (842, 1190) is proper A3
    db.newPage(w, h)
    unit = (w - margins[1] - margins[3]) / cols

    # letters
    for i, letter in enumerate(letters):
        if i // (cols * rows) > 0:
            break
        with db.savedState():
            x = margins[3] + unit * (i % cols)
            y = h - margins[0] - unit * (i // cols + 1)
            db.translate(x, y)
            # caption
            designers = [d.replace(" ", " ") for d in letter["designers"]]
            if len(designers) < 3:
                designers = " & ".join(designers)
            else:
                designers = f"{designers[0]} & al."
            txt = db.FormattedString(f"{letter['typeface']}", **F, align="center")
            txt.append(f"\n{designers}", **F2)
            if letter['publisher'].strip() == "David Jonathan Ross":
                txt.append(f"\nDJR", **F2)
            else:
                txt.append(f"\n{letter['publisher']}", **F2)
            db.textBox(txt, (5, 0, unit - 10, 25))
            # image
            db.scale(0.6)
            iw, ih = db.imageSize(letter["path"])
            ix = (iw - unit) / 2
            iy = (ih - unit) / 2
            db.image(letter["path"], (ix, iy + 12))
    # caption
    with db.savedState():
        db.translate(margins[3], margins[1])
        txt = db.FormattedString(caption, **F, align="center")
        _, h = db.textSize(txt, width=(2*unit))
        db.textBox(txt, (1.5 * unit, 0, 4 * unit, 0.6 * unit))
        p = logo()
        lw = p.bounds()[2] - p.bounds()[0]
        lh = p.bounds()[3] - p.bounds()[1]
        db.translate(3.5 * unit - lw / 2, -lh / 2)
        db.cmykFill(0, 0, 0, 1)
        db.drawPath(p)
    db.endDrawing()
    
# get letter data
basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, "..", "_data", "data.yaml"), "r", encoding="utf-8") as f:
    letters = yaml.safe_load(f)["letters"]
# ignore letters without image and set up paths
letters_ = []
for letter in letters:
    if letter["path"]:
       letter["path"] = letter["path"].replace(".svg", ".pdf")
       letter["path"] = os.path.join(basedir, ".." + letter["path"])
       letters_.append(letter)
# randomize order
random.seed(0.123)
letters = random.sample(letters_, 70)

# overviews

draw_poster(letters)
db.saveImage(os.path.join(basedir, "all-types-of-a_poster.pdf"))
