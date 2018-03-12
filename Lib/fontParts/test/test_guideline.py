import unittest
import collections
from fontParts.base import FontPartsError


class TestGuideline(unittest.TestCase):

    def getGuideline_generic(self):
        guideline, _ = self.objectGenerator("guideline")
        guideline.x = 1
        guideline.y = 2
        guideline.angle = 90
        return guideline

    # --------
    # Position
    # --------

    # x

    def test_x_get(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_set_valid_zero(self):
        guideline = self.getGuideline_generic()
        guideline.x = 0
        self.assertEqual(
            guideline.x,
            0
        )

    def test_x_set_valid_positive(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_set_valid_negative(self):
        guideline = self.getGuideline_generic()
        guideline.x = -1
        self.assertEqual(
            guideline.x,
            -1
        )

    def test_x_set_valid_positive_float(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1.1
        self.assertEqual(
            guideline.x,
            1.1
        )

    def test_x_set_valid_negative_float(self):
        guideline = self.getGuideline_generic()
        guideline.x = -1.1
        self.assertEqual(
            guideline.x,
            -1.1
        )

    def test_x_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(FontPartsError):
            guideline.x = "ABC"

    # y

    def test_y_get(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            guideline.y,
            2
        )

    def test_y_set_valid_zero(self):
        guideline = self.getGuideline_generic()
        guideline.y = 0
        self.assertEqual(
            guideline.y,
            0
        )

    def test_y_set_valid_positive(self):
        guideline = self.getGuideline_generic()
        guideline.y = 1
        self.assertEqual(
            guideline.y,
            1
        )

    def test_y_set_valid_negative(self):
        guideline = self.getGuideline_generic()
        guideline.y = -1
        self.assertEqual(
            guideline.y,
            -1
        )

    def test_y_set_valid_positive_float(self):
        guideline = self.getGuideline_generic()
        guideline.y = 1.1
        self.assertEqual(
            guideline.y,
            1.1
        )

    def test_y_set_valid_negative_float(self):
        guideline = self.getGuideline_generic()
        guideline.y = -1.1
        self.assertEqual(
            guideline.y,
            -1.1
        )

    def test_y_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(FontPartsError):
            guideline.y = "ABC"

    # ----
    # Hash
    # ----

    def test_hash(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            isinstance(guideline, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        guideline_one = self.getGuideline_generic()
        self.assertEqual(
            guideline_one,
            guideline_one
        )

    def test_object_not_equal_other(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        self.assertNotEqual(
            guideline_one,
            guideline_two
        )

    def test_object_equal_self_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        a = guideline_one
        a.x = 200
        self.assertEqual(
            guideline_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        a = guideline_one
        self.assertNotEqual(
            guideline_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        guideline = self.getGuideline_generic()
        try:
            guideline.selected = False
        except NotImplementedError:
            return
        guideline.selected = True
        self.assertEqual(
            guideline.selected,
            True
        )

    def test_not_selected_false(self):
        guideline = self.getGuideline_generic()
        try:
            guideline.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            guideline.selected,
            False
        )
