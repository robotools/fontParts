# fontParts manual
# Segment object
# attribute examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

for g in f:
    for contour in g:
        for segment in contour:
            print(len(segment))
            print(segment.type)
            print(segment.smooth)
            print(segment.points)
            print(segment.onCurve)
            print(segment.offCurve)
