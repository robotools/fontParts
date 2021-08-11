# robothon 2009
# set basic attributes in a glyph
 
from fontParts.world import OpenFont
 
font = OpenFont("test.ufo")
glyph = font['A']

print(glyph.name)
print(glyph.width)
print(glyph.leftMargin)
print(glyph.rightMargin)
print(glyph.box)
print(glyph.str)

glyph.update()