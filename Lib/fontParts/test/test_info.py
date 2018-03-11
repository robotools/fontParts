import unittest
import collections
from fontParts.base import FontPartsError


class TestInfo(unittest.TestCase):

    def getInfo_generic(self):
        info, _ = self.objectGenerator("info")
        info.unitsPerEm = 1000
        return info

    # ----------
    # Dimensions
    # ----------

    def test_get_unitsPerEm(self):
        info = self.getInfo_generic()
        self.assertEqual(
            info.unitsPerEm,
            1000
        )
    def test_set_valid_unitsPerEm_int(self):
        info = self.getInfo_generic()
        info.unitsPerEm = 2000
        self.assertEqual(
            info.unitsPerEm,
            2000
        )
    def test_set_valid_unitsPerEm_float(self):
        info = self.getInfo_generic()
        info.unitsPerEm = 2000.1
        self.assertEqual(
            info.unitsPerEm,
            2000.1
        )
    def test_set_invalid_unitsPerEm_negative(self):
        info = self.getInfo_generic()
        with self.assertRaises(FontPartsError):
            info.unitsPerEm = -1000
    def test_set_invalid_unitsPerEm_string(self):
        info = self.getInfo_generic()
        with self.assertRaises(FontPartsError):
            info.unitsPerEm = "abc"

    # ----
    # Hash
    # ----
    def test_hash(self):
        info = self.getInfo_generic()
        self.assertEqual(
            isinstance(info, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        info_one = self.getInfo_generic()
        self.assertEqual(
            info_one,
            info_one
        )
    def test_object_not_equal_other(self):
        info_one = self.getInfo_generic()
        info_two = self.getInfo_generic()
        self.assertNotEqual(
            info_one,
            info_two
        )
    def test_object_equal_self_variable_assignment(self):
        info_one = self.getInfo_generic()
        a = info_one
        self.assertEqual(
            info_one,
            a
        )
    def test_object_not_equal_other_variable_assignment(self):
        info_one = self.getInfo_generic()
        info_two = self.getInfo_generic()
        a = info_one
        self.assertNotEqual(
            info_two,
            a
        )