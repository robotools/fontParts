from fontParts.world import OpenFont
from fontParts.pens.filterPen import flattenGlyph

f = OpenFont("test.ufo")
g = f["aacute"]
d = 10
flattenGlyph(g, d)
