# fontParts manual
# Font object
# method examples

from fontParts.world import OpenFont
f = OpenFont("test.ufo")

# the keys() method returns a list of glyphnames:
print(list(f.keys()))

# Not implemented in fontParts
# find unicodes for each glyph by using the postscript name:
#f.autoUnicodes()
