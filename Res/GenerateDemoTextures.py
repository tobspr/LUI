

from panda3d.core import *
from random import randint, random


for i in xrange(1024):
    p = PNMImage(randint(1, 60), randint(1,60))
    # p = PNMImage(66,64)
    p.addAlpha()
    p.alphaFill(1.0)
    p.fill(random(), random(), random())

    p.write("demo_textures/" + str(i) + ".png")