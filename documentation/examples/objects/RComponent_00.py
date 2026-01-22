# the easiest way to get to a component
# is to get one from a glyph

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['gbreve']

for c in g.components:
    print(c)
