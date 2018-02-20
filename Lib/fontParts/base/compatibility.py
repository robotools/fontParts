from fontParts.base.base import dynamicProperty

# ----
# Base
# ----

import weakref

class BaseCompatibilityReporter(object):

    objectName = "Base"

    def __init__(self, obj1, obj2):
        self._object1 = obj1
        self._object2 = obj2

    # status

    fatal = False
    warning = False

    def _get_title(self):
        title = "{object1Name} + {object2Name}".format(
            object1Name=self.object1Name,
            object2Name=self.object2Name
        )
        if self.fatal:
            return self.formatFatalString(title)
        elif self.warning:
            return self.formatWarningString(title)
        else:
            return self.formatOKString(title)

    title = dynamicProperty("title")

    # objects

    object1 = dynamicProperty("object1")
    object1Name = dynamicProperty("object1Name")

    def _get_object1(self):
        return self._object1

    def _get_object1Name(self):
        return self._getObjectName(self._object1)

    object2 = dynamicProperty("object2")
    object2Name = dynamicProperty("object2Name")

    def _get_object2(self):
        return self._object2

    def _get_object2Name(self):
        return self._getObjectName(self._object2)

    def _getObjectName(self, obj):
        if hasattr(obj, "name") and obj.name is not None:
            return "\"%s\"" % obj.name
        elif hasattr(obj, "identifier") and obj.identifier is not None:
            return "\"%s\"" % obj.identifier
        elif hasattr(obj, "index"):
            return "[%s]" % obj.index
        else:
            return "<%s>" % id(obj)

    # Report

    def __repr__(self):
        return self.report()

    def report(self, warnings=False):
        raise NotImplementedError

    def formatFatalString(self, text):
        return "[Fatal] {objectName}: ".format(objectName=self.objectName) + text

    def formatWarningString(self, text):
        return "[Warning] {objectName}: ".format(objectName=self.objectName) + text

    def formatOKString(self, text):
        return "[OK] {objectName}: ".format(objectName=self.objectName) + text

    def reportSubObjects(self, reporters, showOK=True, showWarnings=True):
        report = []
        for reporter in reporters:
            if showOK or reporter.fatal or (showWarnings and reporter.warning):
                report.append(repr(reporter))
        return report

    def reportCountDifference(self, subObjectName, object1Name, object1Count, object2Name, object2Count):
        text = "{object1Name} contains {object1Count} {subObjectName} | {object2Name} contains {object2Count} {subObjectName}".format(
            subObjectName=subObjectName,
            object1Name=object1Name,
            object1Count=object1Count,
            object2Name=object2Name,
            object2Count=object2Count
        )
        return text


# ----
# Font
# ----

class FontCompatibilityReporter(BaseCompatibilityReporter):

    pass


# -----
# Layer
# -----

class LayerCompatibilityReporter(BaseCompatibilityReporter):

    pass


# -----
# Glyph
# -----

class GlyphCompatibilityReporter(BaseCompatibilityReporter):

    objectName = "Glyph"

    def __init__(self, glyph1, glyph2):
        super(GlyphCompatibilityReporter, self).__init__(glyph1, glyph2)
        self.contourCountDifference = False
        self.contours = []

    glyph1 = dynamicProperty("object1")
    glyph1Name = dynamicProperty("object1Name")
    glyph2 = dynamicProperty("object2")
    glyph2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        glyph1 = self.glyph1
        glyph2 = self.glyph2
        report = []
        if self.contourCountDifference:
            text = self.reportCountDifference(
                subObjectName="contours",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2)
            )
            report.append(self.formatFatalString(text))
        report += self.reportSubObjects(self.contours, showOK=showOK, showWarnings=showWarnings)
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -------
# Contour
# -------

class ContourCompatibilityReporter(BaseCompatibilityReporter):

    objectName = "Contour"

    def __init__(self, contour1, contour2):
        super(ContourCompatibilityReporter, self).__init__(contour1, contour2)
        self.openDifference = False
        self.directionDifference = False
        self.segmentCountDifference = False
        self.segments = []

    contour1 = dynamicProperty("object1")
    contour1Name = dynamicProperty("object1Name")
    contour2 = dynamicProperty("object2")
    contour2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        contour1 = self.contour1
        contour2 = self.contour2
        report = []
        if self.segmentCountDifference:
            text = self.reportCountDifference(
                subObjectName="segments",
                object1Name=self.contour1Name,
                object1Count=len(contour1),
                object2Name=self.contour2Name,
                object2Count=len(contour2)
            )
            report.append(self.formatFatalString(text))
        if self.openDifference:
            state1 = state2 = "closed"
            if contour1.open:
                state1 = "open"
            if contour2.open:
                state2 = "open"
            text = "{contour1Name} is {state1} | {contour2Name} is {state2}".format(
                contour1Name=self.contour1Name,
                state1=state1,
                contour2Name=self.contour2Name,
                state2=state2
            )
            report.append(self.formatFatalString(text))
        if self.directionDifference:
            state1 = state2 = "counter-clockwise"
            if contour1.clockwise:
                state1 = "clockwise"
            if contour2.clockwise:
                state2 = "clockwise"
            text = "{contour1Name} is {state1} | {contour2Name} is {state2}".format(
                contour1Name=self.contour1Name,
                state1=state1,
                contour2Name=self.contour2Name,
                state2=state2
            )
            report.append(self.formatFatalString(text))
        report += self.reportSubObjects(self.segments, showOK=showOK, showWarnings=showWarnings)
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -------
# Segment
# -------

class SegmentCompatibilityReporter(BaseCompatibilityReporter):

    objectName = "Segment"

    def __init__(self, contour1, contour2):
        super(SegmentCompatibilityReporter, self).__init__(contour1, contour2)
        self.typeDifference = False

    segment1 = dynamicProperty("object1")
    segment1Name = dynamicProperty("object1Name")
    segment2 = dynamicProperty("object2")
    segment2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        segment1 = self.segment1
        segment2 = self.segment2
        report = []
        if self.typeDifference:
            type1 = segment1.type
            type2 = segment2.type
            text = "{segment1Name} is {type1} | {segment2Name} is {type2}".format(
                segment1Name=self.segment1Name,
                type1=type1,
                segment2Name=self.segment2Name,
                type2=type2
            )
            report.append(self.formatFatalString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)

# ---------
# Component
# ---------

class ComponentCompatibilityReporter(BaseCompatibilityReporter):

    pass


# ------
# Anchor
# ------

class AnchorCompatibilityReporter(BaseCompatibilityReporter):

    pass


# ---------
# Guideline
# ---------

class GuidelineCompatibilityReporter(BaseCompatibilityReporter):

    pass
