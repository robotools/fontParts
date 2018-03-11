import unittest
import collections
from fontParts.base import FontPartsError


class TestGlyph(unittest.TestCase):

    def getGlyph_generic(self):
        glyph, _unrequested = self.objectGenerator("glyph")
        glyph.name = "Test Glyph 1"
        glyph.unicode = int(ord("X"))
        glyph.width = 250
        pen = glyph.getPen()
        pen.moveTo((100, 0))
        pen.lineTo((100, 100))
        pen.lineTo((200, 100))
        pen.lineTo((200, 0))
        pen.closePath()
        return glyph

    # -------
    # Metrics
    # -------

    def test_width_get(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.width,
            250
        )
    def test_width_set_valid_positive(self):
        glyph = self.getGlyph_generic()
        glyph.width = 300
        self.assertEqual(
            glyph.width,
            300
        )
    def test_width_set_valid_zero(self):
        glyph = self.getGlyph_generic()
        glyph.width = 0
        self.assertEqual(
            glyph.width,
            0
        )
    def test_width_set_valid_float(self):
        glyph = self.getGlyph_generic()
        glyph.width = 101.5
        self.assertEqual(
            glyph.width,
            101.5
        )
    def test_width_set_valid_negative(self):
        glyph = self.getGlyph_generic()
        glyph.width = -485
        self.assertEqual(
            glyph.width,
            -485
        )
    def test_width_set_invalid_string(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(FontPartsError):
            glyph.width = "abc"
    def test_width_set_invalid_none(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(FontPartsError):
            glyph.width = None

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            hash(glyph_one),
            hash(glyph_one)
        )
    def test_hash_object_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            hash(glyph_one),
            hash(glyph_two)
        )
    def test_hash_object_self_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        self.assertEqual(
            hash(glyph_one),
            hash(a)
        )
    def test_hash_object_other_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            hash(glyph_two),
            hash(a)
        )
    def test_is_hashable(self):
        glyph_one = self.getGlyph_generic()
        self.assertEqual(
            isinstance(glyph_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            glyph_one,
            glyph_one
        )
    def test_object_not_equal_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )
    def test_object_not_equal_other_name_same(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )
    def test_object_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        a.name = "Other"
        self.assertEqual(
            glyph_one,
            a
        )
    def test_object_not_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            glyph_two,
            a
        )