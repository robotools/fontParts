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