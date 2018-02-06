import unittest
from fontParts.base import FontPartsError


class TestBPoint(unittest.TestCase):

    def getBPoint_corner(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint, unrequested

    # ----
    # Type
    # ----

    def test_type(self):
        bPoint, unrequested = self.getBPoint_corner()
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        bPoint_one, unrequested = self.getBPoint_corner()
        bPoint_two, unrequested = self.getBPoint_corner()
        self.assertEqual(
            bPoint_one,
            bPoint_one
        )
        self.assertEqual(
            hash(bPoint_one),
            hash(bPoint_one)
        )
        self.assertNotEqual(
            bPoint_one,
            bPoint_two
        )
        self.assertNotEqual(
            hash(bPoint_one),
            hash(bPoint_two)
        )