import unittest
import collections
from fontParts.base import FontPartsError


class TestSegment(unittest.TestCase):

    def getSegment_line(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        segment = contour[1]
        return segment, unrequested

    # ----
    # Type
    # ----

    def test_typeLine(self):
        # get
        segment, unrequested = self.getSegment_line()
        self.assertEqual(
            segment.type,
            "line"
        )
        # set: move
        segment, unrequested = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(
            segment.type,
            "move"
        )
        self.assertEqual(
            len(segment.points),
            1
        )
        self.assertEqual(
            segment.onCurve.type,
            "move"
        )
        self.assertEqual(
            (segment.onCurve.x, segment.onCurve.y),
            (101, 202)
        )
        # set: curve
        segment, unrequested = self.getSegment_line()
        segment.type = "curve"
        self.assertEqual(
            segment.type,
            "curve"
        )
        self.assertEqual(
            len(segment.points),
            3
        )
        types = tuple(point.type for point in segment.points)
        self.assertEqual(
            types,
            ("offcurve", "offcurve", "curve")
        )
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(
            coordinates,
            ((0, 0), (101, 202), (101, 202))
        )
        # set: qcurve
        segment, unrequested = self.getSegment_line()
        segment.type = "qcurve"
        self.assertEqual(
            segment.type,
            "qcurve"
        )
        self.assertEqual(
            len(segment.points),
            3
        )
        types = tuple(point.type for point in segment.points)
        self.assertEqual(
            types,
            ("offcurve", "offcurve", "qcurve")
        )
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(
            coordinates,
            ((0, 0), (101, 202), (101, 202))
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            segment.type = "xxx"
        with self.assertRaises(FontPartsError):
            segment.type = 123


    # ----
    # Hash
    # ----
    def test_hash(self):
        segment, unrequested = self.getSegment_line()
        self.assertEqual(
            isinstance(segment, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        segment_one, unrequested = self.getSegment_line()
        segment_two, unrequested = self.getSegment_line()
        self.assertEqual(
            segment_one,
            segment_one
        )
        self.assertNotEqual(
            segment_one,
            segment_two
        )
        a = segment_one
        self.assertEqual(
            segment_one,
            a
        )
        self.assertNotEqual(
            segment_two,
            a
        )