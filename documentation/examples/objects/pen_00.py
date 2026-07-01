# fontParts manual
# Pen object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']

pen = g.getPen()

# do stuff with the pen to draw in this glyph
