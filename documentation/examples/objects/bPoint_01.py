# fontParts manual
# bPoint object
# Attribute examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']

for aPt in g[0].bPoints:
    print(aPt.bcpIn, aPt.bcpOut, aPt.anchor)
