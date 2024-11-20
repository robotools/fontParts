from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterator, List, Optional, Tuple, Union

from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.compatibility import ContourCompatibilityReporter
from fontParts.base.deprecated import DeprecatedContour, RemovedContour
from fontParts.base.annotations import (
    QuadrupleType,
    PairCollectionType,
    CollectionType,
    SextupleCollectionType,
    IntFloatType,
    PenType,
    PointPenType,
)

if TYPE_CHECKING:
    from fontParts.base.point import BasePoint
    from fontParts.base.bPoint import BaseBPoint
    from fontParts.base.segment import BaseSegment
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.font import BaseFont

PointCollectionType = CollectionType[PairCollectionType[IntFloatType]]


class BaseContour(
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    IdentifierMixin,
    DeprecatedContour,
    RemovedContour,
):
    """Represent the basis for a contour object.

    :cvar segmentClass: A class representing contour segments. This will
        usually be a :class:`BaseSegment` subclass.
    :cvar bPointClass: A class representing contour bPoints. This will
        usually be a :class:`BaseBPoint` subclass.

    """
    segmentClass = None
    bPointClass = None

    def _reprContents(self) -> List[str]:
        contents = []
        if self.identifier is not None:
            contents.append(f"identifier='{self.identifier!r}'")
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        return contents

    def copyData(self, source: BaseContour) -> None:
        """Copy data from another contour instance.

        This will copy the contents of the following attributes from `source`
        into the current contour instance:

        - :attr:`BaseContour.points`
        - :attr:`BaseContour.bPoints`

        :param source: The source :class:`BaseContour` instance from which
            to copy data.

        Example::

            >>> contour.copyData(sourceContour)

        """
        super(BaseContour, self).copyData(source)
        for sourcePoint in source.points:
            self.appendPoint((0, 0))
            selfPoint = self.points[-1]
            selfPoint.copyData(sourcePoint)

    # -------
    # Parents
    # -------

    # Glyph

    _glyph = None

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get or set the contour's parent glyph object.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the contour
            or :obj:`None`.
        :raises AssertionError: If attempting to set the glyph when it
            has already been set.

        Example::

            >>> glyph = contour.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph: Optional[BaseGlyph]) -> None:
        if self._glyph is not None:
            raise AssertionError("glyph for contour already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the contour's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the contour
            or :obj:`None`.

        Example::

            >>> font = contour.font

        """,)

    def _get_font(self) -> Optional[BaseFont]:
        if self._glyph is None:
            return None
        return self.glyph.font

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the contour's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the contour
            or :obj:`None`.

        Example::

            >>> layer = contour.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # --------------
    # Identification
    # --------------

    # index

    index: dynamicProperty = dynamicProperty(
        "base_index",
        """Get or set the index of the contour.

        The value must be an :class:`int`.

        :return: An :class:`int` representing the contour's index within an
            ordered list of the parent glyph's contours, or :obj:`None` if the
            contour does not belong to a glyph.
        :raises FontPartsError: If the contour does not belong to a glyph.

        Example::

            >>> contour.index
            0

        """,
    )

    def _get_base_index(self) -> Optional[int]:
        glyph = self.glyph
        if glyph is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _set_base_index(self, value: int) -> None:
        glyph = self.glyph
        if glyph is None:
            raise FontPartsError("The contour does not belong to a glyph.")
        value = normalizers.normalizeIndex(value)
        contourCount = len(glyph.contours)
        if value < 0:
            value = -(value % contourCount)
        if value >= contourCount:
            value = contourCount
        self._set_index(value)

    def _get_index(self) -> Optional[int]:
        """Get the index of the native contour.

        This is the environment implementation of the :attr:`BaseContour.index`
        property getter.

        :return: An :class:`int` representing the contour's index within an
            ordered list of the parent glyph's contours, or :obj:`None` if the
            contour does not belong to a glyph. The value will be
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        glyph = self.glyph
        return glyph.contours.index(self)

    def _set_index(self, value: int) -> None:
        """Set the index of the contour.

        This is the environment implementation of the :attr:`BaseContour.index`
        property setter.

        :param value: The index to set as an :class:`int`. The value will have
            been normalized with :func:`normalizers.normalizeIndex`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # identifier

    def getIdentifierForPoint(self, point: BasePoint) -> str:
        """Generate and assign a unique identifier to the given point.

        If `point` already has an identifier, the existing identifier is returned.
        Otherwise, a new unique identifier is created and assigned to `point`.

        :param point: The :class:`BasePoint` instance to which the identifier
            should be assigned.
        :return: A :class:`str` representing the newly assigned identifier.

        Example::

            >>> contour.getIdentifierForPoint(point)
            'ILHGJlygfds'

        """
        point = normalizers.normalizePoint(point)
        return self._getIdentifierforPoint(point)

    def _getIdentifierForPoint(self, point: BasePoint) -> str:
        """Generate and assign a unique identifier to the given native point.

        This is the environment implementation
        of :meth:`BaseContour.getIdentifierForPoint`.

        :param point: The :class:`BasePoint` subclass instance to which the
            identifier should be assigned. The value will have been normalized
            with :func:`normalizers.normalizePoint`.
        :return: A :class:`str` representing the newly assigned identifier.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ----
    # Pens
    # ----

    def draw(self, pen: PenType) -> None:
        """Draw the contour's outline data to the given pen.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPen` to which the
            outline data should be drawn.

        Example::

            >>> contour.draw(pen)

        """
        self._draw(pen)

    def _draw(self, pen: PenType, **kwargs: Any) -> None:
        r"""Draw the native contour's outline data to the given pen.

        This is the environment implementation of :meth:`BaseContour.draw`.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPen` to which the
            outline data should be drawn.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.ufoLib.pointPen import PointToSegmentPen

        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

    def drawPoints(self, pen: PointPenType) -> None:
        """Draw the contour's outline data to the given point pen.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPointPen` to
            which the outline data should be drawn.

        Example::

            >>> contour.drawPoints(pointPen)

        """
        self._drawPoints(pen)

    def _drawPoints(self, pen: PointPenType, **kwargs: Any) -> None:
        r"""Draw the native contour's outline data to the given point pen.

        This is the environment implementation of :meth:`BaseContour.drawPoints`.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPointPen` to
            which the outline data should be drawn.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        # The try: ... except TypeError: ...
        # handles backwards compatibility with
        # point pens that have not been upgraded
        # to point pen protocol 2.
        try:
            pen.beginPath(self.identifier)
        except TypeError:
            pen.beginPath()
        for point in self.points:
            typ = point.type
            if typ == "offcurve":
                typ = None
            try:
                pen.addPoint(
                    pt=(point.x, point.y),
                    segmentType=typ,
                    smooth=point.smooth,
                    name=point.name,
                    identifier=point.identifier,
                )
            except TypeError:
                pen.addPoint(
                    pt=(point.x, point.y),
                    segmentType=typ,
                    smooth=point.smooth,
                    name=point.name,
                )
        pen.endPath()

    # ------------------
    # Data normalization
    # ------------------

    def autoStartSegment(self) -> None:
        """Automatically calculate and set the contour's first segment.

        The behavior of this may vary accross environments.

        Example::

            >>> contour.autoStartSegment()

        """
        self._autoStartSegment()

    def _autoStartSegment(self, **kwargs: Any) -> None:
        r"""Automatically calculate and set the native contour's first segment.

        This is the environment implementation of :meth:`BaseContour.autoStartSegment`.

        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    def round(self) -> None:
        """Round all point coordinates in the contour to the neares integer.

        Example::

            >>> contour.round()

        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        r"""Round all point coordinates in the native contour to the neares integer.

        This is the environment implementation of :meth:`BaseContour.round`.

        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        for point in self.points:
            point.round()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self,
                     matrix: SextupleCollectionType[IntFloatType],
                     **kwargs: Any) -> None:
        r"""Transform the contour according to the given matrix.

        This is the environment implementation of :meth:`BaseContour.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will
             be normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        for point in self.points:
            point.transformBy(matrix)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = ContourCompatibilityReporter

    def isCompatible(self, other: BaseContour) -> tuple[bool, str]:
        """Evaluate interpolation compatibility with another contour.

        :param other: The other :class:`BaseContour` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is a :class:`str`
            of compatibility notes.

        Example::

            >>> compatible, report = self.isCompatible(otherContour)
            >>> compatible
            False
            >>> compatible
            [Fatal] Contour: [0] + [0]
            [Fatal] Contour: [0] contains 4 segments | [0] contains 3 segments
            [Fatal] Contour: [0] is closed | [0] is open

        """
        return super(BaseContour, self).isCompatible(other, BaseContour)

    def _isCompatible(self,
                      other: BaseContour,
                      reporter: ContourCompatibilityReporter) -> None:
        """Evaluate interpolation compatibility with another native contour.

        This is the environment implementation of :meth:`BaseContour.isCompatible`.

        :param other: The other :class:`BaseContour` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.

        """
        contour1 = self
        contour2 = other
        # open/closed
        if contour1.open != contour2.open:
            reporter.openDifference = True
        # direction
        if contour1.clockwise != contour2.clockwise:
            reporter.directionDifference = True
        # segment count
        if len(contour1) != len(contour2.segments):
            reporter.segmentCountDifference = True
            reporter.fatal = True
        # segment pairs
        for i in range(min(len(contour1), len(contour2))):
            segment1 = contour1[i]
            segment2 = contour2[i]
            segmentCompatibility = segment1.isCompatible(segment2)[1]
            if segmentCompatibility.fatal or segmentCompatibility.warning:
                if segmentCompatibility.fatal:
                    reporter.fatal = True
                if segmentCompatibility.warning:
                    reporter.warning = True
                reporter.segments.append(segmentCompatibility)
    # ----
    # Open
    # ----

    open: dynamicProperty = dynamicProperty(
        "base_open",
        """Determine whether the contour is open.

        This property is read-only.

        :return: :obj:`True` if the contour is open, otherwise :obj:`False`.

        Example::

            >>> contour.open
            True

        """
    )

    def _get_base_open(self) -> bool:
        value = self._get_open()
        value = normalizers.normalizeBoolean(value)
        return value

    def _get_open(self) -> bool:
        """Determine whether the native contour is open.

        This is the environment implementation of the :attr:`BaseContour.open`
        property getter.

        :return: :obj:`True` if the contour is open, otherwise :obj:`False`.
            The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ---------
    # Direction
    # ---------

    clockwise: dynamicProperty = dynamicProperty(
        "base_clockwise",
        """Specify or determine whether the contour's winding direction is clockwise.

        The value must be a :class:`bool` indicating the contour's winding
        direction.

        :return: :obj:`True` if the contour's winding direction is clockwise,
            otherwise :obj:`False`.

        """,
    )

    def _get_base_clockwise(self) -> bool:
        value = self._get_clockwise()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_clockwise(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_clockwise(value)

    def _get_clockwise(self) -> bool:
        """Determine whether the native contour's winding direction is clockwise.

        This is the environment implementation of the :attr:`BaseContour.clockwise`
        property getter.

        :return: :obj:`True` if the contour's winding direction is clockwise,
            otherwise :obj:`False`. The value will have been normalized with
            :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_clockwise(self, value: bool) -> None:
        """Specify whether the native contour's winding direction is clockwise.

        This is the environment implementation of the :attr:`BaseContour.clockwise`
        property setter.

        :param value: The winding direction to indicate as a :class:`bool`.
            The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.

        .. note::

            Subclasses may override this method.

        """
        if self.clockwise != value:
            self.reverse()

    def reverse(self) -> None:
        """Reverse the direction of the contour.

        Example::

            >>> contour.clockwise
            False
            >>> contour.reverse()
            >>> contour.clockwise
            True

        """
        self._reverseContour()

    def _reverse(self, **kwargs) -> None:
        r"""Reverse the direction of the contour.

        This is the environment implementation of :meth:`BaseContour.reverse`.

        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        """Check if `point` is within the filled area of the contour.

        :param point: The point to check as a :ref:`type-coordinate`.
        :return: :obj:`True` if `point` is inside the filled area of the
            contour, :obj:`False` otherwise.

        Example::

            >>> contour.pointInside((40, 65))
            True

        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        """Check if `point` is within the filled area of the native contour.

        This is the environment implementation of :meth:`BaseContour.pointInside`.

       :param point: The point to check as a :ref:`type-coordinate`. The value
            will have been normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :return: :obj:`True` if `point` is inside the filled area of the
            contour, :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.pens.pointInsidePen import PointInsidePen

        pen = PointInsidePen(glyphSet=None, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    def contourInside(self, otherContour: BaseContour) -> bool:
        """Check if `otherContour` is within the current contour's filled area.

        :param point: The :class:`BaseContour` instance to check.
        :return: :obj:`True` if `otherContour` is inside the filled area of the
            current contour instance, :obj:`False` otherwise.

            >>> contour.contourInside(otherContour)
            True

        ``contour`` must be a :class:`BaseContour`.
        """
        otherContour = normalizers.normalizeContour(otherContour)
        return self._contourInside(otherContour)

    def _contourInside(self, otherContour: BaseContour) -> bool:
        """Check if `otherContour` is within the current native contour's filled area.

        This is the environment implementation of :meth:`BaseContour.contourInside`.

        :param point: The :class:`BaseContour` instance to check. The value will have
            been normalized with :func:`normalizers.normalizeContour`.
        :return: :obj:`True` if `otherContour` is inside the filled area of the
            current contour instance, :obj:`False` otherwise.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    # ---------------
    # Bounds and Area
    # ---------------

    bounds: dynamicProperty = dynamicProperty(
        "bounds",
        """Get the bounds of the contour.

        This property is read-only.

        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
            in the form ``(x minimum, y minimum, x maximum, y maximum)``
            representing the bounds of the contour, or :obj:`None` if the contour
            is open.

        Example::

            >>> contour.bounds
            (10, 30, 765, 643)


        """
    )

    def _get_base_bounds(self) -> Optional[QuadrupleType[float]]:
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self) -> Optional[QuadrupleType[float]]:
        """Get the bounds of the contour.

        This is the environment implementation of the :attr:`BaseContour.bounds`
        property getter.

        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
            in the form ``(x minimum, y minimum, x maximum, y maximum)``
            representing the bounds of the contour, or :obj:`None` if the contour
            is open.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.pens.boundsPen import BoundsPen

        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds

    area: dynamicProperty = dynamicProperty(
        "area",
        """Get the area of the contour

        This property is read-only.

        :return: A positive :class:`int` or a :class:` float value representing
            the area of the contour, or :obj:`None` if the contour is open.

        Example::

            >>> contour.area
            583

        """
    )

    def _get_base_area(self) -> Optional[float]:
        value = self._get_area()
        if value is not None:
            value = normalizers.normalizeArea(value)
        return value

    def _get_area(self) -> Optional[float]:
        """Get the area of the native contour

        This is the environment implementation of the :attr:`BaseContour.area`
        property getter.

        :return: A positive :class:`int` or a :class:` float value representing
            the area of the contour, or :obj:`None` if the contour is open.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.pens.areaPen import AreaPen

        pen = AreaPen(self.layer)
        self.draw(pen)
        return abs(pen.value)

    # --------
    # Segments
    # --------

    # The base class implements the full segment interaction API.
    # Subclasses do not need to override anything within the contour
    # other than registering segmentClass. Subclasses may choose to
    # implement this API independently if desired.

    def _setContourInSegment(self, segment: BaseSegment) -> None:
        if segment.contour is None:
            segment.contour = self

    segments: dynamicProperty = dynamicProperty(
        "segments",
        """Get the countour's segments.

        This property is read-only.

        :return: A :class:`tuple` of :class:`BaseSegment` instances.

        """
    )

    def _get_segments(self) -> Tuple[BaseSegment]:
        """Get the native countour's segments.

        This is the environment implementation of the :attr:`BaseContour.segments`
        property getter.

        :return: A :class:`tuple` of :class:`BaseSegment` subclass instances.

        .. note::

            Subclasses may override this method.

        """
        points = self.points
        if not points:
            return ()
        segments = [[]]
        lastWasOffCurve = False
        firstIsMove = points[0].type == "move"
        for point in points:
            segments[-1].append(point)
            if point.type != "offcurve":
                segments.append([])
            lastWasOffCurve = point.type == "offcurve"
        if len(segments[-1]) == 0:
            del segments[-1]
        if lastWasOffCurve and firstIsMove:
            # ignore trailing off curves
            del segments[-1]
        if lastWasOffCurve and not firstIsMove and len(segments) > 1:
            segment = segments.pop(-1)
            segment.extend(segments[0])
            del segments[0]
            segments.append(segment)
        if not lastWasOffCurve and not firstIsMove:
            segment = segments.pop(0)
            segments.append(segment)
        # wrap into segments
        wrapped = []
        for points in segments:
            s = self.segmentClass()
            s._setPoints(points)
            self._setContourInSegment(s)
            wrapped.append(s)
        return tuple(wrapped)

    def __getitem__(self, index: int) -> BaseSegment:
        """Get the segment at the specified index.

        :param index: The zero-based index of the point to retrieve as
            an :class:`int`.
        :return: The :class:`BaseSegment` instance located at the specified `index`.
        :raises IndexError: If the specified `index` is out of range.

        """
        return self.segments[index]

    def __iter__(self) -> Iterator[BaseSegment]:
        """Return an iterator over the segments in the contour.

        :return: An iterator over the :class:`BaseSegment` instances belonging to
            the contour.

        """
        return self._iterSegments()

    def _iterSegments(self) -> Iterator[BaseSegment]:
        segments = self.segments
        count = len(segments)
        index = 0
        while count:
            yield segments[index]
            count -= 1
            index += 1

    def __len__(self) -> int:
        """Return the number of segments in the contour.

        :return: An :class:`int` representing the number of :class:`BaseSegment`
            instances belonging to the contour.

        """
        return self._len__segments()

    def _len__segments(self, **kwargs: Any) -> int:
        r"""Return the number of segments in the native contour.

        This is the environment implementation of :meth:`BaseContour.__len__`.

        :return: An :class:`int` representing the number of :class:`BaseSegment`
            subclass instances belonging to the contour.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        return len(self.segments)

    def appendSegment(self,
                      type: Optional[str] = None,
                      points: Optional[PointCollectionType] = None,
                      smooth: bool = False,
                      segment: Optional[BaseSegment] = None) -> None:
        """
        Append a segment to the contour.
        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._appendSegment(type=type, points=points, smooth=smooth)

    def _appendSegment(self,
                       type: Optional[str] = None,
                       points: Optional[PointCollectionType] = None,
                       smooth: bool = False,
                       **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        self._insertSegment(
            len(self), type=type, points=points, smooth=smooth, **kwargs
        )

    def insertSegment(self,
                      index: int,
                      type: Optional[str] = None,
                      points: Optional[PointCollectionType] = None,
                      smooth: bool = False,
                      segment: Optional[BaseSegment] = None) -> None:
        """
        Insert a segment into the contour.
        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._insertSegment(index=index, type=type, points=points, smooth=smooth)

    def _insertSegment(self,
                       index: int,
                       type: Optional[str],
                       points: Optional[PointCollectionType],
                       smooth: bool,
                       **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        onCurve = points[-1]
        offCurve = points[:-1]
        segments = self.segments
        addPointCount = 1
        if self.open:
            index += 1
            addPointCount = 0
        ptCount = sum([len(segments[s].points) for s in range(index)]) + addPointCount
        self.insertPoint(ptCount, onCurve, type=type, smooth=smooth)
        for offCurvePoint in reversed(offCurve):
            self.insertPoint(ptCount, offCurvePoint, type="offcurve")

    def removeSegment(self,
                      segment: Union[int, BaseSegment],
                      preserveCurve: bool = False) -> None:
        """
        Remove segment from the contour.
        If ``preserveCurve`` is set to ``True`` an attempt
        will be made to preserve the shape of the curve
        if the environment supports that functionality.
        """
        if not isinstance(segment, int):
            segment = self.segments.index(segment)
        segment = normalizers.normalizeIndex(segment)
        if segment >= self._len__segments():
            raise ValueError(f"No segment located at index {segment}.")
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removeSegment(segment, preserveCurve)

    def _removeSegment(self, segment: int, preserveCurve: bool, **kwargs: Any) -> None:
        """
        segment will be a valid segment index.
        preserveCurve will be a boolean.

        Subclasses may override this method.
        """
        segment = self.segments[segment]
        for point in segment.points:
            self.removePoint(point, preserveCurve)

    def setStartSegment(self, segment: Union[int, BaseSegment]) -> None:
        """
        Set the first segment on the contour.
        segment can be a segment object or an index.
        """
        if self.open:
            raise FontPartsError("An open contour can not change the starting segment.")
        segments = self.segments
        if not isinstance(segment, int):
            segmentIndex = segments.index(segment)
        else:
            segmentIndex = segment
        if len(self.segments) < 2:
            return
        if segmentIndex == 0:
            return
        if segmentIndex >= len(segments):
            raise ValueError(
                (f"The contour does not contain a segment at index {segmentIndex}")
            )
        self._setStartSegment(segmentIndex)

    def _setStartSegment(self, segmentIndex: int, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        # get the previous segment and set
        # its on curve as the first point
        # in the contour. this matches the
        # iteration behavior of self.segments.
        segmentIndex -= 1
        segments = self.segments
        segment = segments[segmentIndex]
        self.setStartPoint(segment.points[-1])

    # -------
    # bPoints
    # -------

    bPoints: dynamicProperty = dynamicProperty("bPoints")

    def _get_bPoints(self) -> Tuple[BaseBPoint, ...]:
        bPoints = []
        for point in self.points:
            if point.type not in ("move", "line", "curve"):
                continue
            bPoint = self.bPointClass()
            bPoint.contour = self
            bPoint._setPoint(point)
            bPoints.append(bPoint)
        return tuple(bPoints)

    def appendBPoint(self,
                     type: Optional[str] = None,
                     anchor: Optional[PairCollectionType[IntFloatType]] = None,
                     bcpIn: Optional[PairCollectionType[IntFloatType]] = None,
                     bcpOut: Optional[PairCollectionType[IntFloatType]] = None,
                     bPoint: Optional[BaseBPoint] = None) -> None:
        """
        Append a bPoint to the contour.
        """
        if bPoint is not None:
            if type is None:
                type = bPoint.type
            if anchor is None:
                anchor = bPoint.anchor
            if bcpIn is None:
                bcpIn = bPoint.bcpIn
            if bcpOut is None:
                bcpOut = bPoint.bcpOut
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._appendBPoint(type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def _appendBPoint(self,
                      type: Optional[str],
                      anchor: PairCollectionType[IntFloatType],
                      bcpIn: Optional[PairCollectionType[IntFloatType]],
                      bcpOut: Optional[PairCollectionType[IntFloatType]],
                      **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        self.insertBPoint(len(self.bPoints), type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def insertBPoint(self,
                     index: int,
                     type: Optional[str] = None,
                     anchor: Optional[PairCollectionType[IntFloatType]] = None,
                     bcpIn: Optional[PairCollectionType[IntFloatType]] = None,
                     bcpOut: Optional[PairCollectionType[IntFloatType]] = None,
                     bPoint: Optional[BaseBPoint] = None) -> None:
        """
        Insert a bPoint at index in the contour.
        """
        if bPoint is not None:
            if type is None:
                type = bPoint.type
            if anchor is None:
                anchor = bPoint.anchor
            if bcpIn is None:
                bcpIn = bPoint.bcpIn
            if bcpOut is None:
                bcpOut = bPoint.bcpOut
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._insertBPoint(
            index=index, type=type, anchor=anchor, bcpIn=bcpIn, bcpOut=bcpOut
        )

    def _insertBPoint(self,
                      index: int,
                      type: str,
                      anchor: PairCollectionType[IntFloatType],
                      bcpIn: PairCollectionType[IntFloatType],
                      bcpOut: PairCollectionType[IntFloatType],
                      **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        # insert a simple line segment at the given anchor
        # look it up as a bPoint and change the bcpIn and bcpOut there
        # this avoids code duplication
        self._insertSegment(index=index, type="line", points=[anchor], smooth=False)
        bPoints = self.bPoints
        index += 1
        if index >= len(bPoints):
            # its an append instead of an insert
            # so take the last bPoint
            index = -1
        bPoint = bPoints[index]
        bPoint.bcpIn = bcpIn
        bPoint.bcpOut = bcpOut
        bPoint.type = type

    def removeBPoint(self, bPoint: Union[int, BaseBPoint]) -> None:
        """
        Remove the bpoint from the contour.
        bpoint can be a point object or an index.
        """
        if not isinstance(bPoint, int):
            bPoint = bPoint.index
        bPoint = normalizers.normalizeIndex(bPoint)
        if bPoint >= self._len__points():
            raise ValueError(f"No bPoint located at index {bPoint}.")
        self._removeBPoint(bPoint)

    def _removeBPoint(self, index: int, **kwargs: Any) -> None:
        """
        index will be a valid index.

        Subclasses may override this method.
        """
        bPoint = self.bPoints[index]

        nextSegment = bPoint._nextSegment
        offCurves = nextSegment.offCurve
        if offCurves:
            offCurve = offCurves[0]
            self.removePoint(offCurve)

        segment = bPoint._segment
        offCurves = segment.offCurve
        if offCurves:
            offCurve = offCurves[-1]
            self.removePoint(offCurve)

        self.removePoint(bPoint._point)

    # ------
    # Points
    # ------

    def _setContourInPoint(self, point: BasePoint) -> None:
        if point.contour is None:
            point.contour = self

    points: dynamicProperty = dynamicProperty("points")

    def _get_points(self) -> Tuple[BasePoint, ...]:
        """
        Subclasses may override this method.
        """
        return tuple(self._getitem__points(i) for i in range(self._len__points()))

    def _len__points(self) -> int:
        return self._lenPoints()

    def _lenPoints(self, **kwargs: Any) -> int:
        """
        This must return an integer indicating
        the number of points in the contour.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__points(self, index: int) -> BasePoint:
        index = normalizers.normalizeIndex(index)
        if index >= self._len__points():
            raise ValueError(f"No point located at index {index}.")
        point = self._getPoint(index)
        self._setContourInPoint(point)
        return point

    def _getPoint(self, index: int, **kwargs: Any) -> BasePoint:
        """
        This must return a wrapped point.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getPointIndex(self, point: BasePoint) -> int:
        for i, other in enumerate(self.points):
            if point == other:
                return i
        raise FontPartsError("The point could not be found.")

    def appendPoint(self,
                    position: Optional[PairCollectionType[IntFloatType]] = None,
                    type: str = "line",
                    smooth: bool = False,
                    name: Optional[str] = None,
                    identifier: Optional[str] = None,
                    point: Optional[BasePoint] = None) -> None:
        """
        Append a point to the contour.
        """
        if point is not None:
            if position is None:
                position = point.position
            type = point.type
            smooth = point.smooth
            if name is None:
                name = point.name
            if identifier is not None:
                identifier = point.identifier
        self.insertPoint(
            len(self.points),
            position=position,
            type=type,
            smooth=smooth,
            name=name,
            identifier=identifier,
        )

    def insertPoint(self,
                    index: int,
                    position: Optional[PairCollectionType[IntFloatType]] = None,
                    type: str = "line",
                    smooth: bool = False,
                    name: Optional[str] = None,
                    identifier: Optional[str] = None,
                    point: Optional[BasePoint] = None) -> None:
        """
        Insert a point into the contour.
        """
        if point is not None:
            if position is None:
                position = point.position
            type = point.type
            smooth = point.smooth
            if name is None:
                name = point.name
            if identifier is not None:
                identifier = point.identifier
        index = normalizers.normalizeIndex(index)
        position = normalizers.normalizeCoordinateTuple(position)
        type = normalizers.normalizePointType(type)
        smooth = normalizers.normalizeBoolean(smooth)
        if name is not None:
            name = normalizers.normalizePointName(name)
        if identifier is not None:
            identifier = normalizers.normalizeIdentifier(identifier)
        self._insertPoint(
            index,
            position=position,
            type=type,
            smooth=smooth,
            name=name,
            identifier=identifier,
        )

    def _insertPoint(self,
                     index: int,
                     position: PairCollectionType[IntFloatType],
                     type: str = "line",
                     smooth: bool = False,
                     name: Optional[str] = None,
                     identifier: Optional[str] = None,
                     **kwargs: Any) -> None:
        """
        position will be a valid position (x, y).
        type will be a valid type.
        smooth will be a valid boolean.
        name will be a valid name or None.
        identifier will be a valid identifier or None.
        The identifier will not have been tested for uniqueness.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def removePoint(self,
                    point: Union[int, BasePoint],
                    preserveCurve: bool = False) -> None:
        """
        Remove the point from the contour.
        point can be a point object or an index.
        If ``preserveCurve`` is set to ``True`` an attempt
        will be made to preserve the shape of the curve
        if the environment supports that functionality.
        """
        if not isinstance(point, int):
            point = self.points.index(point)
        point = normalizers.normalizeIndex(point)
        if point >= self._len__points():
            raise ValueError(f"No point located at index {point}.")
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removePoint(point, preserveCurve)

    def _removePoint(self,
                     index: int,
                     preserveCurve: bool,
                     **kwargs: Any) -> None:
        """
        index will be a valid index. preserveCurve will be a boolean.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def setStartPoint(self, point: Union[int, Any]) -> None:
        """
        Set the first point on the contour.
        point can be a point object or an index.
        """
        if self.open:
            raise FontPartsError("An open contour can not change the starting point.")
        points = self.points
        if not isinstance(point, int):
            pointIndex = points.index(point)
        else:
            pointIndex = point
        if pointIndex == 0:
            return
        if pointIndex >= len(points):
            raise ValueError(
                (f"The contour does not contain a point at index {pointIndex}")
            )
        self._setStartPoint(pointIndex)

    def _setStartPoint(self, pointIndex: int, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        points = self.points
        points = points[pointIndex:] + points[:pointIndex]
        # Clear the points.
        for point in self.points:
            self.removePoint(point)
        # Add the points.
        for point in points:
            self.appendPoint(
                (point.x, point.y),
                type=point.type,
                smooth=point.smooth,
                name=point.name,
                identifier=point.identifier,
            )

    # ---------
    # Selection
    # ---------

    # segments

    selectedSegments: dynamicProperty = dynamicProperty(
        "base_selectedSegments",
        """
        A list of segments selected in the contour.

        Getting selected segment objects:

            >>> for segment in contour.selectedSegments:
            ...     segment.move((10, 20))

        Setting selected segment objects:

            >>> contour.selectedSegments = someSegments

        Setting also supports segment indexes:

            >>> contour.selectedSegments = [0, 2]
        """,
    )

    def _get_base_selectedSegments(self) -> Tuple[BaseSegment, ...]:
        selected = tuple(
            normalizers.normalizeSegment(segment)
            for segment in self._get_selectedSegments()
        )
        return selected

    def _get_selectedSegments(self) -> Tuple[BaseSegment, ...]:
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.segments)

    def _set_base_selectedSegments(self, value: Tuple[BaseSegment, ...]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeSegmentIndex(i)
            else:
                i = normalizers.normalizeSegment(i)
            normalized.append(i)
        self._set_selectedSegments(normalized)

    def _set_selectedSegments(self, value: CollectionType[BaseSegment]) -> None:
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.segments, value)

    # points

    selectedPoints: dynamicProperty = dynamicProperty(
        "base_selectedPoints",
        """
        A list of points selected in the contour.

        Getting selected point objects:

            >>> for point in contour.selectedPoints:
            ...     point.move((10, 20))

        Setting selected point objects:

            >>> contour.selectedPoints = somePoints

        Setting also supports point indexes:

            >>> contour.selectedPoints = [0, 2]
        """,
    )

    def _get_base_selectedPoints(self) -> Tuple[BasePoint, ...]:
        selected = tuple(
            normalizers.normalizePoint(point) for point in self._get_selectedPoints()
        )
        return selected

    def _get_selectedPoints(self) -> Tuple[BasePoint, ...]:
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.points)

    def _set_base_selectedPoints(self, value: CollectionType[BasePoint]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizePointIndex(i)
            else:
                i = normalizers.normalizePoint(i)
            normalized.append(i)
        self._set_selectedPoints(normalized)

    def _set_selectedPoints(self, value: CollectionType[BasePoint]) -> None:
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.points, value)

    # bPoints

    selectedBPoints: dynamicProperty = dynamicProperty(
        "base_selectedBPoints",
        """
        A list of bPoints selected in the contour.

        Getting selected bPoint objects:

            >>> for bPoint in contour.selectedBPoints:
            ...     bPoint.move((10, 20))

        Setting selected bPoint objects:

            >>> contour.selectedBPoints = someBPoints

        Setting also supports bPoint indexes:

            >>> contour.selectedBPoints = [0, 2]
        """,
    )

    def _get_base_selectedBPoints(self) -> Tuple[BaseBPoint, ...]:
        selected = tuple(
            normalizers.normalizeBPoint(bPoint)
            for bPoint in self._get_selectedBPoints()
        )
        return selected

    def _get_selectedBPoints(self) -> Tuple[BaseBPoint, ...]:
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.bPoints)

    def _set_base_selectedBPoints(self, value: CollectionType[BaseBPoint]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeBPointIndex(i)
            else:
                i = normalizers.normalizeBPoint(i)
            normalized.append(i)
        self._set_selectedBPoints(normalized)

    def _set_selectedBPoints(self, value: CollectionType[BaseBPoint]) -> None:
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.bPoints, value)
