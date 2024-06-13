# robothon06
# interpolate two glyphs in the same font a bunch of times

from fontParts.world import OpenFont, RGlyph

f = OpenFont("test.ufo")

# This example runs to completion, but it doesn't do anything in fontParts.
# In robofab, it created a new glyph using the magic spring-into-existence
# syntax f[name].interpolate(...) on a non-existing f[name], which doesn't
# work in fontParts. But neither does this attempt to make it work.
for i in range(0, 10):
    factor = i*.1
    name = "result_%f"%factor
    print("interpolating", name)
    f[name] = RGlyph()
    f[name].interpolate(factor, f["A"], f["B"])

f.update()
