# fontParts manual
# Glyphmath howto
# Fun examples

#FLM: Fun with GlyphMath

# this example is meant to run with the RoboFab Demo Font
# as the Current Font. So, if you're doing this in FontLab
# import the Demo Font UFO first.

from fontParts.world import OpenFont
from random import random

f = OpenFont("test.ufo")
condensedLight = f["a#condensed_light"]
wideLight = f["a#wide_light"]
wideBold = f["a#wide_bold"]

diff = wideLight - condensedLight

destination = f.newGlyph("a#deltaexperiment")
destination.clear()
x = wideBold + (condensedLight-wideLight)*random()

destination.appendGlyph( x)
destination.width = x.width

f.update()
