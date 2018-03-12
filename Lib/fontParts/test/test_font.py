import unittest
import collections
from fontParts.base import FontPartsError


class TestFont(unittest.TestCase):

    # ------
    # Layers
    # ------

    def getFont_layers(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newLayer("layer " + name)
        return font

    def test_getLayer_unknown(self):
        font = self.getFont_layers()
        with self.assertRaises(FontPartsError):
            font.getLayer("There is no layer with this name.")

    # ------
    # Glyphs
    # ------

    def getFont_glyphs(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newGlyph(name)
        return font

    def getFont_guidelines(self):
        font, _ = self.objectGenerator("font")
        font.appendGuideline((1, 2), 0, "Test Guideline 1")
        font.appendGuideline((3, 4), 90, "Test Guideline 2")
        return font

    # len

    def test_len_initial(self):
        font = self.getFont_glyphs()
        self.assertEqual(
            len(font),
            4
        )

    def test_len_two_layers(self):
        font = self.getFont_glyphs()
        layer = font.newLayer("test")
        layer.newGlyph("X")
        self.assertEqual(
            len(font),
            4
        )

    # ----
    # Hash
    # ----

    def test_hash_same_object(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            hash(font_one),
            hash(font_one)
        )

    def test_hash_different_object(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(
            hash(font_one),
            hash(font_two)
        )

    def test_hash_same_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        self.assertEqual(
            hash(font_one),
            hash(a)
        )

    def test_hash_different_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(
            hash(font_two),
            hash(a)
        )

    def test_hash_is_hasbable(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            isinstance(font_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            font_one,
            font_one
        )

    def test_object_not_equal_other(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(
            font_one,
            font_two
        )

    def test_object_equal_self_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        a.newGlyph("XYZ")
        self.assertEqual(
            font_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(
            font_two,
            a
        )

    # ---------
    # Selection
    # ---------

    # Font

    def test_selected_true(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        font.selected = True
        self.assertEqual(
            font.selected,
            True
        )

    def test_selected_false(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selected,
            False
        )

    # Layers

    def test_selectedLayer_default(self):
        font = self.getFont_layers()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedLayers,
            ()
        )

    def test_selectedLayer_setSubObject(self):
        font = self.getFont_layers()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer2 = font.getLayer("layer B")
        layer1.selected = True
        layer2.selected = True
        self.assertEqual(
            font.selectedLayers,
            (layer1, layer2)
        )

    def test_selectedLayer_setFilledList(self):
        font = self.getFont_layers()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        layer3 = font.getLayer("layer C")
        layer4 = font.getLayer("layer D")
        font.selectedLayers = [layer3, layer4]
        self.assertEqual(
            font.selectedLayers,
            (layer3, layer4)
        )

    def test_selectedLayer_setEmptyList(self):
        font = self.getFont_layers()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer1.selected = True
        font.selectedLayers = []
        self.assertEqual(
            font.selectedLayers,
            ()
        )

    # Glyphs

    def test_selectedGlyphs_default(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    def test_selectedGlyphs_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph1, glyph2)
        )

    def test_selectedGlyphs_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph3 = font["C"]
        glyph4 = font["D"]
        font.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph3, glyph4)
        )

    def test_selectedGlyphs_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphs = []
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    # Glyph names

    def test_selectedGlyphNames_default(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(font.selectedGlyphNames)),
            ("A", "B")
        )

    def test_selectedGlyphNames_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        font.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            tuple(sorted(font.selectedGlyphNames)),
            ("C", "D")
        )

    def test_selectedGlyphNames_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphNames = []
        self.assertEqual(
            font.selectedGlyphNames,
            ()
        )

    # Guidelines

    def test_selectedGuidelines_default(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )

    def test_selectedGuidelines_setSubObject(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        guideline2.selected = True
        self.assertEqual(
            font.selectedGuidelines,
            (guideline2,)
        )

    def test_selectedGuidelines_setFilledList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        font.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(
            font.selectedGuidelines,
            (guideline1, guideline2)
        )

    def test_selectedGuidelines_setEmptyList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = True
        except NotImplementedError:
            return
        font.selectedGuidelines = []
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )
