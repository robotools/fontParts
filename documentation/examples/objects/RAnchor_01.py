# fontParts manual
# Anchor object
# attribute examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']

if len(g.anchors) > 0:
    for a in g.anchors:
        print(a.position)
