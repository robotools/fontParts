import unittest
import collections
from fontParts.base import FontPartsError


class TestGroups(unittest.TestCase):

    def getGroups_generic(self):
        groups, _unrequested = self.objectGenerator("groups")
        groups.update({
            "group 1" : ["A", "B", "C"],
            "group 2" : ["x", "y", "z"],
            "group 3" : [],
            "group 4" : ["A"]
        })
        return groups

    # ---
    # len
    # ---

    def test_len_initial(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            len(groups),
            4
        )
    def test_len_clear(self):
        groups = self.getGroups_generic()
        groups.clear()
        self.assertEqual(
            len(groups),
            0
        )

    # ---------
    # Searching
    # ---------

    def test_find_found(self):
        groups = self.getGroups_generic()
        found = groups.findGlyph("A")
        found.sort()
        self.assertEqual(
            found,
            [u"group 1", u"group 4"]
        )
    def test_find_not_found(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            groups.findGlyph("five"),
            []
        )
    def test_find_invalid_key(self):
        groups = self.getGroups_generic()
        with self.assertRaises(FontPartsError):
            groups.findGlyph(5)

    # ----
    # Hash
    # ----
    def test_hash(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            isinstance(groups, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        groups_one = self.getGroups_generic()
        self.assertEqual(
            groups_one,
            groups_one
        )
    def test_object_not_equal_other(self):
        groups_one = self.getGroups_generic()
        groups_two = self.getGroups_generic()
        self.assertNotEqual(
            groups_one,
            groups_two
        )
    def test_object_equal_self_variable_assignment(self):
        groups_one = self.getGroups_generic()
        a = groups_one
        self.assertEqual(
            groups_one,
            a
        )
    def test_object_not_equal_other_variable_assignment(self):
        groups_one = self.getGroups_generic()
        groups_two = self.getGroups_generic()
        a = groups_one
        self.assertNotEqual(
            groups_two,
            a
        )