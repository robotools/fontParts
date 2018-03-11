import unittest
import collections
from fontParts.base import FontPartsError


class TestKerning(unittest.TestCase):

    def getKerning_generic(self):
        kerning, _unrequested = self.objectGenerator("kerning")
        kerning.update({
            ("public.kern1.X", "public.kern2.X") : 100,
            ("B", "public.kern2.X") : 101,
            ("public.kern1.X", "B") : 102,
            ("A", "A") : 103,
        })
        return kerning

    # ---
    # len
    # ---

    def test_len(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            len(kerning),
            4
        )
        kerning.clear()
        self.assertEqual(
            len(kerning),
            0
        )

    # --------
    # contains
    # --------

    def test_contains(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ('A','A') in kerning,
            True
        )
        self.assertEqual(
            ("public.kern1.X", "public.kern2.X") in kerning,
            True
        )
        self.assertEqual(
            ("B", "public.kern2.X") in kerning,
            True
        )
        self.assertEqual(
            ("H", "H") in kerning,
            False
        )

    # ---
    # del
    # ---

    def test_del(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ('A','A') in kerning,
            True
        )
        del kerning[('A','A')]
        self.assertEqual(
            ('A','A') in kerning,
            False
        )

    # ---
    # get
    # ---

    def test_get(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[('A','A')],
            103
        )
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            100
        )
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            101
        )
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            102
        )

    # ---
    # set
    # ---

    def test_set(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[('A','A')],
            103
        )
        kerning[('A','A')] = 1
        self.assertEqual(
            kerning[('A','A')],
            1
        )
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            100
        )
        kerning[("public.kern1.X", "public.kern2.X")] = 2
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            2
        )
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            101
        )
        kerning[("B", "public.kern2.X")] = 3
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            3
        )
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            102
        )
        kerning[("public.kern1.X", "B")] = 4
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            4
        )

    # -----
    # clear
    # -----

    def test_clear(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            len(kerning),
            4
        )
        kerning.clear()
        self.assertEqual(
            len(kerning),
            0
        )

    # ----
    # Hash
    # ----
    def test_hash(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            isinstance(kerning, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        self.assertEqual(
            kerning_one,
            kerning_one
        )
        self.assertNotEqual(
            kerning_one,
            kerning_two
        )
        a = kerning_one
        self.assertEqual(
            kerning_one,
            a
        )
        self.assertNotEqual(
            kerning_two,
            a
        )