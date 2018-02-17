import unittest
import collections
from fontParts.base import FontPartsError


class TestGuideline(unittest.TestCase):

    def getGuideline_generic(self):
        guideline, unrequested = self.objectGenerator("guideline")
        guideline.x = 1
        guideline.y = 2
        guideline.angle = 90
        return guideline, unrequested

    # --------
    # Position
    # --------

    def test_x(self):
        guideline, unrequested = self.getGuideline_generic()
        # get
        self.assertEqual(
            guideline.x,
            1
        )
        # set: valid
        guideline.x = 0
        self.assertEqual(
            guideline.x,
            0
        )
        guideline.x = 1
        self.assertEqual(
            guideline.x,
            1
        )
        guideline.x = -1
        self.assertEqual(
            guideline.x,
            -1
        )
        guideline.x = 1.1
        self.assertEqual(
            guideline.x,
            1.1
        )
        guideline.x = -1.1
        self.assertEqual(
            guideline.x,
            -1.1
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            guideline.x = "ABC"

    # ----
    # Hash
    # ----
    def test_hash(self):
        guideline, unrequested = self.getGuideline_generic()
        self.assertEqual(
            isinstance(guideline, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        guideline_one, unrequested = self.getGuideline_generic()
        guideline_two, unrequested = self.getGuideline_generic()
        self.assertEqual(
            guideline_one,
            guideline_one
        )
        self.assertNotEqual(
            guideline_one,
            guideline_two
        )
        a = guideline_one
        self.assertEqual(
            guideline_one,
            a
        )
        self.assertNotEqual(
            guideline_two,
            a
        )
