# robothon06
# use some methods to transform a glyph

from fontParts.world import OpenFont

font = OpenFont("test.ufo")

# ask a font for a glyph by name
glyph = font['A']

# now you have a glyph object
# make it do stuff by calling some of its methods
glyph.move((100, 75))
glyph.scale((.5, 1.5))
glyph.appendGlyph(font['B'])
glyph.removeOverlap()
glyph.correctDirection()
glyph.update()
