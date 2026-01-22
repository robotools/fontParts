# robothon06
# work with kerning 3
# print a specific set of pairs

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
kerning = font.kerning

for left, right in list(kerning.keys()):
    if kerning[(left, right)] < -100:
        print(left, right, kerning[(left, right)])