# open a couple of fonts in FL first!
from fontParts.world import OpenFont

font = OpenFont("test.ufo")
print(font.path)
print(font.kerning)
print(font.info)