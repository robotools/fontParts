import unittest
import collections
from fontParts.base import FontPartsError


class TestBPoint(unittest.TestCase):

    def getBPoint_corner(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint

    # ----
    # Type
    # ----

    def test_type_corner(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    def test_type_curve(self):
        bPoint = self.getBPoint_corner()
        bPoint.type = "curve"
        self.assertEqual(
            bPoint.type,
            "curve"
        )

    def test_type_not_equal(self):
        bPoint = self.getBPoint_corner()
        bPoint.type = "curve"
        self.assertNotEqual(
            bPoint.type,
            "corner"
        )

    # ------
    # Anchor
    # ------

    def test_anchor_get(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.anchor,
            (101, 202)
        )

    def test_anchor_change(self):
        bPoint = self.getBPoint_corner()
        bPoint.anchor = (51,45)
        self.assertEqual(
            bPoint.anchor,
            (51, 45)
        )

    # -----
    # Index
    # -----

    def test_index(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.index,
            1
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            isinstance(bPoint, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        bPoint_one = self.getBPoint_corner()
        self.assertEqual(
            bPoint_one,
            bPoint_one
        )

    def test_object_not_equal_other(self):
        bPoint_one = self.getBPoint_corner()
        bPoint_two = self.getBPoint_corner()
        self.assertNotEqual(
            bPoint_one,
            bPoint_two
        )

    def test_object_equal_self_variable_assignment(self):
        bPoint_one = self.getBPoint_corner()
        a = bPoint_one
        a.anchor = (51,45)
        self.assertEqual(
            bPoint_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        bPoint_one = self.getBPoint_corner()
        bPoint_two = self.getBPoint_corner()
        a = bPoint_one
        self.assertNotEqual(
            bPoint_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        bPoint = self.getBPoint_corner()
        try:
            bPoint.selected = False
        except NotImplementedError:
            return
        bPoint.selected = True
        self.assertEqual(
            bPoint.selected,
            True
        )

    def test_selected_false(self):
        bPoint = self.getBPoint_corner()
        try:
            bPoint.selected = False
        except NotImplementedError:
            return
        bPoint.selected = False
        self.assertEqual(
            bPoint.selected,
            False
        )
