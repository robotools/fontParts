import unittest
import collections
from fontParts.base import FontPartsError


class TestContour(unittest.TestCase):

    # ------
    # Bounds
    # ------

    def getContour_bounds(self):
        contour, unrequested = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour, unrequested

    def getContour_boundsExtrema(self):
        contour, unrequested = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((50, 100), "line")
        contour.appendPoint((117, 100), "offcurve")
        contour.appendPoint((117, 0), "offcurve")
        contour.appendPoint((50, 0), "curve")
        return contour, unrequested

    def test_bounds(self):
        # get
        contour, unrequested = self.getContour_bounds()
        self.assertEqual(
            contour.bounds,
            (0, 0, 100, 100)
        )
        # get: float
        contour.moveBy((0.5, -0.5))
        self.assertEqual(
            contour.bounds,
            (0.5, -0.5, 100.5, 99.5)
        )
        # get: point not at extrema
        contour, unrequested = self.getContour_boundsExtrema()
        bounds = tuple(int(round(i)) for i in contour.bounds)
        self.assertEqual(
            bounds,
            (0, 0, 100, 100)
        )
        # set
        with self.assertRaises(FontPartsError):
            contour.bounds = (1, 2, 3, 4)

    # ----
    # Hash
    # ----
    def test_hash(self):
        contour, unrequested = self.getContour_bounds()
        self.assertEqual(
            isinstance(contour, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        contour_one, unrequested = self.getContour_bounds()
        contour_two, unrequested = self.getContour_bounds()
        self.assertEqual(
            contour_one,
            contour_one
        )
        self.assertNotEqual(
            contour_one,
            contour_two
        )
        a = contour_one
        self.assertEqual(
            contour_one,
            a
        )
        self.assertNotEqual(
            contour_two,
            a
        )