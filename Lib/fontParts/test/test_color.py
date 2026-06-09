import unittest
from fontParts.base.color import Color


class TestColor(unittest.TestCase):
    def test_new_tuple(self):
        bounds = Color((0.1, 0.2, 0.3, 1.0))
        self.assertEqual(bounds.r, 0.1)
        self.assertEqual(bounds.g, 0.2)
        self.assertEqual(bounds.b, 0.3)
        self.assertEqual(bounds.a, 1.0)

    def test_new_args(self):
        bounds = Color((0.1, 0.2, 0.3, 1.0))
        self.assertEqual(bounds.r, 0.1)
        self.assertEqual(bounds.g, 0.2)
        self.assertEqual(bounds.b, 0.3)
        self.assertEqual(bounds.a, 1.0)

    def test_new_kwargs(self):
        bounds = Color(r=0.1, g=0.2, b=0.3, a=1.0)
        self.assertEqual(bounds.r, 0.1)
        self.assertEqual(bounds.g, 0.2)
        self.assertEqual(bounds.b, 0.3)
        self.assertEqual(bounds.a, 1.0)
