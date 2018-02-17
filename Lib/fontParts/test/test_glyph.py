import unittest
import collections
from fontParts.base import FontPartsError


class TestGlyph(unittest.TestCase):

    def getGlyph_generic(self):
        glyph, unrequested = self.objectGenerator("glyph")
        glyph.name = "Test Glyph 1"
        glyph.unicode = int(ord("X"))
        glyph.width = 250
        pen = glyph.getPen()
        pen.moveTo((100, 0))
        pen.lineTo((100, 100))
        pen.lineTo((200, 100))
        pen.lineTo((200, 0))
        pen.closePath()
        return glyph, unrequested

    # -------
    # Metrics
    # -------

    def test_width(self):
        # get
        glyph, unrequested = self.getGlyph_generic()
        self.assertEqual(
            glyph.width,
            250
        )
        # set: valid
        glyph.width = 300
        self.assertEqual(
            glyph.width,
            300
        )
        glyph.width = 0
        self.assertEqual(
            glyph.width,
            0
        )
        glyph.width = 101.5
        self.assertEqual(
            glyph.width,
            101.5
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            glyph.width = "abc"
        with self.assertRaises(FontPartsError):
            glyph.width = None

    # ----
    # Hash
    # ----

    def test_hash(self):
        glyph_one, unrequested = self.getGlyph_generic()
        glyph_two, unrequested = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            hash(glyph_one),
            hash(glyph_one)
        )
        glyph_two.name = "Test"
        self.assertNotEqual(
            hash(glyph_one),
            hash(glyph_two)
        )
        a = glyph_one
        self.assertEqual(
            hash(glyph_one),
            hash(a)
        )
        self.assertNotEqual(
            hash(glyph_two),
            hash(a)
        )
        self.assertEqual(
            isinstance(glyph_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        glyph_one, unrequested = self.getGlyph_generic()
        glyph_two, unrequested = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            glyph_one,
            glyph_one
        )
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )
        glyph_two.name = "Test"
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )
        a = glyph_one
        self.assertEqual(
            glyph_one,
            a
        )
        self.assertNotEqual(
            glyph_two,
            a
        )