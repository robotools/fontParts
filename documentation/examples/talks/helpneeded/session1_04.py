# robothon06
# getting data from the info object

from fontParts.world import OpenFont

font = OpenFont("test.ufo")

# naming attributes
print(font.info.familyName)
print(font.info.styleName)
print(font.info.fullName)

# dimension attributes
print(font.info.unitsPerEm)
print(font.info.ascender)
print(font.info.descender)