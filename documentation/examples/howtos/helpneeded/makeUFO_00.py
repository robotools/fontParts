# fontParts manual
# Makeufo howto
# Makeufo from a font binary examples

from fontParts.tools.toolsAll import fontToUFO
from fontParts.interface.all.dialogs import GetFile, PutFile

srcPath = GetFile('Select the source')
dstPath = PutFile('Save as...')

fontToUFO(srcPath, dstPath)
