# Getting to feature data in fontParts
from fontParts.world import OpenFont

f = OpenFont("test.ufo")

print(f.naked().features)

# these are raw fontParts feature objects.
