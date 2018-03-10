from fontParts.test import testEnvironment
from fontParts.nonelab.font import RFont
from fontParts.nonelab.info import RInfo
from fontParts.nonelab.groups import RGroups
from fontParts.nonelab.kerning import RKerning
from fontParts.nonelab.features import RFeatures
from fontParts.nonelab.layer import RLayer
from fontParts.nonelab.glyph import RGlyph
from fontParts.nonelab.contour import RContour
from fontParts.nonelab.segment import RSegment
from fontParts.nonelab.bPoint import RBPoint
from fontParts.nonelab.point import RPoint
from fontParts.nonelab.anchor import RAnchor
from fontParts.nonelab.component import RComponent
from fontParts.nonelab.image import RImage
from fontParts.nonelab.lib import RLib
from fontParts.nonelab.guideline import RGuideline



# defcon does not have prebuilt support for
# selection states, so we simulate selection
# behavior with a small subclasses for testing
# purposes only.

def _get_selected(self):
    if not hasattr(self.naked(), "_testSelected"):
        return False
    return self.naked()._testSelected

def _set_selected(self, value):
    self.naked()._testSelected = value


class NLTestGuideline(RGuideline):

    _get_selected = _get_selected
    _set_selected = _set_selected


class NLTestAnchor(RAnchor):

    _get_selected = _get_selected
    _set_selected = _set_selected


class NLTestComponent(RComponent):

    _get_selected = _get_selected
    _set_selected = _set_selected


class NLTestContour(RContour):

    _get_selected = _get_selected
    _set_selected = _set_selected


class NLTestGlyph(RGlyph):

    contourClass = NLTestContour
    componentClass = NLTestComponent
    anchorClass = NLTestAnchor
    guidelineClass = NLTestGuideline
    _get_selected = _get_selected
    _set_selected = _set_selected


classMapping = dict(
    font=RFont,
    info=RInfo,
    groups=RGroups,
    kerning=RKerning,
    features=RFeatures,
    layer=RLayer,
    glyph=NLTestGlyph,
    contour=NLTestContour,
    segment=RSegment,
    bPoint=RBPoint,
    point=RPoint,
    anchor=NLTestAnchor,
    component=NLTestComponent,
    image=RImage,
    lib=RLib,
    guideline=NLTestGuideline,
)

def noneLabObjectGenerator(cls):
    unrequested = []
    obj = classMapping[cls]()
    return obj, []

if __name__ == "__main__":
    import sys
    if {"-v", "--verbose"}.intersection(sys.argv):
        verbosity = 2
    else:
        verbosity = 1
    testEnvironment(noneLabObjectGenerator, verbosity=verbosity)
