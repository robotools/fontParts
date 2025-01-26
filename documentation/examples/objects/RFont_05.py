# fontParts manual
# Font object
# method examples, available in FontLab

from fontParts.world import OpenFont
f = OpenFont("test.ufo")

# the keys() method returns a list of glyphnames:
print(f.keys())

# Not implemented in fontParts
# generate font binaries
# f.generate('otfcff')
