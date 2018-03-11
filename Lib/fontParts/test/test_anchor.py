import unittest
import collections
from fontParts.base import FontPartsError
from fontParts.base.deprecated import RemovedWarning
from fontTools.misc.py23 import basestring


class TestAnchor(unittest.TestCase):

    def getAnchor_generic(self):
        anchor, _unrequested = self.objectGenerator("anchor")
        anchor.name = "Anchor Attribute Test"
        anchor.x = 1
        anchor.y = 2
        anchor.color = None
        return anchor

    # ----------
    # Attributes
    # ----------

    def test_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.name, "Anchor Attribute Test")
    def test_set_valid(self):
        anchor = self.getAnchor_generic()
        anchor.name = u"foo"
        self.assertEqual(anchor.name, u"foo")
    def test_set_none(self):
        anchor = self.getAnchor_generic()
        anchor.name = None
        self.assertIsNone(anchor.name)
    def test_set_invalid(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.name = 123

    def test_color_get_none(self):
        anchor = self.getAnchor_generic()
        self.assertIsNone(anchor.color)
    def test_color_set_valid_max(self):
        anchor = self.getAnchor_generic()
        anchor.color = (1, 1, 1, 1)
        self.assertEqual(anchor.color, (1, 1, 1, 1))
    def test_color_set_valid_min(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0, 0, 0, 0)
        self.assertEqual(anchor.color, (0, 0, 0, 0))
    def test_color_set_valid_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        self.assertEqual(anchor.color, (0.1, 0.2, 0.3, 0.4))
    def test_color_set_none(self):
        anchor = self.getAnchor_generic()
        anchor.color = None
        self.assertIsNone(anchor.color)
    def test_color_set_invalid_over_max(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.color = (1.1, 0.2, 0.3, 0.4)
    def test_color_set_invalid_uner_min(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.color = (-0.1, 0.2, 0.3, 0.4)
    def test_color_set_invalid_too_few(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.color = (0.1, 0.2, 0.3)
    def test_color_set_invalid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.color = "0.1,0.2,0.3,0.4"
    def test_color_set_invalid_int(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.color = 123

    def test_identifier_get_none(self):
        anchor = self.getAnchor_generic()
        self.assertIsNone(anchor.identifier)
    def test_identifier_generated_type(self):
        anchor = self.getAnchor_generic()
        anchor.generateIdentifier()
        self.assertIsInstance(anchor.identifier, basestring)
    def test_identifier_consistencey(self):
        anchor = self.getAnchor_generic()
        anchor.generateIdentifier()
        # get: twice to test consistency
        self.assertEqual(anchor.identifier, anchor.identifier)
    def test_identifier_cannot_set(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.identifier = "ABC"

    def getAnchor_index(self):
        glyph, _unrequested = self.objectGenerator("glyph")
        glyph.appendAnchor("anchor 0", (0, 0))
        glyph.appendAnchor("anchor 1", (0, 0))
        glyph.appendAnchor("anchor 2", (0, 0))
        return glyph

    def test_index(self):
        glyph = self.getAnchor_index()
        for i, anchor in enumerate(glyph.anchors):
            self.assertEqual(anchor.index, i)

    def test_x_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.x, 1)
    def test_x_set_valid_positive(self):
        anchor = self.getAnchor_generic()
        anchor.x = 100
        self.assertEqual(anchor.x, 100)
    def test_x_set_valid_negative(self):
        anchor = self.getAnchor_generic()
        anchor.x = -100
        self.assertEqual(anchor.x, -100)
    def test_x_set_valid_zero(self):
        anchor = self.getAnchor_generic()
        anchor.x = 0
        self.assertEqual(anchor.x, 0)
    def test_x_set_valid_positive_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.x = 1.1
        self.assertEqual(anchor.x, 1.1)
    def test_x_set_valid_negative_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.x = -1.1
        self.assertEqual(anchor.x, -1.1)
    def test_x_set_invalid_none(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.x = None
    def test_x_set_valid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.x = "ABC"

    def test_y_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.y, 2)
    def test_y_set_valid_positive(self):
        anchor = self.getAnchor_generic()
        anchor.y = 100
        self.assertEqual(anchor.y, 100)
    def test_y_set_valid_negative(self):
        anchor = self.getAnchor_generic()
        anchor.y = -100
        self.assertEqual(anchor.y, -100)
    def test_y_set_valid_zero(self):
        anchor = self.getAnchor_generic()
        anchor.y = 0
        self.assertEqual(anchor.y, 0)
    def test_y_set_valid_positive_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.y = 1.1
        self.assertEqual(anchor.y, 1.1)
    def test_y_set_valid_negative_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.y = -1.1
        self.assertEqual(anchor.y, -1.1)
    def test_y_set_invalid_none(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.y = None
    def test_y_set_valid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.y = "ABC"

    # -------
    # Methods
    # -------

    def getAnchor_copy(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        return anchor

    def test_copy_seperate_objects(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertIsNot(anchor, copied)
    def test_copy_same_name(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.name, copied.name)
    def test_copy_same_color(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.color, copied.color)
    def test_copy_same_identifier(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.identifier, copied.identifier)
    def test_copy_generated_identifier_different(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        anchor.generateIdentifier()
        copied.generateIdentifier()
        self.assertNotEqual(anchor.identifier, copied.identifier)
    def test_copy_same_x(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.x, copied.x)
    def test_copy_same_y(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.y, copied.y)

    def test_transformBy_valid_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(anchor.x, -1)
        self.assertEqual(anchor.y, 8)
    def test_transformBy_valid_origin(self):
        anchor = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
    def test_transformBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.transformBy((1, 0, 0, 1, 0, "0"))
    def test_transformBy_invalid_all_string_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.transformBy("1, 0, 0, 1, 0, 0")
    def test_transformBy_invalid_int_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.transformBy(123)

    def test_moveBy_valid(self):
        anchor = self.getAnchor_generic()
        anchor.moveBy((-1, 2))
        self.assertEqual(anchor.x, 0)
        self.assertEqual(anchor.y, 4)
    def test_moveBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.moveBy((-1, "2"))
    def test_moveBy_invalid_all_strings_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.moveBy("-1, 2")
    def test_moveBy_invalid_int_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.moveBy(1)

    def test_scaleBy_valid_one_value_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, -4)
    def test_scaleBy_valid_two_values_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2, 3))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, 6)
    def test_scaleBy_valid_two_values_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
    def test_scaleBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.scaleBy((-1, "2"))
    def test_scaleBy_invalid_two_string_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.scaleBy("-1, 2")
    def test_scaleBy_invalid_tuple_too_many_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.scaleBy((-1, 2, -3))

    def test_rotateBy_valid_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.rotateBy(45)
        self.assertAlmostEqual(anchor.x, -0.707, places=3)
        self.assertAlmostEqual(anchor.y, 2.121, places=3)
    def test_rotateBy_valid_origin(self):
        anchor = self.getAnchor_generic()
        anchor.rotateBy(45, origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
    def test_rotateBy_invalid_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.rotateBy("45")
    def test_rotateBy_invalid_too_large_value_positive(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.rotateBy(361)
    def test_rotateBy_invalid_too_large_value_negative(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.rotateBy(-361)

    def test_skewBy_valid_no_origin_one_value(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy(100)
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertEqual(anchor.y, 2.0)
    def test_skewBy_valid_no_origin_two_values(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy((100, 200))
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertAlmostEqual(anchor.y, 2.364, places=3)
    def test_skewBy_valid_origin_one_value(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy(100, origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
    def test_skewBy_valid_origin_two_values(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    def getAnchor_round(self):
        anchor = self.getAnchor_generic()
        anchor.x = 1.1
        anchor.y = 2.5
        return anchor

    def test_round_close_to(self):
        anchor = self.getAnchor_round()
        anchor.round()
        self.assertEqual(anchor.x, 1)
    def test_round_at_half(self):
        anchor = self.getAnchor_round()
        anchor.round()
        self.assertEqual(anchor.y, 2)

    # ----------
    # Deprecated
    # ----------

    def test_removed_draw(self):
        glyph = self.getAnchor_index()
        pen = glyph.getPen()
        anchor = glyph.anchors[0]
        with self.assertRaises(RemovedWarning):
            anchor.draw(pen)

    def test_removed_drawPoints(self):
        glyph = self.getAnchor_index()
        pen = glyph.getPen()
        anchor = glyph.anchors[0]
        with self.assertRaises(RemovedWarning):
            anchor.drawPoints(pen)

    # ----
    # Hash
    # ----
    def test_hash(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(
            isinstance(anchor, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        anchor_one = self.getAnchor_generic()
        self.assertEqual(
            anchor_one,
            anchor_one
        )
    def test_object_not_equal_other(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        self.assertNotEqual(
            anchor_one,
            anchor_two
        )
    def test_object_equal_variable_assignment_self(self):
        anchor_one = self.getAnchor_generic()
        a = anchor_one
        a.moveBy((-1, 2))
        self.assertEqual(
            anchor_one,
            a
        )
    def test_object_not_equal_variable_assignment_other(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        a = anchor_one
        self.assertNotEqual(
            anchor_two,
            a
        )