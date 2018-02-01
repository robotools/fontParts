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

classMapping = dict(
    font=RFont,
    info=RInfo,
    groups=RGroups,
    kerning=RKerning,
    features=RFeatures,
    layer=RLayer,
    glyph=RGlyph,
    contour=RContour,
    segment=RSegment,
    bPoint=RBPoint,
    point=RPoint,
    anchor=RAnchor,
    component=RComponent,
    image=RImage,
    lib=RLib,
    guideline=RGuideline,
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
