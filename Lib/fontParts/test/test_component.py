import unittest
import collections
from fontParts.base import FontPartsError


class TestComponent(unittest.TestCase):

    def getComponent_generic(self):
        component, _unrequested = self.objectGenerator("component")
        component.baseGlyph = "A"
        component.transformation = (1, 0, 0, 1, 0, 0)
        return component

    # ----------
    # Base Glyph
    # ----------

    def test_baseGlyph_generic(self):
        component = self.getComponent_generic()
        # get
        self.assertEqual(
            component.baseGlyph,
            "A"
        )
    def test_baseGlyph_valid_set(self):
        component = self.getComponent_generic()
        component.baseGlyph = "B"
        self.assertEqual(
            component.baseGlyph,
            "B"
        )
    def test_baseGlyph_invalid_set_none(self):
        component = self.getComponent_generic()
        with self.assertRaises(FontPartsError):
            component.baseGlyph = None
    def test_baseGlyph_invalid_set_empty_string(self):
        component = self.getComponent_generic()
        with self.assertRaises(FontPartsError):
            component.baseGlyph = ""
    def test_baseGlyph_invalid_set_int(self):
        component = self.getComponent_generic()
        with self.assertRaises(FontPartsError):
            component.baseGlyph = 123

    # ------
    # Bounds
    # ------

    def getComponent_bounds(self):
        font, _unrequested = self.objectGenerator("font")
        _unrequested.append(font)
        glyph = font.newGlyph("A")
        _unrequested.append(glyph)
        pen = glyph.getPen()
        pen.moveTo((0, 0))
        pen.lineTo((0, 100))
        pen.lineTo((100, 100))
        pen.lineTo((100, 0))
        pen.closePath()
        glyph = font.newGlyph("B")
        _unrequested.append(glyph)
        component = glyph.appendComponent("A")
        return component

    def test_bounds_get(self):
        component = self.getComponent_bounds()
        self.assertEqual(
            component.bounds,
            (0, 0, 100, 100)
        )
    def test_bounds_on_move(self):
        component = self.getComponent_bounds()
        component.moveBy((0.1, -0.1))
        self.assertEqual(
            component.bounds,
            (0.1, -0.1, 100.1, 99.9)
        )
    def test_bounds_on_scale(self):
        component = self.getComponent_bounds()
        component.scaleBy((2, 0.5))
        self.assertEqual(
            component.bounds,
            (0, 0, 200, 50)
        )
    def test_bounds_invalid_set(self):
        component = self.getComponent_bounds()
        with self.assertRaises(FontPartsError):
            component.bounds = (0, 0, 100, 100)

    # ----
    # Hash
    # ----
    def test_hash(self):
        component = self.getComponent_generic()
        self.assertEqual(
            isinstance(component, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        component_one = self.getComponent_generic()
        self.assertEqual(
            component_one,
            component_one
        )
    def test_object_not_equal_other(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        self.assertNotEqual(
            component_one,
            component_two
        )
    def test_object_equal_assigned_variable(self):
        component_one = self.getComponent_generic()
        a = component_one
        a.baseGlyph = "C"
        self.assertEqual(
            component_one,
            a
        )
    def test_object_not_equal_assigned_variable_other(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        a = component_one
        self.assertNotEqual(
            component_two,
            a
        )