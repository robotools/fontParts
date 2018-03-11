import unittest
import collections
from fontParts.base import FontPartsError


class TestContour(unittest.TestCase):

    # ------
    # Bounds
    # ------

    def getContour_bounds(self):
        contour, _unrequested = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour

    def getContour_boundsExtrema(self):
        contour, _unrequested = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((50, 100), "line")
        contour.appendPoint((117, 100), "offcurve")
        contour.appendPoint((117, 0), "offcurve")
        contour.appendPoint((50, 0), "curve")
        return contour

    def test_bounds_get(self):
        contour = self.getContour_bounds()
        self.assertEqual(
            contour.bounds,
            (0, 0, 100, 100)
        )
    def test_bounds_set_float(self):
        contour = self.getContour_bounds()
        contour.moveBy((0.5, -0.5))
        self.assertEqual(
            contour.bounds,
            (0.5, -0.5, 100.5, 99.5)
        )
    def test_bounds_point_not_at_extrema(self):
        contour = self.getContour_bounds()
        contour = self.getContour_boundsExtrema()
        bounds = tuple(int(round(i)) for i in contour.bounds)
        self.assertEqual(
            bounds,
            (0, 0, 100, 100)
        )
    def test_invalid_bounds_set(self):
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.bounds = (1, 2, 3, 4)

    # ----
    # Hash
    # ----
    def test_hash(self):
        contour = self.getContour_bounds()
        self.assertEqual(
            isinstance(contour, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        contour_one = self.getContour_bounds()
        self.assertEqual(
            contour_one,
            contour_one
        )
    def test_object_not_equal_self(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        self.assertNotEqual(
            contour_one,
            contour_two
        )
    def test_object_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        a = contour_one
        a.moveBy((0.5, -0.5))
        self.assertEqual(
            contour_one,
            a
        )
    def test_object_not_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        a = contour_one
        self.assertNotEqual(
            contour_two,
            a
        )