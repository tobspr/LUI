
"""

LUI Atlas Generator

"""


from os import listdir
from os.path import join

from panda3d.core import TexturePool, loadPrcFileData, PNMImage

import sys
sys.path.insert(0, "../")

from LUI import LUIAtlasPacker


# Supress PNMImage warnings about incorrect sRGB profile
loadPrcFileData("", "notify-level-pnmimage error")
loadPrcFileData("", "notify-level-lui spam")


class AtlasEntry:

    def __init__(self, verbose_name, source_path):
        self.name = verbose_name
        self.path = source_path
        self.tex = TexturePool.load_texture(source_path)
        self.w = self.tex.get_x_size()
        self.h = self.tex.get_y_size()
        self.area = self.w * self.h
        self.assigned_pos = None

    def __repr__(self):
        return self.name


def generate_atlas(files, dest_dat, dest_png):
    entries = []

    virtual_atlas_size = 32
    all_entries_matched = False

    print "Loading", len(files), "entries .."
    for verbose_name, source in files:
        entries.append(AtlasEntry(verbose_name, source))

    entries = sorted(entries, key=lambda a: -a.area)
    print "Loaded!"



    while not all_entries_matched:
        print "Trying to pack everything in a", virtual_atlas_size, "x", virtual_atlas_size, "atlas .."

        packer = LUIAtlasPacker(virtual_atlas_size)
        all_entries_matched = True

        for entry in entries:
            uv = packer.find_position(entry.w, entry.h)
            if uv.get_x() < 0:
                print "  Not all images matched"
                all_entries_matched = False
                virtual_atlas_size *= 2
                break
            entry.assigned_pos = uv

        


    dest = PNMImage(virtual_atlas_size, virtual_atlas_size)

    for entry in entries:
        src = PNMImage(entry.w, entry.h, 4)
        entry.tex.store(src)
        dest.copy_sub_image(src, int(entry.assigned_pos.get_x()), int(entry.assigned_pos.get_y()))

    dest.write(dest_png)


if __name__ == "__main__":

    supported_extensions = ["png", "jpg", "gif", "dds", "tga"]
    root_dir = "demo_textures"
    files = listdir(root_dir)
    convert = []

    for f in files:
        extension = f.split(".")[-1]
        verbose_name = ''.join(f.split(".")[:-1])
        if extension in supported_extensions:
            convert.append(
                (verbose_name, join(root_dir, f)))
    generate_atlas(convert, "atlas.dat", "atlas.png")
