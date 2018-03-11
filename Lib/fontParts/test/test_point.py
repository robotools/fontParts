import unittest
import collections
from fontParts.base import FontPartsError


class TestPoint(unittest.TestCase):

    def getPoint_generic(self):
        contour, _ = self.objectGenerator("contour")
        _.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        point = contour.points[1]
        return point

    # ----
    # Type
    # ----

    def test_get(self):
        point = self.getPoint_generic()
        # get
        self.assertEqual(
            point.type,
            "line"
        )
    def test_set_move(self):
        point = self.getPoint_generic()
        point.type = "move"
        self.assertEqual(
            point.type,
            "move"
        )
    def test_set_curve(self):
        point = self.getPoint_generic()
        point.type = "curve"
        self.assertEqual(
            point.type,
            "curve"
        )
    def test_set_wcurve(self):
        point = self.getPoint_generic()
        point.type = "qcurve"
        self.assertEqual(
            point.type,
            "qcurve"
        )
    def test_set_offcurve(self):
        point = self.getPoint_generic()
        point.type = "offcurve"
        self.assertEqual(
            point.type,
            "offcurve"
        )
    def test_set_invalid_point_type_string(self):
        point = self.getPoint_generic()
        with self.assertRaises(FontPartsError):
            point.type = "xxx"
    def test_set_invalid_point_type_int(self):
        point = self.getPoint_generic()
        with self.assertRaises(FontPartsError):
            point.type = 123

    # ----
    # Hash
    # ----
    def test_hash(self):
        point = self.getPoint_generic()
        self.assertEqual(
            isinstance(point, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        point_one = self.getPoint_generic()
        self.assertEqual(
            point_one,
            point_one
        )
    def test_object_not_equal_other(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        self.assertNotEqual(
            point_one,
            point_two
        )
    def test_object_equal_self_variable_assignment(self):
        point_one = self.getPoint_generic()
        a = point_one
        self.assertEqual(
            point_one,
            a
        )
    def test_object_not_equal_other_variable_assignment(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        a = point_one
        self.assertNotEqual(
            point_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected(self):
        point = self.getPoint_generic()
        try:
            point.selected = False
        except NotImplementedError:
            return
        point.selected = True
        self.assertEqual(
            point.selected,
            True
        )
        point.selected = False
        self.assertEqual(
            point.selected,
            False
        )