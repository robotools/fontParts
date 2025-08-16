# robothon06

from fontParts.world import OpenFont

# We need to import a class with a different
# implementation for the glyph object.
# It looks a bit odd, but this is how it is done
from fontParts.objects.objectsRF import RGlyph as _RGlyph

f = OpenFont("test.ufo")

# pick two compatible glyphs as masters
m1 = f["A"]
m2 = f["B"]

# make a new glyph object from this other glyph class
g = _RGlyph()

# interpolation factor which is  bound to make floats
oddFactor = 0.2382345

# go!
g.interpolate(oddFactor, m1, m2)

# let's have a look at the raw results
for contour in g:
    for pt in contour.points:
        print("float", pt.x, pt.y)

# a glyph can round itself off:
g.round()

# and then it looks like integers again
for contour in g:
    for pt in contour.points:
        print("integer", pt.x, pt.y)
