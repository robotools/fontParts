import unittest
import collections
from unittest.mock import patch


class TestKerning(unittest.TestCase):
    def getKerning_generic(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups["public.kern1.X"] = ["A", "B", "C"]
        groups["public.kern2.X"] = ["A", "B", "C"]
        kerning = font.kerning
        kerning.update(
            {
                ("public.kern1.X", "public.kern2.X"): 100,
                ("B", "public.kern2.X"): 101,
                ("public.kern1.X", "B"): 102,
                ("A", "A"): 103,
            }
        )
        return kerning

    def getKerning_font2(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups["public.kern1.X"] = ["A", "B", "C"]
        groups["public.kern2.X"] = ["A", "B", "C"]
        kerning = font.kerning
        kerning.update(
            {
                ("public.kern1.X", "public.kern2.X"): 200,
                ("B", "public.kern2.X"): 201,
                ("public.kern1.X", "B"): 202,
                ("A", "A"): 203,
            }
        )
        return kerning

    # ----
    # repr
    # ----

    def test_reprContents(self):
        kerning = self.getKerning_generic()
        self.assertIn("for font", kerning._reprContents())

    def test_reprContents_no_font(self):
        kerning, _ = self.objectGenerator("kerning")
        kerning[("A", "V")] = -50
        self.assertEqual(len(kerning._reprContents()), 0)

    # -------
    # Parents
    # -------

    def test_get_font(self):
        font, _ = self.objectGenerator("font")
        kerning, _ = self.objectGenerator("kerning")
        kerning._font = lambda: font
        self.assertEqual(kerning.font, font)

    def test_get_font_orphan_font(self):
        kerning, _ = self.objectGenerator("kerning")
        self.assertIsNone(kerning.font)

    def test_set_font(self):
        font, _ = self.objectGenerator("font")
        kerning, _ = self.objectGenerator("kerning")
        kerning.font = font
        self.assertEqual(kerning._font(), font)

    def test_set_font_same_value(self):
        font, _ = self.objectGenerator("font")
        kerning, _ = self.objectGenerator("kerning")
        kerning._font = lambda: font
        kerning.font = font
        self.assertEqual(kerning._font(), font)

    def test_set_font_different_value(self):
        font1, _ = self.objectGenerator("font")
        font2, _ = self.objectGenerator("font")
        kerning, _ = self.objectGenerator("kerning")
        kerning._font = lambda: font1
        with self.assertRaises(AssertionError):
            kerning.font = font2

    def test_set_font_value_none(self):
        kerning, _ = self.objectGenerator("kerning")
        kerning.font = None
        self.assertIsNone(kerning._font)

    # --------------
    # Transformation
    # --------------

    def test_scaleBy_int(self):
        kerning = self.getKerning_generic()
        kerning.scaleBy(2)
        self.assertEqual(kerning[("A", "A")], 206)

    def test_scaleBy_float(self):
        kerning = self.getKerning_generic()
        kerning.scaleBy(1.5)
        self.assertEqual(kerning[("A", "A")], 154.5)

    def test_scaleBy_factor(self):
        kerning = self.getKerning_generic()
        kerning.scaleBy((2, 3.5))
        self.assertEqual(kerning[("A", "A")], 206)

    # -------------
    # Normalization
    # -------------

    def test_round_multiple_1(self):
        kerning = self.getKerning_generic()
        kerning[("A", "V")] = 1.4
        kerning[("V", "A")] = 1.5
        kerning[("L", "T")] = 1.6
        kerning.round(1)
        self.assertEqual(kerning[("A", "V")], 1.0)
        self.assertEqual(kerning[("V", "A")], 2.0)
        self.assertEqual(kerning[("L", "T")], 2.0)

    def test_round_multiple_2(self):
        kerning = self.getKerning_generic()
        kerning[("A", "V")] = 11
        kerning[("V", "A")] = 15
        kerning[("L", "T")] = 16
        kerning.round(2)
        self.assertEqual(kerning[("A", "V")], 12)
        self.assertEqual(kerning[("V", "A")], 16)
        self.assertEqual(kerning[("L", "T")], 16)

    def test_round_negative_values(self):
        kerning = self.getKerning_generic()
        kerning[("A", "V")] = -1.4
        kerning[("V", "A")] = -1.5
        kerning.round(1)
        self.assertEqual(kerning[("A", "V")], -1.0)
        self.assertEqual(kerning[("V", "A")], -1.0)

    def test_round_large_multiple(self):
        kerning = self.getKerning_generic()
        kerning[("A", "V")] = 13
        kerning[("V", "A")] = 17
        kerning.round(5)
        self.assertEqual(kerning[("A", "V")], 15)
        self.assertEqual(kerning[("V", "A")], 15)

    def test_round_multiple_zero(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(ZeroDivisionError):
            kerning.round(0)

    def test_round_multiple_invalid_type(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(TypeError):
            kerning.round(2.5)

    # -------------
    # Interpolation
    # -------------

    def test_interpolate_without_rounding(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        maxKerning = self.getKerning_font2()
        interpolated.interpolate(0.515, minKerning, maxKerning, round=False)
        self.assertEqual(interpolated[("public.kern1.X", "public.kern2.X")], 151.5)

    def test_interpolate_with_rounding(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        maxKerning = self.getKerning_font2()
        interpolated.interpolate(0.515, minKerning, maxKerning, round=True)
        self.assertEqual(interpolated[("public.kern1.X", "public.kern2.X")], 152)

    def test_interpolate_minKerning_invalid_type(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        with self.assertRaises(TypeError):
            interpolated.interpolate(0.515, minKerning, "kerningMax")

    def test_interpolate_maxKerning_invalid_type(self):
        interpolated = self.getKerning_generic()
        maxKerning = self.getKerning_generic()
        with self.assertRaises(TypeError):
            interpolated.interpolate(0.515, "minKerning", maxKerning)

    def test_interpolate_incompatible_keys_raise(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        maxKerning = self.getKerning_font2()
        del maxKerning.font.groups["public.kern1.X"]
        maxKerning.font.groups["public.kern1.DIFFERENT"] = ["A", "B", "C"]
        with self.assertRaises(ValueError):
            interpolated.interpolate(0.515, minKerning, maxKerning, suppressError=False)
            self.assertEqual(len(interpolated), 0)

    def test_interpolate_incompatible_keys_supressError(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        maxKerning = self.getKerning_font2()
        del maxKerning.font.groups["public.kern1.X"]
        maxKerning.font.groups["public.kern1.DIFFERENT"] = ["A", "B", "C"]
        interpolated.interpolate(0.515, minKerning, maxKerning, suppressError=True)
        self.assertEqual(len(interpolated), 0)

    def test_interpolate_incompatible_contents_supressError(self):
        interpolated = self.getKerning_generic()
        minKerning = self.getKerning_generic()
        maxKerning = self.getKerning_font2()
        maxKerning.font.groups["public.kern1.X"] = ["A", "B", "Z"]
        interpolated.interpolate(0.515, minKerning, maxKerning, suppressError=True)
        self.assertEqual(len(interpolated), 0)

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def test_remove(self):
        kerning = self.getKerning_generic()
        with patch.object(type(kerning), "__delitem__") as mock_del:
            kerning.remove([("A", "A")])
            mock_del.assert_called_once()

    def test_asDict_returnIntegers_true(self):
        kerning, _ = self.objectGenerator("kerning")
        kerning[("A", "A")] = 10.5
        result = kerning.asDict(returnIntegers=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result[("A", "A")], 11)

    def test_asDict_returnIntegers_false(self):
        kerning, _ = self.objectGenerator("kerning")
        kerning[("A", "A")] = 10.5
        result = kerning.asDict(returnIntegers=False)
        self.assertIsInstance(result, dict)
        self.assertEqual(result[("A", "A")], 10.5)

    def test_asDict_returnIntegers_empty(self):
        kerning, _ = self.objectGenerator("kerning")
        result = kerning.asDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    # ---
    # len
    # ---

    def test_len_initial(self):
        kerning = self.getKerning_generic()
        self.assertEqual(len(kerning), 4)

    def test_len_clear(self):
        kerning = self.getKerning_generic()
        kerning.clear()
        self.assertEqual(len(kerning), 0)

    # --------
    # contains
    # --------

    def test_contains_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(("A", "A") in kerning, True)

    def test_contains_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(("public.kern1.X", "public.kern2.X") in kerning, True)

    def test_contains_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(("B", "public.kern2.X") in kerning, True)

    def test_contains_missing_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(("H", "H") in kerning, False)

    # ---
    # del
    # ---

    def test_del(self):
        kerning = self.getKerning_generic()
        # Be sure it is here before deleting
        self.assertEqual(("A", "A") in kerning, True)
        # Delete
        del kerning[("A", "A")]
        # Test
        self.assertEqual(("A", "A") in kerning, False)

    # ---
    # get
    # ---

    def test_get_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning[("A", "A")], 103)

    def test_get_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning[("public.kern1.X", "public.kern2.X")], 100)

    def test_get_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning[("B", "public.kern2.X")], 101)

    def test_get_group_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning[("public.kern1.X", "B")], 102)

    def test_get_fallback_default(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.get(("F", "F")), None)

    def test_get_fallback_default_user(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.get(("F", "F"), None), None)
        self.assertEqual(kerning.get(("F", "F"), 0), 0)

    # ---
    # set
    # ---

    def test_set_glyph_glyph(self):
        kerning = self.getKerning_generic()
        kerning[("A", "A")] = 1
        self.assertEqual(kerning[("A", "A")], 1)

    def test_set_group_group(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "public.kern2.X")] = 2
        self.assertEqual(kerning[("public.kern1.X", "public.kern2.X")], 2)

    def test_set_glyph_group(self):
        kerning = self.getKerning_generic()
        kerning[("B", "public.kern2.X")] = 3
        self.assertEqual(kerning[("B", "public.kern2.X")], 3)

    def test_set_group_glyph(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "B")] = 4
        self.assertEqual(kerning[("public.kern1.X", "B")], 4)

    # ----
    # Find
    # ----

    def test_find_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.find(("A", "A")), 103)

    def test_find_glyph_glyph_none(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.find(("D", "D")), None)

    def test_find_group_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.find(("A", "B")), 102)

    def test_find_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.find(("B", "B")), 101)

    def test_find_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(kerning.find(("C", "C")), 100)

    # ----
    # Hash
    # ----

    def test_hash(self):
        kerning = self.getKerning_generic()
        self.assertEqual(isinstance(kerning, collections.abc.Hashable), True)

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        kerning_one = self.getKerning_generic()
        self.assertEqual(kerning_one, kerning_one)

    def test_object_not_equal_other(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        self.assertNotEqual(kerning_one, kerning_two)

    def test_object_equal_self_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        a = kerning_one
        self.assertEqual(kerning_one, a)

    def test_object_not_equal_other_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        a = kerning_one
        self.assertNotEqual(kerning_two, a)
