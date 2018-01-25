from fontTools.misc.py23 import *
import warnings

"""
A collection of deprecated roboFab methods.
Those methods are added to keep scripts and code compatible.
"""


# ========
# = base =
# ========

class DeprecatedBase(object):

    def setParent(self, parent):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.setParent()'" % objName, DeprecationWarning)

    def update(self):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.update': use %s.changed()" % (objName, objName), DeprecationWarning)
        self.changed()

    def setChanged(self):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.setChanged': use %s.changed()" % (objName, objName), DeprecationWarning)
        self.changed()


# ==================
# = transformation =
# ==================

class DeprecatedTransformation(object):

    def move(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.move()': use %s.moveBy()" % (objName, objName), DeprecationWarning)
        self.moveBy(*args, **kwargs)

    def translate(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.translate()': use %s.moveBy()" % (objName, objName), DeprecationWarning)
        self.moveBy(*args, **kwargs)

    def scale(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.scale()': use %s.scaleBy()" % (objName, objName), DeprecationWarning)
        self.scaleBy(*args, **kwargs)

    def rotate(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.rotate()': use %s.rotateBy()" % (objName, objName), DeprecationWarning)
        self.rotateBy(*args, **kwargs)

    def transform(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.transform()': use %s.transformBy()" % (objName, objName), DeprecationWarning)
        self.transformBy(*args, **kwargs)

    def skew(self, *args, **kwargs):
        objName = self.__class__.__name__.replace("Deprecated", "")
        warnings.warn("'%s.skew()': use %s.skewBy()" % (objName, objName), DeprecationWarning)
        self.skewBy(*args, **kwargs)


# ==========
# = Point =
# ==========

class DeprecatedPoint(DeprecatedBase, DeprecatedTransformation):

    def select(self, state=True):
        warnings.warn("'Point.select'", DeprecationWarning)


# ==========
# = Anchor =
# ==========

class DeprecatedAnchor(DeprecatedBase, DeprecatedTransformation):

    def _get_position(self):
        warnings.warn("'Anchor.position': use Anchor.x, Anchor.y", DeprecationWarning)
        return self.x, self.y

    def _set_position(self, position):
        warnings.warn("'Anchor.position': use Anchor.x, Anchor.y", DeprecationWarning)
        x, y = position
        self.x = x
        self.y = y

    position = property(_get_position, _set_position, doc="Deprecated Anchor.position")

    def draw(self, pen):
        warnings.warn("'Anchor.draw': UFO3 is not drawing anchors into pens", DeprecationWarning)

    def drawPoints(self, pen):
        warnings.warn("'Anchor.drawPoints': UFO3 is not drawing anchors into point pens", DeprecationWarning)


# =============
# = Component =
# =============

class DeprecatedComponent(DeprecatedBase, DeprecatedTransformation):

    def _get_box(self):
        warnings.warn("'Component.box': use Component.bounds", DeprecationWarning)
        return self.bounds

    box = property(_get_box, doc="Deprecated Component.box")


# ===========
# = Segment =
# ===========

class DeprecatedSegment(DeprecatedBase, DeprecatedTransformation):

    def insertPoint(self, point):
        warnings.warn("Segment.insertPoint()", DeprecationWarning)

    def removePoint(self, point):
        warnings.warn("Segment.removePoint()", DeprecationWarning)


# ===========
# = Contour =
# ===========

class DeprecatedContour(DeprecatedBase, DeprecatedTransformation):

    def _get_box(self):
        warnings.warn("'Contour.box': use Contour.bounds", DeprecationWarning)
        return self.bounds

    box = property(_get_box, doc="Deprecated Contour.box")

    def reverseContour(self):
        warnings.warn("'Contour.reverseContour()': use 'Contour.reverse()'", DeprecationWarning)
        self.reverse()


# =========
# = Glyph =
# =========

class DeprecatedGlyph(DeprecatedBase, DeprecatedTransformation):

    def _get_mark(self):
        warnings.warn("'Glyph.mark': use Glyph.markColor", DeprecationWarning)
        return self.markColor

    def _set_mark(self, value):
        warnings.warn("'Glyph.mark': use Glyph.markColor", DeprecationWarning)
        self.markColor = value

    mark = property(_get_mark, _set_mark, doc="Deprecated Mark color")

    def _get_box(self):
        warnings.warn("'Glyph.box': use Glyph.bounds", DeprecationWarning)
        return self.bounds

    box = property(_get_box, doc="Deprecated Glyph.box")

    def getAnchors(self):
        warnings.warn("'Glyph.getAnchors()': use Glyph.anchors", DeprecationWarning)
        return self.anchors

    def getComponents(self):
        warnings.warn("'Glyph.getComponents()': use Glyph.components", DeprecationWarning)
        return self.components

    def center(self, padding=None):
        warnings.warn("'Glyph.center()'", DeprecationWarning)

    def clearVGuides(self):
        warnings.warn("'Glyph.clearVGuides()': use Glyph.clearGuidelines()", DeprecationWarning)

    def clearHGuides(self):
        warnings.warn("'Glyph.clearHGuides()': use Glyph.clearGuidelines()", DeprecationWarning)


# =======
# = Lib =
# =======

class DeprecatedLib(DeprecatedBase):

    pass


# ==========
# = Groups =
# ==========

class DeprecatedGroups(DeprecatedBase):

    pass


# ===========
# = Kerning =
# ===========

class DeprecatedKerning(DeprecatedTransformation):

    def setParent(self, parent):
        warnings.warn("'Kerning.setParent()'", DeprecationWarning)

    def setChanged(self):
        warnings.warn("'Kerning.setChanged': use Kerning.changed()", DeprecationWarning)
        self.changed()

    def swapNames(self, swaptable):
        warnings.warn("Kerning.swapNames()", DeprecationWarning)

    def getLeft(self, glyphName):
        warnings.warn("Kerning.getLeft()", DeprecationWarning)

    def getRight(self, glyphName):
        warnings.warn("Kerning.getRight()", DeprecationWarning)

    def getExtremes(self):
        warnings.warn("Kerning.getExtremes()", DeprecationWarning)

    def add(self, value):
        warnings.warn("Kerning.add()", DeprecationWarning)

    def minimize(self, minimum=10):
        warnings.warn("Kerning.minimize()", DeprecationWarning)

    def importAFM(self, path, clearExisting=True):
        warnings.warn("Kerning.importAFM()", DeprecationWarning)

    def getAverage(self):
        warnings.warn("Kerning.getAverage()", DeprecationWarning)

    def combine(self, kerningDicts, overwriteExisting=True):
        warnings.warn("Kerning.combine()", DeprecationWarning)

    def eliminate(self, leftGlyphsToEliminate=None, rightGlyphsToEliminate=None, analyzeOnly=False):
        warnings.warn("Kerning.eliminate()", DeprecationWarning)

    def occurrenceCount(self, glyphsToCount):
        warnings.warn("Kerning.occurrenceCount()", DeprecationWarning)

    def implodeClasses(self, leftClassDict=None, rightClassDict=None, analyzeOnly=False):
        warnings.warn("Kerning.implodeClasses()", DeprecationWarning)

    def explodeClasses(self, leftClassDict=None, rightClassDict=None, analyzeOnly=False):
        warnings.warn("Kerning.explodeClasses()", DeprecationWarning)


# ========
# = Info =
# ========

class DeprecatedInfo(DeprecatedBase):

    pass


# ============
# = Features =
# ============

class DeprecatedFeatures(DeprecatedBase):

    def round(self):
        warnings.warn("'Feature.round()'", DeprecationWarning)


# ========
# = Font =
# ========

class DeprecatedFont(DeprecatedBase):

    def getParent(self):
        warnings.warn("'Font.getParent()'", DeprecationWarning)

    def _get_fileName(self):
        warnings.warn("'Font.fileName': use os.path.basename(Font.path)", DeprecationWarning)
        return self.path

    fileName = property(_get_fileName, doc="Deprecated Font.fileName")

    def generateGlyph(self, *args, **kwargs):
        warnings.warn("'Font.generateGlyph()'", DeprecationWarning)

    def compileGlyph(self, *args, **kwargs):
        warnings.warn("'Font.compileGlyph()'", DeprecationWarning)

    def getWidth(self, glyphName):
        warnings.warn("'Font.getWidth(): use Font[glyphName].width'", DeprecationWarning)
        return self[glyphName].width

    def getGlyph(self, glyphName):
        warnings.warn("'Font.getGlyph(): use Font[glyphName]'", DeprecationWarning)
        return self[glyphName]

    def getGlyphNameToFileNameFunc(self):
        warnings.warn("'Font.getGlyphNameToFileNameFunc()'", DeprecationWarning)
