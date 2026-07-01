# robothon06
# interpolate two glyphs in the same font

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
factor = 0.5

f["C"].interpolate(factor, f["A"], f["B"])
f["C"].update()