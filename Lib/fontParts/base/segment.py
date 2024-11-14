from __future__ import annotations
from typing import TYPE_CHECKING, Any, Generator, List, Optional, Tuple, Union

from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedSegment, RemovedSegment
from fontParts.base.compatibility import SegmentCompatibilityReporter
from fontParts.base.annotations import (
    CollectionType,
    SextupleCollectionType,
    IntFloatType
)

if TYPE_CHECKING:
    from fontParts.base.point import BasePoint
    from fontParts.base.contour import BaseContour
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.font import BaseFont


class BaseSegment(
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    DeprecatedSegment,
    RemovedSegment,
):
    def _setPoints(self, points: CollectionType[BasePoint]) -> None:
        if hasattr(self, "_points"):
            raise AssertionError("segment has points")
        self._points = points

    def _reprContents(self) -> List[str]:
        contents = [
            f"{self.type}",
        ]
        if self.index is not None:
            contents.append(f"index='{self.index!r}'")
        return contents

    # this class should not be used in hashable
    # collections since it is dynamically generated.

    __hash__ = None

    # -------
    # Parents
    # -------

    # Contour

    _contour: Optional[BaseContour] = None

    contour: dynamicProperty = dynamicProperty("contour", "The segment's parent contour.")

    def _get_contour(self) -> Optional[BaseContour]:
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour: Optional[BaseContour]) -> None:
        if self._contour is not None:
            raise AssertionError("contour for segment already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

    glyph: dynamicProperty = dynamicProperty("glyph", "The segment's parent glyph.")

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer: dynamicProperty = dynamicProperty("layer", "The segment's parent layer.")

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty("font", "The segment's parent font.")

    def _get_font(self) -> Optional[BaseFont]:
        if self._contour is None:
            return None
        return self.glyph.font

    # --------
    # Equality
    # --------

    def __eq__(self, other: object) -> bool:
        """
        The :meth:`BaseObject.__eq__` method can't be used here
        because the :class:`BaseContour` implementation contructs
        segment objects without assigning an underlying ``naked``
        object. Therefore, comparisons will always fail. This
        method overrides the base method and compares the
        :class:`BasePoint` contained by the segment.

        Subclasses may override this method.
        """
        if isinstance(other, self.__class__):
            return self.points == other.points
        return NotImplemented

    # --------------
    # Identification
    # --------------

    index: dynamicProperty = dynamicProperty(
        "base_index",
        (
            "The index of the segment within the ordered "
            "list of the parent contour's segments."
        ),
    )

    def _get_base_index(self) -> Optional[int]:
        if self.contour is None:
            return None
        value = self._get_index()
        normalizedValue = normalizers.normalizeIndex(value)
        return normalizedValue

    def _get_index(self) -> int:
        """
        Subclasses may override this method.
        """
        contour = self.contour
        value = contour.segments.index(self)
        return value

    # ----------
    # Attributes
    # ----------

    type: dynamicProperty = dynamicProperty(
        "base_type",
        ("The segment type. The possible types are " "move, line, curve, qcurve."),
    )

    def _get_base_type(self) -> str:
        value = self._get_type()
        value = normalizers.normalizeSegmentType(value)
        return value

    def _set_base_type(self, value: str) -> None:
        value = normalizers.normalizeSegmentType(value)
        self._set_type(value)

    def _get_type(self) -> str:
        """
        Subclasses may override this method.
        """
        onCurve = self.onCurve
        if onCurve is None:
            return "qcurve"
        return onCurve.type

    def _set_type(self, newType: str) -> None:
        """
        Subclasses may override this method.
        """
        oldType = self.type
        if oldType == newType:
            return
        if self.onCurve is None:
            # special case with a single qcurve segment
            # and only offcurves, don't convert
            return
        contour = self.contour
        if contour is None:
            raise FontPartsError("The segment does not belong to a contour.")
        # converting line <-> move
        if newType in ("move", "line") and oldType in ("move", "line"):
            pass
        # converting to a move or line
        elif newType not in ("curve", "qcurve"):
            offCurves = self.offCurve
            for point in offCurves:
                contour.removePoint(point)
        # converting a line/move to a curve/qcurve
        else:
            segments = contour.segments
            i = segments.index(self)
            prev = segments[i - 1].onCurve
            on = self.onCurve
            x = on.x
            y = on.y
            points = contour.points
            i = points.index(on)
            contour.insertPoint(i, (x, y), "offcurve")
            off2 = contour.points[i]
            contour.insertPoint(i, (prev.x, prev.y), "offcurve")
            off1 = contour.points[i]
            del self._points
            self._setPoints((off1, off2, on))
        self.onCurve.type = newType

    smooth: dynamicProperty = dynamicProperty(
        "base_smooth", ("Boolean indicating if the segment is " "smooth or not.")
    )

    def _get_base_smooth(self) -> bool:
        value = self._get_smooth()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_smooth(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_smooth(value)

    def _get_smooth(self) -> bool:
        """
        Subclasses may override this method.
        """
        onCurve = self.onCurve
        if onCurve is None:
            return True
        return onCurve.smooth

    def _set_smooth(self, value: bool) -> None:
        """
        Subclasses may override this method.
        """
        onCurve = self.onCurve
        if onCurve is not None:
            self.onCurve.smooth = value

    # ------
    # Points
    # ------

    def __getitem__(self, index: int) -> BasePoint:
        return self._getItem(index)

    def _getItem(self, index: int) -> BasePoint:
        """
        Subclasses may override this method.
        """
        return self.points[index]

    def __iter__(self):
        return self._iterPoints()

    def _iterPoints(self, **kwargs: Any) -> Generator[BasePoint]:
        """
        Subclasses may override this method.
        """
        points = self.points
        count = len(points)
        index = 0
        while count:
            yield points[index]
            count -= 1
            index += 1

    def __len__(self) -> int:
        return self._len()

    def _len(self, **kwargs: Any) -> int:
        """
        Subclasses may override this method.
        """
        return len(self.points)

    points: dynamicProperty = dynamicProperty("base_points", "A list of points in the segment.")

    def _get_base_points(self) -> Tuple[BasePoint, ...]:
        return self._get_points()

    def _get_points(self) -> Tuple[BasePoint, ...]:
        """
        Subclasses may override this method.
        """
        if not hasattr(self, "_points"):
            return ()
        return tuple(self._points)

    onCurve: dynamicProperty = dynamicProperty("base_onCurve", "The on curve point in the segment.")

    def _get_base_onCurve(self) -> Optional[BasePoint]:
        return self._get_onCurve()

    def _get_onCurve(self) -> Optional[BasePoint]:
        """
        Subclasses may override this method.
        """
        value = self.points[-1]
        if value.type == "offcurve":
            return None
        return value

    offCurve: dynamicProperty = dynamicProperty("base_offCurve", "The off curve points in the segment.")

    def _get_base_offCurve(self) -> Tuple[BasePoint, ...]:
        """
        Subclasses may override this method.
        """
        return self._get_offCurve()

    def _get_offCurve(self) -> Tuple[BasePoint, ...]:
        """
        Subclasses may override this method.
        """
        if self.points and self.points[-1].type == "offcurve":
            return self.points
        return self.points[:-1]

    # --------------
    # Transformation
    # --------------

    def _transformBy(self,
                     matrix: SextupleCollectionType[IntFloatType],
                     **kwargs: Any):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.transformBy(matrix)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = SegmentCompatibilityReporter

    def isCompatible(self, other: BaseSegment) -> Tuple[bool, str]:
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compatible, report = self.isCompatible(otherSegment)
            >>> compatible
            False
            >>> compatible
            [Fatal] Segment: [0] + [0]
            [Fatal] Segment: [0] is line | [0] is move
            [Fatal] Segment: [1] + [1]
            [Fatal] Segment: [1] is line | [1] is qcurve

        This will return a ``bool`` indicating if the segment is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseSegment, self).isCompatible(other, BaseSegment)

    def _isCompatible(self,
                      other: BaseSegment,
                      reporter: SegmentCompatibilityReporter) -> None:
        """
        This is the environment implementation of
        :meth:`BaseSegment.isCompatible`.

        Subclasses may override this method.
        """
        segment1 = self
        segment2 = other
        # type
        if segment1.type != segment2.type:
            # line <-> curve can be converted
            if set((segment1.type, segment2.type)) != set(("curve", "line")):
                reporter.typeDifference = True
                reporter.fatal = True

    # ----
    # Misc
    # ----

    def round(self) -> None:
        """
        Round coordinates in all points.
        """
        for point in self.points:
            point.round()
