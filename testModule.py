
import LUI

print "Exposed attributes/classes:"
print dir(LUI)

sprite = LUI.LUISprite()
print sprite.getPos()
# Does not work
# print sprite.getPos().x
# Does not work 
# print sprite.getPos().getX()
print type(sprite.getPos())