# see if "A" and "B" can interpolate
from fontParts.world import OpenFont
f = OpenFont("test.ufo")
a = f["a"]
print(a.isCompatible(f["b"], False))
