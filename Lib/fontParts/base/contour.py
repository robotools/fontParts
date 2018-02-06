from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject, TransformationMixin, dynamicProperty, reference)
from fontParts.base import normalizers
from fontParts.base.bPoint import absoluteBCPIn, absoluteBCPOut
from fontParts.base.deprecated import DeprecatedContour, RemovedContour


class BaseContour(BaseObject, TransformationMixin, DeprecatedContour, RemovedContour):

    segmentClass = None
    bPointClass = None

    def _reprContents(self):
        contents = []
        if self.identifier is not None:
            contents.append("identifier='%r'" % self.identifier)
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        return contents

    def copyData(self, source):
        super(BaseContour, self).copyData(source)
        for sourcePoint in source.points:
            self.appendPoint((0, 0))
            selfPoint = self.points[-1]
            selfPoint.copyData(sourcePoint)

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.glyph

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The contour's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        assert self._glyph is None
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    font = dynamicProperty("font", "The contour's parent font.")

    def _get_font(self):
        if self._glyph is None:
            return None
        return self.glyph.font

    # Layer

    layer = dynamicProperty("layer", "The contour's parent layer.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # --------------
    # Identification
    # --------------

    # index

    index = dynamicProperty("base_index", "The index of the contour within the ordered list of the parent glyph's contours.")

    def _get_base_index(self):
        glyph = self.glyph
        if glyph is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _set_base_index(self, value):
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

    def _get_index(self):
        """
        Subclasses may override this method.
        """
        glyph = self.glyph
        return glyph.contours.index(self)

    def _set_index(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # identifier

    identifier = dynamicProperty("base_identifier", "The unique identifier for the contour.")

    def _get_base_identifier(self):
        value = self._get_identifier()
        if value is not None:
            value = normalizers.normalizeIdentifier(value)
        return value

    def _get_identifier(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def getIdentifier(self):
        """
        Create a new, unique identifier for and assign it to the contour.
        If the contour already has an identifier, the existing one should be returned.
        """
        return self._getIdentifier()

    def _getIdentifier(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def getIdentifierForPoint(self, point):
        """
        Create a new, unique identifier for and assign it to the point.
        If the point already has an identifier, the existing one should be returned.
        """
        point = normalizers.normalizePoint(point)
        return self._getIdentifierforPoint(point)

    def _getIdentifierforPoint(self, point):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()


    # ----
    # Pens
    # ----

    def draw(self, pen, **kwargs):
        """
        Draw the contour with the given Pen.
        """
        self._draw(pen, **kwargs)

    def _draw(self, pen, **kwargs):
        """
        Subclasses may override this method.
        """
        from ufoLib.pointPen import PointToSegmentPen
        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

    def drawPoints(self, pen, **kwargs):
        """
        Draw the contour with the given PointPen.
        """
        self._drawPoints(pen, **kwargs)

    def _drawPoints(self, pen, **kwargs):
        """
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
                pen.addPoint(pt=(point.x, point.y), segmentType=typ, smooth=point.smooth, identifier=point.identifier)
            except TypeError:
                pen.addPoint(pt=(point.x, point.y), segmentType=typ, smooth=point.smooth)
        pen.endPath()

    # ------------------
    # Data normalization
    # ------------------

    def autoStartSegment(self, **kwargs):
        """
        Automatically set the segment with on curve in the
        lower left of the contour as the first segment.
        """
        self._autoStartSegment(**kwargs)

    def _autoStartSegment(self, **kwargs):
        """
        Subclasses may override this method.

        XXX port this from robofab
        """
        self.raiseNotImplementedError()

    def round(self, **kwargs):
        """
        Round coordinates in all points.
        """
        self._round(**kwargs)

    def _round(self, **kwargs):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.round()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.transformBy(matrix, origin=origin)

    # ----
    # Open
    # ----

    open = dynamicProperty("base_open", "Boolean indicating if the contour is open.")

    def _get_base_open(self):
        value = self._get_open()
        value = normalizers.normalizeBoolean(value)
        return value

    def _get_open(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---------
    # Direction
    # ---------

    clockwise = dynamicProperty("base_clockwise", "Boolean indicating if the contour's winding direction is clockwise.")

    def _get_base_clockwise(self):
        value = self._get_clockwise()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_clockwise(self, value):
        value = normalizers.normalizeBoolean(value)
        self._set_clockwise(value)

    def _get_clockwise(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_clockwise(self, value):
        """
        Subclasses may override this method.
        """
        if self.clockwise != value:
            self.reverse()

    def reverse(self, **kwargs):
        """
        Reverse the direction of the contour.
        """
        self._reverseContour()

    def _reverse(self, **kwargs):
        """
        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point):
        """
        Determine if point is in the black or white of the contour.

        point must be an (x, y) tuple.
        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.pointInsidePen import PointInsidePen
        pen = PointInsidePen(glyphSet=None, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    bounds = dynamicProperty("bounds", "The bounds of the contour: (xMin, yMin, xMax, yMax) or None.")

    def _get_base_bounds(self):
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.boundsPen import BoundsPen
        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds

    # --------
    # Segments
    # --------

    """
    The base class implements the full segment interaction API.
    Subclasses do not need to override anything within the contour
    other than registering segmentClass. Subclasses may choose to
    implement this API independently if desired.
    """

    def _setContourInSegment(self, segment):
        if segment.contour is None:
            segment.contour = self

    segments = dynamicProperty("segments")

    def _get_segments(self):
        """
        Subclasses may override this method.
        """
        points = list(self.points)
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
        if lastWasOffCurve and not firstIsMove:
            segment = segments.pop(-1)
            assert len(segments[0]) == 1
            segment.append(segments[0][0])
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
        return wrapped

    def __getitem__(self, index):
        return self.segments[index]

    def __iter__(self):
        return self._iterSegments()

    def _iterSegments(self):
        segments = self.segments
        count = len(segments)
        index = 0
        while count:
            yield segments[index]
            count -= 1
            index += 1

    def __len__(self):
        return self._len__segments()

    def _len__segments(self, **kwargs):
        """
        Subclasses may override this method.
        """
        return len(self.segments)

    def appendSegment(self, type, points, smooth=False, **kwargs):
        """
        Append a segment to the contour.
        """
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._appendSegment(type=type, points=points, smooth=smooth, **kwargs)

    def _appendSegment(self, type=None, points=None, smooth=False, **kwargs):
        """
        Subclasses may override this method.
        """
        self._insertSegment(len(self), type=type, points=points, smooth=smooth)

    def insertSegment(self, index, type, points, smooth=False, **kwargs):
        """
        Insert a segment into the contour.
        """
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._insertSegment(index=index, type=type, points=points, smooth=smooth, **kwargs)

    def _insertSegment(self, index=None, type=None, points=None, smooth=False, **kwargs):
        """
        Subclasses may override this method.
        """
        onCurve = points[-1]
        offCurve = points[:-1]
        self.insertPoint(index, onCurve, type=type, smooth=smooth)
        for offCurvePoint in reversed(offCurve):
            self.insertPoint(index, offCurvePoint, type="offcurve")

    def removeSegment(self, segment, **kwargs):
        """
        Remove segment from the contour.
        """
        if not isinstance(segment, int):
            segment = self.segments.index(segment)
        segment = normalizers.normalizeIndex(segment)
        if segment >= self._len__segments():
            raise FontPartsError("No segment located at index %d." % segment)
        self._removeSegment(segment, **kwargs)

    def _removeSegment(self, segment, **kwargs):
        """
        segment will be a valid segment index.

        Subclasses may override this method.
        """
        segment = self.segments[segment]
        for point in segment.points:
            self.removePoint(point)

    def setStartSegment(self, segment, **kwargs):
        """
        Set the first segment on the contour.
        segment can be a segment object or an index.
        """
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
            raise FontPartsError("The contour does not contain a segment at index %d" % segmentIndex)
        self._setStartSegment(segmentIndex, **kwargs)

    def _setStartSegment(self, segmentIndex, **kwargs):
        """
        Subclasses may override this method.
        """
        segments = self.segments
        oldStart = self.segments[0]
        oldLast = self.segments[-1]
        # If the contour ends with a curve on top of a move,
        # delete the move.
        if oldLast.type == "curve" or oldLast.type == "qcurve":
            startOn = oldStart.onCurve
            lastOn = oldLast.onCurve
            if startOn.x == lastOn.x and startOn.y == lastOn.y:
                self.removeSegment(0)
                # Shift new the start index.
                segmentIndex = segmentIndex - 1
                segments = self.segments
        # If the first point is a move, convert it to a line.
        if segments[0].type == "move":
            segments[0].type = "line"
        # Reorder the points internally.
        segments = segments[segmentIndex:] + segments[:segmentIndex]
        points = []
        for segment in segments:
            for point in segment:
                points.append(((point.x, point.y), point.type, point.smooth, point.name, point.identifier))
        # Clear the points.
        for point in self.points:
            self.removePoint(point)
        # Add the points.
        for point in points:
            position, type, smooth, name, identifier = point
            self.appendPoint(
                position,
                type=type,
                smooth=smooth,
                name=name,
                identifier=identifier
            )

    # -------
    # bPoints
    # -------

    bPoints = dynamicProperty("bPoints")

    def _get_bPoints(self):
        bPoints = []
        for point in self.points:
            if point.type not in ("move", "line", "curve"):
                continue
            bPoint = self.bPointClass()
            bPoint.contour = self
            bPoint._setPoint(point)
            bPoints.append(bPoint)
        return tuple(bPoints)

    def appendBPoint(self, type, anchor, bcpIn=None, bcpOut=None, **kwargs):
        """
        Append a bPoint to the contour.
        """
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._appendBPoint(type, anchor, bcpIn=bcpIn, bcpOut=bcpOut, **kwargs)

    def _appendBPoint(self, type, anchor, bcpIn=None, bcpOut=None, **kwargs):
        """
        Subclasses may override this method.
        """
        self.insertBPoint(len(self.bPoints), type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def insertBPoint(self, index, type, anchor, bcpIn=None, bcpOut=None, **kwargs):
        """
        Insert a bPoint at index in the contour.
        """
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._insertBPoint(index=index, type=type, anchor=anchor, bcpIn=bcpIn, bcpOut=bcpOut, **kwargs)

    def _insertBPoint(self, index, type, anchor, bcpIn, bcpOut, **kwargs):
        """
        Subclasses may override this method.
        """
        segments = self.segments
        # insert a curve point that we can work with
        nextSegment = segments[index]
        if nextSegment.type not in ("move", "line", "curve"):
            raise FontPartsError("Unknonw segment type (%s) in contour." % nextSegment.type)
        if nextSegment.type == "move":
            prevSegment = segments[index - 1]
            prevOn = prevSegment.onCurve
            if bcpIn != (0, 0):
                new = self.appendSegment(
                    "curve",
                    [(prevOn.x, prevOn.y), absoluteBCPIn(anchor, bcpIn), anchor],
                    smooth=False
                )
                if type == "curve":
                    new.smooth = True
            else:
                new = self.appendSegment(
                    "line",
                    [anchor],
                    smooth=False
                )
            # if the user wants an outgoing bcp, we must add a curve ontop of the move
            if bcpOut != (0, 0):
                nextOn = nextSegment.onCurve
                self.appendSegment(
                    "curve",
                    [absoluteBCPOut(anchor, bcpOut), (nextOn.x, nextOn.y), (nextOn.x, nextOn.y)],
                    smooth=False
                )
        else:
            # handle the bcps
            if nextSegment.type != "curve":
                prevSegment = segments[index - 1]
                prevOn = prevSegment.onCurve
                prevOutX, prevOutY = (prevOn.x, prevOn.y)
            else:
                prevOut = nextSegment.offCurve[0]
                prevOutX, prevOutY = (prevOut.x, prevOut.y)
            newSegment = self.insertSegment(
                index,
                type="curve",
                points=[(prevOutX, prevOutY), anchor, anchor],
                smooth=False
            )
            segments = self.segments
            p = index - 1
            if p < 0:
                p = -1
            prevSegment = segments[p]
            n = index + 1
            if n >= len(segments):
                n = 0
            nextSegment = segments[n]
            if nextSegment.type == "move":
                raise FontPartsError("still working out curving at the end of a contour")
            elif nextSegment.type == "qcurve":
                return
            # set the new incoming bcp
            newIn = newSegment.offCurve[1]
            nIX, nIY = absoluteBCPIn(anchor, bcpIn)
            newIn.x = nIX
            newIn.y = nIY
            # set the new outgoing bcp
            hasCurve = True
            if nextSegment.type != "curve":
                if bcpOut != (0, 0):
                    nextSegment.type = "curve"
                    hasCurve = True
                else:
                    hasCurve = False
            if hasCurve:
                newOut = nextSegment.offCurve[0]
                nOX, nOY = absoluteBCPOut(anchor, bcpOut)
                newOut.x = nOX
                newOut.y = nOY
            # now check to see if we can convert the curve segment to a line segment
            newAnchor = newSegment.onCurve
            newA = newSegment.offCurve[0]
            newB = newSegment.offCurve[1]
            nextAnchor = nextSegment.onCurve
            prevAnchor = prevSegment.onCurve
            if (prevAnchor.x, prevAnchor.y) == (newA.x, newA.y) and (newAnchor.x, newAnchor.y) == (newB.x, newB.y):
                newSegment.type = "line"
            # the user wants a smooth segment
            if type == "curve":
                newSegment.smooth = True

    def removeBPoint(self, bPoint, **kwargs):
        """
        Remove the bpoint from the contour.
        bpoint can be a point object or an index.
        """
        if not isinstance(bPoint, int):
            bPoint = bPoint.index
        bPoint = normalizers.normalizeIndex(bPoint)
        if bPoint >= self._len__points():
            raise FontPartsError("No bPoint located at index %d." % bPoint)
        self._removeBPoint(bPoint, **kwargs)

    def _removeBPoint(self, index, **kwargs):
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

    def _setContourInPoint(self, point):
        if point.contour is None:
            point.contour = self

    points = dynamicProperty("points")

    def _get_points(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__points(i) for i in range(self._len__points())])

    def _len__points(self):
        return self._lenPoints()

    def _lenPoints(self, **kwargs):
        """
        This must return an integer indicating
        the number of points in the contour.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__points(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__points():
            raise FontPartsError("No point located at index %d." % index)
        point = self._getPoint(index)
        self._setContourInPoint(point)
        return point

    def _getPoint(self, index, **kwargs):
        """
        This must return a wrapped point.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getPointIndex(self, point):
        for i, other in enumerate(self.points):
            if point == other:
                return i
        raise FontPartsError("The point could not be found.")

    def appendPoint(self, position, type="line", smooth=False, name=None, identifier=None, **kwargs):
        """
        Append a point to the contour.
        """
        self.insertPoint(len(self.points), position=position, type=type, smooth=smooth, name=name, identifier=identifier, **kwargs)

    def insertPoint(self, index, position, type="line", smooth=False, name=None, identifier=None, **kwargs):
        """
        Insert a point into the contour.
        """
        index = normalizers.normalizeIndex(index)
        position = normalizers.normalizeCoordinateTuple(position)
        type = normalizers.normalizePointType(type)
        smooth = normalizers.normalizeBoolean(smooth)
        if name is not None:
            name = normalizers.normalizePointName(name)
        if identifier is not None:
            identifier = normalizers.normalizeIdentifier(identifier)
        self._insertPoint(index, position=position, type=type, smooth=smooth, name=name, identifier=identifier, **kwargs)

    def _insertPoint(self, index, position, type="line", smooth=False, name=None, identifier=None, **kwargs):
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

    def removePoint(self, point, **kwargs):
        """
        Remove the point from the contour.
        point can be a point object or an index.
        """
        if not isinstance(point, int):
            point = self.points.index(point)
        point = normalizers.normalizeIndex(point)
        if point >= self._len__points():
            raise FontPartsError("No point located at index %d." % point)
        self._removePoint(point, **kwargs)

    def _removePoint(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()
