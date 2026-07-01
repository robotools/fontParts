# fontParts manual
# Font object
# Usage examples

# start using the current font
from fontParts.world import OpenFont
f = OpenFont("test.ufo")

# get a clean, empty new font object,
# appropriate for the current environment
from fontParts.world import RFont
f = RFont()

# get an open dialog and start a new font
f = OpenFont("test.ufo")
