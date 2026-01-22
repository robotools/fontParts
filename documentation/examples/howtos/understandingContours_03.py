from fontParts.world import OpenFont

f = OpenFont("test.ufo")
# bpoints
c = f["a"]
for aPt in c[0].bPoints:
    print(aPt.anchor)
    print(aPt.bcpIn)
    print(aPt.bcpOut)
    print(aPt.type)
