import unittest
import collections
from fontParts.base import FontPartsError
from fontParts.base.compatibility import SegmentCompatibilityReporter


class TestContour(unittest.TestCase):
    def getContour_bounds(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour

    # ----
    # Repr
    # ----

    def test_reprContents_noGlyph_noID(self):
        contour = self.getContour_bounds()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph_ID(self):
        contour = self.getContour_bounds()
        contour.getIdentifier()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        idFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == f"identifier='{contour.identifier!r}'":
                idFound = True
        self.assertTrue(idFound)

    def test_reprContents_Glyph_ID(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        contour.getIdentifier()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        idFound = False
        glyphFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == f"identifier='{contour.identifier!r}'":
                idFound = True
            if i == "in glyph":
                glyphFound = True
        self.assertTrue(idFound)
        self.assertTrue(glyphFound)

    def test_reprContents_Glyph_noID(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        glyphFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == "in glyph":
                glyphFound = True
        self.assertTrue(glyphFound)

    # ----
    # Copy
    # ----

    def test_copyData(self):
        contour = self.getContour_bounds()
        contourOther, _ = self.objectGenerator("contour")
        contourOther.copyData(contour)
        self.assertEqual(contour.bounds, contourOther.bounds)

    # -------
    # Parents
    # -------

    def test_parent_glyph_set_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        self.assertEqual(glyph, contour.glyph)

    def test_parent_glyph_set_glyph_None(self):
        contour = self.getContour_bounds()
        contour.glyph = None
        self.assertEqual(None, contour.glyph)

    def test_parent_glyph_set_already_set(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph2, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        self.assertEqual(glyph, contour.glyph)
        with self.assertRaises(AssertionError):
            contour.glyph = glyph2

    def test_parent_glyph_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.glyph)

    def test_parent_glyph_get(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour = glyph.appendContour(contour)
        self.assertEqual(glyph, contour.glyph)

    def test_parent_font_set(self):
        font, _ = self.objectGenerator("font")
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.font = font

    def test_parent_font_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.font)

    def test_parent_font_get(self):
        font, _ = self.objectGenerator("font")
        layer, _ = self.objectGenerator("layer")
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        layer.font = font
        glyph.layer = layer
        contour = glyph.appendContour(contour)
        self.assertEqual(font, contour.font)

    def test_parent_layer_set(self):
        layer, _ = self.objectGenerator("layer")
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.layer = layer

    def test_parent_layer_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.layer)

    def test_parent_layer_get(self):
        layer, _ = self.objectGenerator("layer")
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        glyph.layer = layer
        contour = glyph.appendContour(contour)
        self.assertEqual(layer, contour.layer)

    # ----
    # Pens
    # ----

    def test_drawPoints_oldProtocol(self):
        contour = self.getContour_bounds()

        class OldProtocolPen:
            def __init__(self):
                self.calls = []

            def beginPath(self):
                self.calls.append(("beginPath",))

            def addPoint(self, pt, segmentType=None, smooth=False, name=None):
                self.calls.append(("addPoint", pt, segmentType, smooth, name))

            def endPath(self):
                self.calls.append(("endPath",))

        pen = OldProtocolPen()
        contour.drawPoints(pen)

        self.assertEqual(len(pen.calls), 6)
        self.assertEqual(pen.calls[0], ("beginPath",))
        self.assertEqual(pen.calls[-1], ("endPath",))

    # -------------
    # Normalization
    # -------------

    def test_round(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 99.5), "line")
        contour.appendPoint((99.6, 100.4), "line")
        contour.appendPoint((100, 0), "line")
        contour.round()
        result = self.getContour_bounds()
        self.assertEqual(contour.bounds, result.bounds)

    # -------------
    # Interpolation
    # -------------

    def test_isCompatible_sameContours(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        compatible, report = contour1.isCompatible(contour2)
        self.assertTrue(compatible)
        self.assertFalse(report.fatal)
        self.assertFalse(report.warning)

    def test_isCompatible_differentSegmentCount(self):
        contour1 = self.getContour_bounds()
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((0, 0), "line")
        contour2.appendPoint((50, 100), "line")
        contour2.appendPoint((100, 0), "line")
        compatible, report = contour1.isCompatible(contour2)
        self.assertFalse(compatible)
        self.assertTrue(report.fatal)
        self.assertTrue(report.segmentCountDifference)

    def test_isCompatible_differentOpenClosed(self):
        contour1 = self.getContour_bounds()
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((0, 0), "move")
        contour2.appendPoint((0, 100), "line")
        contour2.appendPoint((100, 100), "line")
        contour2.appendPoint((100, 0), "line")
        compatible, report = contour1.isCompatible(contour2)
        self.assertFalse(compatible)
        self.assertTrue(report.openDifference)
        self.assertTrue(report.fatal)

    def test_isCompatible_differentDirection(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        contour2.reverse()
        compatible, report = contour1.isCompatible(contour2)
        self.assertTrue(compatible)
        self.assertFalse(report.fatal)
        self.assertFalse(report.warning)
        self.assertTrue(report.directionDifference)

    def test_isCompatible_incompatibleSegments(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        contour2[0].type = "qcurve"
        compatible, report = contour1.isCompatible(contour2)
        self.assertFalse(compatible)
        self.assertTrue(report.fatal)
        self.assertTrue(len(report.segments) > 0)

    def test_isCompatible_multipleIssues(self):
        contour1 = self.getContour_bounds()
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((0, 0), "move")
        contour2.appendPoint((0, 100), "line")
        contour2.appendPoint((100, 100), "line")
        contour2.appendPoint((100, 0), "line")
        contour2[1].type = "qcurve"
        compatible, report = contour1.isCompatible(contour2)
        self.assertFalse(compatible)
        self.assertTrue(report.openDifference)
        self.assertTrue(report.fatal)

    # ---------
    # Direction
    # ---------

    def test_set_clockwise(self):
        contour = self.getContour_bounds()
        contour.clockwise = True
        self.assertTrue(contour.clockwise)
        contour.clockwise = False
        self.assertFalse(contour.clockwise)

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def test_pointInside(self):
        contour = self.getContour_bounds()
        self.assertTrue(contour.pointInside((50, 50)))
        self.assertFalse(contour.pointInside((200, 200)))

    def test_contourInside(self):
        outerContour = self.getContour_bounds()
        innerContour, _ = self.objectGenerator("contour")
        innerContour.appendPoint((25, 25), "line")
        innerContour.appendPoint((25, 75), "line")
        innerContour.appendPoint((75, 75), "line")
        innerContour.appendPoint((75, 25), "line")
        self.assertTrue(outerContour.contourInside(innerContour))
        self.assertFalse(innerContour.contourInside(outerContour))

    # -----
    # Index
    # -----

    def test_index(self):
        glyph, _ = self.objectGenerator("glyph")
        contour1 = glyph.appendContour(self.getContour_bounds())
        contour2 = glyph.appendContour(self.getContour_bounds())
        contour3 = glyph.appendContour(self.getContour_bounds())
        self.assertEqual(contour1.index, 0)
        self.assertEqual(contour2.index, 1)
        self.assertEqual(contour3.index, 2)

    def test_set_index(self):
        glyph, _ = self.objectGenerator("glyph")
        contour1 = glyph.appendContour(self.getContour_bounds())
        contour2 = glyph.appendContour(self.getContour_bounds())
        contour3 = glyph.appendContour(self.getContour_bounds())

        contour1.index = 2
        self.assertEqual(contour1.index, 2)
        self.assertEqual(contour2.index, 0)
        self.assertEqual(contour3.index, 1)

        contour1.index = 1
        self.assertEqual(contour1.index, 1)
        self.assertEqual(contour2.index, 0)
        self.assertEqual(contour3.index, 2)

        contour1.index = 3
        self.assertEqual(contour1.index, 2)

    # --------------
    # Identification
    # --------------

    def test_get_index_no_glyph(self):
        contour = self.getContour_bounds()
        self.assertEqual(contour.index, None)

    def test_get_index_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        c1 = glyph.appendContour(contour)
        self.assertEqual(c1.index, 0)
        c2 = glyph.appendContour(contour)
        self.assertEqual(c2.index, 1)

    # ------
    # Bounds
    # ------

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
        self.assertEqual(contour.bounds, (0, 0, 100, 100))

    def test_bounds_set_float(self):
        contour = self.getContour_bounds()
        contour.moveBy((0.5, -0.5))
        self.assertEqual(contour.bounds, (0.5, -0.5, 100.5, 99.5))

    def test_bounds_point_not_at_extrema(self):
        contour = self.getContour_bounds()
        contour = self.getContour_boundsExtrema()
        bounds = tuple(int(round(i)) for i in contour.bounds)
        self.assertEqual(bounds, (0, 0, 100, 100))

    def test_invalid_bounds_set(self):
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.bounds = (1, 2, 3, 4)

    def test_empty_bounds(self):
        contour, _ = self.objectGenerator("contour")
        self.assertIsNone(contour.bounds)

    # ----
    # Area
    # ----

    def test_area(self):
        contour = self.getContour_bounds()
        self.assertEqual(contour.area, 10000)

    def test_empty_area(self):
        contour, _ = self.objectGenerator("contour")
        self.assertIsNone(contour.area)

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        contour_one = self.getContour_bounds()
        self.assertEqual(hash(contour_one), hash(contour_one))

    def test_hash_object_other(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        self.assertNotEqual(hash(contour_one), hash(contour_two))

    def test_hash_object_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        a = contour_one
        self.assertEqual(hash(contour_one), hash(a))

    def test_hash_object_other_variable_assignment(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        a = contour_one
        self.assertNotEqual(hash(contour_two), hash(a))

    def test_is_hashable(self):
        contour_one = self.getContour_bounds()
        self.assertTrue(isinstance(contour_one, collections.abc.Hashable))

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        contour_one = self.getContour_bounds()
        self.assertEqual(contour_one, contour_one)

    def test_object_not_equal_self(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        self.assertNotEqual(contour_one, contour_two)

    def test_object_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        a = contour_one
        a.moveBy((0.5, -0.5))
        self.assertEqual(contour_one, a)

    def test_object_not_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        a = contour_one
        self.assertNotEqual(contour_two, a)

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
        self.assertEqual(contour.selected, True)

    def test_selected_false(self):
        contour = self.getContour_bounds()
        try:
            contour.selected = False
        except NotImplementedError:
            return
        self.assertEqual(contour.selected, False)

    def test_selectedSegments_default(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(contour.selectedSegments, ())

    def test_selectedSegments_setSubObject(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        segment2.selected = True
        self.assertEqual(contour.selectedSegments == (segment2,), True)

    def test_selectedSegments_setFilledList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        contour.selectedSegments = [segment1, segment2]
        self.assertEqual(contour.selectedSegments, (segment1, segment2))

    def test_selectedSegments_setEmptyList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = True
        except NotImplementedError:
            return
        contour.selectedSegments = []
        self.assertEqual(contour.selectedSegments, ())

    def test_selectedPoints_default(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(contour.selectedPoints, ())

    def test_selectedPoints_setSubObject(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        point2.selected = True
        self.assertEqual(contour.selectedPoints, (point2,))

    def test_selectedPoints_setFilledList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        contour.selectedPoints = [point1, point2]
        self.assertEqual(contour.selectedPoints, (point1, point2))

    def test_selectedPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        try:
            point1.selected = True
        except NotImplementedError:
            return
        contour.selectedPoints = []
        self.assertEqual(contour.selectedPoints, ())

    def test_selectedBPoints_default(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(contour.selectedBPoints, ())

    def test_selectedBPoints_setSubObject(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        bPoint2.selected = True
        self.assertEqual(contour.selectedBPoints, (bPoint2,))

    def test_selectedBPoints_setFilledList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        contour.selectedBPoints = [bPoint1, bPoint2]
        self.assertEqual(contour.selectedBPoints, (bPoint1, bPoint2))

    def test_selectedBPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        try:
            bPoint1.selected = True
        except NotImplementedError:
            return
        contour.selectedBPoints = []
        self.assertEqual(contour.selectedBPoints, ())

    # --------
    # Segments
    # --------

    def test_segments_offcurves_end(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_begin_end(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_begin(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_middle(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["curve", "line", "curve"]
        )

    def test_segments_empty(self):
        contour, _ = self.objectGenerator("contour")
        segments = contour.segments
        self.assertEqual(segments, ())

    def test_segment_insert_open(self):
        # at index 0
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((2, 2), "line")
        contour.appendPoint((3, 3), "line")
        contour.insertSegment(0, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (1, 1), (2, 2), (3, 3)],
        )
        # at index 1
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((2, 2), "line")
        contour.appendPoint((3, 3), "line")
        contour.insertSegment(1, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (2, 2), (1, 1), (3, 3)],
        )

    def test_segment_insert_curve_open(self):
        # at index 0
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((2, 2), "offcurve")
        contour.appendPoint((3, 3), "offcurve")
        contour.appendPoint((4, 4), "curve")
        contour.appendPoint((5, 5), "line")
        contour.insertSegment(0, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        )
        # at index 1
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((2, 2), "offcurve")
        contour.appendPoint((3, 3), "offcurve")
        contour.appendPoint((4, 4), "curve")
        contour.appendPoint((5, 5), "line")
        contour.insertSegment(1, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (2, 2), (3, 3), (4, 4), (1, 1), (5, 5)],
        )

    def test_segment_insert_closed(self):
        # at index 0
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((2, 2), "line")
        contour.appendPoint((3, 3), "line")
        contour.insertSegment(0, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (1, 1), (2, 2), (3, 3)],
        )
        # at index 1
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((2, 2), "line")
        contour.appendPoint((3, 3), "line")
        contour.insertSegment(1, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (2, 2), (1, 1), (3, 3)],
        )

    def test_segment_insert_curve_closed(self):
        # at index 0
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((2, 2), "offcurve")
        contour.appendPoint((3, 3), "offcurve")
        contour.appendPoint((4, 4), "curve")
        contour.appendPoint((5, 5), "line")
        contour.insertSegment(0, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        )
        # at index 1
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((2, 2), "offcurve")
        contour.appendPoint((3, 3), "offcurve")
        contour.appendPoint((4, 4), "curve")
        contour.appendPoint((5, 5), "line")
        contour.insertSegment(1, "line", [(1, 1)])
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(0, 0), (2, 2), (3, 3), (4, 4), (1, 1), (5, 5)],
        )

    def test_setStartSegment_index(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((50, 0), "curve")
        contour.appendPoint((75, 0), "offcurve")
        contour.appendPoint((100, 25), "offcurve")
        contour.appendPoint((100, 50), "curve")
        contour.appendPoint((100, 75), "offcurve")
        contour.appendPoint((75, 100), "offcurve")
        contour.appendPoint((50, 100), "curve")
        contour.appendPoint((25, 100), "offcurve")
        contour.appendPoint((0, 75), "offcurve")
        contour.appendPoint((0, 50), "curve")
        contour.appendPoint((0, 25), "offcurve")
        contour.appendPoint((25, 0), "offcurve")
        contour.setStartSegment(1)
        self.assertEqual(contour.points[0].type, "curve")
        self.assertEqual((contour.points[0].x, contour.points[0].y), (100, 50))

    def test_setStartSegment_segment(self):
        contour = self.getContour_bounds()
        targetSegment = contour.segments[1]
        contour.setStartSegment(targetSegment)
        self.assertEqual(contour.points[0].position, (0, 100))

    def test_setStartSegment_index_out_of_range(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((100, 0), "line")
        with self.assertRaises(ValueError):
            contour.setStartSegment(5)

    def test_setStartSegment_open_contour(self):
        contour, _ = self.objectGenerator("contour")
        with self.assertRaises(FontPartsError):
            contour.setStartSegment(1)

    def test_iterSegment(self):
        contour = self.getContour_bounds()
        iterator = iter(contour)
        self.assertIsInstance(iterator, collections.abc.Iterator)
        segments = list(iterator)
        self.assertEqual(len(segments), len(contour.segments))
        self.assertEqual([segment.type for segment in segments], ["line"] * 4)

    def test_appendSegment_points(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((10, 0), "line")
        initialLength = len(contour)
        points = [(50, 50)]
        contour.appendSegment(type="line", points=points)
        appendedPoints = [p.position for p in contour.segments[-1].points]
        self.assertEqual(len(contour), initialLength + 1)
        self.assertEqual(appendedPoints, points)

    def test_appendSegment_segment(self):
        contour1, _ = self.objectGenerator("contour")
        contour1.appendPoint((0, 0), "move")
        contour1.appendPoint((10, 0), "line")
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        segment = contour2.segments[0]
        points = [p.position for p in segment]
        contour1.appendSegment(segment=segment)
        appendedPoints = [p.position for p in contour1.segments[-1].points]
        self.assertEqual(len(contour1), initialLength + 1)
        self.assertEqual(appendedPoints, points)

    def test_appendSegment_overrides(self):
        contour1, _ = self.objectGenerator("contour")
        contour1.appendPoint((0, 0), "move")
        contour1.appendPoint((10, 0), "line")
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50))
        segment = contour2.segments[0]
        overridePoints = [(120, 120)]
        contour1.appendSegment(type="curve", segment=segment, points=overridePoints)
        appendedPoints = [p.position for p in contour1.segments[-1].points]
        self.assertEqual(len(contour1), initialLength + 1)
        self.assertEqual(appendedPoints, overridePoints)

    def test_appendSegment_raises(self):
        contour = self.getContour_bounds()
        with self.assertRaises(TypeError):
            contour.appendSegment(type=None, points=[(50, 50)])
        with self.assertRaises(TypeError):
            contour.appendSegment(type="line", points=None)

    def test_insertSegment_segment(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        contour2.appendPoint((60, 60), "offcurve")
        segment = contour2.segments[0]
        contour1.insertSegment(0, segment=segment)
        insertedPoints = [p.position for p in contour1.segments[0].points]
        originalPoints = [p.position for p in segment.points]
        self.assertEqual(len(contour1), initialLength + 1)
        self.assertEqual(insertedPoints, originalPoints)
        self.assertEqual(contour1.segments[0].type, "line")

    def test_insertSegment_overrides(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50))
        segment = contour2.segments[0]
        overridePoints = [(120, 120)]
        contour1.insertSegment(0, type="curve", segment=segment, points=overridePoints)
        insertedPoints = [p.position for p in contour1.segments[0].points]
        self.assertEqual(len(contour1), initialLength + 1)
        self.assertEqual(insertedPoints, overridePoints)
        self.assertEqual(contour1.segments[0].type, "curve")

    def test_insertSegment_raises(self):
        contour = self.getContour_bounds()
        with self.assertRaises(TypeError):
            contour.insertSegment(None, type="line", points=[(50, 50)])
        with self.assertRaises(TypeError):
            contour.insertSegment(0, type=None, points=[(50, 50)])
        with self.assertRaises(TypeError):
            contour.insertSegment(0, type="line", points=None)

    def test_removeSegment_index(self):
        contour = self.getContour_bounds()
        initialLength = len(contour)
        contour.removeSegment(0)
        self.assertEqual(len(contour), initialLength - 1)

    def test_removeSegment_index_out_of_range(self):
        contour = self.getContour_bounds()
        with self.assertRaises(ValueError):
            contour.removeSegment(10)

    def test_removeSegment_segment(self):
        contour = self.getContour_bounds()
        initialLength = len(contour)
        segment = contour.segments[0]
        contour.removeSegment(segment)
        self.assertEqual(len(contour), initialLength - 1)

    # -------
    # bPoints
    # -------

    def test_appendBPoint_values(self):
        contour = self.getContour_bounds()
        initialLength = len(contour.bPoints)
        contour.appendBPoint(type="corner", anchor=(0, 0))
        self.assertEqual(len(contour.bPoints), initialLength + 1)
        self.assertEqual(contour.bPoints[-1].type, "corner")
        self.assertEqual(contour.bPoints[-1].anchor, (0, 0))

    def test_appendBPoint_bPoint(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        bPoint = contour2.bPoints[0]
        contour1.appendBPoint(bPoint=bPoint)
        self.assertEqual(len(contour1.bPoints), initialLength + 1)
        self.assertEqual(contour1.bPoints[-1].type, "corner")
        self.assertEqual(contour1.bPoints[-1].anchor, (50, 50))

    def test_appendBPoint_overrides(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        bPoint = contour2.bPoints[0]
        contour1.appendBPoint(
            type="curve", anchor=(0, 0), bcpIn=(10, 10), bcpOut=(20, 20), bPoint=bPoint
        )
        self.assertEqual(len(contour1.bPoints), initialLength + 1)
        self.assertEqual(contour1.bPoints[-1].type, "curve")
        self.assertEqual(contour1.bPoints[-1].anchor, (0, 0))
        self.assertEqual(contour1.bPoints[-1].bcpIn, (10, 10))
        self.assertEqual(contour1.bPoints[-1].bcpOut, (20, 20))

    def test_insertBPoint_values(self):
        contour = self.getContour_bounds()
        initialLength = len(contour.bPoints)
        contour.insertBPoint(0, type="curve", anchor=(50, 50))
        self.assertEqual(len(contour.bPoints), initialLength + 1)
        self.assertEqual(contour.bPoints[1].anchor, (50, 50))

    def test_insertBPoint_bPoint(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        bPoint = contour2.bPoints[0]
        contour1.insertBPoint(0, bPoint=bPoint)
        self.assertEqual(len(contour1.bPoints), initialLength + 1)
        self.assertEqual(contour1.bPoints[1].type, "corner")
        self.assertEqual(contour1.bPoints[1].anchor, (50, 50))

    def test_insertBPoint_overrides(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "line")
        bPoint = contour2.bPoints[0]
        contour1.insertBPoint(
            0,
            type="curve",
            anchor=(0, 0),
            bcpIn=(10, 10),
            bcpOut=(20, 20),
            bPoint=bPoint,
        )
        self.assertEqual(len(contour1.bPoints), initialLength + 1)
        self.assertEqual(contour1.bPoints[1].type, "curve")
        self.assertEqual(contour1.bPoints[1].anchor, (0, 0))
        self.assertEqual(contour1.bPoints[1].bcpIn, (10, 10))
        self.assertEqual(contour1.bPoints[1].bcpOut, (20, 20))

    def test_insertBPoint_raises(self):
        contour = self.getContour_bounds()
        with self.assertRaises(TypeError):
            contour.insertBPoint(None, type="corner", anchor=(50, 50))
        with self.assertRaises(TypeError):
            contour.insertBPoint(0, type=None, anchor=(50, 50))
        with self.assertRaises(TypeError):
            contour.insertBPoint(0, type="corner", anchor=None)

    def test_removeBPoint_index(self):
        contour = self.getContour_bounds()
        initialLength = len(contour.bPoints)
        contour.removeBPoint(0)
        self.assertEqual(len(contour.bPoints), initialLength - 1)
        self.assertEqual(contour.bPoints[0].anchor, (0, 100))

    def test_removeBPoint_index_out_of_range(self):
        contour = self.getContour_bounds()
        with self.assertRaises(ValueError):
            contour.removeBPoint(10)

    def test_removeBPoint_bPoint(self):
        contour = self.getContour_bounds()
        initialLength = len(contour)
        bPoint = contour.bPoints[0]
        contour.removeBPoint(bPoint)
        self.assertEqual(len(contour.bPoints), initialLength - 1)

    def test_removeBPoint_offcurves(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "curve")
        contour.appendPoint((0, 50), "offcurve")
        contour.appendPoint((50, 100), "offcurve")
        contour.appendPoint((100, 100), "curve")
        contour.appendPoint((150, 100), "offcurve")
        contour.appendPoint((200, 50), "offcurve")
        initialLength = len(contour.bPoints)
        contour.removeBPoint(-2)
        self.assertEqual(len(contour.bPoints), initialLength - 1)

    # ------
    # points
    # ------

    def test_setStartPoint(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((1, 1), "line")
        contour.appendPoint((2, 2), "line")
        contour.appendPoint((3, 3), "line")

        contour.setStartPoint(2)
        self.assertEqual(
            [(point.x, point.y) for point in contour.points],
            [(2, 2), (3, 3), (0, 0), (1, 1)],
        )

    def test_setStartPoint_index_zero(self):
        contour = self.getContour_bounds()
        contour.setStartPoint(0)
        self.assertEqual(contour.points[0].position, (0, 0))

    def test_setStartPoint_index_out_of_range(self):
        contour = self.getContour_bounds()
        with self.assertRaises(ValueError):
            contour.setStartPoint(10)

    def test_setStartPoint_open_contour(self):
        contour, _ = self.objectGenerator("contour")
        with self.assertRaises(FontPartsError):
            contour.setStartPoint(0)

    def test_appendPoint_position(self):
        contour = self.getContour_bounds()
        initialLength = len(contour.points)
        contour.appendPoint(position=(10, 10))
        self.assertEqual(len(contour.bPoints), initialLength + 1)
        self.assertEqual(contour.points[-1].position, (10, 10))
        self.assertEqual(contour.points[-1].type, "line")

    def test_appendPoint_bPoint(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "curve")
        point = contour2.points[0]
        contour1.appendPoint(point=point)
        self.assertEqual(len(contour1.points), initialLength + 1)
        self.assertEqual(contour1.points[-1].position, (50, 50))
        self.assertEqual(contour1.points[-1].type, "curve")

    def test_appendPoint_overrides(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "curve")
        point = contour2.points[0]
        contour1.appendPoint(
            position=(10, 10), type="line", name="test", identifier="test", point=point
        )
        self.assertEqual(len(contour1.points), initialLength + 1)
        self.assertEqual(contour1.points[-1].position, (10, 10))
        self.assertEqual(contour1.points[-1].type, "line")
        self.assertEqual(contour1.points[-1].name, "test")
        self.assertEqual(contour1.points[-1].identifier, "test")

    def test_insertPoint_position(self):
        contour = self.getContour_bounds()
        initialLength = len(contour.points)
        contour.insertPoint(0, position=(10, 10))
        self.assertEqual(len(contour.bPoints), initialLength + 1)
        self.assertEqual(contour.points[0].position, (10, 10))
        self.assertEqual(contour.points[0].type, "line")

    def test_insertPoint_point(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "curve")
        point = contour2.points[0]
        contour1.insertPoint(0, point=point)
        self.assertEqual(len(contour1.points), initialLength + 1)
        self.assertEqual(contour1.points[0].position, (50, 50))
        self.assertEqual(contour1.points[0].type, "curve")

    def test_insertPoint_overrides(self):
        contour1 = self.getContour_bounds()
        initialLength = len(contour1)
        contour2, _ = self.objectGenerator("contour")
        contour2.appendPoint((50, 50), "curve")
        point = contour2.points[0]
        contour1.insertPoint(
            0,
            position=(10, 10),
            type="line",
            name="test",
            identifier="test",
            point=point,
        )
        self.assertEqual(len(contour1.points), initialLength + 1)
        self.assertEqual(contour1.points[0].position, (10, 10))
        self.assertEqual(contour1.points[0].type, "line")
        self.assertEqual(contour1.points[0].name, "test")
        self.assertEqual(contour1.points[0].identifier, "test")

    def test_insertPoint_raises(self):
        contour = self.getContour_bounds()
        with self.assertRaises(TypeError):
            contour.insertPoint(None, type="line", position=(50, 50))
        with self.assertRaises(TypeError):
            contour.insertPoint(0, type="line", position=None)
