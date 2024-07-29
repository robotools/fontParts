# fontParts manual
# Usepens howto
# DigestPointStructurePen examples

from fontParts.world import OpenFont
from fontParts.pens.digestPen import DigestPointStructurePen

f = OpenFont("test.ufo")

myPen = DigestPointStructurePen()
f['period'].drawPoints(myPen)

print(myPen.getDigest())
