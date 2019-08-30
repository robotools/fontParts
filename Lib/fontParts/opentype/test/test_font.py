import unittest
import collections
import tempfile
import os
import shutil
from fontParts.opentype.font import OTFont
from fontTools.ttLib import TTFont

class TestOTFont(unittest.TestCase):

  def test_open(self):
    f = OTFont("OpenSans-Regular.ttf")
    self.assertTrue(f)

  def test_layer(self):
    f = OTFont("OpenSans-Regular.ttf")
    self.assertEqual(len(f.layers),1)

  def test_glyph_in_layers(self):
    f = OTFont("OpenSans-Regular.ttf")
    l = f.layers[0]
    self.assertTrue("Iota" in l)
    self.assertTrue("a" in l)

  def test_read_metadata(self):
    f = OTFont("OpenSans-Regular.ttf")
    g = f.layers[0]["Iota"]
    self.assertEqual("Iota", g.name)
    self.assertEqual(0x0399, g.unicode)

  def test_contours(self):
    f = OTFont("OpenSans-Regular.ttf")
    a = f.layers[0]["a"]
    self.assertEqual(len(a.contours), 2)

  def test_read_sidebearings(self):
    f = OTFont("OpenSans-Regular.ttf")
    self.assertEqual(f.layers[0]["H"].leftMargin, 201)
    self.assertEqual(f.layers[0]["H"].rightMargin, 200)
    self.assertEqual(f.layers[0]["H"].bottomMargin, 0)
    self.assertEqual(f.layers[0]["H"].topMargin, 727)
    self.assertEqual(f.layers[0]["H"].height, 2189)
    self.assertEqual(f.layers[0]["H"].width, 1511)
    self.assertEqual(f.layers[0]["H"].bounds, (201, 0, 1311, 1462))

  def test_component_read(self):
    f = OTFont("OpenSans-Regular.ttf")
    a = f.layers[0]["uni1EB6"]
    self.assertEqual(len(a.components), 3)
    self.assertEqual(a.components[0].baseGlyph, "A")
    self.assertEqual(a.components[1].baseGlyph, "breve")
    self.assertEqual(a.components[1].offset, (45,356))
    self.assertEqual(a.components[2].baseGlyph, "dotbelow")
    self.assertEqual(a.components[2].offset, (1257,0))

  def test_write_sidebearings1(self):
    f = OTFont("OpenSans-Regular.ttf")
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

    tt = TTFont("OS-H51.ttf")
    self.assertEqual(tt["hmtx"]["H"][1], 51)

  def test_write_sidebearings2(self):
    f = OTFont("OpenSans-Regular.ttf")
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

    tt = TTFont("OS-H51.ttf")
    self.assertEqual(tt["hmtx"]["H"][1], 51)