# robothon06
# Use FontLab pathfinder functionality to cut one glyph from another

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
base = f["A"]
cutter = f["B"]
dest = f["C"]

dest.clear()
dest.appendGlyph(base)
dest.width = base.width
dest.naked().Bsubtract(cutter.naked())
dest.update()
