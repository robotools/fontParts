from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Sequence
from _collections_abc import Callable

from fontParts.base.base import dynamicProperty
from fontParts.base.annotations import DiffType

if TYPE_CHECKING:
    from fontParts.base.base import BaseObject
    from fontParts.base.font import BaseFont
    from fontParts.base.layer import BaseLayer
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.contour import BaseContour
    from fontParts.base.component import BaseComponent
    from fontParts.base.anchor import BaseAnchor
    from fontParts.base.guideline import BaseGuideline

# ----
# Base
# ----


class BaseCompatibilityReporter(object):
    objectName = "Base"

    def __init__(self, obj1: BaseObject, obj2: BaseObject) -> None:
        self._object1 = obj1
        self._object2 = obj2

    # status

    fatal = False
    warning = False

    def _get_title(self) -> str:
        title = f"{self.object1Name} + {self.object2Name}"
        if self.fatal:
            return self.formatFatalString(title)
        elif self.warning:
            return self.formatWarningString(title)
        else:
            return self.formatOKString(title)

    title: dynamicProperty = dynamicProperty("title")

    # objects

    object1: dynamicProperty = dynamicProperty("object1")
    object1Name: dynamicProperty = dynamicProperty("object1Name")

    def _get_object1(self) -> Any:
        return self._object1

    def _get_object1Name(self) -> str:
        return self._getObjectName(self._object1)

    object2: dynamicProperty = dynamicProperty("object2")
    object2Name: dynamicProperty = dynamicProperty("object2Name")

    def _get_object2(self) -> Any:
        return self._object2

    def _get_object2Name(self) -> str:
        return self._getObjectName(self._object2)

    @staticmethod
    def _getObjectName(obj) -> str:
        if hasattr(obj, "name") and obj.name is not None:
            return f'"{obj.name}"'
        elif hasattr(obj, "identifier") and obj.identifier is not None:
            return f'"{obj.identifier}"'
        elif hasattr(obj, "index"):
            return f"[{obj.index}]"
        else:
            return f"<{id(obj)}>"

    # Report

    def __repr__(self) -> str:
        return self.report()

    def report(self, showOK: bool = False, showWarnings: bool = False) -> str:
        raise NotImplementedError

    def formatFatalString(self, text: str) -> str:
        return f"[Fatal] {self.objectName}: " + text

    def formatWarningString(self, text: str) -> str:
        return f"[Warning] {self.objectName}: " + text

    def formatOKString(self, text: str) -> str:
        return f"[OK] {self.objectName}: " + text

    @staticmethod
    def reportSubObjects(
        reporters: Sequence[BaseCompatibilityReporter],
        showOK: bool = True,
        showWarnings: bool = True,
    ) -> List[str]:
        report = []
        for reporter in reporters:
            if showOK or reporter.fatal or (showWarnings and reporter.warning):
                report.append(repr(reporter))
        return report

    @staticmethod
    def reportCountDifference(
        subObjectName: str,
        object1Name: str,
        object1Count: int,
        object2Name: str,
        object2Count: int,
    ) -> str:
        text = f"{object1Name} contains {object1Count} {subObjectName} | {object2Name} contains {object2Count} {subObjectName}"
        return text

    @staticmethod
    def reportOrderDifference(
        subObjectName: str,
        object1Name: str,
        object1Order: List[str],
        object2Name: str,
        object2Order: List[str],
    ) -> str:
        text = f"{object1Name} has {subObjectName} ordered {object1Order} | {object2Name} has {object2Order}"
        return text

    @staticmethod
    def reportDifferences(
        object1Name: str, subObjectName: str, subObjectID: str, object2Name: str
    ) -> str:
        text = (
            f"{object1Name} contains {subObjectName} {subObjectID} not in {object2Name}"
        )
        return text


# ----
# Font
# ----


class FontCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Font"

    def __init__(self, font1: BaseFont, font2: BaseFont) -> None:
        super(FontCompatibilityReporter, self).__init__(font1, font2)
        self.guidelineCountDifference = False
        self.layerCountDifference = False
        self.guidelinesMissingFromFont2: List[str] = []
        self.guidelinesMissingInFont1: List[str] = []
        self.layersMissingFromFont2: List[str] = []
        self.layersMissingInFont1: List[str] = []
        self.layers: List[LayerCompatibilityReporter] = []

    font1 = dynamicProperty("object1")
    font1Name = dynamicProperty("object1Name")
    font2 = dynamicProperty("object2")
    font2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        font1 = self.font1
        font2 = self.font2
        report = []
        if self.guidelineCountDifference:
            text = self.reportCountDifference(
                subObjectName="guidelines",
                object1Name=self.font1Name,
                object1Count=len(font1.guidelines),
                object2Name=self.font2Name,
                object2Count=len(font2.guidelines),
            )
            report.append(self.formatWarningString(text))
        for name in self.guidelinesMissingFromFont2:
            text = self.reportDifferences(
                object1Name=self.font1Name,
                subObjectName="guideline",
                subObjectID=name,
                object2Name=self.font2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.guidelinesMissingInFont1:
            text = self.reportDifferences(
                object1Name=self.font2Name,
                subObjectName="guideline",
                subObjectID=name,
                object2Name=self.font1Name,
            )
            report.append(self.formatWarningString(text))
        if self.layerCountDifference:
            text = self.reportCountDifference(
                subObjectName="layers",
                object1Name=self.font1Name,
                object1Count=len(font1.layerOrder),
                object2Name=self.font2Name,
                object2Count=len(font2.layerOrder),
            )
            report.append(self.formatWarningString(text))
        for name in self.layersMissingFromFont2:
            text = self.reportDifferences(
                object1Name=self.font1Name,
                subObjectName="layer",
                subObjectID=name,
                object2Name=self.font2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.layersMissingInFont1:
            text = self.reportDifferences(
                object1Name=self.font2Name,
                subObjectName="layer",
                subObjectID=name,
                object2Name=self.font1Name,
            )
            report.append(self.formatWarningString(text))
        report += self.reportSubObjects(
            self.layers, showOK=showOK, showWarnings=showWarnings
        )

        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -----
# Layer
# -----


class LayerCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Layer"

    def __init__(self, layer1: BaseLayer, layer2: BaseLayer) -> None:
        super(LayerCompatibilityReporter, self).__init__(layer1, layer2)
        self.glyphCountDifference = False
        self.glyphsMissingFromLayer2: List[str] = []
        self.glyphsMissingInLayer1: List[str] = []
        self.glyphs: List[GlyphCompatibilityReporter] = []

    layer1 = dynamicProperty("object1")
    layer1Name = dynamicProperty("object1Name")
    layer2 = dynamicProperty("object2")
    layer2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        layer1 = self.layer1
        layer2 = self.layer2
        report = []
        if self.glyphCountDifference:
            text = self.reportCountDifference(
                subObjectName="glyphs",
                object1Name=self.layer1Name,
                object1Count=len(layer1),
                object2Name=self.layer2Name,
                object2Count=len(layer2),
            )
            report.append(self.formatWarningString(text))
        for name in self.glyphsMissingFromLayer2:
            text = self.reportDifferences(
                object1Name=self.layer1Name,
                subObjectName="glyph",
                subObjectID=name,
                object2Name=self.layer2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.glyphsMissingInLayer1:
            text = self.reportDifferences(
                object1Name=self.layer2Name,
                subObjectName="glyph",
                subObjectID=name,
                object2Name=self.layer1Name,
            )
            report.append(self.formatWarningString(text))
        report += self.reportSubObjects(
            self.glyphs, showOK=showOK, showWarnings=showWarnings
        )

        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -----
# Glyph
# -----


class GlyphCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Glyph"

    def __init__(self, glyph1: BaseGlyph, glyph2: BaseGlyph) -> None:
        super(GlyphCompatibilityReporter, self).__init__(glyph1, glyph2)
        self.contourCountDifference = False
        self.componentCountDifference = False
        self.guidelineCountDifference = False
        self.anchorDifferences: DiffType = []
        self.anchorCountDifference = False
        self.anchorOrderDifference = False
        self.anchorsMissingFromGlyph1: List[str] = []
        self.anchorsMissingFromGlyph2: List[str] = []
        self.componentDifferences: DiffType = []
        self.componentOrderDifference = False
        self.componentsMissingFromGlyph1: List[str] = []
        self.componentsMissingFromGlyph2: List[str] = []
        self.guidelinesMissingFromGlyph1: List[str] = []
        self.guidelinesMissingFromGlyph2: List[str] = []
        self.contours: List[ContourCompatibilityReporter] = []

    glyph1 = dynamicProperty("object1")
    glyph1Name = dynamicProperty("object1Name")
    glyph2 = dynamicProperty("object2")
    glyph2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
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
                object2Count=len(glyph2),
            )
            report.append(self.formatFatalString(text))
        report += self.reportSubObjects(
            self.contours, showOK=showOK, showWarnings=showWarnings
        )

        # Component test
        if self.componentCountDifference:
            text = self.reportCountDifference(
                subObjectName="components",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.components),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.components),
            )
            report.append(self.formatFatalString(text))
        elif self.componentOrderDifference:
            text = self.reportOrderDifference(
                subObjectName="components",
                object1Name=self.glyph1Name,
                object1Order=[c.baseGlyph for c in glyph1.components],
                object2Name=self.glyph2Name,
                object2Order=[c.baseGlyph for c in glyph2.components],
            )
            report.append(self.formatWarningString(text))
        for name in self.componentsMissingFromGlyph2:
            text = self.reportDifferences(
                object1Name=self.glyph1Name,
                subObjectName="component",
                subObjectID=name,
                object2Name=self.glyph2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.componentsMissingFromGlyph1:
            text = self.reportDifferences(
                object1Name=self.glyph2Name,
                subObjectName="component",
                subObjectID=name,
                object2Name=self.glyph1Name,
            )
            report.append(self.formatWarningString(text))

        # Anchor test
        if self.anchorCountDifference:
            text = self.reportCountDifference(
                subObjectName="anchors",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.anchors),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.anchors),
            )
            report.append(self.formatWarningString(text))
        elif self.anchorOrderDifference:
            text = self.reportOrderDifference(
                subObjectName="anchors",
                object1Name=self.glyph1Name,
                object1Order=[a.name for a in glyph1.anchors],
                object2Name=self.glyph2Name,
                object2Order=[a.name for a in glyph2.anchors],
            )
            report.append(self.formatWarningString(text))
        for name in self.anchorsMissingFromGlyph2:
            text = self.reportDifferences(
                object1Name=self.glyph1Name,
                subObjectName="anchor",
                subObjectID=name,
                object2Name=self.glyph2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.anchorsMissingFromGlyph1:
            text = self.reportDifferences(
                object1Name=self.glyph2Name,
                subObjectName="anchor",
                subObjectID=name,
                object2Name=self.glyph1Name,
            )
            report.append(self.formatWarningString(text))

        # Guideline test
        if self.guidelineCountDifference:
            text = self.reportCountDifference(
                subObjectName="guidelines",
                object1Name=self.glyph1Name,
                object1Count=len(glyph1.guidelines),
                object2Name=self.glyph2Name,
                object2Count=len(glyph2.guidelines),
            )
            report.append(self.formatWarningString(text))
        for name in self.guidelinesMissingFromGlyph2:
            text = self.reportDifferences(
                object1Name=self.glyph1Name,
                subObjectName="guideline",
                subObjectID=name,
                object2Name=self.glyph2Name,
            )
            report.append(self.formatWarningString(text))
        for name in self.guidelinesMissingFromGlyph1:
            text = self.reportDifferences(
                object1Name=self.glyph2Name,
                subObjectName="guideline",
                subObjectID=name,
                object2Name=self.glyph1Name,
            )
            report.append(self.formatWarningString(text))

        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -------
# Contour
# -------


class ContourCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Contour"

    def __init__(self, contour1: BaseContour, contour2: BaseContour) -> None:
        super(ContourCompatibilityReporter, self).__init__(contour1, contour2)
        self.openDifference = False
        self.directionDifference = False
        self.segmentCountDifference = False
        self.segments: List[SegmentCompatibilityReporter] = []

    contour1 = dynamicProperty("object1")
    contour1Name = dynamicProperty("object1Name")
    contour2 = dynamicProperty("object2")
    contour2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        contour1 = self.contour1
        contour2 = self.contour2
        report = []
        if self.segmentCountDifference:
            text = self.reportCountDifference(
                subObjectName="segments",
                object1Name=self.contour1Name,
                object1Count=len(contour1),
                object2Name=self.contour2Name,
                object2Count=len(contour2),
            )
            report.append(self.formatFatalString(text))
        if self.openDifference:
            state1 = state2 = "closed"
            if contour1.open:
                state1 = "open"
            if contour2.open:
                state2 = "open"
            text = f"{self.contour1Name} is {state1} | {self.contour2Name} is {state2}"
            report.append(self.formatFatalString(text))
        if self.directionDifference:
            state1 = state2 = "counter-clockwise"
            if contour1.clockwise:
                state1 = "clockwise"
            if contour2.clockwise:
                state2 = "clockwise"
            text = f"{self.contour1Name} is {state1} | {self.contour2Name} is {state2}"
            report.append(self.formatFatalString(text))
        report += self.reportSubObjects(
            self.segments, showOK=showOK, showWarnings=showWarnings
        )
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# -------
# Segment
# -------


class SegmentCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Segment"

    def __init__(self, contour1: BaseContour, contour2: BaseContour) -> None:
        super(SegmentCompatibilityReporter, self).__init__(contour1, contour2)
        self.typeDifference = False

    segment1 = dynamicProperty("object1")
    segment1Name = dynamicProperty("object1Name")
    segment2 = dynamicProperty("object2")
    segment2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        segment1 = self.segment1
        segment2 = self.segment2
        report = []
        if self.typeDifference:
            type1 = segment1.type
            type2 = segment2.type
            text = f"{self.segment1Name} is {type1} | {self.segment2Name} is {type2}"
            report.append(self.formatFatalString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# ---------
# Component
# ---------


class ComponentCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Component"

    def __init__(self, component1: BaseComponent, component2: BaseComponent) -> None:
        super(ComponentCompatibilityReporter, self).__init__(component1, component2)
        self.baseDifference = False

    component1 = dynamicProperty("object1")
    component1Name = dynamicProperty("object1Name")
    component2 = dynamicProperty("object2")
    component2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        component1 = self.component1
        component2 = self.component2
        report = []
        if self.baseDifference:
            name1 = component1.baseName
            name2 = component2.baseName
            text = f"{self.component1Name} has base glyph {name1} | {self.component2Name} has base glyph {name2}"
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# ------
# Anchor
# ------


class AnchorCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Anchor"

    def __init__(self, anchor1: BaseAnchor, anchor2: BaseAnchor) -> None:
        super(AnchorCompatibilityReporter, self).__init__(anchor1, anchor2)
        self.nameDifference = False

    anchor1 = dynamicProperty("object1")
    anchor1Name = dynamicProperty("object1Name")
    anchor2 = dynamicProperty("object2")
    anchor2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        anchor1 = self.anchor1
        anchor2 = self.anchor2
        report = []
        if self.nameDifference:
            name1 = anchor1.name
            name2 = anchor2.name
            text = f"{self.anchor1Name} has name {name1} | {self.anchor2Name} has name {name2}"
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)


# ---------
# Guideline
# ---------


class GuidelineCompatibilityReporter(BaseCompatibilityReporter):
    objectName = "Guideline"

    def __init__(self, guideline1: BaseGuideline, guideline2: BaseGuideline) -> None:
        super(GuidelineCompatibilityReporter, self).__init__(guideline1, guideline2)
        self.nameDifference = False

    guideline1 = dynamicProperty("object1")
    guideline1Name = dynamicProperty("object1Name")
    guideline2 = dynamicProperty("object2")
    guideline2Name = dynamicProperty("object2Name")

    def report(self, showOK: bool = True, showWarnings: bool = True) -> str:
        guideline1 = self.guideline1
        guideline2 = self.guideline2
        report = []
        if self.nameDifference:
            name1 = guideline1.name
            name2 = guideline2.name
            text = f"{self.guideline1Name} has name {name1} | {self.guideline2Name} has name {name2}"
            report.append(self.formatWarningString(text))
        if report or showOK:
            report.insert(0, self.title)
        return "\n".join(report)
