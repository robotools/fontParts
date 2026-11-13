import plistlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from fontParts.test import testEnvironment
from fontParts.fontshell.font import RFont
from fontParts.fontshell.info import RInfo
from fontParts.fontshell.groups import RGroups
from fontParts.fontshell.kerning import RKerning
from fontParts.fontshell.features import RFeatures
from fontParts.fontshell.layer import RLayer
from fontParts.fontshell.glyph import RGlyph
from fontParts.fontshell.contour import RContour
from fontParts.fontshell.segment import RSegment
from fontParts.fontshell.bPoint import RBPoint
from fontParts.fontshell.point import RPoint
from fontParts.fontshell.anchor import RAnchor
from fontParts.fontshell.component import RComponent
from fontParts.fontshell.image import RImage
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.guideline import RGuideline


# defcon does not have prebuilt support for
# selection states, so we simulate selection
# behavior with a small subclasses for testing
# purposes only.


def _get_selected(self):
    if isinstance(self, FSTestSegment):
        for point in self.points:
            if point.selected:
                return True
        return False
    elif isinstance(self, FSTestBPoint):
        point = self._point.naked()
        return point.name == "selected"
    elif isinstance(self, FSTestPoint):
        return self.name == "selected"
    else:
        if not hasattr(self.naked(), "_testSelected"):
            return False
        return self.naked()._testSelected


def _set_selected(self, value):
    if isinstance(self, FSTestSegment):
        for point in self.points:
            point.selected = value
    elif isinstance(self, FSTestBPoint):
        point = self._point.naked()
        if value:
            point.name = "selected"
        else:
            point.name = None
    elif isinstance(self, FSTestPoint):
        if value:
            self.name = "selected"
        else:
            self.name = None
    else:
        self.naked()._testSelected = value


class FSTestPoint(RPoint):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestBPoint(RBPoint):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestSegment(RSegment):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestGuideline(RGuideline):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestImage(RImage):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestAnchor(RAnchor):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestComponent(RComponent):
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestContour(RContour):
    segmentClass = FSTestSegment
    bPointClass = FSTestBPoint
    pointClass = FSTestPoint
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestGlyph(RGlyph):
    contourClass = FSTestContour
    componentClass = FSTestComponent
    anchorClass = FSTestAnchor
    guidelineClass = FSTestGuideline
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestLayer(RLayer):
    glyphClass = FSTestGlyph
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestFont(RFont):
    layerClass = FSTestLayer
    guidelineClass = FSTestGuideline
    _get_selected = _get_selected
    _set_selected = _set_selected


classMapping = dict(
    font=FSTestFont,
    info=RInfo,
    groups=RGroups,
    kerning=RKerning,
    features=RFeatures,
    layer=FSTestLayer,
    glyph=FSTestGlyph,
    contour=FSTestContour,
    segment=FSTestSegment,
    bPoint=FSTestBPoint,
    point=FSTestPoint,
    anchor=FSTestAnchor,
    component=FSTestComponent,
    image=FSTestImage,
    lib=RLib,
    guideline=FSTestGuideline,
)


def fontshellObjectGenerator(cls):
    unrequested = []
    obj = classMapping[cls]()
    return obj, unrequested


class TestRKerning(unittest.TestCase):
    def test_round_scaled_values_are_int(self):
        font = RFont()
        font.kerning.update({("A", "V"): -24, ("V", "A"): 10})
        font.kerning.scaleBy(2)
        font.kerning.round()
        self.assertEqual(dict(font.kerning.items()), {("A", "V"): -48, ("V", "A"): 20})
        for value in font.kerning.values():
            self.assertIs(type(value), int)

    def test_round_integral_float_values(self):
        for multiple in (1, 2, 5, -2):
            with self.subTest(multiple=multiple):
                kerning = RKerning()
                kerning.update(
                    {
                        ("A", "V"): -10.0,
                        ("V", "A"): 10.0,
                        ("T", "o"): 0.0,
                        ("V", "T"): -0.0,
                    }
                )
                kerning.round(multiple)
                self.assertEqual(
                    dict(kerning.items()),
                    {("A", "V"): -10, ("V", "A"): 10, ("T", "o"): 0, ("V", "T"): 0},
                )
                for value in kerning.values():
                    self.assertIs(type(value), int)

    def test_round_preserves_native_kerning(self):
        font = RFont()
        kerning = font.kerning
        nativeKerning = kerning.naked()
        kerning[("A", "V")] = -20.0
        nativeKerning.dirty = False
        observer = Mock()
        nativeKerning.addObserver(
            observer, "changed", nativeKerning.updateNotificationName
        )
        try:
            kerning.round()
            self.assertIs(font.kerning.naked(), nativeKerning)
            self.assertIs(type(nativeKerning[("A", "V")]), int)
            self.assertTrue(nativeKerning.dirty)
            observer.changed.assert_called_once()
            nativeKerning.dirty = False
            observer.reset_mock()
            kerning.round()
            self.assertFalse(nativeKerning.dirty)
            observer.changed.assert_not_called()
        finally:
            nativeKerning.removeObserver(observer, nativeKerning.updateNotificationName)

    def test_round_empty_kerning(self):
        kerning = RKerning()
        kerning.naked().dirty = False
        kerning.round()
        self.assertEqual(dict(kerning.items()), {})
        self.assertFalse(kerning.naked().dirty)

    def test_round_ufo_round_trip(self):
        font = RFont()
        font.kerning.update(
            {
                ("A", "V"): -48.0,
                ("V", "A"): 20.0,
                ("T", "o"): 0.0,
                ("L", "T"): float(-(1 << 63)),
                ("T", "L"): float(1 << 64),
                ("A", "A"): 1e300,
                ("V", "V"): -1e300,
            }
        )
        font.kerning.round()
        expected = dict(font.kerning.items())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.ufo"
            font.save(path)
            with (path / "kerning.plist").open("rb") as stream:
                saved = plistlib.load(stream)
            reopened = RFont(path)
            self.assertEqual(dict(reopened.kerning.items()), expected)
            for left, right in (("A", "V"), ("V", "A"), ("T", "o"), ("L", "T")):
                self.assertIs(type(saved[left][right]), int)
                self.assertIs(type(reopened.kerning[(left, right)]), int)
            for left, right in (("T", "L"), ("A", "A"), ("V", "V")):
                self.assertIs(type(saved[left][right]), float)
                self.assertIs(type(reopened.kerning[(left, right)]), float)


if __name__ == "__main__":
    import sys

    if {"-v", "--verbose"}.intersection(sys.argv):
        verbosity = 2
    else:
        verbosity = 1
    nativeSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRKerning)
    nativeResult = unittest.TextTestRunner(verbosity=verbosity).run(nativeSuite)
    success = testEnvironment(fontshellObjectGenerator, verbosity=verbosity, inApp=True)
    sys.exit(not (success and nativeResult.wasSuccessful()))
