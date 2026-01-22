# robothon06
# get a particular glyph

from fontParts.world import OpenFont

font = OpenFont("test.ufo")

print(font['A'])
print(font['Adieresis'])
print(font['two'])
print(font['afii12934'])