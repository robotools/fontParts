import unittest
import collections
from fontParts.base import FontPartsError


class TestFont(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getFont_glyphs(self):
        font, _unrequested = self.objectGenerator("font")
        for name in "ABCD":
            glyph = font.newGlyph(name)
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