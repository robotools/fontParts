# example of accessing the hint data,
# using the font.psHints object.

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
print(f.psHints.asDict())
