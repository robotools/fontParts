from fontParts.fontshell.ttf.font import TTFont
from fontParts.fontshell.otf.font import OTFont
import fontTools
import unittest
import collections
import tempfile
import os
import shutil

class TestTTFont(unittest.TestCase):

  def test_open(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertTrue(f)

  def test_layer(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(len(f.layers),1)

  def test_glyph_in_layers(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    l = f.layers[0]
    self.assertTrue("Iota" in l)
    self.assertTrue("a" in l)

  def test_read_metadata(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    g = f.layers[0]["Iota"]
    self.assertEqual("Iota", g.name)
    self.assertEqual(0x0399, g.unicode)

  def test_contours(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    a = f.layers[0]["a"]
    self.assertEqual(len(a.contours), 2)
    self.assertEqual(len(a.contours[0].points),26)
    self.assertEqual(a.contours[0].points[0].x, 850)
    self.assertEqual(a.contours[0].points[0].y, 0)
    self.assertEqual(a.contours[0].points[-1].x, 973)
    self.assertEqual(a.contours[0].points[-1].y, 0)

  def test_read_sidebearings(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(f.layers[0]["H"].leftMargin, 201)
    self.assertEqual(f.layers[0]["H"].rightMargin, 200)
    self.assertEqual(f.layers[0]["H"].bottomMargin, 0)
    self.assertEqual(f.layers[0]["H"].topMargin, 727)
    self.assertEqual(f.layers[0]["H"].height, 2189)
    self.assertEqual(f.layers[0]["H"].width, 1511)
    self.assertEqual(f.layers[0]["H"].bounds, (201, 0, 1311, 1462))

  def test_component_read(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    a = f.layers[0]["uni1EB6"]
    self.assertEqual(len(a.components), 3)
    self.assertEqual(a.components[0].baseGlyph, "A")
    self.assertEqual(a.components[1].baseGlyph, "breve")
    self.assertEqual(a.components[1].offset, (45,356))
    self.assertEqual(a.components[2].baseGlyph, "dotbelow")
    self.assertEqual(a.components[2].offset, (1257,0))

  def test_write_sidebearings1(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(f.layers[0]["H"].leftMargin, 201)
    self.assertEqual(f.layers[0]["H"].rightMargin, 200)

    f.layers[0]["H"].leftMargin = 51
    self.assertEqual(f.layers[0]["H"].leftMargin, 51)
    self.assertEqual(f.layers[0]["H"].rightMargin, 200)

    f.layers[0]["H"].rightMargin = 52
    self.assertEqual(f.layers[0]["H"].leftMargin, 51)
    self.assertEqual(f.layers[0]["H"].rightMargin, 52)
    self.assertEqual(f.layers[0]["H"].width,1213)
    f.save("OS-H51.ttf")

    tt = fontTools.ttLib.TTFont("OS-H51.ttf")
    self.assertEqual(tt["hmtx"]["H"][1], 51)
    os.unlink("OS-H51.ttf")

  def test_write_sidebearings2(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(f.layers[0]["H"].leftMargin, 201)
    self.assertEqual(f.layers[0]["H"].rightMargin, 200)

    f.layers[0]["H"].rightMargin = 52
    self.assertEqual(f.layers[0]["H"].leftMargin, 201)
    self.assertEqual(f.layers[0]["H"].rightMargin, 52)

    f.layers[0]["H"].leftMargin = 51
    self.assertEqual(f.layers[0]["H"].leftMargin, 51)
    self.assertEqual(f.layers[0]["H"].rightMargin, 52)
    self.assertEqual(f.layers[0]["H"].width,1213)
    f.save("OS-H51.ttf")

    tt = fontTools.ttLib.TTFont("OS-H51.ttf")
    self.assertEqual(tt["hmtx"]["H"][1], 51)
    os.unlink("OS-H51.ttf")

  def test_area(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    # Use notdef because it consists of a positive box and a negative box.
    self.assertEqual(f.layers[0][".notdef"].area, 1462*841-633*1254)

  def test_kern_ttf(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(f.kerning[("A","V")],-82)

  def test_kern_otf(self):
    f = OTFont("test-Fonts/OpenSans-Regular.otf")
    self.assertEqual(f.kerning[("A","V")],-82)

  def test_write_kern_ttf(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    f.kerning[("A","V")] = -100
    f.save("OS-AV100.ttf")

    f2 = TTFont("OS-AV100.ttf")
    self.assertEqual(f2.kerning[("A","V")],-100)
    os.unlink("OS-AV100.ttf")

  def test_read_info(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    self.assertEqual(f.info.familyName, "Open Sans")
    self.assertEqual(f.info.styleName, "Regular")
    # styleMapFamilyName
    # styleMapStyleName
    self.assertEqual(f.info.versionMajor, 1)
    self.assertEqual(f.info.versionMinor, 10)
    # year
    self.assertEqual(f.info.copyright, u"Digitized data copyright © 2010-2011, Google Corporation.")
    self.assertEqual(f.info.trademark, u"Open Sans is a trademark of Google and may be registered in certain jurisdictions.")
    self.assertEqual(f.info.unitsPerEm,  2048)
    self.assertEqual(f.info.descender,   -600)
    self.assertEqual(f.info.xHeight,     1096)
    self.assertEqual(f.info.capHeight,   1462)
    self.assertEqual(f.info.ascender,    2189)
    self.assertEqual(f.info.italicAngle, 0)
    # note

  def test_write_info(self):
    f = TTFont("test-Fonts/OpenSans-Regular.ttf")
    f.info.versionMinor = 9
    f.info.versionMajor = 2
    f.info.familyName = "Renamed Open Sans"
    f.save("test-Fonts/OpenSans-Renamed.ttf")

    g = TTFont("test-Fonts/OpenSans-Renamed.ttf")
    self.assertEqual(f.info.versionMinor, 9)
    self.assertEqual(f.info.versionMajor, 2)
    self.assertEqual(f.info.familyName, "Renamed Open Sans")

  def test_contours_otf(self):
    f = OTFont("test-Fonts/OpenSans-Regular.otf")
    a = f.layers[0]["a"]
    self.assertEqual(len(a.contours), 2)
    self.assertEqual(len(a.contours[0].points),28)
    self.assertEqual(a.contours[0].points[0].x, 973)
    self.assertEqual(a.contours[0].points[0].y, 0)
    self.assertEqual(a.contours[0].points[-1].x, 850)
    self.assertEqual(a.contours[0].points[-1].y, 0)

if __name__ == '__main__':
    unittest.main()
