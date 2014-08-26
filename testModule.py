
from panda3d.core import NodePath
import LUI


print "Exposed attributes/classes:"
print dir(LUI)


for i in xrange(100):
    sprite = LUI.LUISprite()
    # sprite = NodePath("sprite")
    print sprite.getPos()
    # Does not work
    # print sprite.getPos().x
    # Does not work 
    # print sprite.getPos().getX()
    print type(sprite.getPos())
    print type(sprite.getPos())
    print type(sprite.getPos())
    print type(sprite.getPos())
    print type(sprite.getPos())

