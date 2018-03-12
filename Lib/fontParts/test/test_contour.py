import unittest
import collections
from fontParts.base import FontPartsError


class TestContour(unittest.TestCase):

    # ------
    # Bounds
    # ------

    def getContour_bounds(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour

    def getContour_boundsExtrema(self):
        contour, _ = self.objectGenerator("contour")
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

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        contour = self.getContour_bounds()
        try:
            contour.selected = False
        except NotImplementedError:
            return
        contour.selected = True
        self.assertEqual(
            contour.selected,
            True
        )

    def test_selected_false(self):
        contour = self.getContour_bounds()
        try:
            contour.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selected,
            False
        )

    def test_selectedSegments_default(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedSegments,
            ()
        )

    def test_selectedSegments_setSubObject(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        segment2.selected = True
        self.assertEqual(
            contour.selectedSegments == (segment2,),
            True
        )

    def test_selectedSegments_setFilledList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        contour.selectedSegments = [segment1, segment2]
        self.assertEqual(
            contour.selectedSegments,
            (segment1, segment2)
        )

    def test_selectedSegments_setEmptyList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = True
        except NotImplementedError:
            return
        contour.selectedSegments = []
        self.assertEqual(
            contour.selectedSegments,
            ()
        )

    def test_selectedPoints_default(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedPoints,
            ()
        )

    def test_selectedPoints_setSubObject(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        point2.selected = True
        self.assertEqual(
            contour.selectedPoints,
            (point2,)
        )

    def test_selectedPoints_setFilledList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        contour.selectedPoints = [point1, point2]
        self.assertEqual(
            contour.selectedPoints,
            (point1, point2)
        )

    def test_selectedPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = True
        except NotImplementedError:
            return
        contour.selectedPoints = []
        self.assertEqual(
            contour.selectedPoints,
            ()
        )

    def test_selectedBPoints_default(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedBPoints,
            ()
        )

    def test_selectedBPoints_setSubObject(self):
        contour= self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        bPoint2.selected = True
        self.assertEqual(
            contour.selectedBPoints,
            (bPoint2,)
        )

    def test_selectedBPoints_setFilledList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        contour.selectedBPoints = [bPoint1, bPoint2]
        self.assertEqual(
            contour.selectedBPoints,
            (bPoint1, bPoint2)
        )

    def test_selectedBPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = True
        except NotImplementedError:
            return
        contour.selectedBPoints = []
        self.assertEqual(
            contour.selectedBPoints,
            ()
        )
