import unittest
from fontParts.base.color import Color


class TestColor(unittest.TestCase):
    def test_new_tuple(self):
        color = Color((0.1, 0.2, 0.3, 1.0))
        self.assertEqual(color.r, 0.1)
        self.assertEqual(color.g, 0.2)
        self.assertEqual(color.b, 0.3)
        self.assertEqual(color.a, 1.0)

    def test_new_args(self):
        color = Color((0.1, 0.2, 0.3, 1.0))
        self.assertEqual(color.r, 0.1)
        self.assertEqual(color.g, 0.2)
        self.assertEqual(color.b, 0.3)
        self.assertEqual(color.a, 1.0)

    def test_new_kwargs(self):
        color = Color(r=0.1, g=0.2, b=0.3, a=1.0)
        self.assertEqual(color.r, 0.1)
        self.assertEqual(color.g, 0.2)
        self.assertEqual(color.b, 0.3)
        self.assertEqual(color.a, 1.0)
