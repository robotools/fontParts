# fontParts manual
# Component object
# attribute examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

print(f['gbreve'].components[0].baseGlyph)
print(f['gbreve'].components[1].baseGlyph)

# move the component in the base glyph
f['gbreve'].components[1].offset = (100,100)

# scale the component in the base glyph
f['gbreve'].components[0].scale = (.5, .25)
