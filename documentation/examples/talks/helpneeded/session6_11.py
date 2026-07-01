# robothon06
# show OpenType naming records
# in the fontlab API

from fontParts.world import OpenFont

f = OpenFont("test.ufo")
fn = f.naked()

for r in fn.fontnames:
    print(r.nid, r.pid, r.eid, r.lid, r.name)
