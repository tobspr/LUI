
from panda3d.core import *

loadPrcFileData("", """
notify-level-lui spam
""")

import LUI


print "Exposed attributes/classes:"
print dir(LUI)


sprite = LUI.LUISprite()
print sprite.getPos()

pos = LPoint2(1.5,1.0)
sprite.setPos(pos)
print sprite.getPos()

root = LUI.LUIRoot()
print type(root)