# robothon06
# set basic attributes in a glyph

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
glyph = font['A']

glyph.width = 200
print(glyph.width)

glyph.leftMargin = 50
print(glyph.leftMargin)

glyph.rightMargin = 50
print(glyph.rightMargin)

glyph.str = 666
print(glyph.str)

glyph.update()
