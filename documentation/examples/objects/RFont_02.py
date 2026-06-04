# cache the kerning object for speed

from fontParts.world import OpenFont

f = OpenFont("test.ufo")

cachedKerning = f.kerning
# continue to use cachedKerning, not f.kerning.