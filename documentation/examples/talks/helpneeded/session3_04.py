# robothon06
# building a glyph from parts
# the hard way

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

# make a new glyph
f.newGlyph("aacute")

# add the component for the base glyph, a
f["aacute"].appendComponent("a")

# add the component for the accent, acute
# note it has an offset
f["aacute"].appendComponent("acute", (200, 0))

# set the width too
f["aacute"].width = f["a"].width

f.update()