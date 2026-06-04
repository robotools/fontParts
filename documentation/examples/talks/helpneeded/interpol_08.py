# robothon06
# interpolate two fonts with a series of factors.
# for each factor create a new font file.

import os
from fontParts.world import SelectFont, NewFont
from fontParts.interface.all.dialogs import AskString, GetFolder

font1 = SelectFont("Select font 1")
font2 = SelectFont("Select font 2")
where = GetFolder("Select a folder to save the interpolations")

instances = [
    ("Light", 0),
    ("NotTooLight", 0.25),
    ("Regular", 0.5),
    ("Demi", 0.75),
    ("Medium", 1),
]

for thing in instances:
    name, value = thing
    print("generating", name, value)
    dst = NewFont()
    # this interpolates the glyphs
    dst.interpolate(value, font1, font2, doProgress=True)
    # this interpolates the kerning
    # comment this line out of you're just testing
    #dst.kerning.interpolate(font1.kerning, font2.kerning, value)
    dst.info.familyName = "MyBigFamily"
    dst.info.styleName = name
    dst.info.autoNaming()
    dst.update()
    fileName = dst.info.familyName + "-" + dst.info.styleName + ".vfb"
    path = os.path.join(where, fileName)
    print('saving at', path)
    dst.save(path)
    dst.close()
