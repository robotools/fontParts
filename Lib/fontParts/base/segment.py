from __future__ import annotations
from typing import TYPE_CHECKING, Any, Generator, List, Optional, Tuple

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
    IntFloatType,
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

    __hash__ = None  # type: ignore[assignment]

    # -------
    # Parents
    # -------

    # Contour

    _contour: Optional[BaseContour] = None

    contour: dynamicProperty = dynamicProperty(
        "contour",
        """Get or set the segment's parent contour object.

        The value must be a :class:`BaseContour` instance or :obj:`None`.

        :return: The :class:`BaseContour` instance containing the segment
            or :obj:`None`.
        :raises AssertionError: If attempting to set the contour when it
            has already been set.

        Example::

            >>> contour = segment.contour

        """,
    )

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

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get the segment's parent glyph object.

        This property is read-only.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the segment
            or :obj:`None`.

        Example::

            >>> glyph = segment.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the segment's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the segemnt
            or :obj:`None`.

        Example::

            >>> layer = segment.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the segment's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the segment
            or :obj:`None`.

        Example::

            >>> font = segment.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._contour is None:
            return None
        return self.glyph.font

    # --------
    # Equality
    # --------

    def __eq__(self, other: object) -> bool:
        """Check for equality with another segment.

        The :meth:`BaseObject.__eq__` method can't be used here
        because the :class:`BaseContour` implementation contructs
        segment objects without assigning an underlying `naked`
        object. Therefore, comparisons will always fail. This
        method overrides the base method and compares the
        :class:`BasePoint` contained by the segment.

        :param other: The segment to compare with.
        :return: :obj:`True` if the segments are equal, :obj:`False` otherwise.

        .. note::

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
        """Get the index of the segment.

        This property is read-only.

        :return: An :class:`int` representing the segment's index within an
            ordered list of the parent contour's segments, or :obj:`None` if the
            segment does not belong to a contour.

        Example::

            >>> segment.index
            0

        """,
    )

    def _get_base_index(self) -> Optional[int]:
        if self.contour is None:
            return None
        value = self._get_index()
        normalizedValue = normalizers.normalizeIndex(value)
        return normalizedValue

    def _get_index(self) -> int:
        """Get the index of the native segment.

        This is the environment implementation of the :attr:`BaseSegment.index`
        property getter.

        :return: An :class:`int` representing the segment's index within an
            ordered list of the parent contour's segments, or :obj:`None` if the
            segment does not belong to a contour.

        .. note::

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
        """Get or set the segment's type.

        The value must be a :class:`str` containing one of the following
        alternatives:

        +----------------+---------------------------------+
        | Type           | Description                     |
        +----------------+---------------------------------+
        | ``'move'``     | An on-curve move to.            |
        | ``'line'``     | An on-curve line to.            |
        | ``'curve'``    | An on-curve cubic curve to.     |
        | ``'qcurve'``   | An on-curve quadratic curve to. |
        +----------------+---------------------------------+

        :return: A :class:`str` representing the type of the segment.

        """,
    )

    def _get_base_type(self) -> str:
        value = self._get_type()
        value = normalizers.normalizeSegmentType(value)
        return value

    def _set_base_type(self, value: str) -> None:
        value = normalizers.normalizeSegmentType(value)
        self._set_type(value)

    def _get_type(self) -> str:
        """Get the native segment's type.

        This is the environment implementation of the :attr:`BaseSegment.type`
        property getter.

        :return: A :class:`str` representing the type of the segment. The value
         will have been normalized with :func:`normalizers.normalizeSegmentType`.

        .. note::

            Subclasses may override this method.

        """
        onCurve = self.onCurve
        if onCurve is None:
            return "qcurve"
        return onCurve.type

    def _set_type(self, newType: str) -> None:
        """Set the native segment's type.

        This is the environment implementation of the :attr:`BaseSegment.type`
        property setter.

        :param newType: The segment type definition as a :class:`str`. The value
            will have been normalized with :func:`normalizers.normalizeSegmentType`.
        :raises FontPartsError: If the segment does not belong to a contour.

        .. note::

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
        "base_smooth",
        """Get or set the segment's smooth state.

        The value must be a :class:`bool` indicating the segment's smooth state.

        :return: :obj:`True` if the segment is smooth, :obj:`False` if it is sharp.

        Example::

            >>> segment.smooth
            False
            >>> segment.smooth = True

        """,
    )

    def _get_base_smooth(self) -> bool:
        value = self._get_smooth()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_smooth(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_smooth(value)

    def _get_smooth(self) -> bool:
        """Get the native segment's smooth state.

        This is the environment implementation of the :attr:`BaseSegment.smooth`
        property getter.

        :return: :obj:`True` if the segment is smooth, :obj:`False` if it is
            sharp. The value will have been normalized
            with :func:`normalizers.normalizeBoolean`.

        .. note::

            Subclasses may override this method.

        """
        onCurve = self.onCurve
        if onCurve is None:
            return True
        return onCurve.smooth

    def _set_smooth(self, value: bool) -> None:
        """Set the native segment's smooth state.

        This is the environment implementation of the :attr:`BaseSegment.smooth`
        property setter.

        :param value: The point's smooth state as a :class:`bool`. The value
            will have been normalized with :func:`normalizers.normalizeBoolean`.

        .. note::

            Subclasses may override this method.

        """
        onCurve = self.onCurve
        if onCurve is not None:
            self.onCurve.smooth = value

    # ------
    # Points
    # ------

    def __getitem__(self, index: int) -> BasePoint:
        """Get the point at the specified index.

        :param index: The zero-based index of the point to retrieve as
            an :class:`int`.
        :return: The :class:`BasePoint` instance located at the specified `index`.
        :raises IndexError: If the specified `index` is out of range.

        """
        return self._getItem(index)

    def _getItem(self, index: int) -> BasePoint:
        """Get the native point at the specified index.

        This is the environment implementation of :meth:`BaseSegment.__getitem__`.

        :param index: The zero-based index of the point to retrieve as
            an :class:`int`.
        :return: The :class:`BasePoint` instance located at the specified `index`.
        :raises IndexError: If the specified `index` is out of range.

        .. note::

            Subclasses may override this method.

        """
        return self.points[index]

    def __iter__(self):
        """Return an iterator over the points in the segment.

        :return: An iterator over the :class:`BasePoint` instances belonging to
            the segment.

        """
        return self._iterPoints()

    def _iterPoints(self, **kwargs: Any) -> Generator[BasePoint]:
        """Return an iterator over the points in the native segment.

        This is the environment implementation of :meth:`BaseSegment.__iter__`.

        :return: An iterator over the :class:`BasePoint` instances belonging to
            the segment.

        .. note::

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
        """Return the number of points in the segment.

        :return: An :class:`int` representing the number of :class:`BasePoint`
            instances belonging to the segment.

        """
        return self._len()

    def _len(self, **kwargs: Any) -> int:
        """Return the number of points in the native segment.

        This is the environment implementation of :meth:`BaseSegment.__len__`.

        :return: An :class:`int` representing the number of :class:`BasePoint`
            instances belonging to the segment.

        .. note::

            Subclasses may override this method.

        """
        return len(self.points)

    points: dynamicProperty = dynamicProperty(
        "base_points",
        """Get a list of all points in the segment.

        This attribute is read-only.

        :return: A :class:`tuple` of :class`BasePoints`.

        """,
    )

    def _get_base_points(self) -> Tuple[BasePoint, ...]:
        return self._get_points()

    def _get_points(self) -> Tuple[BasePoint, ...]:
        """Get a list of all points in the native segment.

        This is the environment implementation of the :attr:`BaseSegment.points`
        property getter.

        :return: A :class:`tuple` of :class`BasePoints`.

        .. note::

            Subclasses may override this method.

        """
        if not hasattr(self, "_points"):
            return ()
        return tuple(self._points)

    onCurve: dynamicProperty = dynamicProperty(
        "base_onCurve",
        """Get the on-curve point in the segment.

        This property is read-only.

        :return: An on-curve :class:`BasePoint` instance or :obj:`None`.

        """,
    )

    def _get_base_onCurve(self) -> Optional[BasePoint]:
        return self._get_onCurve()

    def _get_onCurve(self) -> Optional[BasePoint]:
        """Get the on-curve point in the native segment.

        This is the environment implementation of
        the :attr:`BaseSegment.onCurve` property getter.

        :return: An on-curve :class:`BasePoint` instance or :obj:`None`.

        .. note::

            Subclasses may override this method.

        """
        value = self.points[-1]
        if value.type == "offcurve":
            return None
        return value

    offCurve: dynamicProperty = dynamicProperty(
        "base_offCurve",
        """Get the off-curve points in the segment.

        This property is read-only.

        :return: An off-curve :class:`BasePoint` instance or :obj:`None`.

        """,
    )

    def _get_base_offCurve(self) -> Tuple[BasePoint, ...]:
        return self._get_offCurve()

    def _get_offCurve(self) -> Tuple[BasePoint, ...]:
        """Get the off-curve points in the native segment.

        This is the environment implementation of
        the :attr:`BaseSegment.offCurve` property getter.

        :return: An off-curve :class:`BasePoint` instance or :obj:`None`.

        .. note::

            Subclasses may override this method.

        """
        if self.points and self.points[-1].type == "offcurve":
            return self.points
        return self.points[:-1]

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any):
        r"""Transform the native object according to the given matrix.

        This is the environment implementation of :meth:`TransformationMixin.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will have
            been normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        for point in self.points:
            point.transformBy(matrix)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = SegmentCompatibilityReporter

    def isCompatible(self, other: BaseSegment) -> Tuple[bool, str]:
        """Evaluate interpolation compatibility with another segment.

        This method will return a :class:`bool` indicating if the segment is
        compatible for interpolation with `other`, and a :class:`str`
        containing compatibility notes.

        :param other: The other :class:`BaseSegment` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is a :class:`str`
            of compatibility notes.

        Example::

            >>> compatible, report = self.isCompatible(otherSegment)
            >>> compatible
            False
            >>> compatible
            [Fatal] Segment: [0] + [0]
            [Fatal] Segment: [0] is line | [0] is move
            [Fatal] Segment: [1] + [1]
            [Fatal] Segment: [1] is line | [1] is qcurve

        """
        return super(BaseSegment, self).isCompatible(other, BaseSegment)

    def _isCompatible(
        self, other: BaseSegment, reporter: SegmentCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native segment.

        This is the environment implementation of :meth:`BaseSegment.isCompatible`.

        :param other: The other :class:`BaseSegment` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

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
        """Round coordinates in all the segment's points."""
        for point in self.points:
            point.round()
