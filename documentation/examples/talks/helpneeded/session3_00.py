# robothon06
# work with kerning 1
from fontParts.world import OpenFont
font = OpenFont("test.ufo")
# now the kerning object is generated once
kerning = font.kerning
# and ready for your instructions.
print(kerning)
print(len(kerning))
print(list(kerning.keys()))
# proceed to work with the myKerning object
# this happens in the following examples too.