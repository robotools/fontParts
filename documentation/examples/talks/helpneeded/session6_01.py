# robothon 2006
# get info attributes for all fonts
# and dump them to a text file

from fontParts.world import AllFonts
from fontParts.interface.all.dialogs import PutFile

text = []

for font in AllFonts():
    text.append(str(font.path))
    text.append(str(font.info.familyName))
    text.append(str(font.info.styleName))
    text.append(str(font.info.fullName))
    text.append(str(font.info.unitsPerEm))
    text.append(str(font.info.ascender))
    text.append(str(font.info.descender))
    text.append('')

text = '\n'.join(text)
path = PutFile('Save file as:')
if path:
    file = open(path, 'w')
    file.write(text)
    file.close()