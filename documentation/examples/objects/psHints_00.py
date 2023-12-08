# example of accessing the postscript blues
# data using the font.info attributes.

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

print(f.info.postscriptBlueValues)
print(f.info.postscriptOtherBlues)
print(f.info.postscriptFamilyBlues)
print(f.info.postscriptFamilyOtherBlues)
