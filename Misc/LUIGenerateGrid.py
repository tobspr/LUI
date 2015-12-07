
from os import makedirs
from os.path import dirname, join, isdir
from panda3d.core import *


# Configuration
# source = raw_input("Source png file: ")
# destPath = dirname(source)
# borderSize = int(raw_input("Border size in pixel: "))

source = "btn_gray.png"
destPath = "../Builtin/res/"
destName = "ButtonDefault_#.png"
borderSize = 3

def extractSubImage(x, y, w, h, name):
    print "Extracting sub image to",name
    subPNM = PNMImage(w, h, 4)
    subPNM.copySubImage(img, 0, 0, x, y, w, h)
    suffix = destName.replace("#", name)
    subPNM.write(destPath + suffix)



img = PNMImage(source)
w, h = img.getReadXSize(), img.getReadYSize()

if not isdir(destPath):
    makedirs(destPath)

# top left
extractSubImage(0, 0, borderSize, borderSize, "TL")

# top right
extractSubImage(w-borderSize, 0, borderSize, borderSize, "TR")

# bottom left
extractSubImage(0, h-borderSize, borderSize, borderSize, "BL")

# bottom right
extractSubImage(w-borderSize, h-borderSize, borderSize, borderSize, "BR")

# top
extractSubImage(borderSize, 0, w-2*borderSize, borderSize, "Top")

# bottom
extractSubImage(borderSize, h - borderSize, w-2*borderSize, borderSize, "Bottom")

# left
extractSubImage(0, borderSize, borderSize, h-2*borderSize, "Left")

# right
extractSubImage(w-borderSize, borderSize, borderSize, h-2*borderSize, "Right")

# mid
# extractSubImage(borderSize, borderSize, w-2*borderSize, h-2*borderSize, "Mid")
extractSubImage(borderSize, borderSize, 1, h-2*borderSize, "Mid")
