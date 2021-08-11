# robothon06
# work with kerning 4

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
kerning = font.kerning

for left, right in list(kerning.keys()):
    if left == "acircumflex":
        print(left, right, kerning[(left, right)])