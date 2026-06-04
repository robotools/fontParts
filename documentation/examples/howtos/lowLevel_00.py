from fontParts.world import OpenFont
f = OpenFont("test.ufo")
# this is the high level RoboFab object
print(f)
# this is the low level FontLab object, not a part of RoboFab
print(f.naked())
