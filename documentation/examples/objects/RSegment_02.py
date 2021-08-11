# fontParts manual
# Segment object
# method examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

for g in f:
    for contour in g:
        for segment in contour:
            segment.move((50, 25))
