# robothon 2006
# batch save as

import os
from fontParts.world import AllFonts
from fontParts.interface.all.dialogs import GetFolder

path = GetFolder()
if path:
    for font in AllFonts():
        fileName = os.path.basename(font.path)
        newPath = os.path.join(path, fileName)
        font.save(newPath)