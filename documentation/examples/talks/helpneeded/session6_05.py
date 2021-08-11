# rename the selected glyphs
# in the current font to <glyphname>.sc
 
from fontParts.world import OpenFont
f = OpenFont("test.ufo")
 
for g in f:
    if g.selected == 0:
        continue
    newName = g.name+".sc"
    print("moving", g.name, "to", newName)
    f.insertGlyph(g, name=newName)
    f.removeGlyph(g.name)
    f.update()
