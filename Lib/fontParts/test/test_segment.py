import unittest
from collections.abc import Hashable, Iterator
from fontParts.base import FontPartsError


class TestSegment(unittest.TestCase):
    def getSegment_line(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        segment = contour[1]
        return segment

    def getSegment_offcurves(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "offcurve")
        contour.appendPoint((100, 0), "offcurve")
        contour.appendPoint((100, 100), "offcurve")
        contour.appendPoint((0, 100), "offcurve")
        segment = contour[0]
        return segment

    # ----
    # Repr
    # ----

    def test_reprContents(self):
        segment = self.getSegment_line()
        result = segment._reprContents()
        self.assertIn(segment.type, result)
        self.assertIn(f"index={segment.index}", result)

    def test_reprContents_no_index(self):
        segment, _ = self.objectGenerator("segment")
        result = segment._reprContents()
        self.assertIn(segment.type, result)

    # -----
    # Index
    # -----

    def test_get_index(self):
        segment = self.getSegment_line()
        self.assertEqual(segment.index, 1)

    def test_get_index_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.index)

    # -------
    # Parents
    # -------

    def getGlyph_contour(self):
        glyph, _ = self.objectGenerator("glyph")
        pen = glyph.getPen()
        pen.moveTo((100, -10))
        pen.lineTo((100, 100))
        pen.lineTo((200, 100))
        pen.lineTo((200, 0))
        pen.closePath()
        return glyph

    def test_get_contour(self):
        contour, _ = self.objectGenerator("contour")
        segment, _ = self.objectGenerator("segment")
        segment._contour = lambda: contour
        self.assertEqual(segment.contour, contour)

    def test_get_contour_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.contour)

    def test_set_conotur(self):
        contour, _ = self.objectGenerator("contour")
        segment, _ = self.objectGenerator("segment")
        segment.contour = contour
        self.assertEqual(segment._contour(), contour)

    def test_set_contour_value_set(self):
        contour, _ = self.objectGenerator("contour")
        segment, _ = self.objectGenerator("segment")
        segment._contour = contour
        with self.assertRaises(AssertionError):
            segment.contour = contour

    def test_set_contour_value_none(self):
        segment, _ = self.objectGenerator("segment")
        segment.contour = None
        self.assertIsNone(segment._contour)

    def test_get_glyph(self):
        glyph = self.getGlyph_contour()
        segment = glyph[0][0]
        self.assertEqual(segment.glyph, glyph)

    def test_get_glyph_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.glyph)

    def test_get_layer(self):
        layer, _ = self.objectGenerator("layer")
        layer["A"] = self.getGlyph_contour()
        segment = layer["A"][0][0]
        self.assertEqual(segment.layer, layer)

    def test_get_layer_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.layer)

    def test_get_font(self):
        font, _ = self.objectGenerator("font")
        font["A"] = self.getGlyph_contour()
        segment = font["A"][0][0]
        self.assertEqual(segment.font, font)

    def test_get_font_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.font)

    # -----
    # Index
    # -----

    def test_get_index(self):
        segment = self.getSegment_line()
        self.assertEqual(segment.index, 1)

    def test_get_index_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.index)

    # ----
    # Type
    # ----

    def test_type_get(self):
        segment = self.getSegment_line()
        self.assertEqual(segment.type, "line")

    def test_set_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(segment.type, "move")

    def test_len_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(len(segment.points), 1)

    def test_oncuve_type_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(segment.onCurve.type, "move")

    def test_oncuve_x_y(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual((segment.onCurve.x, segment.onCurve.y), (101, 202))

    def test_set_curve(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        self.assertEqual(segment.type, "curve")

    def test_len_curve(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        self.assertEqual(len(segment.points), 3)

    def test_curve_pt_types(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        types = tuple(point.type for point in segment.points)
        self.assertEqual(types, ("offcurve", "offcurve", "curve"))

    def test_curve_pt_x_y(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(coordinates, ((0, 0), (101, 202), (101, 202)))

    def test_set_qcurve(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        self.assertEqual(segment.type, "qcurve")

    def test_len_qcurve(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        self.assertEqual(len(segment.points), 3)

    def test_qcurve_pt_types(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        types = tuple(point.type for point in segment.points)
        self.assertEqual(types, ("offcurve", "offcurve", "qcurve"))

    def test_qcurve_pt_x_y(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(coordinates, ((0, 0), (101, 202), (101, 202)))

    def test_set_invalid_segment_type_string(self):
        segment = self.getSegment_line()
        with self.assertRaises(ValueError):
            segment.type = "xxx"

    def test_set_invalid_segment_type_int(self):
        segment = self.getSegment_line()
        with self.assertRaises(TypeError):
            segment.type = 123

    def test_offCurve_only_segment(self):
        segment = self.getSegment_offcurves()
        self.assertEqual(len(segment.contour), 1)
        # onCurve is a dummy None value, telling this is an on-curve-less quad blob
        self.assertIsNone(segment.onCurve)
        self.assertEqual(segment.points, segment.offCurve)
        self.assertEqual(segment.type, "qcurve")

    def test_set_type_no_oncurve(self):
        segment = self.getSegment_offcurves()
        segment.type = "line"
        self.assertEqual(segment.type, "qcurve")

    def test_set_type_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        with self.assertRaises(FontPartsError):
            segment.type = "move"

    def test_set_type_same_value(self):
        segment = self.getSegment_line()
        segment.type = "line"
        self.assertEqual(segment.type, "line")

    # ------
    # Smooth
    # ------

    def test_get_smooth(self):
        segment = self.getSegment_line()
        self.assertFalse(segment.smooth)

    def test_get_smooth_no_oncurve(self):
        segment = self.getSegment_offcurves()
        self.assertTrue(segment.smooth)

    def test_set_smooth(self):
        segment = self.getSegment_line()
        segment.smooth = False
        self.assertFalse(segment.smooth)

    def test_set_smooth_no_oncurve(self):
        segment = self.getSegment_offcurves()
        segment.smooth = False
        self.assertTrue(segment.smooth)

    # -------
    # OnCurve
    # -------

    def test_get_onCurve(self):
        segment = self.getSegment_line()
        result = segment.onCurve.position
        self.assertEqual(result, (101, 202))

    def test_get_onCurve_no_points(self):
        segment, _ = self.objectGenerator("segment")
        self.assertIsNone(segment.onCurve)

    # ----
    # Iter
    # ----

    def test_iter(self):
        segment = self.getSegment_line()
        points = [p.position for p in segment]
        self.assertIsInstance(iter(segment), Iterator)
        self.assertEqual(points, [(101, 202)])

    # ---
    # Len
    # ---

    def test_len(self):
        segment = self.getSegment_line()
        self.assertEqual(len(segment), 1)

    def test_len_orphan_segment(self):
        segment, _ = self.objectGenerator("segment")
        self.assertEqual(len(segment), 0)

    # ----
    # Hash
    # ----

    def test_hash(self):
        segment = self.getSegment_line()
        self.assertEqual(isinstance(segment, Hashable), False)

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        segment_one = self.getSegment_line()
        self.assertEqual(segment_one, segment_one)

    def test_object_not_equal_other(self):
        segment_one = self.getSegment_line()
        segment_two = self.getSegment_line()
        self.assertNotEqual(segment_one, segment_two)

    def test_object_equal_self_variable_assignment(self):
        segment_one = self.getSegment_line()
        a = segment_one
        self.assertEqual(segment_one, a)

    def test_object_not_equal_other_variable_assignment(self):
        segment_one = self.getSegment_line()
        segment_two = self.getSegment_line()
        a = segment_one
        self.assertNotEqual(segment_two, a)

    def test_equal_invalid_type(self):
        segment_one = self.getSegment_line()
        segment_two = "invalidType"
        result = segment_one.__eq__(segment_two)
        self.assertEqual(result, NotImplemented)

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        segment = self.getSegment_line()
        try:
            segment.selected = False
        except NotImplementedError:
            return
        segment.selected = True
        self.assertEqual(segment.selected, True)

    def test_selected_false(self):
        segment = self.getSegment_line()
        try:
            segment.selected = False
        except NotImplementedError:
            return
        self.assertEqual(segment.selected, False)

    # -------------
    # Interpolation
    # -------------

    def test_isCompatible(self):
        segment1 = self.getSegment_line()
        segment2 = self.getSegment_line()
        segment2.type = "curve"
        compatible, report = segment1.isCompatible(segment2)
        self.assertTrue(compatible)
        self.assertFalse(report.fatal)
        self.assertFalse(report.typeDifference)

    def test_isCompatible_inconvertible_types(self):
        segment1 = self.getSegment_line()
        segment2 = self.getSegment_offcurves()
        compatible, report = segment1.isCompatible(segment2)
        self.assertFalse(compatible)
        self.assertTrue(report.fatal)
        self.assertTrue(report.typeDifference)

    # -----
    # Round
    # -----

    def test_round(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 10.4), "move")
        contour.appendPoint((10.5, 10.6), "line")
        segment = contour[1]
        segment.round()
        points = segment[0]
        self.assertEqual(points.position, (11, 11))
