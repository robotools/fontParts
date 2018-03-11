import unittest
import collections
from fontParts.base import FontPartsError


class TestKerning(unittest.TestCase):

    def getKerning_generic(self):
        kerning, _ = self.objectGenerator("kerning")
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

    def test_len_initial(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            len(kerning),
            4
        )
    def test_len_clear(self):
        kerning = self.getKerning_generic()
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
        # Be sure it is here before deleting
        self.assertEqual(
            ('A','A') in kerning,
            True
        )
        # Delete
        del kerning[('A','A')]
        # Test
        self.assertEqual(
            ('A','A') in kerning,
            False
        )

    # ---
    # get
    # ---

    def test_get_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[('A','A')],
            103
        )
    def test_get_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            100
        )
    def test_get_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            101
        )
    def test_get_group_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            102
        )

    # ---
    # set
    # ---

    def test_set_glyph_glyph(self):
        kerning = self.getKerning_generic()
        kerning[('A','A')] = 1
        self.assertEqual(
            kerning[('A','A')],
            1
        )
    def test_set_group_group(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "public.kern2.X")] = 2
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            2
        )
    def test_set_glyph_group(self):
        kerning = self.getKerning_generic()
        kerning[("B", "public.kern2.X")] = 3
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            3
        )
    def test_set_group_glyph(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "B")] = 4
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            4
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

    def test_object_equal_self(self):
        kerning_one = self.getKerning_generic()
        self.assertEqual(
            kerning_one,
            kerning_one
        )
    def test_object_not_equal_other(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        self.assertNotEqual(
            kerning_one,
            kerning_two
        )
    def test_object_equal_self_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        a = kerning_one
        self.assertEqual(
            kerning_one,
            a
        )
    def test_object_not_equal_other_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        a = kerning_one
        self.assertNotEqual(
            kerning_two,
            a
        )