# fontParts manual
# bPoint object
# Usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']
for aPt in g[0].bPoints:
    print(aPt)
