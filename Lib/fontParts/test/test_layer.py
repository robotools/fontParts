import unittest
from fontParts.base import FontPartsError


class TestLayer(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getLayer_glyphs(self):
        layer, unrequested = self.objectGenerator("layer")
        for name in "ABCD":
            glyph = layer.newGlyph(name)
        return layer, unrequested

    # len

    def test_len(self):
        layer, unrequested = self.getLayer_glyphs()
        self.assertEqual(
            len(layer),
            4
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        layer_one, unrequested = self.getLayer_glyphs()
        layer_two, unrequested = self.getLayer_glyphs()
        self.assertEqual(
            hash(layer_one),
            hash(layer_one)
        )
        self.assertNotEqual(
            hash(layer_one),
            hash(layer_two)
        )
        a = layer_one
        self.assertEqual(
            hash(layer_one),
            hash(a)
        )
        self.assertNotEqual(
            hash(layer_two),
            hash(a)
        )

    def test_equal(self):
        layer_one, unrequested = self.getLayer_glyphs()
        layer_two, unrequested = self.getLayer_glyphs()
        self.assertEqual(
            layer_one,
            layer_one
        )
        self.assertNotEqual(
            layer_one,
            layer_two
        )
        a = layer_one
        self.assertEqual(
            layer_one,
            a
        )
        self.assertNotEqual(
            layer_two,
            a
        )