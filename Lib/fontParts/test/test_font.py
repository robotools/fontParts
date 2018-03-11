import unittest
import collections
from fontParts.base import FontPartsError


class TestFont(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getFont_glyphs(self):
        font, unrequested = self.objectGenerator("font")
        for name in "ABCD":
            glyph = font.newGlyph(name)
        return font, unrequested

    def getFont_layers(self):
        font, unrequested = self.objectGenerator("font")
        for name in "ABCD":
            glyph = font.newLayer("layer " + name)
        return font, unrequested

    def getFont_guidelines(self):
        font, unrequested = self.objectGenerator("font")
        font.appendGuideline((1, 2), 0, "Test Guideline 1")
        font.appendGuideline((3, 4), 90, "Test Guideline 2")
        return font, unrequested

    # len

    def test_len(self):
        font, unrequested = self.getFont_glyphs()
        # one layer
        self.assertEqual(
            len(font),
            4
        )
        # two layers
        layer = font.newLayer("test")
        layer.newGlyph("X")
        self.assertEqual(
            len(font),
            4
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        font_one, unrequested = self.getFont_glyphs()
        font_two, unrequested = self.getFont_glyphs()
        self.assertEqual(
            hash(font_one),
            hash(font_one)
        )
        self.assertNotEqual(
            hash(font_one),
            hash(font_two)
        )
        a = font_one
        self.assertEqual(
            hash(font_one),
            hash(a)
        )
        self.assertNotEqual(
            hash(font_two),
            hash(a)
        )
        self.assertEqual(
            isinstance(font_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        font_one, unrequested = self.getFont_glyphs()
        font_two, unrequested = self.getFont_glyphs()
        self.assertEqual(
            font_one,
            font_one
        )
        self.assertNotEqual(
            font_one,
            font_two
        )
        a = font_one
        self.assertEqual(
            font_one,
            a
        )
        self.assertNotEqual(
            font_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected(self):
        font, unrequested = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        font.selected = True
        self.assertEqual(
            font.selected,
            True
        )
        font.selected = True
        self.assertEqual(
            font.selected,
            True
        )

    def test_selectedLayer(self):
        font, unrequested = self.getFont_layers()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer2 = font.getLayer("layer B")
        layer3 = font.getLayer("layer C")
        layer4 = font.getLayer("layer D")
        self.assertEqual(
            font.selectedLayers,
            ()
        )
        layer1.selected = True
        layer2.selected = True
        self.assertEqual(
            font.selectedLayers,
            (layer1, layer2)
        )
        font.selectedLayers = [layer3, layer4]
        self.assertEqual(
            font.selectedLayers,
            (layer3, layer4)
        )
        font.selectedLayers = []
        self.assertEqual(
            font.selectedLayers,
            ()
        )

    def test_selectedGlyphs(self):
        font, unrequested = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph3 = font["C"]
        glyph4 = font["D"]
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            font.selectedGlyphs,
            (glyph1, glyph2)
        )
        font.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            font.selectedGlyphs,
            (glyph3, glyph4)
        )
        font.selectedGlyphs = []
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames(self):
        font, unrequested = self.getFont_glyphs()
        try:
            font.getLayer(font.defaultLayer).selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph3 = font["C"]
        glyph4 = font["D"]
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            font.selectedGlyphNames,
            ("A", "B")
        )
        font.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            font.selectedGlyphNames,
            ("C", "D")
        )
        font.selectedGlyphNames = []
        self.assertEqual(
            font.selectedGlyphNames,
            ()
        )

    def test_selectedGuidelines(self):
        font, unrequested = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )
        guideline2.selected = True
        self.assertEqual(
            font.selectedGuidelines,
            (guideline2,)
        )
        font.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(
            font.selectedGuidelines,
            (guideline1, guideline2)
        )
        font.selectedGuidelines = []
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )