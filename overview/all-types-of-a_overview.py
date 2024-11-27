import glob
import random
import yaml


BLUE = (0.3, 0.3, 1)
F = {
    "font": "AdapterMonoPEVF-All",
    "fontVariations": {"wght": 500},
    "openTypeFeatures": {"ss12": True},
    "fontSize": 5,
    "lineHeight": 8,
}

def draw_overview(letters, negative=False, show_captions=False):
    unit = 50
    cols, rows = 6, 6
    w, h = unit * cols, unit * rows + 10
    
    newDrawing()
    newPage(w, h)
    if negative:
        fill(0)
    else:
        fill(1)
    rect(0, 0, w, h)
    
    # list in the background
    if show_captions:
        fill(*BLUE)
        translate(0, 10)
        refs = FormattedString(**F, fill=BLUE)
        for i, letter in enumerate(letters):
            ref = f"{letter['typeface']} by " + ", ".join(letter["designers"])
            refs.append("%d  " % (i+1), openTypeFeatures={"ss12": True})
            refs.append(ref + "\n", openTypeFeatures={"ss12": False})
        text(refs, (40, h - 30))

    for i, letter in enumerate(letters):
        x = unit * (i % cols)
        y = unit * (rows - (i // cols) - 1)
        with savedState():
            translate(x, y)
            # caption
            if show_captions:
                txt = FormattedString(str(i+1), **F)
                text(txt, (unit / 2, 0), align="center")
            # image
            scale(0.3527777778)
            im = ImageObject(".." + letter["path"])
            if negative:
                # letter SVGs are black on transparent background
                im.colorInvert()
            image(im, (0, 0))
    endDrawing()

def draw_letter(letter, negative=False, duration=0.2):
    w, h = 1080, 1080
    
    newPage(w, h)
    frameDuration(duration)
    if negative:
        fill(0)
    else:
        fill(1)
    rect(0, 0, w, h)
    im = ImageObject()
    with im:
        scale(7.6)
        image(".." + letter["path"].replace(".svg", ".pdf"), (0,0))
        im.colorInvert()
    image(im, (0, 0))
    
# get letter data
with open("../_data/data.yaml", "r", encoding="utf-8") as f:
    letters = yaml.safe_load(f)["letters"]
# ignore letters without image
letters = [l for l in letters if l["path"]]
# randomize order
letter_paths = random.sample(letters, len(letters))

# overviews
# draw_overview(letters[:36], negative=True, show_captions=False)
# saveImage("../assets/sharing_image.png", imageResolution=300)
# draw_overview(letters[:36], negative=False, show_captions=True)
# saveImage("all-types-of-a_overview.png", imageResolution=300)
# saveImage("all-types-of-a_overview.pdf")

# animation

newDrawing()
for letter in letters:
    draw_letter(letter, negative=True)
saveImage("all-types-of-a_animation.mp4")
endDrawing()