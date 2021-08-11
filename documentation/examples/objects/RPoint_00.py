# fontParts manual
# Point object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
g = f['a']

contour = g[0]
print(contour.points[0])

from random import randint
for p in contour.points:
    p.x += randint(-10,10)
    p.y += randint(-10,10)

contour.update()
