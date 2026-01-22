# robothon06
# set font info in all fonts

from fontParts.world import AllFonts

for font in AllFonts():
    font.info.familyName = "MyFamily"
    font.info.ascender = 700
    font.info.descender = -300
    font.update()
