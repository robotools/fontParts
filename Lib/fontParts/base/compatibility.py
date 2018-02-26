from fontParts.base.base import dynamicProperty

# ----
# Base
# ----

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
        self.componentCountDifference = False
        self.guidelineCountDifference = False
        self.anchorCountDifference = False
        self.contours = []
        self.components = []
        self.guidelines = []
        self.anchors = []

    glyph1 = dynamicProperty("object1")
    glyph1Name = dynamicProperty("object1Name")
    glyph2 = dynamicProperty("object2")
    glyph2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        glyph1 = self.glyph1
        glyph2 = self.glyph2
        report = []

        # Contour test
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

        # Component test
        if self.componentCountDifference:
            text = self.reportCountDifference(
                subObjectName="components",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.components),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.components)
            )
            report.append(self.formatFatalString(text))
        report += self.reportSubObjects(self.components, showOK=showOK, showWarnings=showWarnings)
        
        # Anchor test
        if self.anchorCountDifference:
            text = self.reportCountDifference(
                subObjectName="anchors",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.anchors),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.anchors)
            )
            report.append(self.formatWarningString(text))
        report += self.reportSubObjects(self.anchors, showOK=showOK, showWarnings=showWarnings)
        
        # Guideline test
        if self.guidelineCountDifference:
            text = self.reportCountDifference(
                subObjectName="guidelines",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.guidelines),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.guidelines)
            )
            report.append(self.formatWarningString(text))
        report += self.reportSubObjects(self.guidelines, showOK=showOK, showWarnings=showWarnings)
        
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

    objectName = "Component"

    def __init__(self, component1, component2):
        super(ComponentCompatibilityReporter, self).__init__(component1, component2)
        self.baseDifference = False

    component1 = dynamicProperty("object1")
    component1Name = dynamicProperty("object1Name")
    component2 = dynamicProperty("object2")
    component2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        component1 = self.component1
        component2 = self.component2
        report = []
        if self.baseDifference:
            name1 = component1.baseName
            name2 = component2.baseName
            text = "{component1Name} has base glyph {name1} | {component2Name} has base glyph {name2}".format(
                component1Name=self.component1Name,
                name1=name1,
                component2Name=self.component2Name,
                name2=name2
            )
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)

# ------
# Anchor
# ------

class AnchorCompatibilityReporter(BaseCompatibilityReporter):

    objectName = "Anchor"

    def __init__(self, anchor1, anchor2):
        super(AnchorCompatibilityReporter, self).__init__(anchor1, anchor2)
        self.nameDifference = False

    anchor1 = dynamicProperty("object1")
    anchor1Name = dynamicProperty("object1Name")
    anchor2 = dynamicProperty("object2")
    anchor2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        anchor1 = self.anchor1
        anchor2 = self.anchor2
        report = []
        if self.nameDifference:
            name1 = anchor1.name
            name2 = anchor2.name
            text = "{anchor1Name} has name {name1} | {anchor2Name} has name {name2}".format(
                anchor1Name=self.anchor1Name,
                name1=name1,
                anchor2Name=self.anchor2Name,
                name2=name2
            )
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# ---------
# Guideline
# ---------

class GuidelineCompatibilityReporter(BaseCompatibilityReporter):

    objectName = "Guideline"

    def __init__(self, guideline1, guideline2):
        super(GuidelineCompatibilityReporter, self).__init__(guideline1, guideline2)
        self.nameDifference = False

    guideline1 = dynamicProperty("object1")
    guideline1Name = dynamicProperty("object1Name")
    guideline2 = dynamicProperty("object2")
    guideline2Name = dynamicProperty("object2Name")

    def report(self, showOK=True, showWarnings=True):
        guideline1 = self.guideline1
        guideline2 = self.guideline2
        report = []
        if self.nameDifference:
            name1 = guideline1.name
            name2 = guideline2.name
            text = "{guideline1Name} has name {name1} | {guideline2Name} has name {name2}".format(
                guideline1Name=self.guideline1Name,
                name1=name1,
                guideline2Name=self.guideline2Name,
                name2=name2
            )
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)
