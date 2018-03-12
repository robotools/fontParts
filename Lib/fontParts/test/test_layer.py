import unittest
import collections
from fontParts.base import FontPartsError


class TestLayer(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getLayer_glyphs(self):
        layer, _ = self.objectGenerator("layer")
        for name in "ABCD":
            glyph = layer.newGlyph(name)
        return layer

    def test_len(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            len(layer),
            4
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            isinstance(layer, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        layer_one = self.getLayer_glyphs()
        self.assertEqual(
            layer_one,
            layer_one
        )

    def test_object_not_equal_other(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        self.assertNotEqual(
            layer_one,
            layer_two
        )

    def test_object_equal_self_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        a = layer_one
        self.assertEqual(
            layer_one,
            a
        )

    def test_object_not_equal_self_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        a = layer_one
        self.assertNotEqual(
            layer_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        layer.selected = True
        self.assertEqual(
            layer.selected,
            True
        )

    def test_selected_false(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selected,
            False
        )

    # Glyphs

    def test_selectedGlyphs_default(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    def test_selectedGlyphs_setSubObject(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph1, glyph2)
        )

    def test_selectedGlyphs_setFilledList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph3 = layer["C"]
        glyph4 = layer["D"]
        layer.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph3, glyph4)
        )

    def test_selectedGlyphs_setEmptyList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph1.selected = True
        layer.selectedGlyphs = []
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    # Glyph Names

    def test_selectedGlyphNames_default(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames_setSubObject(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphNames)),
            ("A", "B")
        )

    def test_selectedGlyphNames_setFilledList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph3 = layer["C"]
        glyph4 = layer["D"]
        layer.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphNames)),
            ("C", "D")
        )

    def test_selectedGlyphNames_setEmptyList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph1.selected = True
        layer.selectedGlyphNames = []
        self.assertEqual(
            layer.selectedGlyphNames,
            ()
        )
