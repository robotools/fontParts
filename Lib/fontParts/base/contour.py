from __future__ import annotations
from typing import TYPE_CHECKING, cast, Any, Iterator, List, Optional, Tuple, Union

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

        """,
    )

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
            1
            >>> contour.index = 0

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
        normalizedValue = normalizers.normalizeIndex(value)
        if normalizedValue is None:
            return
        contourCount = len(glyph.contours)
        if normalizedValue < 0:
            normalizedValue = -(normalizedValue % contourCount)
        if normalizedValue >= contourCount:
            normalizedValue = contourCount
        self._set_index(normalizedValue)

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
        return self._getIdentifierForPoint(point)

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

        The behavior of this may vary across environments.

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

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def round(self) -> None:
        """Round all point coordinates in the contour to the nearest integer.

        Example::

            >>> contour.round()

        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        r"""Round all point coordinates in the native contour to the nearest integer.

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

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
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

    def isCompatible(
        self, other: BaseContour
    ) -> Tuple[bool, ContourCompatibilityReporter]:
        """Evaluate interpolation compatibility with another contour.

        :param other: The other :class:`BaseContour` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.ContourCompatibilityReporter`
            instance.

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

    def _isCompatible(
        self, other: BaseContour, reporter: ContourCompatibilityReporter
    ) -> None:
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

        """,
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

        :param value: A :class:`bool` indicating the desired winding
         direction. :obj:`True` sets the direction to clockwise,
         and :obj:`False` to counter-clockwise. The value will have been
         normalized with :func:`normalizers.normalizeBoolean`.

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

        .. important::

            Subclasses must override this method.

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

        Example::

            >>> contour.contourInside(otherContour)
            True

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

        .. important::

            Subclasses must override this method.

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


        """,
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

        """,
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

        Example::

            >>> contour.segments
            (<BaseSegment curve index='0' at 4573388368>, ...)

        """,
    )

    def _get_segments(self) -> Tuple[BaseSegment, ...]:
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
        segments: List[List[BasePoint]] = [[]]
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
        wrapped: List[BaseSegment] = []
        for points in segments:
            if self.segmentClass is None:
                raise TypeError("segmentClass cannot be None.")
            segment = self.segmentClass()
            segment._setPoints(points)
            self._setContourInSegment(segment)
            wrapped.append(segment)
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

        :return: An iterator over the :class:`BaseSegment` instances belonging
            to the contour.

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

    def appendSegment(
        self,
        type: Optional[str] = None,
        points: Optional[PointCollectionType] = None,
        smooth: bool = False,
        segment: Optional[BaseSegment] = None,
    ) -> None:
        """Append the given segment to the contour.

        If `type` or `points` are specified, those values will be used instead
        of the values in the given `segment` object. The specified `smooth`
        state will be applied if ``segment=None``.

        :param type: An optional :attr:`BaseSegment.type` to be applied to
            the segment as a :class:`str`. Defaults to :obj:`None`.
        :param points: The optional :attr:`BaseSegment.points` to be applied to
            the segment as a :class:`list` or :class:`tuple`
            of :ref:`type-coordinate` items. Defaults to :obj:`None`.
        :param smooth: The :attr:`BaseSegment.smooth` state to be applied to the
            segment as a :class:`bool`. Defaults to :obj:`False`.
        :param segment:  An optional :class:`BaseSegment` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        if type is None:
            raise TypeError("Type cannot be None.")
        type = normalizers.normalizeSegmentType(type)
        if points is not None:
            normalizedPoints = [normalizers.normalizeCoordinateTuple(p) for p in points]
        # Avoid mypy invariant List error.
        castPoints = cast(PointCollectionType, normalizedPoints)
        smooth = normalizers.normalizeBoolean(smooth)
        self._appendSegment(type=type, points=castPoints, smooth=smooth)

    def _appendSegment(
        self, type: str, points: PointCollectionType, smooth: bool, **kwargs: Any
    ) -> None:
        r"""Append the given segment to the native contour.

        This is the environment implementation of :meth:`BaseContour.appendSegment`.

        :param type: The :attr:`BaseSegment.type` to be applied to the segment as
            a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizeSegmentType`.
        :param points: The :attr:`BaseSegment.points` to be applied to the segment as
            a :class:`list` or :class:`tuple` of :ref:`type-coordinate` items.
            The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param smooth: The :attr:`BaseSegment.smooth` state to be applied to the segment
            as a :class:`bool`. The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        self._insertSegment(
            len(self), type=type, points=points, smooth=smooth, **kwargs
        )

    def insertSegment(
        self,
        index: int,
        type: Optional[str] = None,
        points: Optional[PointCollectionType] = None,
        smooth: bool = False,
        segment: Optional[BaseSegment] = None,
    ) -> None:
        """Insert the given segment into the contour.

        If `type` or `points` are specified, those values will be used instead
        of the values in the given `segment` object. The specified `smooth`
        state will be applied if ``segment=None``.

        :param index: The :attr:`BaseSegment.index` to be applied to the segment
            as a :class:`int`.
        :param type: An optional :attr:`BaseSegment.type` to be applied to the
            segment as a :class:`str`. Defaults to :obj:`None`.
        :param points: The optional :attr:`BaseSegment.points` to be applied to
            the segment as a :class:`list` or :class:`tuple`
            of :ref:`type-coordinate` items. Defaults to :obj:`None`.
        :param smooth: The :attr:`BaseSegment.smooth` state to be applied to the
            segment as a :class:`bool`. Defaults to :obj:`False`.
        :param segment: An optional :class:`BaseSegment` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None:
            raise TypeError("Index cannot be None.")
        if type is None:
            raise TypeError("Type cannot be None.")
        type = normalizers.normalizeSegmentType(type)
        if points is not None:
            normalizedPoints = [normalizers.normalizeCoordinateTuple(p) for p in points]
        # Avoid mypy invariant List error.
        castPoints = cast(PointCollectionType, normalizedPoints)
        smooth = normalizers.normalizeBoolean(smooth)
        self._insertSegment(index=index, type=type, points=castPoints, smooth=smooth)

    def _insertSegment(
        self,
        index: int,
        type: str,
        points: PointCollectionType,
        smooth: bool,
        **kwargs: Any,
    ) -> None:
        r"""Insert the given segment into the native contour.

        This is the environment implementation of :meth:`BaseContour.insertSegment`.

        :param index: The :attr:`BaseSegment.index` to be applied to the segment
            as a :class:`int`. The value will have been normalized
            with :func:`normalizers.normalizeIndex`.
        :param type: The :attr:`BaseSegment.type` to be applied to the segment as
            a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizeSegmentType`.
        :param points: The :attr:`BaseSegment.points` to be applied to the segment as
            a :class:`list` or :class:`tuple` of :ref:`type-coordinate` items.
            The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param smooth: The :attr:`BaseSegment.smooth` state to be applied to the
            segment as a :class:`bool`. The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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

    def removeSegment(
        self, segment: Union[BaseSegment, int], preserveCurve: bool = False
    ) -> None:
        """Remove the given segment from the contour.

        If ``preserveCurve=True``, an attempt will be made to preserve the
        overall shape of the curve after the segment is removed, provided the
        environment supports such functionality.

        :param segment: The segment to remove as a :class:`BaseSegment` instance,
            or an :class:`int` representing the segment's index.
        :param preserveCurve: A :class:`bool` indicating whether to preserve
            the curve's shape after the segment is removed. Defaults to :obj:`False`.
        :raises ValueError: If the segment index is out of range or if the
            specified segment is not part of the contour.

        Example::

            >>> contour.removeSegment(mySegment)
            >>> contour.removeSegment(2, preserveCurve=True)

        """
        if not isinstance(segment, int):
            index = self.segments.index(segment)
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None:
            return
        if normalizedIndex >= self._len__segments():
            raise ValueError(f"No segment located at index {normalizedIndex}.")
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removeSegment(normalizedIndex, preserveCurve)

    def _removeSegment(self, index: int, preserveCurve: bool, **kwargs: Any) -> None:
        r"""Remove the given segment from the native contour.

        This is the environment implementation of :meth:`BaseContour.removeSegment`.

        :param index: The segment to remove as an :class:`int` representing
            the segment's index. The value will have been normalized
            with :func:`normalizers.normalizeIndex`.
        :param preserveCurve: A :class:`bool` indicating whether to preserve
            the curve's shape after the segment is removed. Defaults to :obj:`False`.
            The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        segment = self.segments[index]
        for point in segment.points:
            self.removePoint(point, preserveCurve)

    def setStartSegment(self, segment: Union[BaseSegment, int]) -> None:
        """Set the first segment in the contour.

        :param segment: The segment to set as the first instance in the contour
            as a :class:`BaseSegment` instance, or an :class:`int` representing
            the segment's index.
        :raises FontPartsError: If the contour is open.
        :raises ValueError: If the segment index is out of range or if the
            specified segment is not part of the contour.

        Example::

            >>> contour.setStartSegment(mySegment)
            >>> contour.setStartSegment(2)

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
        r"""Set the first segment in the native contour.

        This is the environment implementation of :meth:`BaseContour.setStartSegment`.

        :param segmentIndex: An :class:`int` representing the index of the
            segment to be set as the first instance in the contour.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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

    bPoints: dynamicProperty = dynamicProperty(
        "bPoints",
        """Get a list of all bPoints in the contour.

        This property is read-only.

        :return: A :class:`tuple` of :class`BaseBPoints`.

        """,
    )

    def _get_bPoints(self) -> Tuple[BaseBPoint, ...]:
        bPoints: List[BaseBPoint] = []
        for point in self.points:
            if point.type not in ("move", "line", "curve"):
                continue
            if self.bPointClass is None:
                raise TypeError("bPointClass cannot be None.")
            bPoint = self.bPointClass()
            bPoint.contour = self
            bPoint._setPoint(point)
            bPoints.append(bPoint)
        return tuple(bPoints)

    def appendBPoint(
        self,
        type: Optional[str] = None,
        anchor: Optional[PairCollectionType[IntFloatType]] = None,
        bcpIn: Optional[PairCollectionType[IntFloatType]] = None,
        bcpOut: Optional[PairCollectionType[IntFloatType]] = None,
        bPoint: Optional[BaseBPoint] = None,
    ) -> None:
        """Append the given bPoint to the contour.

        If `type`, `anchor`, `bcpIn` or `bcpOut` are specified, those values
        will be used instead of the values in the given `segment` object.

        :param type: An optional :attr:`BaseBPoint.type` to be applied to
            the bPoint as a :class:`str`. Defaults to :obj:`None`.
        :param anchor: An optional :attr:`BaseBPoint.anchor` to be applied to
            the bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bcpIn: An optional :attr:`BaseBPoint.bcpIn` to be applied to the
            bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bcpOut: An optional :attr:`BaseBPoint.bcpOut` to be applied to the
            bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bPoint: An optional :class:`BaseBPoint` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

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
        if type is None:
            raise TypeError("Type cannot be None.")
        type = normalizers.normalizeBPointType(type)
        if anchor is None:
            raise TypeError("Anchor cannot be None.")
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._appendBPoint(type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def _appendBPoint(
        self,
        type: str,
        anchor: PairCollectionType[IntFloatType],
        bcpIn: PairCollectionType[IntFloatType],
        bcpOut: PairCollectionType[IntFloatType],
        **kwargs: Any,
    ) -> None:
        r"""Append the given bPoint to the native contour.

        This is the environment implementation of :meth:`BaseContour.appendBPoint`.

        :param type: The :attr:`BaseBPoint.type` to be applied to the bPoint as
            a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizeBPointType`.
        :param anchor: The :attr:`BaseBPoint.anchor` to be applied to the bPoint
            as a :ref:`type-coordinate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param bcpIn: The :attr:`BaseBPoint.bcpIn` to be applied to the bPoint
            as a :ref:`type-coordinate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param bcpOut: An optional :attr:`BaseBPoint.bcpOut` to be applied to
            the bPoint as a :ref:`type-coordinate`. The value will have been
            normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        self.insertBPoint(len(self.bPoints), type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def insertBPoint(
        self,
        index: int,
        type: Optional[str] = None,
        anchor: Optional[PairCollectionType[IntFloatType]] = None,
        bcpIn: Optional[PairCollectionType[IntFloatType]] = None,
        bcpOut: Optional[PairCollectionType[IntFloatType]] = None,
        bPoint: Optional[BaseBPoint] = None,
    ) -> None:
        """Insert the given bPoint into the contour.

        If `type`, `anchor`, `bcpIn` or `bcpOut` are specified, those values
        will be used instead of the values in the given `segment` object.

        :param index: The :attr:`BaseBPoint.index` to be applied to the bPoint
            as an :class:`int`.
        :param type: An optional :attr:`BaseBPoint.type` to be applied to
            the bPoint as a :class:`str`. Defaults to :obj:`None`.
        :param anchor: An optional :attr:`BaseBPoint.anchor` to be applied to
            the bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bcpIn: An optional :attr:`BaseBPoint.bcpIn` to be applied to the
            bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bcpOut: An optional :attr:`BaseBPoint.bcpOut` to be applied to the
            bPoint as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param bPoint: An optional :class:`BaseBPoint` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

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
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None:
            raise TypeError("Index cannot be None.")
        if type is None:
            raise TypeError("Type cannot be None.")
        type = normalizers.normalizeBPointType(type)
        if anchor is None:
            raise TypeError("Anchor cannot be None.")
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._insertBPoint(
            index=normalizedIndex, type=type, anchor=anchor, bcpIn=bcpIn, bcpOut=bcpOut
        )

    def _insertBPoint(
        self,
        index: int,
        type: str,
        anchor: PairCollectionType[IntFloatType],
        bcpIn: PairCollectionType[IntFloatType],
        bcpOut: PairCollectionType[IntFloatType],
        **kwargs: Any,
    ) -> None:
        r"""Insert the given bPoint into the native contour.

        This is the environment implementation of :meth:`BaseContour.insertBPoint`.

        :param index: The :attr:`BaseBPoint.index` to be applied to the bPoint
            as an :class:`int`. The value will have been normalized
            with :func:`normalizers.normalizeIndex`.
        :param type: An optional :attr:`BaseBPoint.type` to be applied to
            the bPoint as a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizeBPointType`.
        :param anchor: The :attr:`BaseBPoint.anchor` to be applied to the bPoint
            as a :ref:`type-coordinate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param bcpIn: The :attr:`BaseBPoint.bcpIn` to be applied to the bPoint
            as a :ref:`type-coordinate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :param bcpOut: An optional :attr:`BaseBPoint.bcpOut` to be applied to
            the bPoint as a :ref:`type-coordinate`. The value will have been
            normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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

    def removeBPoint(self, bPoint: Union[BaseBPoint, int]) -> None:
        """Remove the given bPoint from the contour.

        :param bPoint: The bPoint to remove as a :class:`BaseBPoint` instance,
            or an :class:`int` representing the bPoint's index.
        :raises ValueError: If the bPoint index is out of range or if the
            specified bPoint is not part of the contour.

        Example::

            >>> contour.removeBPoint(myBPoint)
            >>> contour.removeBPoint(2)

        """
        index = bPoint.index if not isinstance(bPoint, int) else bPoint
        normalizedIndex = normalizers.normalizeIndex(index)
        # Avoid mypy conflict with normalizeIndex -> Optional[int]
        if normalizedIndex is None:
            return
        if normalizedIndex >= self._len__points():
            raise ValueError(f"No bPoint located at index {normalizedIndex}.")
        self._removeBPoint(normalizedIndex)

    def _removeBPoint(self, index: int, **kwargs: Any) -> None:
        r"""Remove the given bPoint from the native contour.

        This is the environment implementation of :meth:`BaseContour.removeBPoint`.

        :param index: The index representing the :class:`BaseBPoint` subclass
            instance to remove as an :class:`int. The value will have been
            normalized with :func:`normalizers.normalizeIndex`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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

    points: dynamicProperty = dynamicProperty(
        "points",
        """Get a list of all points in the contour.

        This property is read-only.

        :return: A :class:`tuple` of :class`BasePoints`.

        """,
    )

    def _get_points(self) -> Tuple[BasePoint, ...]:
        """Get a list of all points in the native contour.

        This is the environment implementation of the :attr:`BaseContour.points`
        property getter.

        :return: A :class:`tuple` of :class`BasePoint` subclass instances.

        .. note::

            Subclasses may override this method.

        """
        return tuple(self._getitem__points(i) for i in range(self._len__points()))

    def _len__points(self) -> int:
        return self._lenPoints()

    def _lenPoints(self, **kwargs: Any) -> int:
        r"""Return the number of points in the native contour.

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` representing the number of :class:`BasePoint`
            subclass instances belonging to the contour.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getitem__points(self, index: int) -> BasePoint:
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None or normalizedIndex >= self._len__points():
            raise ValueError(f"No point located at index {normalizedIndex}.")
        point = self._getPoint(normalizedIndex)
        self._setContourInPoint(point)
        return point

    def _getPoint(self, index: int, **kwargs: Any) -> BasePoint:
        r"""Get the given point from the native contour.

        :param index: The index representing the :class:`BaseBPoint` subclass
            instance to retrieve as an :class:`int. The value will have been
            normalized with :func:`normalizers.normalizeIndex`.
        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`BasePoint` subclass instance.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getPointIndex(self, point: BasePoint) -> int:
        for i, other in enumerate(self.points):
            if point == other:
                return i
        raise FontPartsError("The point could not be found.")

    def appendPoint(
        self,
        position: Optional[PairCollectionType[IntFloatType]] = None,
        type: str = "line",
        smooth: bool = False,
        name: Optional[str] = None,
        identifier: Optional[str] = None,
        point: Optional[BasePoint] = None,
    ) -> None:
        """Append the given point to the contour.

        If `position`, `type` or `name` are specified, those values will be used
        instead of the values in the given `segment` object. The specified
        `smooth` state will be applied if ``point=None``.

        :param position: An optional position to be applied to the point as
            a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param type: An optional :attr:`BasePoint.type` to be applied to
            the point as a :class:`str`. Defaults to ``'line'``.
        :param smooth: The :attr:`BasePoint.smooth` state to be applied to the
            point as a :class:`bool`. Defaults to :obj:`False`.
        :param name: An optional :attr:`BasePoint.name` to be applied to the
            point as a :class:`str`. Defaults to :obj:`None`.
        :param identifier: An optional :attr:`BasePoint.identifier` to be
            applied to the point as a :class:`str`. Defaults to :obj:`None`.
        :param point: An optional :class:`BasePoint` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

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

    def insertPoint(
        self,
        index: int,
        position: Optional[PairCollectionType[IntFloatType]] = None,
        type: str = "line",
        smooth: bool = False,
        name: Optional[str] = None,
        identifier: Optional[str] = None,
        point: Optional[BasePoint] = None,
    ) -> None:
        """Insert the given point into the contour.

        If `position`, `type` or `name` are specified, those values will be used
        instead of the values in the given `segment` object. The specified
        `smooth` state will be applied if ``point=None``.

        :param index: The :attr:`BasePoint.index` to be applied to the point
            as an :class:`int`.
        :param position: An optional position to be applied to the point as
            a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param type: An optional :attr:`BasePoint.type` to be applied to
            the point as a :class:`str`. Defaults to ``'line'``.
        :param smooth: The :attr:`BasePoint.smooth` state to be applied to the
            point as a :class:`bool`. Defaults to :obj:`False`.
        :param name: An optional :attr:`BasePoint.name` to be applied to the
            point as a :class:`str`. Defaults to :obj:`None`.
        :param identifier: An optional :attr:`BasePoint.identifier` to be
            applied to the point as a :class:`str`. Defaults to :obj:`None`.
        :param point: An optional :class:`BasePoint` instance from which
            attribute values will be copied. Defualts to :obj:`None`.

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
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None:
            raise TypeError("Index cannot be None.")
        if position is None:
            raise TypeError("Position cannot be None.")
        position = normalizers.normalizeCoordinateTuple(position)
        type = normalizers.normalizePointType(type)
        smooth = normalizers.normalizeBoolean(smooth)
        if name is not None:
            name = normalizers.normalizePointName(name)
        if identifier is not None:
            identifier = normalizers.normalizeIdentifier(identifier)
        self._insertPoint(
            normalizedIndex,
            position=position,
            type=type,
            smooth=smooth,
            name=name,
            identifier=identifier,
        )

    def _insertPoint(
        self,
        index: int,
        position: PairCollectionType[IntFloatType],
        type: str,
        smooth: bool,
        name: Optional[str],
        identifier: Optional[str],
        **kwargs: Any,
    ) -> None:
        r"""Insert the given point into the native contour.

        This is the environment implementation of :meth:`BaseContour.insertPoint`.

        :param index: The :attr:`BasePoint.index` to be applied to the point
            as an :class:`int`. The value will have been normalized
            with :func:`normalizers.normalizeIndex`.
        :param position: The position to be applied to the point as
            a :ref:`type-coordinate`. The value will have been normalized with
            :func:`normalizers.normalizeCoordinateTuple`.
        :param type: The :attr:`BasePoint.type` to be applied to the point as
            a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizePointType`.
        :param smooth: The :attr:`BasePoint.smooth` state to be applied to the
            point as a :class:`bool`. The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.
        :param name: An optional :attr:`BasePoint.name` to be applied to the
            point as a :class:`str`. The value will have been normalized
            with :func:`normalizers.normalizePointName`
        :param identifier: An optional :attr:`BasePoint.identifier` to be
            applied to the point as a :class:`str`. The value will have been
            normalized with :func:`normalizers.normalizeIdentifier`, but will
            not have been tested for uniqueness.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def removePoint(
        self, point: Union[BasePoint, int], preserveCurve: bool = False
    ) -> None:
        """Remove the given point from the contour.

        If ``preserveCurve=True``, an attempt will be made to preserve the
        overall shape of the curve after the segment is removed, provided the
        environment supports such functionality.

        :param point: The point to remove as a :class:`BasePoint` instance,
            or an :class:`int` representing the points's index.
        :param preserveCurve: A :class:`bool` indicating whether to preserve
            the curve's shape after the point is removed. Defaults to :obj:`False`.
        :raises ValueError: If the point index is out of range or if the
            specified point is not part of the contour.

        Example::

            >>> contour.removePoint(myPoint)
            >>> contour.removePoint(2, preserveCurve=True)

        """
        index = self.points.index(point) if not isinstance(point, int) else point
        normalizedIndex = normalizers.normalizeIndex(index)
        # Avoid mypy conflict with normalizeIndex -> Optional[int]
        if normalizedIndex is None:
            return
        if normalizedIndex >= self._len__points():
            raise ValueError(f"No point located at index {normalizedIndex}.")
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removePoint(normalizedIndex, preserveCurve)

    def _removePoint(self, index: int, preserveCurve: bool, **kwargs: Any) -> None:
        r"""Remove the given point from the native contour.

        This is the environment implementation of :meth:`BaseContour.removePoint`.

        :param index: The index representing the :class:`BasePoint` subclass
            instance to remove as an :class:`int. The value will have been
            normalized with :func:`normalizers.normalizeIndex`.
        :param preserveCurve: A :class:`bool` indicating whether to preserve
            the curve's shape after the point is removed. The value will have been
            normalized with :func:`normalizers.normalizeBoolean`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def setStartPoint(self, point: Union[BasePoint, int]) -> None:
        """Set the first segment in the contour.

        :param segment: The point to set as the first instance in the contour
            as a :class:`BasePoint` instance, or an :class:`int` representing
            the point's index.
        :raises FontPartsError: If the contour is open.
        :raises ValueError: If the point index is out of range or if the
            specified point is not part of the contour.

        Example::

            >>> contour.setStartPoint(myPoint)
            >>> contour.setStartPoint(2)

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
        r"""Set the first segment in the native contour.

        This is the environment implementation of :meth:`BaseContour.setStartPoint`.

        :param pointIndex: An :class:`int` representing the index of the point
            to be set as the first instance in the contour.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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
        """Get or set the selected segments in the contour.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseSegment` instances or :class:`int` values
        representing segment indexes to select.

        :return: A :class:`tuple` of the currently selected :class:`BaseSegment`
            instances.

        Getting selected segments::

            >>> for segment in contour.selectedSegments:
            ...     segment.move((10, 20))

        Setting selected segments::

            >>> contour.selectedSegments = someSegments

        Setting selection using indexes::

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
        """Get the selected segments in the native contour.

        This is the environment implementation of the
        :attr:`BaseContour.selectedSegments` property getter.

        :return: A :class:`tuple` of the currently selected :class:`BaseSegment`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizeSegment`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.segments)

    def _set_base_selectedSegments(
        self, value: CollectionType[Union[BaseSegment, int]]
    ) -> None:
        normalized = []
        for segment in value:
            normalizedSegment: Union[BaseSegment, int]
            if isinstance(segment, int):
                normalizedIndex = normalizers.normalizeIndex(segment)
                # Avoid mypy conflict with normalizeIndex -> Optional[int]
                if normalizedIndex is None:
                    continue
                normalizedSegment = normalizedIndex
            else:
                normalizedSegment = normalizers.normalizeSegment(segment)
            normalized.append(normalizedSegment)
        self._set_selectedSegments(normalized)

    def _set_selectedSegments(
        self, value: CollectionType[Union[BaseSegment, int]]
    ) -> None:
        """Set the selected segments in the native contour.

        This is the environment implementation of the
        :attr:`BaseContour.selectedSegments` property setter.

        :param value: The segments to select as a :class:`tuple`
            or :class:`list` of either :class:`BaseContour` instances
            or :class:`int` values representing segment indexes. Each value item
            will have been normalized with :func:`normalizers.normalizeSegment`
            or :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.segments, value)

    # points

    selectedPoints: dynamicProperty = dynamicProperty(
        "base_selectedPoints",
        """Get or set the selected points in the contour.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BasePoint` instances or :class:`int` values
        representing point indexes to select.

        :return: A :class:`tuple` of the currently selected :class:`BasePoint`
            instances.

        Getting selected points::

            >>> for point in contour.selectedPoints:
            ...     point.move((10, 20))

        Setting selected points::

            >>> contour.selectedPoints = somePoints

        Setting selection using indexes::

            >>> contour.selectedPoints = [0, 2]

        """,
    )

    def _get_base_selectedPoints(self) -> Tuple[BasePoint, ...]:
        selected = tuple(
            normalizers.normalizePoint(point) for point in self._get_selectedPoints()
        )
        return selected

    def _get_selectedPoints(self) -> Tuple[BasePoint, ...]:
        """Get the selected points in the native contour.

        This is the environment implementation of
        the :attr:`BaseContour.selectedPoints` property getter.

        :return: A :class:`tuple` of the currently selected :class:`BasePoint`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizePoint`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.points)

    def _set_base_selectedPoints(
        self, value: CollectionType[Union[BasePoint, int]]
    ) -> None:
        normalized = []
        for point in value:
            normalizedPoint: Union[BasePoint, int]
            if isinstance(point, int):
                normalizedIndex = normalizers.normalizeIndex(point)
                # Avoid mypy conflict with normalizeIndex -> Optional[int]
                if normalizedIndex is None:
                    continue
                normalizedPoint = normalizedIndex
            else:
                normalizedPoint = normalizers.normalizePoint(point)
            normalized.append(normalizedPoint)
        self._set_selectedPoints(normalized)

    def _set_selectedPoints(self, value: CollectionType[Union[BasePoint, int]]) -> None:
        """Set the selected points in the native contour.

        This is the environment implementation of
        the :attr:`BaseContour.selectedPoints` property setter.

        :param value: The points to select as a :class:`tuple` or :class:`list`
            of either :class:`BasePoint` instances or :class:`int` values
            representing point indexes to select. Each value item will have been
            normalized with :func:`normalizers.normalizePoint`
            or :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.points, value)

    # bPoints

    selectedBPoints: dynamicProperty = dynamicProperty(
        "base_selectedBPoints",
        """Get or set the selected bPoints in the contour.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseBPoint` instances or :class:`int` values
        representing bPoint indexes to select.

        :return: A :class:`tuple` of the currently selected :class:`BaseBPoint`
            instances.

        Getting selected bPoints::

            >>> for bPoint in contour.selectedBPoints:
            ...     bPoint.move((10, 20))

        Setting selected bPoints::

            >>> contour.selectedBPoints = someBPoints

        Setting selection using indexes::

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
        """Get the selected bPoints in the native contour.

        This is the environment implementation of
        the :attr:`BaseContour.selectedBPoints` property getter.

        :return: A :class:`tuple` of the currently selected :class:`BaseBPoint`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizeBPoint`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.bPoints)

    def _set_base_selectedBPoints(
        self, value: CollectionType[Union[BaseBPoint, int]]
    ) -> None:
        normalized = []
        for bPoint in value:
            normalizedBPoint: Union[BaseBPoint, int]
            if isinstance(bPoint, int):
                normalizedIndex = normalizers.normalizeIndex(bPoint)
                # Avoid mypy conflict with normalizeIndex -> Optional[int]
                if normalizedIndex is None:
                    continue
                normalizedBPoint = normalizedIndex
            else:
                normalizedBPoint = normalizers.normalizeBPoint(bPoint)
            normalized.append(normalizedBPoint)
        self._set_selectedBPoints(normalized)

    def _set_selectedBPoints(
        self, value: CollectionType[Union[BaseBPoint, int]]
    ) -> None:
        """Set the selected bPoints in the native contour.

        This is the environment implementation of
        the :attr:`BaseContour.selectedBPoints` property setter.

        :param value: The bPoints to select as a :class:`tuple` or :class:`list`
            of either :class:`BaseBPoint` instances or :class:`int` values
            representing bPoint indexes to select. Each value item will have been
            normalized with :func:`normalizers.normalizeBPoint`
            or :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.bPoints, value)
