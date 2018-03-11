import unittest
import collections
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
        layer, unrequested = self.getLayer_glyphs()
        self.assertEqual(
            isinstance(layer, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

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

    # ---------
    # Selection
    # ---------

    def test_selected(self):
        layer, unrequested = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        layer.selected = True
        self.assertEqual(
            layer.selected,
            True
        )
        layer.selected = True
        self.assertEqual(
            layer.selected,
            True
        )

    def test_selectedGlyphs(self):
        layer, unrequested = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph3 = layer["C"]
        glyph4 = layer["D"]
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            layer.selectedGlyphs,
            (glyph1, glyph2)
        )
        layer.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            layer.selectedGlyphs,
            (glyph3, glyph4)
        )
        layer.selectedGlyphs = []
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames(self):
        layer, unrequested = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph3 = layer["C"]
        glyph4 = layer["D"]
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            layer.selectedGlyphNames,
            ("A", "B")
        )
        layer.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            layer.selectedGlyphNames,
            ("C", "D")
        )
        layer.selectedGlyphNames = []
        self.assertEqual(
            layer.selectedGlyphNames,
            ()
        )
