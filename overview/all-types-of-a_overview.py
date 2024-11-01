import glob

unit = 50
cols, rows = 6, 6
w, h = unit * cols, unit * rows + 10
newPage(w, h)
fill(1)
rect(0, 0, w, h)
BLUE = (0.3, 0.3, 1)
F = {
    "font": "AdapterMonoPEVF-All",
    "fontVariations": {"wght": 500},
    "openTypeFeatures": {"ss12": True},
    "fontSize": 4,
}
fill(*BLUE)
translate(0, 10)
# # list
# with open("all-types-of-a_descriptions.txt", "r", encoding="utf-8") as f:
#     refs = FormattedString(**F, fill=BLUE)
#     for i, ref in enumerate(f.readlines()):
#         refs.append("%d  " % (i+1), openTypeFeatures={"ss12": True})
#         refs.append(ref + "\n", openTypeFeatures={"ss12": False})
#     text(refs, (40, h - 30))

F["fontSize"] = 7
F["fontVariations"]["wght"] = 700
fill(0)
rect(0, 0, w, h)
for i, path in enumerate(sorted(glob.glob("../assets/letters/*.svg"))):
    x = unit * (i % cols)
    y = unit * (rows - (i // cols) - 1)
    with savedState():
        translate(x, y)
        txt = FormattedString(str(i+1), **F)
        text(txt, (unit / 2, 0), align="center")
        # image
        scale(0.3527777778)
        image(path, (0, 0))

saveImage("../assets/sharing_image.png", imageResolution=300)
saveImage("all-types-of-a_overview.png", imageResolution=300)
saveImage("all-types-of-a_overview.pdf")
