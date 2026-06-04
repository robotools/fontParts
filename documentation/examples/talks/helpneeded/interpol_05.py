# robothon06
# prepare glyph for interpolation
# move startpoints
# fix directions
# fix contour order

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
glyph = f["A"]

glyph.autoContourOrder()
glyph.correctDirection()
for c in glyph.contours:
    c.autoStartSegment()
glyph.update()
