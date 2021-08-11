# robothon06
# show encoding 

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
fn = f.naked()

# object containing encoding records.
# you can iterate through it by using an index.
print(fn.encoding)

for i in range(len(fn.encoding)):
    er = fn.encoding[i]
    print(er, er.name, er.str)
