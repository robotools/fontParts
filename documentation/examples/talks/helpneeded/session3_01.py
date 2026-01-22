# robothon06
# work with kerning 2

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
kerning = font.kerning

# calculate the average offset
print(kerning.getAverage())

# count pairs with these glyphs
print(kerning.occurrenceCount(["a", "b"]))

# get the maximum values
print(kerning.getExtremes())

# count the pars
print("font has %d kerning pairs" % len(kerning))

# this prints all the pairs
for (left, right), value in list(kerning.items()):
    print((left, right), value)