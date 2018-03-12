import unittest
import collections
from fontParts.base import FontPartsError


class TestGlyph(unittest.TestCase):

    def getGlyph_generic(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.name = "Test Glyph 1"
        glyph.unicode = int(ord("X"))
        glyph.width = 250
        pen = glyph.getPen()
        pen.moveTo((100, 0))
        pen.lineTo((100, 100))
        pen.lineTo((200, 100))
        pen.lineTo((200, 0))
        pen.closePath()
        pen.moveTo((110, 10))
        pen.lineTo((110, 90))
        pen.lineTo((190, 90))
        pen.lineTo((190, 10))
        pen.closePath()
        pen.addComponent("Test Glyph 2", (1, 0, 0, 1, 0, 0))
        pen.addComponent("Test Glyph 3", (1, 0, 0, 1, 0, 0))
        glyph.appendAnchor("Test Anchor 1", (1, 2))
        glyph.appendAnchor("Test Anchor 2", (3, 4))
        glyph.appendGuideline((1, 2), 0, "Test Guideline 1")
        glyph.appendGuideline((3, 4), 90, "Test Guideline 2")
        return glyph

    # -------
    # Metrics
    # -------

    def test_width_get(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.width,
            250
        )

    def test_width_set_valid_positive(self):
        glyph = self.getGlyph_generic()
        glyph.width = 300
        self.assertEqual(
            glyph.width,
            300
        )

    def test_width_set_valid_zero(self):
        glyph = self.getGlyph_generic()
        glyph.width = 0
        self.assertEqual(
            glyph.width,
            0
        )

    def test_width_set_valid_float(self):
        glyph = self.getGlyph_generic()
        glyph.width = 101.5
        self.assertEqual(
            glyph.width,
            101.5
        )

    def test_width_set_valid_negative(self):
        glyph = self.getGlyph_generic()
        glyph.width = -485
        self.assertEqual(
            glyph.width,
            -485
        )

    def test_width_set_invalid_string(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(FontPartsError):
            glyph.width = "abc"

    def test_width_set_invalid_none(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(FontPartsError):
            glyph.width = None

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            hash(glyph_one),
            hash(glyph_one)
        )

    def test_hash_object_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            hash(glyph_one),
            hash(glyph_two)
        )

    def test_hash_object_self_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        self.assertEqual(
            hash(glyph_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            hash(glyph_two),
            hash(a)
        )

    def test_is_hashable(self):
        glyph_one = self.getGlyph_generic()
        self.assertEqual(
            isinstance(glyph_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            glyph_one,
            glyph_one
        )

    def test_object_not_equal_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )

    def test_object_not_equal_other_name_same(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )

    def test_object_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        a.name = "Other"
        self.assertEqual(
            glyph_one,
            a
        )

    def test_object_not_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            glyph_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        glyph = self.getGlyph_generic()
        try:
            glyph.selected = False
        except NotImplementedError:
            return
        glyph.selected = True
        self.assertEqual(
            glyph.selected,
            True
        )

    def test_not_selected_false(self):
        glyph = self.getGlyph_generic()
        try:
            glyph.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selected,
            False
        )

    # Contours

    def test_selectedContours_default(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedContours,
            ()
        )

    def test_selectedContours_setSubObject(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        contour2 = glyph.contours[1]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        contour2.selected = True
        self.assertEqual(
            glyph.selectedContours,
            (contour2,)
        )

    def test_selectedContours_setFilledList(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        contour2 = glyph.contours[1]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        glyph.selectedContours = [contour1, contour2]
        self.assertEqual(
            glyph.selectedContours,
            (contour1, contour2)
        )

    def test_selectedContours_setEmptyList(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        try:
            contour1.selected = True
        except NotImplementedError:
            return
        glyph.selectedContours = []
        self.assertEqual(
            glyph.selectedContours,
            ()
        )

    # Components

    def test_selectedComponents_default(self):
        glyph = self.getGlyph_generic()
        component1 = glyph.components[0]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedComponents,
            ()
        )

    def test_selectedComponents_setSubObject(self):
        glyph = self.getGlyph_generic()
        component1 = glyph.components[0]
        component2 = glyph.components[1]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        component2.selected = True
        self.assertEqual(
            glyph.selectedComponents,
            (component2,)
        )

    def test_selectedComponents_setFilledList(self):
        glyph = self.getGlyph_generic()
        component1 = glyph.components[0]
        component2 = glyph.components[1]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        glyph.selectedComponents = [component1, component2]
        self.assertEqual(
            glyph.selectedComponents,
            (component1, component2)
        )

    def test_selectedComponents_setEmptyList(self):
        glyph = self.getGlyph_generic()
        component1 = glyph.components[0]
        try:
            component1.selected = True
        except NotImplementedError:
            return
        glyph.selectedComponents = []
        self.assertEqual(
            glyph.selectedComponents,
            ()
        )

    # Anchors

    def test_selectedAnchors_default(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedAnchors,
            ()
        )

    def test_selectedAnchors_setSubObject(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        anchor2 = glyph.anchors[1]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        anchor2.selected = True
        self.assertEqual(
            glyph.selectedAnchors,
            (anchor2,)
        )

    def test_selectedAnchors_setFilledList(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        anchor2 = glyph.anchors[1]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        glyph.selectedAnchors = [anchor1, anchor2]
        self.assertEqual(
            glyph.selectedAnchors,
            (anchor1, anchor2)
        )

    def test_selectedAnchors_setEmptyList(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        try:
            anchor1.selected = True
        except NotImplementedError:
            return
        glyph.selectedAnchors = []
        self.assertEqual(
            glyph.selectedAnchors,
            ()
        )

    # Guidelines

    def test_selectedGuidelines_default(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedGuidelines,
            ()
        )

    def test_selectedGuidelines_setSubObject(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        guideline2 = glyph.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        guideline2.selected = True
        self.assertEqual(
            glyph.selectedGuidelines,
            (guideline2,)
        )

    def test_selectedGuidelines_setFilledList(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        guideline2 = glyph.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        glyph.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(
            glyph.selectedGuidelines,
            (guideline1, guideline2)
        )

    def test_selectedGuidelines_setEmptyList(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        try:
            guideline1.selected = True
        except NotImplementedError:
            return
        glyph.selectedGuidelines = []
        self.assertEqual(
            glyph.selectedGuidelines,
            ()
        )
