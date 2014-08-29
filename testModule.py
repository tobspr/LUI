
from panda3d.core import *

loadPrcFileData("", """
notify-level-lui spam
""")

import LUI


print "Exposed attributes/classes:"
print dir(LUI)


sprite = LUI.LUISprite()
print sprite.getPos()

pos = LPoint2(0.5,1.0)
sprite.setPos(pos)
print sprite.getPos()
print sprite.getPos().getX()

# sprite.setTexcoordStart(0.0, 0.0)

root = LUI.LUIRoot()
print type(root)