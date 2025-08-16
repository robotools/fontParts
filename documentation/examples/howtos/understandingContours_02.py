from fontParts.world import OpenFont

f = OpenFont("test.ufo")
# get straight to the points in a contour
# through the points attribute
g = f["a"]
for aPt in g[0].points:
    print(aPt)
