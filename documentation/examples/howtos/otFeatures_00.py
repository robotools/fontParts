# Getting to feature data in a UFO.

from fontParts.world import OpenFont

path = "test.ufo"

f = OpenFont(path)

print(list(f.lib.keys()))
print(f.lib["public.openTypeMeta"])
print(f.features.text)
