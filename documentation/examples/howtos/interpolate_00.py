from fontParts.world import OpenFont
f = OpenFont("test.ufo")
a = f["a"]
# RGlyph.isCompatible doesn't accept the boolean argument.
#print(a.isCompatible(f["b"], False))
print(a.isCompatible(f["b"]))
