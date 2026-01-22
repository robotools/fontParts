# fontParts doesn't seem to expose the kerning table.

# showing where the data lives in the RoboFab objects.
from fontParts.world import OpenFont

f = OpenFont("test.ufo")

# these are pairs
print(list(f.kerning.keys()))

# get the value for this pair
print(f.kerning[('MMK_L_baseserif', 'n')])
