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

    def test_baseGlyph(self):
        component = self.getComponent_generic()
        # get
        self.assertEqual(
            component.baseGlyph,
            "A"
        )
        # set: valid
        component.baseGlyph = "B"
        self.assertEqual(
            component.baseGlyph,
            "B"
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            component.baseGlyph = None
        with self.assertRaises(FontPartsError):
            component.baseGlyph = ""
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

    def test_bounds(self):
        component = self.getComponent_bounds()
        # get
        self.assertEqual(
            component.bounds,
            (0, 0, 100, 100)
        )
        component.moveBy((0.1, -0.1))
        self.assertEqual(
            component.bounds,
            (0.1, -0.1, 100.1, 99.9)
        )
        component.scaleBy((2, 0.5))
        self.assertEqual(
            component.bounds,
            (0.2, -0.05, 200.2, 49.95)
        )
        # set
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

    def test_equal(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        self.assertEqual(
            component_one,
            component_one
        )
        self.assertNotEqual(
            component_one,
            component_two
        )
        a = component_one
        self.assertEqual(
            component_one,
            a
        )
        self.assertNotEqual(
            component_two,
            a
        )