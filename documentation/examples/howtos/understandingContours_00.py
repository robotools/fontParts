from fontParts.world import OpenFont

f = OpenFont("test.ufo")
# take a glyph (one with outlines obviously)
g = f["a"]
# get to contours by index:
print(g[0])
