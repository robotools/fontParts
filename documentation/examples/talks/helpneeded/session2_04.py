# robothon06
# iterate through a glyph's contours

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
glyph = font['A']
print("glyph has %d contours" % len(glyph))
for contour in glyph.contours:
    print(contour)