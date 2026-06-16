import unittest
from fontParts.base.bounds import Bounds


class TestBounds(unittest.TestCase):
    def test_new_tuple(self):
        bounds = Bounds((1, 2, 3, 4))
        self.assertEqual(bounds.xMin, 1.0)
        self.assertEqual(bounds.yMin, 2.0)
        self.assertEqual(bounds.xMax, 3.0)
        self.assertEqual(bounds.yMax, 4.0)

    def test_new_args(self):
        bounds = Bounds(1, 2, 3, 4)
        self.assertEqual(bounds.xMin, 1.0)
        self.assertEqual(bounds.yMin, 2.0)
        self.assertEqual(bounds.xMax, 3.0)
        self.assertEqual(bounds.yMax, 4.0)

    def test_new_kwargs(self):
        bounds = Bounds(xMin=1, yMin=2, xMax=3, yMax=4)
        self.assertEqual(bounds.xMin, 1.0)
        self.assertEqual(bounds.yMin, 2.0)
        self.assertEqual(bounds.xMax, 3.0)
        self.assertEqual(bounds.yMax, 4.0)

    def test_width(self):
        bounds = Bounds(1, 2, 3, 4)
        self.assertEqual(bounds.width, 2.0)

    def test_height(self):
        bounds = Bounds(1, 2, 3, 4)
        self.assertEqual(bounds.height, 2.0)

    def test_xCenter(self):
        bounds = Bounds(1, 2, 3, 4)
        self.assertEqual(bounds.xCenter, 2.0)

    def test_yCenter(self):
        bounds = Bounds(1, 2, 3, 4)
        self.assertEqual(bounds.yCenter, 3.0)
