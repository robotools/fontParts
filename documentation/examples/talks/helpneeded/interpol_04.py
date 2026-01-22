# see if "A" and "B" can interpolate
# and find out what's wrong if you can
from fontParts.world import OpenFont
f = OpenFont("test.ufo")
a = f["a"]
print(a.isCompatible(f["b"], True))
