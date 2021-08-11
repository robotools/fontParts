# use a point pen

from fontParts.world import OpenFont
from fontParts.pens.pointPen import PrintingPointPen

font = OpenFont("test.ufo")
glyph = font['A']

pen = PrintingPointPen()
glyph.drawPoints(pen)
