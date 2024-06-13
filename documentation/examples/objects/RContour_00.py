# fontParts manual
# Contour object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
# take a glyph (one with outlines obviously)
g = f['adieresis']

# get to contours by index:
print(g[0])

# Show that we can get straight to the bPoints
print(len(g[0].points))
