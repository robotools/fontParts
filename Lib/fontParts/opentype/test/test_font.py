import unittest
import collections
import tempfile
import os
import shutil
from fontParts.opentype.font import OTFont

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

  def test_contours(self):
    f = OTFont("OpenSans-Regular.ttf")
    a = f.layers[0]["a"]
    self.assertEqual(len(a.contours), 2)
