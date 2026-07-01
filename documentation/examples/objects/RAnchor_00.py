# fontParts manual
# Anchor object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

for g in f:
    if len(g.anchors) > 0:
        print(g, g.anchors)
