# robothon 2006
# batch generate

from fontParts.world import AllFonts

for font in AllFonts():
    font.generate('otfcff')