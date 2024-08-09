# fontParts manual
# Lib object
# attribute examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

# RFont objects have a lib:
print(f.lib)

# content of the lib of a font exported from RoboFog
print(list(f.lib.keys()))
