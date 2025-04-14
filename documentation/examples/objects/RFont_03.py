# fontParts manual
# Font object
# attribute examples
# Most useful attributes of RFont
# are actually stored in RFont.info

from fontParts.world import OpenFont
f = OpenFont("test.ufo")
print(f.info.unitsPerEm)

# kerning data is available in the kerning object:
print(f.kerning)

# len() gives you the "length" of the font, i.e. the number of glyphs
print("glyphs in this font:", len(f))

# treat a font object as a dictionary to get to the glyphs
print(f["A"])
