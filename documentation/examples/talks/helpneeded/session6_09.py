# show the objects from the fontlab layer

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
print(f.naked())

g =  f["A"]
print(g.naked())
