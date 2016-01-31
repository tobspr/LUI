from __future__ import print_function

from common import *


@timeit(200, 100)
def test_01_create_lui_objects():
    for i in range(100):
        object = LUIObject(parent=region.root)
    region.root.remove_all_children()

@timeit(200, 100)
def test_02_create_lui_sprites():
    for i in range(100):
        object = LUISprite(region.root, "blank", "skin")
    region.root.remove_all_children()

@timeit(200, 2500)
def test_03_reattach_lui_objects():
    object = LUIObject()
    object2 = LUIObject(parent=region.root)
    for i in range(2500):
        object.parent = region.root
        object.parent = None
        object.parent = object2
        object.parent = None
    region.root.remove_all_children()

@timeit(200, 2500)
def test_04_positioning():
    object = LUIObject(parent=region.root)
    for i in range(2500):
        object.left = 3
        object.right = 8
        object.top = 3
        object.bottom = -2
        object.center_vertical = True
        object.center_horizontal = True
        object.centered = False, False
        object.top += 3
    region.root.remove_all_children()

@timeit(40, 10)
def test_05_vertical_layouts():
    layout = LUIVerticalLayout(parent=region.root)
    for i in range(10):
        for k in range(10):
            obj = LUIObject()
            sprite = LUISprite(obj, "blank", "skin")
            layout.add(obj)
        layout.reset()
    region.root.remove_all_children()

# Execute all tests
[v() for k, v in sorted(dict(locals()).items()) if k.startswith("test_")]
