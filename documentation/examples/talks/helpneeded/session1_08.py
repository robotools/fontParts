# robothon06
# iteration through glyphs in a font

from fontParts.world import OpenFont

font = OpenFont("test.ufo")

print("font has %d glyphs" % len(font))

for glyph in font:
    print(glyph)