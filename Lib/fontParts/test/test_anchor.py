import unittest
import collections
from fontParts.base import FontPartsError
from fontParts.base.deprecated import RemovedWarning
from fontTools.misc.py23 import basestring


class TestAnchor(unittest.TestCase):

    def getAnchor_generic(self):
        anchor, unrequested = self.objectGenerator("anchor")
        anchor.name = "Anchor Attribute Test"
        anchor.x = 1
        anchor.y = 2
        anchor.color = None
        return anchor, unrequested

    # ----------
    # Attributes
    # ----------

    def test_name(self):
        anchor, unrequested = self.getAnchor_generic()
        # get
        self.assertEqual(anchor.name, "Anchor Attribute Test")
        # set: valid
        anchor.name = u"foo"
        self.assertEqual(anchor.name, u"foo")
        # set: None
        anchor.name = None
        self.assertIsNone(anchor.name)
        # set: invalid
        with self.assertRaises(FontPartsError):
            anchor.name = 123

    def test_color(self):
        anchor, unrequested = self.getAnchor_generic()
        # get
        self.assertIsNone(anchor.color)
        # set: valid
        anchor.color = (1, 1, 1, 1)
        self.assertEqual(anchor.color, (1, 1, 1, 1))
        anchor.color = (0, 0, 0, 0)
        self.assertEqual(anchor.color, (0, 0, 0, 0))
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        self.assertEqual(anchor.color, (0.1, 0.2, 0.3, 0.4))
        # set: None
        anchor.color = None
        self.assertIsNone(anchor.color)
        # set: invalid
        with self.assertRaises(FontPartsError):
            anchor.color = (1.1, 0.2, 0.3, 0.4)
        with self.assertRaises(FontPartsError):
            anchor.color = (-0.1, 0.2, 0.3, 0.4)
        with self.assertRaises(FontPartsError):
            anchor.color = (0.1, 0.2, 0.3)
        with self.assertRaises(FontPartsError):
            anchor.color = "0.1,0.2,0.3,0.4"
        with self.assertRaises(FontPartsError):
            anchor.color = 123

    def test_identifier(self):
        anchor, unrequested = self.getAnchor_generic()
        # get
        self.assertIsNone(anchor.identifier)
        # get
        anchor.generateIdentifier()
        self.assertIsInstance(anchor.identifier, basestring)
        # get: twice to test consistency
        self.assertEqual(anchor.identifier, anchor.identifier)
        # set
        with self.assertRaises(FontPartsError):
            anchor.identifier = "ABC"

    def getAnchor_index(self):
        glyph, unrequested = self.objectGenerator("glyph")
        glyph.appendAnchor("anchor 0", (0, 0))
        glyph.appendAnchor("anchor 1", (0, 0))
        glyph.appendAnchor("anchor 2", (0, 0))
        return glyph, unrequested

    def test_index(self):
        glyph, unrequested = self.getAnchor_index()
        for i, anchor in enumerate(glyph.anchors):
            self.assertEqual(anchor.index, i)

    def test_x(self):
        anchor, unrequested = self.getAnchor_generic()
        # get
        self.assertEqual(anchor.x, 1)
        # set: valid
        anchor.x = 100
        self.assertEqual(anchor.x, 100)
        anchor.x = -100
        self.assertEqual(anchor.x, -100)
        anchor.x = 0
        self.assertEqual(anchor.x, 0)
        anchor.x = 1.1
        self.assertEqual(anchor.x, 1.1)
        anchor.x = -1.1
        self.assertEqual(anchor.x, -1.1)
        # set: invalid
        with self.assertRaises(FontPartsError):
            anchor.x = None
        with self.assertRaises(FontPartsError):
            anchor.x = "ABC"

    def test_y(self):
        anchor, unrequested = self.getAnchor_generic()
        # get
        self.assertEqual(anchor.y, 2)
        # set: valid
        anchor.y = 200
        self.assertEqual(anchor.y, 200)
        anchor.y = -200
        self.assertEqual(anchor.y, -200)
        anchor.y = 0
        self.assertEqual(anchor.y, 0)
        anchor.y = 1.1
        self.assertEqual(anchor.y, 1.1)
        anchor.y = -1.1
        self.assertEqual(anchor.y, -1.1)
        # set: invalid
        with self.assertRaises(FontPartsError):
            anchor.y = None
        with self.assertRaises(FontPartsError):
            anchor.y = "ABC"

    # -------
    # Methods
    # -------

    def getAnchor_copy(self):
        anchor, unrequested = self.getAnchor_generic()
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        return anchor, unrequested

    def test_copy(self):
        anchor, unrequested = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertIsNot(anchor, copied)
        self.assertEqual(anchor.name, copied.name)
        self.assertEqual(anchor.color, copied.color)
        self.assertEqual(anchor.identifier, copied.identifier)
        anchor.generateIdentifier()
        copied.generateIdentifier()
        self.assertNotEqual(anchor.identifier, copied.identifier)
        self.assertEqual(anchor.x, copied.x)
        self.assertEqual(anchor.y, copied.y)

    def test_transformBy(self):
        # valid + no origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(anchor.x, -1)
        self.assertEqual(anchor.y, 8)
        # valid + origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
        # invalid
        with self.assertRaises(FontPartsError):
            anchor.transformBy((1, 0, 0, 1, 0, "0"))
        with self.assertRaises(FontPartsError):
            anchor.transformBy("1, 0, 0, 1, 0, 0")
        with self.assertRaises(FontPartsError):
            anchor.transformBy(123)

    def test_moveBy(self):
        # valid + no origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.moveBy((-1, 2))
        self.assertEqual(anchor.x, 0)
        self.assertEqual(anchor.y, 4)
        # invalid
        with self.assertRaises(FontPartsError):
            anchor.transformBy((-1, "2"))
        with self.assertRaises(FontPartsError):
            anchor.transformBy("-1, 2")
        with self.assertRaises(FontPartsError):
            anchor.transformBy(1)

    def test_scaleBy(self):
        # valid + no origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.scaleBy((-2))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, -4)
        anchor, unrequested = self.getAnchor_generic()
        anchor.scaleBy((-2, 3))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, 6)
        # valid + origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
        # invalid
        with self.assertRaises(FontPartsError):
            anchor.scaleBy((-1, "2"))
        with self.assertRaises(FontPartsError):
            anchor.scaleBy("-1, 2")
        with self.assertRaises(FontPartsError):
            anchor.scaleBy((-1, 2, -3))

    def test_rotateBy(self):
        # valid + no origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.rotateBy(45)
        self.assertAlmostEqual(anchor.x, -0.707, places=3)
        self.assertAlmostEqual(anchor.y, 2.121, places=3)
        # valid + origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.rotateBy(45, origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
        # invalid
        with self.assertRaises(FontPartsError):
            anchor.rotateBy("45")
        with self.assertRaises(FontPartsError):
            anchor.rotateBy(361)
        with self.assertRaises(FontPartsError):
            anchor.rotateBy(-361)

    def test_skewBy(self):
        # valid + no origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.skewBy(100)
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertEqual(anchor.y, 2.0)
        anchor, unrequested = self.getAnchor_generic()
        anchor.skewBy((100, 200))
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertAlmostEqual(anchor.y, 2.364, places=3)
        # valid + origin
        anchor, unrequested = self.getAnchor_generic()
        anchor.skewBy(100, origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)
        anchor, unrequested = self.getAnchor_generic()
        anchor.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    def getAnchor_round(self):
        anchor, unrequested = self.getAnchor_generic()
        anchor.x = 1.1
        anchor.y = 2.5
        return anchor, unrequested

    def test_round(self):
        anchor, unrequested = self.getAnchor_round()
        anchor.round()
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    # ----------
    # Deprecated
    # ----------

    def test_draw(self):
        glyph, unrequested = self.getAnchor_index()
        pen = glyph.getPen()
        anchor = glyph.anchors[0]
        with self.assertRaises(RemovedWarning):
            anchor.draw(pen)

    def test_drawPoints(self):
        glyph, unrequested = self.getAnchor_index()
        pen = glyph.getPen()
        anchor = glyph.anchors[0]
        with self.assertRaises(RemovedWarning):
            anchor.drawPoints(pen)

    # ----
    # Hash
    # ----
    def test_hash(self):
        anchor, unrequested = self.getAnchor_generic()
        self.assertEqual(
            isinstance(anchor, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        anchor_one, unrequested = self.getAnchor_generic()
        anchor_two, unrequested = self.getAnchor_generic()
        self.assertEqual(
            anchor_one,
            anchor_one
        )
        self.assertNotEqual(
            anchor_one,
            anchor_two
        )
        a = anchor_one
        self.assertEqual(
            anchor_one,
            a
        )
        self.assertNotEqual(
            anchor_two,
            a
        )