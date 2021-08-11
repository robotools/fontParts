# fontParts manual
# Segment object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

for g in f:
    for contour in g:
        for segment in contour:
            print(segment)
