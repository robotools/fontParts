from fontParts.world import OpenFont
f = OpenFont("test.ufo")
a = f["a"]
# fontParts RGlyph.isCompatible doesn't take the boolean argument.
# Moved to helpneeded as this argument is the only difference with interpolate_00.py
print(a.isCompatible(f["b"], True))
