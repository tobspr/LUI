
from os import makedirs
from os.path import dirname, join, isdir
from panda3d.core import *


# Configuration
# source = raw_input("Source png file: ")
# destPath = dirname(source)
# borderSize = int(raw_input("Border size in pixel: "))

source = "btn_hover.png"
destPath = "btn_hover"
borderSize = 6

def extractSubImage(x, y, w, h, name):
    print "Extracting sub image to",name
    subPNM = PNMImage(w, h, 4)
    subPNM.copySubImage(img, 0, 0, x, y, w, h)
    subPNM.write(join(destPath, name + ".png"))


img = PNMImage(source)
w, h = img.getReadXSize(), img.getReadYSize()

if not isdir(destPath):
    makedirs(destPath)

# top left
extractSubImage(0, 0, borderSize, borderSize, "tl")

# top right
extractSubImage(w-borderSize, 0, borderSize, borderSize, "tr")

# bottom left
extractSubImage(0, h-borderSize, borderSize, borderSize, "bl")

# bottom right
extractSubImage(w-borderSize, h-borderSize, borderSize, borderSize, "br")

# top
extractSubImage(borderSize, 0, w-2*borderSize, borderSize, "top")

# bottom
extractSubImage(borderSize, h - borderSize, w-2*borderSize, borderSize, "bottom")

# left
extractSubImage(0, borderSize, borderSize, h-2*borderSize, "left")

# right
extractSubImage(w-borderSize, borderSize, borderSize, h-2*borderSize, "right")

# mid
extractSubImage(borderSize, borderSize, w-2*borderSize, h-2*borderSize, "mid")
