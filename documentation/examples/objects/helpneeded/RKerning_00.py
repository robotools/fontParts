# fontParts manual
# Kerning object
# usage examples

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
print(f.kerning)

# f.kerning returns an empty dict in fontParts. That can't be right,
# so this example goes into helpneeded UFN. The test font does have
# kerning for the V,A kern pair through a kerning class.

# getting a value from the kerning dictionary
print(f.kerning[('V', 'A')])
print(f.kerning[('T', 'X')])
print(list(f.kerning.keys()))
