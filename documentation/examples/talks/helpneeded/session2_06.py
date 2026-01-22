# robothon06
# iterate through points

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
glyph = font['A']
for p in glyph[0].points:
    print(p.x, p.y, p.type)