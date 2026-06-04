# fontParts manual
# Font object
# Iterate through the font object to get to the glyphs.

from fontParts.world import OpenFont
f = OpenFont("test.ufo")

for glyph in f:
    print(glyph.name)
