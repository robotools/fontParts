import unittest
import collections
from fontParts.base import FontPartsError


class TestFeatures(unittest.TestCase):

    def getFeatures_generic(self):
        features, _unrequested = self.objectGenerator("features")
        features.text = "# test"
        return features

    # ----
    # Text
    # ----

    def test_text_get(self):
        features = self.getFeatures_generic()
        self.assertEqual(
            features.text,
            "# test"
        )
    def test_text_valid_set(self):
        features = self.getFeatures_generic()
        features.text = "# foo"
        self.assertEqual(
            features.text,
            "# foo"
        )
    def test_text_set_none(self):
        features = self.getFeatures_generic()
        features.text = None
        self.assertIsNone(features.text)
    def test_text_invalid_set(self):
        features = self.getFeatures_generic()
        with self.assertRaises(FontPartsError):
            features.text = 123

    # ----
    # Hash
    # ----
    def test_hash(self):
        features = self.getFeatures_generic()
        self.assertEqual(
            isinstance(features, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        features_one = self.getFeatures_generic()
        self.assertEqual(
            features_one,
            features_one
        )
    def test_object_not_equal_other(self):
        features_one = self.getFeatures_generic()
        features_two = self.getFeatures_generic()
        self.assertNotEqual(
            features_one,
            features_two
        )
    def test_object_equal_self_variable_assignment(self):
        features_one = self.getFeatures_generic()
        a = features_one
        a.text += "# testing"
        self.assertEqual(
            features_one,
            a
        )
    def test_object_not_equal_self_variable_assignment(self):
        features_one = self.getFeatures_generic()
        features_two = self.getFeatures_generic()
        a = features_one
        self.assertNotEqual(
            features_two,
            a
        )