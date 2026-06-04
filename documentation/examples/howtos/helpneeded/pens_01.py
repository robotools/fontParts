# fontParts manual
# Usepens howto
# attribute examples

from fontParts.world import OpenFont
from fontParts.pens.digestPen import DigestPointPen

f = OpenFont("test.ufo")

myPen = DigestPointPen()
f['period'].drawPoints(myPen)

print(myPen.getDigest())
