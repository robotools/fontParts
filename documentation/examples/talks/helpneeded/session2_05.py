# robothon06
# get a specific contour and view it
# through point, segment and bPoint structures

from fontParts.world import OpenFont

font = OpenFont("test.ufo")
glyph = font['A']
contour = glyph[0]
print(contour.points)
print(countours.segments)
print(contour.bPoints)
