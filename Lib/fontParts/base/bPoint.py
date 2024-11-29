from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Optional
from fontTools.misc import transform

from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference,
)
from fontParts.base.errors import FontPartsError
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedBPoint, RemovedBPoint
from fontParts.base.annotations import (
    PairType,
    PairCollectionType,
    SextupleCollectionType,
    IntFloatType,
)

if TYPE_CHECKING:
    from fontParts.base.contour import BaseContour
    from fontParts.base.font import BaseFont
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.point import BasePoint
    from fontParts.base.segment import BaseSegment


class BaseBPoint(
    BaseObject,
    TransformationMixin,
    SelectionMixin,
    DeprecatedBPoint,
    IdentifierMixin,
    RemovedBPoint,
):
    """Represent the basis for a bPoint object."""

    def _reprContents(self) -> List[str]:
        contents = [
            f"{self.type}",
            f"anchor='({self.anchor[0]}, {self.anchor[1]})'",
        ]
        return contents

    def _setPoint(self, point: BasePoint) -> None:
        if hasattr(self, "_point"):
            raise AssertionError("point for bPoint already set")
        self._point = point

    def __eq__(self, other):
        if hasattr(other, "_point"):
            return self._point == other._point
        return NotImplemented

    # this class should not be used in hashable
    # collections since it is dynamically generated.

    __hash__ = None

    # -------
    # Parents
    # -------

    # identifier

    def _get_identifier(self) -> Optional[str]:
        """Get the native bPoint's unique identifier.

        This is the environment implementation of :attr:`BaseBPoint.identifier`.

        If the native object does not have an identifier assigned, one may be
        assigned with :meth:`BaseBPoint.getIdentifier`

        :return: The unique identifier assigned to the object as a :class:`str`,
            or :obj:`None` indicating the object has no identifier.

        .. note::

            Subclasses may override this method.

        """
        return self._point.identifier

    def _getIdentifier(self) -> str:
        """Generate and assign a unique identifier to the native bPoint.

        This is the environment implementation of :meth:`BaseBPoint.getIdentifier`.

        :return: A unique object identifier as a :class:`str`.

        .. note::

            Subclasses may override this method.

        """
        return self._point.getIdentifier()

    # Segment

    _segment: dynamicProperty = dynamicProperty("base_segment")

    def _get_base_segment(self) -> Optional[BaseSegment]:
        point = self._point
        for segment in self.contour.segments:
            if segment.onCurve == point:
                return segment
        return None

    _nextSegment: dynamicProperty = dynamicProperty("base_nextSegment")

    def _get_base_nextSegment(self) -> Optional[BaseSegment]:
        contour = self.contour
        if contour is None:
            return None
        segments = contour.segments
        segment = self._segment
        i = segments.index(segment) + 1
        if i >= len(segments):
            i = i % len(segments)
        nextSegment = segments[i]
        return nextSegment

    # Contour

    _contour: Optional[BaseContour] = None

    contour = dynamicProperty(
        "contour",
        """Get or set the bPoint's parent contour object.

        The value must be a :class:`BaseContour` instance or :obj:`None`.

        :return: The :class:`BaseContour` instance containing the bPoint
            or :obj:`None`.
        :raises AssertionError: If attempting to set the contour when it
            has already been set.

        Example::

            >>> contour = bPoint.contour

        """,
    )

    def _get_contour(self) -> Optional[BaseContour]:
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour: Optional[BaseContour]) -> None:
        if self._contour is not None:
            raise AssertionError("contour for bPoint already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get the bPoint's parent glyph object.

        This property is read-only.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the bPoint
            or :obj:`None`.

        Example::

            >>> glyph = bPoint.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the bPoint's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the bPoint
            or :obj:`None`.

        Example::

            >>> layer = bPoint.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the bPoint's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the bPoint
            or :obj:`None`.

        Example::

            >>> font = bPoint.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._contour is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # anchor

    anchor: dynamicProperty = dynamicProperty(
        "base_anchor",
        """Get or set the the bPoint's anchor point.

        The value must be a :ref:`type-coordianate`.

        :return: a :ref:`type-coordianate` representing the anchor point of the bPoint.

        """,
    )

    def _get_base_anchor(self) -> PairType[IntFloatType]:
        value = self._get_anchor()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_anchor(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_anchor(value)

    def _get_anchor(self) -> PairType[IntFloatType]:
        """Get the the bPoint's anchor point.

        This is the environment implementation of the :attr:`BaseBPoint.anchor`
        property getter.

        :return: a :ref:`type-coordianate` representing the anchor point of the
            bPoint. The value will be normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        point = self._point
        return (point.x, point.y)

    def _set_anchor(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the the bPoint's anchor point.

        This is the environment implementation of the :attr:`BaseBPoint.anchor`
        property setter.

        :param value: The anchor point to set as a :ref:`type-coordianate`.
            The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        pX, pY = self.anchor
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))

    # bcp in

    bcpIn: dynamicProperty = dynamicProperty(
        "base_bcpIn",
        """Get or set the bPoint's incoming off-curve.

        The value must be a :ref:`type-coordinate`.

        :return: A :ref:`type-coordinate` representing the incoming
            off-curve of the bPoin.

        """,
    )

    def _get_base_bcpIn(self) -> PairType[IntFloatType]:
        value = self._get_bcpIn()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpIn(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpIn(value)

    def _get_bcpIn(self) -> PairType[IntFloatType]:
        """Get the bPoint's incoming off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpIn`
        property getter.

        :return: A :ref:`type-coordinate` representing the incoming off-curve of
            the bPoin. The value will be normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        segment = self._segment
        offCurves = segment.offCurve
        if offCurves:
            bcp = offCurves[-1]
            x, y = relativeBCPIn(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpIn(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the bPoint's incoming off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpIn`
        property setter.

        :param value: The incoming off-curve to set as
            a :ref:`type-coordianate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :raises FontPartsError: When attempting to set the incoming off-curve
            for a the first point in an open contour.

        .. note::

            Subclasses may override this method.

        """
        x, y = absoluteBCPIn(self.anchor, value)
        segment = self._segment
        if segment.type == "move" and value != (0, 0):
            raise FontPartsError(
                ("Cannot set the bcpIn for the first " "point in an open contour.")
            )

        offCurves = segment.offCurve
        if offCurves:
            # if the two off-curves are located at the anchor
            # coordinates we can switch to a line segment type.
            if value == (0, 0) and self.bcpOut == (0, 0):
                segment.type = "line"
                segment.smooth = False
            else:
                offCurves[-1].x = x
                offCurves[-1].y = y
        elif value != (0, 0):
            segment.type = "curve"
            offCurves = segment.offCurve
            offCurves[-1].x = x
            offCurves[-1].y = y

    # bcp out

    bcpOut: dynamicProperty = dynamicProperty(
        "base_bcpOut",
        """Get or set the bPoint's outgoing off-curve.

        The value must be a :ref:`type-coordinate`.

        :return: A :ref:`type-coordinate` representing the outgoing
            off-curve of the bPoin.

        """,
    )

    def _get_base_bcpOut(self) -> PairType[IntFloatType]:
        value = self._get_bcpOut()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpOut(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpOut(value)

    def _get_bcpOut(self) -> PairType[IntFloatType]:
        """Get the bPoint's outgoing off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpOut`
        property getter.

        :return: A :ref:`type-coordinate` representing the outgoing
            off-curve of the bPoin. The value will be normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        nextSegment = self._nextSegment
        offCurves = nextSegment.offCurve
        if offCurves:
            bcp = offCurves[0]
            x, y = relativeBCPOut(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpOut(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the bPoint's outgoing off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpOut`
        property setter.

        :param value: The outgoing off-curve to set as
            a :ref:`type-coordianate`. The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.
        :raises FontPartsError: When attempting to set the outgoing off-curve
            for a the last point in an open contour.

        .. note::

            Subclasses may override this method.

        """
        x, y = absoluteBCPOut(self.anchor, value)
        segment = self._segment
        nextSegment = self._nextSegment
        if nextSegment.type == "move" and value != (0, 0):
            raise FontPartsError(
                ("Cannot set the bcpOut for the last " "point in an open contour.")
            )
        else:
            offCurves = nextSegment.offCurve
            if offCurves:
                # if the off-curves are located at the anchor coordinates
                # we can switch to a "line" segment type
                if value == (0, 0) and self.bcpIn == (0, 0):
                    segment.type = "line"
                    segment.smooth = False
                else:
                    offCurves[0].x = x
                    offCurves[0].y = y
            elif value != (0, 0):
                nextSegment.type = "curve"
                offCurves = nextSegment.offCurve
                offCurves[0].x = x
                offCurves[0].y = y

    # type

    type: dynamicProperty = dynamicProperty(
        "base_type",
        """Get or set the bPoint's type.

        The value must be a :class:`str` containing one of the following
        alternatives:

        +--------------+-----------------------------------------------------------+
        | Type         | Description                                               |
        +--------------+-----------------------------------------------------------+
        | ``'curve'``  | A point where bcpIn and bcpOut are smooth (linked).       |
        | ``'corner'`` | A point where bcpIn and bcpOut are not smooth (unlinked). |
        +--------+-----------------------------------------------------------------+

        :return: A :class:`str` representing the type of the bPoint.

        """,
    )

    def _get_base_type(self) -> str:
        value = self._get_type()
        value = normalizers.normalizeBPointType(value)
        return value

    def _set_base_type(self, value: str) -> None:
        value = normalizers.normalizeBPointType(value)
        self._set_type(value)

    def _get_type(self) -> str:
        """Get the bPoint's type.

        This is the environment implementation of the :attr:`BaseBPoint.type`
        property getter.

        :return: A :class:`str` representing the type of the bPoint. The value
            will be normalized with :func:`normalizers.normalizeBPointType`.
        :raises FontPartsError: If the point's type cannot be converted to a valid
            bPoint type.

        .. note::

            Subclasses may override this method.

        """
        point = self._point
        typ = point.type
        bType = None
        if point.smooth:
            if typ == "curve":
                bType = "curve"
            elif typ == "line" or typ == "move":
                nextSegment = self._nextSegment
                if nextSegment is not None and nextSegment.type == "curve":
                    bType = "curve"
                else:
                    bType = "corner"
        elif typ in ("move", "line", "curve"):
            bType = "corner"

        if bType is None:
            raise FontPartsError(f"A {typ} point can not be converted to a bPoint.")
        return bType

    def _set_type(self, value: str) -> None:
        """Set the bPoint's type.

        This is the environment implementation of the :attr:`BaseBPoint.type`
        property setter.

        :param value: The outgoing off-curve to set as a :class:`str`. The value
            will have been normalized with :func:`normalizers.normalizeBPointType`.

        .. note::

            Subclasses may override this method.

        """
        point = self._point
        # convert corner to curve
        if value == "curve" and point.type == "line":
            # This needs to insert off-curves without
            # generating unnecessary points in the
            # following segment. The segment object
            # implements this logic, so delegate the
            # change to the corresponding segment.
            segment = self._segment
            segment.type = "curve"
            segment.smooth = True
        # convert curve to corner
        elif value == "corner" and point.type == "curve":
            point.smooth = False

    # --------------
    # Identification
    # --------------

    index: dynamicProperty = dynamicProperty(
        "base_index",
        """Get the index of the bPoint.

        This property is read-only.

        :return: An :class:`int` representing the bPoint's index within an
            ordered list of the parent contour's bPoints, or :obj:`None` if the
            bPoint does not belong to a contour.

        Example::

            >>> bPoint.index
            0

        """,
    )

    def _get_base_index(self) -> Optional[int]:
        if self.contour is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self) -> Optional[int]:
        """Get the index of the native bPoint.

        This is the environment implementation of the :attr:`BaseBPoint.index`
        property getter.

        :return: An :class:`int` representing the bPoint's index within an
            ordered list of the parent contour's bPoints, or :obj:`None` if the
            bPoint does not belong to a contour. The value will be
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        contour = self.contour
        value = contour.bPoints.index(self)
        return value

    # --------------
    # Transformation
    # --------------

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Transform the native bPoint.

        This is the environment implementation of :meth:`BaseBPoint.transformBy`.

        :param matrix: The transformation to apply as a :ref:`type-transformation`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        anchor = self.anchor
        bcpIn = absoluteBCPIn(anchor, self.bcpIn)
        bcpOut = absoluteBCPOut(anchor, self.bcpOut)
        points = [bcpIn, anchor, bcpOut]
        t = transform.Transform(*matrix)
        bcpIn, anchor, bcpOut = t.transformPoints(points)
        x, y = anchor
        self._point.x = x
        self._point.y = y
        self.bcpIn = relativeBCPIn(anchor, bcpIn)
        self.bcpOut = relativeBCPOut(anchor, bcpOut)

    # ----
    # Misc
    # ----

    def round(self) -> None:
        """Round the bPoint's coordinates.

        This applies to:

        - :attr:`anchor`
        - :attr:`bcpIn`
        - :attr:`bcpOut`

        Example::

            >>> bPoint.round()

        """
        x, y = self.anchor
        self.anchor = (
            normalizers.normalizeVisualRounding(x),
            normalizers.normalizeVisualRounding(y),
        )
        x, y = self.bcpIn
        self.bcpIn = (
            normalizers.normalizeVisualRounding(x),
            normalizers.normalizeVisualRounding(y),
        )
        x, y = self.bcpOut
        self.bcpOut = (
            normalizers.normalizeVisualRounding(x),
            normalizers.normalizeVisualRounding(y),
        )


def relativeBCPIn(
    anchor: PairCollectionType[IntFloatType], BCPIn: PairCollectionType[IntFloatType]
) -> PairType[IntFloatType]:
    """convert absolute incoming bcp value to a relative value.

    :param anchor: The anchor reference point from which to measure the relative
        BCP value as a :ref:`type-coordinate.
    :param BCPIn: The absolute incoming BCP value to be converted as
        a :ref:`type-coordinate.
    :return: The relative position of the incoming BCP as a :ref:`type-coordinate.

    """
    return (BCPIn[0] - anchor[0], BCPIn[1] - anchor[1])


def absoluteBCPIn(
    anchor: PairCollectionType[IntFloatType], BCPIn: PairCollectionType[IntFloatType]
) -> PairType[IntFloatType]:
    """convert relative incoming bcp value to an absolute value.

    :param anchor: The anchor reference point from which the relative BCP value
        is measured as a :ref:`type-coordinate.
    :param BCPIn: The relative incoming BCP value to be converted as
        a :ref:`type-coordinate.
    :return: The absolute position of the incoming BCP as a :ref:`type-coordinate.

    """
    return (BCPIn[0] + anchor[0], BCPIn[1] + anchor[1])


def relativeBCPOut(
    anchor: PairCollectionType[IntFloatType], BCPOut: PairCollectionType[IntFloatType]
) -> PairType[IntFloatType]:
    """convert absolute outgoing bcp value to a relative value.

    :param anchor: The anchor reference point from which to measure the relative
        BCP value as a :ref:`type-coordinate.
    :param BCPOut: The absolute outgoing BCP value to be converted as
        a :ref:`type-coordinate.
    :return: The relative position of the outgoing BCP as a :ref:`type-coordinate.

    """
    return (BCPOut[0] - anchor[0], BCPOut[1] - anchor[1])


def absoluteBCPOut(
    anchor: PairCollectionType[IntFloatType], BCPOut: PairCollectionType[IntFloatType]
) -> PairType[IntFloatType]:
    """convert relative outgoing bcp value to an absolute value.

    :param anchor: The anchor reference point from which the relative BCP value
        is measured as a :ref:`type-coordinate.
    :param BCPOut: The relative outgoing BCP value to be converted as
        a :ref:`type-coordinate.
    :return: The absolute position of the outgoing BCP as a :ref:`type-coordinate.

    """
    return (BCPOut[0] + anchor[0], BCPOut[1] + anchor[1])
