# iteration through alphabetically sorted glyphnames

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
print("font has %d glyphs" % len(font))

# names is now a list of strings, the names of the glyphs
# not the glyphs themselves!
names = list(font.keys())

# the list of names is sorted
names.sort()

# now we iterate through the list of names
for glyphName in names:
    # now we ask for the glyph with glyphName
    print(font[glyphName])
