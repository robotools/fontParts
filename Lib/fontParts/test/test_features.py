import unittest
from fontParts.base import FontPartsError


class TestFeatures(unittest.TestCase):

    def getFeatures_generic(self):
        features, unreferenced = self.objectGenerator("features")
        features.text = "# test"
        return features, unreferenced

    # ----
    # Text
    # ----

    def test_text(self):
        features, unreferenced = self.getFeatures_generic()
        # get
        self.assertEqual(
            features.text,
            "# test"
        )
        # set: valid
        features.text = "# foo"
        self.assertEqual(
            features.text,
            "# foo"
        )
        features.text = None
        self.assertIsNone(features.text)
        # set: invalid
        with self.assertRaises(FontPartsError):
            features.text = 123

    # ----
    # Hash
    # ----

    def test_hash(self):
        features_one, unrequested = self.getFeatures_generic()
        features_two, unrequested = self.getFeatures_generic()
        self.assertEqual(
            features_one,
            features_one
        )
        self.assertEqual(
            hash(features_one),
            hash(features_one)
        )
        self.assertNotEqual(
            features_one,
            features_two
        )
        self.assertNotEqual(
            hash(features_one),
            hash(features_two)
        )
