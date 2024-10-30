from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference
)
from fontParts.base.errors import FontPartsError
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedBPoint, RemovedBPoint


class BaseBPoint(
                 BaseObject,
                 TransformationMixin,
                 SelectionMixin,
                 DeprecatedBPoint,
                 IdentifierMixin,
                 RemovedBPoint
                 ):

    def _reprContents(self):
        contents = [
            "%s" % self.type,
            "anchor='({x}, {y})'".format(x=self.anchor[0], y=self.anchor[1]),
        ]
        return contents

    def _setPoint(self, point):
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

    def _get_identifier(self):
        """
        Subclasses may override this method.
        """
        return self._point.identifier

    def _getIdentifier(self):
        """
        Subclasses may override this method.
        """
        return self._point.getIdentifier()

    # Segment

    _segment = dynamicProperty("base_segment")

    def _get_base_segment(self):
        point = self._point
        for segment in self.contour.segments:
            if segment.onCurve == point:
                return segment

    _nextSegment = dynamicProperty("base_nextSegment")

    def _get_base_nextSegment(self):
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

    _contour = None

    contour = dynamicProperty("contour", "The bPoint's parent contour.")

    def _get_contour(self):
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour):
        if self._contour is not None:
            raise AssertionError("contour for bPoint already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

<<<<<<< HEAD
    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get the bPoint's parent glyph object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the bPoint
            or :obj:`None`.
<<<<<<< HEAD
=======
    glyph = dynamicProperty("glyph", "The bPoint's parent glyph.")
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _get_glyph(self):
=======
<<<<<<< HEAD

        Example::

=======

        Example::

>>>>>>> v1
            >>> glyph = bPoint.glyph

        """
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

<<<<<<< HEAD
    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the bPoint's parent layer object.

<<<<<<< HEAD
        :return: The :class:`BaseLayer` instance containing the bPoint
            or :obj:`None`.

=======
        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the bPoint
            or :obj:`None`.

>>>>>>> v1
        Example::

            >>> layer = bPoint.layer

        """
    )

    def _get_layer(self) -> Optional[BaseLayer]:
=======
    layer = dynamicProperty("layer", "The bPoint's parent layer.")

    def _get_layer(self):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

<<<<<<< HEAD
    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the bPoint's parent font object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: The :class:`BaseFont` instance containing the bPoint
            or :obj:`None`.

        Example::

            >>> font = bPoint.font
<<<<<<< HEAD
=======
    font = dynamicProperty("font", "The bPoint's parent font.")
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _get_font(self):
=======
<<<<<<< HEAD

        """
    )

=======

        """
    )

>>>>>>> v1
    def _get_font(self) -> Optional[BaseFont]:
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        if self._contour is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # anchor

<<<<<<< HEAD
    anchor = dynamicProperty("base_anchor", "The anchor point.")

    def _get_base_anchor(self):
=======
    anchor: dynamicProperty = dynamicProperty(
        "base_anchor",
        """Get or set the the bPoint's anchor point.
<<<<<<< HEAD

        The value must be a :ref:`type-coordianate`.

        :return: a :ref:`type-coordianate` representing the anchor point of the bPoint.

        """
    )

=======

        The value must be a :ref:`type-coordianate`.

        :return: a :ref:`type-coordianate` representing the anchor point of the bPoint.

        """
    )

>>>>>>> v1
    def _get_base_anchor(self) -> CoordinateType:
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = self._get_anchor()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_anchor(self, value):
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_anchor(value)

<<<<<<< HEAD
    def _get_anchor(self) -> CoordinateType:
        """Get the the bPoint's anchor point.

        This is the environment implementation of the :attr:`BaseBPoint.anchor`
        property getter.

        :return: a :ref:`type-coordianate` representing the anchor point of the
<<<<<<< HEAD
            bPoint. The value will have been normalized
=======
            bPoint. The value will be normalized
>>>>>>> v1
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

=======
    def _get_anchor(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        point = self._point
        return (point.x, point.y)

    def _set_anchor(self, value):
        """
        Subclasses may override this method.
        """
        pX, pY = self.anchor
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))

    # bcp in

<<<<<<< HEAD
    bcpIn = dynamicProperty("base_bcpIn", "The incoming off curve.")

    def _get_base_bcpIn(self):
=======
    bcpIn: dynamicProperty = dynamicProperty(
        "base_bcpIn",
        """Get or set the bPoint's incoming off-curve.

        The value must be a :ref:`type-coordinate`.
<<<<<<< HEAD

        :return: A :ref:`type-coordinate` representing the incoming
            off-curve of the bPoin.

=======

        :return: A :ref:`type-coordinate` representing the incoming
            off-curve of the bPoin.

>>>>>>> v1
        """
    )

    def _get_base_bcpIn(self) -> CoordinateType:
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = self._get_bcpIn()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpIn(self, value):
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpIn(value)

<<<<<<< HEAD
    def _get_bcpIn(self) -> CoordinateType:
        """Get the bPoint's incoming off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpIn`
        property getter.

        :return: A :ref:`type-coordinate` representing the incoming off-curve of
<<<<<<< HEAD
            the bPoin. The value will have been normalized
=======
            the bPoin. The value will be normalized
>>>>>>> v1
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

=======
    def _get_bcpIn(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        segment = self._segment
        offCurves = segment.offCurve
        if offCurves:
            bcp = offCurves[-1]
            x, y = relativeBCPIn(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpIn(self, value):
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPIn(self.anchor, value)
        segment = self._segment
        if segment.type == "move" and value != (0, 0):
            raise FontPartsError(("Cannot set the bcpIn for the first "
                                  "point in an open contour.")
                                 )
        else:
            offCurves = segment.offCurve
            if offCurves:
                # if the two off curves are located at the anchor
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

    bcpOut = dynamicProperty("base_bcpOut", "The outgoing off curve.")

    def _get_base_bcpOut(self):
        value = self._get_bcpOut()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpOut(self, value):
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpOut(value)

<<<<<<< HEAD
    def _get_bcpOut(self) -> CoordinateType:
        """Get the bPoint's outgoing off-curve.

        This is the environment implementation of the :attr:`BaseBPoint.bcpOut`
        property getter.

        :return: A :ref:`type-coordinate` representing the outgoing
<<<<<<< HEAD
            off-curve of the bPoin. The value will have been normalized
=======
            off-curve of the bPoin. The value will be normalized
>>>>>>> v1
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

=======
    def _get_bcpOut(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        nextSegment = self._nextSegment
        offCurves = nextSegment.offCurve
        if offCurves:
            bcp = offCurves[0]
            x, y = relativeBCPOut(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpOut(self, value):
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPOut(self.anchor, value)
        segment = self._segment
        nextSegment = self._nextSegment
        if nextSegment.type == "move" and value != (0, 0):
            raise FontPartsError(("Cannot set the bcpOut for the last "
                                  "point in an open contour.")
                                 )
        else:
            offCurves = nextSegment.offCurve
            if offCurves:
                # if the off curves are located at the anchor coordinates
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

<<<<<<< HEAD
    type: dynamicProperty = dynamicProperty(
        "base_type",
        """Get or set the bPoint's type.

        The value must be a :class:`str` containing one of the following
        alternatives:

<<<<<<< HEAD
        +--------+---------------------------------------------------------+
        | type   | Description                                             |
        +--------+---------------------------------------------------------+
        | curve  | A point where bcpIn and bcpOut are smooth (linked).     |
        | corner | A point where bcpIn and bcpOut are not smooth (linked). |
        +--------+---------------------------------------------------------+
=======
        +--------------+-----------------------------------------------------------+
        | Type         | Description                                               |
        +--------------+-----------------------------------------------------------+
        | ``'curve'``  | A point where bcpIn and bcpOut are smooth (linked).       |
        | ``'corner'`` | A point where bcpIn and bcpOut are not smooth (unlinked). |
        +--------+-----------------------------------------------------------------+
>>>>>>> v1

        :return: A :class:`str` representing the type of the bPoint.
=======
    type = dynamicProperty("base_type", "The bPoint type.")
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _get_base_type(self):
        value = self._get_type()
        value = normalizers.normalizeBPointType(value)
        return value

    def _set_base_type(self, value):
        value = normalizers.normalizeBPointType(value)
        self._set_type(value)

<<<<<<< HEAD
    def _get_type(self) -> str:
        """Get the bPoint's type.

        This is the environment implementation of the :attr:`BaseBPoint.type`
        property getter.

        :return: A :class:`str` representing the type of the bPoint. The value
<<<<<<< HEAD
            will have been normalized with :func:`normalizers.normalizeBPointType`.
=======
            will be normalized with :func:`normalizers.normalizeBPointType`.
>>>>>>> v1
        :raises FontPartsError: If the point's type cannot be converted to a valid
            bPoint type.

        .. note::

            Subclasses may override this method.

=======
    def _get_type(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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
            raise FontPartsError("A %s point can not be converted to a bPoint."
                                         % typ)
        return bType

    def _set_type(self, value):
        """
        Subclasses may override this method.
        """
        point = self._point
        # convert corner to curve
        if value == "curve" and point.type == "line":
            # This needs to insert off curves without
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

<<<<<<< HEAD
    index = dynamicProperty("index",
                            ("The index of the bPoint within the ordered "
                             "list of the parent contour's bPoints. None "
                             "if the bPoint does not belong to a contour.")
                            )
=======
    index: dynamicProperty = dynamicProperty(
        "base_index",
        """Get the index of the bPoint.
<<<<<<< HEAD

        :return: An :class:`int` representing the bPoint's index within an
            ordered list of the parent contour's bPoints, or :obj:`None` if the
            bPoint does not belong to a contour.

        Example::

            >>> bPoint.index
            0

        """
    )

=======

        This property is read-only.
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

<<<<<<< HEAD
        :return: An :class:`int` representing the bPoint's index within an
            ordered list of the parent contour's bPoints, or :obj:`None` if the
            bPoint does not belong to a contour.

        Example::

            >>> bPoint.index
            0

        """
    )

>>>>>>> v1
    def _get_base_index(self) -> Optional[int]:
=======
    def _get_base_index(self):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        if self.contour is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

<<<<<<< HEAD
    def _get_index(self) -> Optional[int]:
        """Get the index of the native bPoint.

        This is the environment implementation of the :attr:`BaseBPoint.index`
        property getter.

        :return: An :class:`int` representing the bPoint's index within an
            ordered list of the parent contour's bPoints, or :obj:`None` if the
<<<<<<< HEAD
            bPoint does not belong to a contour. The value will have been
=======
            bPoint does not belong to a contour. The value will be
>>>>>>> v1
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

=======
    def _get_index(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        contour = self.contour
        value = contour.bPoints.index(self)
        return value

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
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

    def round(self):
        """
        Round coordinates.
        """
        x, y = self.anchor
        self.anchor = (normalizers.normalizeVisualRounding(x),
                       normalizers.normalizeVisualRounding(y))
        x, y = self.bcpIn
        self.bcpIn = (normalizers.normalizeVisualRounding(x),
                      normalizers.normalizeVisualRounding(y))
        x, y = self.bcpOut
        self.bcpOut = (normalizers.normalizeVisualRounding(x),
                       normalizers.normalizeVisualRounding(y))


def relativeBCPIn(anchor, BCPIn):
    """convert absolute incoming bcp value to a relative value"""
    return (BCPIn[0] - anchor[0], BCPIn[1] - anchor[1])


def absoluteBCPIn(anchor, BCPIn):
    """convert relative incoming bcp value to an absolute value"""
    return (BCPIn[0] + anchor[0], BCPIn[1] + anchor[1])


def relativeBCPOut(anchor, BCPOut):
    """convert absolute outgoing bcp value to a relative value"""
    return (BCPOut[0] - anchor[0], BCPOut[1] - anchor[1])


def absoluteBCPOut(anchor, BCPOut):
    """convert relative outgoing bcp value to an absolute value"""
    return (BCPOut[0] + anchor[0], BCPOut[1] + anchor[1])
