# fontParts manual
# Usetransformations howto
# usage examples

from fontTools.misc.transform import Identity
from fontParts.world import OpenFont
import math

m = Identity
print(m)

m = m.rotate(math.radians(20))
print(m)

f = OpenFont("test.ufo")
for c in f:
    c.transform(m)
    c.update()
