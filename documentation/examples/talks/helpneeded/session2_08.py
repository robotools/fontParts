# robothon06
# get a pen and use it to print the coordinates
# to the output window. This is actually almost-python
# code which you can use it other scripts!

from fontParts.world import OpenFont
from fontParts.pens.pointPen import PrintingSegmentPen

font = OpenFont("test.ufo")
glyph = font['A']

# PrintingSegmentPen won't actually draw anything
# just print the coordinates to the output:
pen = PrintingSegmentPen()
glyph.draw(pen)
