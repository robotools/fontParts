# robothon06
# get a particular glyph

from fontParts.world import OpenFont

font = OpenFont("test.ufo")

font.info.familyName = "myFamilyName"
font.info.styleName = "myStyleName"
font.info.autoNaming()

print(font.info.fullName)
print(font.info.fontName)
print(font.info.fondName)