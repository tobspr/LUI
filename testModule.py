
from panda3d.core import *
import LUI


print "Exposed attributes/classes:"
print dir(LUI)


sprite = LUI.LUISprite()
print sprite.getPos()
sprite.setPos(LPoint2(1.5,1.0))
print sprite.getPos()

root = LUI.LUIRoot
print type(root)