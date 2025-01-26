# fontParts manual
# Glyph object
# Usage examples

# start using the current font
from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']

# suppose you've done the right imports
# different ways of creating glyphs
# a new empty glyph object
from fontParts.world import RGlyph
g = RGlyph()
