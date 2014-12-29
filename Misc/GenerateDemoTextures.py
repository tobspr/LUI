

from panda3d.core import *
from random import randint, random

from os import makedirs

try:
    makedirs("demo_textures/")
except:
    pass

for i in xrange(512):
    p = PNMImage(randint(1, 60), randint(1,60))
    # p = PNMImage(66,64)
    # p.addAlpha()
    # p.alphaFill(1.0)
    p.fill(random(), random(), random())
    # p.fill(1,1,1)

    p.write("demo_textures/" + str(i) + ".png")