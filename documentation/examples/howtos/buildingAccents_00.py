# fontParts manual
# Buildingaccents howto
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
f.newGlyph("aacute")
f["aacute"].appendComponent("a")
f["aacute"].appendComponent("acute", (200, 0))
f["aacute"].width = f["a"].width
f.update()
