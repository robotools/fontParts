# fontParts manual
# Generatefonts howto
# usage examples

import os.path
from fontParts.world import OpenFont

font = OpenFont("test.ufo")
path = font.path
dir, fileName = os.path.split(path)
# fontParts does not seem to expose the fullName attribute through the RInfo class
path = os.sep.join([dir, font.info.fullName])
# raises NotImplemented
font.generate('mactype1', path)
