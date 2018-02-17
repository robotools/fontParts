import os
from copy import deepcopy
import fontMath
from fontTools.misc.py23 import basestring
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject, TransformationMixin, dynamicProperty, interpolate)
from fontParts.base.image import BaseImage
from fontParts.base import normalizers
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedGlyph, RemovedGlyph


class BaseGlyph(BaseObject, TransformationMixin, DeprecatedGlyph, RemovedGlyph):

    """
        Glyph object.
    """

    copyAttributes = (
        "name",
        "unicodes",
        "width",
        "height",
        "note",
        "markColor",
        "lib"
    )

    def _reprContents(self):
        contents = [
            "'%s'" % self.name,
        ]
        if self.layer is not None:
            contents.append("('%s')" % self.layer.name)
        return contents

    def __hash__(self):
        """
        Allow glyph object to be used as a key
        in a dictionary.
        
        Subclasses may override this method.
        """
        return id(self.naked())

    def copy(self):
        """
        Copy the glyph into a new glyph that does not
        belong to a glyph.

            >>> copiedGlyph = glyph.copy()

        This will copy:

        - name
        - unicodes
        - width
        - height
        - note
        - markColor
        - lib
        - contours
        - components
        - anchors
        - guidelines
        - image
        """
        return super(BaseGlyph, self).copy()

    def copyData(self, source):
        super(BaseGlyph, self).copyData(source)
        pen = self.getPointPen()
        source.drawPoints(pen)
        for sourceAnchor in source.anchors:
            self.appendAnchor(sourceAnchor.name, (sourceAnchor.x, sourceAnchor.y), sourceAnchor.color)
        for sourceGuideline in self.guidelines:
            selfGuideline = self.appendGuideline(
                (sourceGuideline.x, sourceGuideline.y),
                sourceGuideline.angle,
                sourceGuideline.name,
                sourceGuideline.color
            )
        sourceImage = source.image
        if sourceImage.data is not None:
            selfImage = self.addImage(data=sourceImage.data)
            selfImage.transformation = sourceImage.transformation
            selfImage.color = sourceImage.color

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.font

    # Layer

    _layer = None

    layer = dynamicProperty(
        "layer",
        """
        The glyph's parent layer.

            >>> layer = glyph.layer
        """
    )

    def _get_layer(self):
        if self._layer is None:
            return None
        return self._layer

    def _set_layer(self, layer):
        self._layer = layer

    # Font

    font = dynamicProperty(
        "font",
        """
        The glyph's parent font.

            >>> font = glyph.font
        """
    )

    def _get_font(self):
        if self._layer is None:
            return None
        return self.layer.font

    # --------------
    # Identification
    # --------------

    # Name

    name = dynamicProperty(
        "base_name",
        """
        The glyph's name.

            >>> glyph.name
            "A"
            >>> glyph.name = "A.alt"
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGlyphName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        value = normalizers.normalizeGlyphName(value)
        layer = self.layer
        if layer is not None and value in layer:
            raise FontPartsError("A glyph with the name '%s' already exists." % value)
        self._set_name(value)

    def _get_name(self):
        """
        Get the name of the glyph.
        This must return a unicode string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        Set the name of the glyph.
        This will be a unicode string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # Unicodes

    unicodes = dynamicProperty(
        "base_unicodes",
        """
        The glyph's unicode values in order from most to least important.

            >>> glyph.unicodes
            [65]
            >>> glyph.unicodes = [65, 0x42]
            >>> glyph.unicodes = []

        The values in the returned list will be integers.
        When setting you may send int or hex values.
        """
    )

    def _get_base_unicodes(self):
        value = self._get_unicodes()
        value = normalizers.normalizeGlyphUnicodes(value)
        value = tuple(value)
        return value

    def _set_base_unicodes(self, value):
        value = list(value)
        value = normalizers.normalizeGlyphUnicodes(value)
        self._set_unicodes(value)

    def _get_unicodes(self):
        """
        Get the unicodes assigned to the glyph.
        This must return a list of zero or more integers.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_unicodes(self, value):
        """
        Assign the unicodes to the glyph.
        This will be a list of zero or more integers.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    unicode = dynamicProperty(
        "base_unicode",
        """
        The glyph's primary unicode value.

            >>> glyph.unicode
            65
            >>> glyph.unicode = None

        The returned value will be an integer or None.
        When setting you may send int or hex values or None.
        """
    )

    def _get_base_unicode(self):
        value = self._get_unicode()
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
        return value

    def _set_base_unicode(self, value):
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
            self._set_unicode(value)
        else:
            self._set_unicodes(())

    def _get_unicode(self):
        """
        Get the primary unicode assigned to the glyph.
        This must return an integer or None.

        Subclasses may override this method.
        """
        values = self.unicodes
        if values:
            return values[0]
        return None

    def _set_unicode(self, value):
        """
        Assign the primary unicode to the glyph.
        This will be an integer or None.

        Subclasses may override this method.
        """
        values = list(self.unicodes)
        if value in values:
            values.remove(value)
        values.insert(0, value)
        self.unicodes = values

    def autoUnicodes(self):
        """
        Use heuristics to set the Unicode values in the glyph.

            >>> glyph.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -------
    # Metrics
    # -------

    # horizontal

    width = dynamicProperty(
        "base_width",
        """
        The glyph's width.

            >>> glyph.width
            500
            >>> glyph.width = 200
        """
    )

    def _get_base_width(self):
        value = self._get_width()
        value = normalizers.normalizeGlyphWidth(value)
        return value

    def _set_base_width(self, value):
        value = normalizers.normalizeGlyphWidth(value)
        self._set_width(value)

    def _get_width(self):
        """
        This must return an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_width(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    leftMargin = dynamicProperty(
        "base_leftMargin",
        """
        The glyph's left margin.

            >>> glyph.leftMargin
            35
            >>> glyph.leftMargin = 45
        """
    )

    def _get_base_leftMargin(self):
        value = self._get_leftMargin()
        value = normalizers.normalizeGlyphLeftMargin(value)
        return value

    def _set_base_leftMargin(self, value):
        value = normalizers.normalizeGlyphLeftMargin(value)
        self._set_leftMargin(value)

    def _get_leftMargin(self):
        """
        This must return an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return 0
        xMin, yMin, xMax, yMax = bounds
        return xMin

    def _set_leftMargin(self, value):
        """
        value will be an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        diff = value - self.leftMargin
        self.moveBy((diff, 0))
        self.width += diff

    rightMargin = dynamicProperty(
        "base_rightMargin",
        """
        The glyph's right margin.

            >>> glyph.rightMargin
            35
            >>> glyph.rightMargin = 45
        """
    )

    def _get_base_rightMargin(self):
        value = self._get_rightMargin()
        value = normalizers.normalizeGlyphRightMargin(value)
        return value

    def _set_base_rightMargin(self, value):
        value = normalizers.normalizeGlyphRightMargin(value)
        self._set_rightMargin(value)

    def _get_rightMargin(self):
        """
        This must return an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return self.width
        xMin, yMin, xMax, yMax = bounds
        return self.width - xMax

    def _set_rightMargin(self, value):
        """
        value will be an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            self.width = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.width = xMax + value

    # vertical

    height = dynamicProperty(
        "base_height",
        """
        The glyph's height.

            >>> glyph.height
            500
            >>> glyph.height = 200
        """
    )

    def _get_base_height(self):
        value = self._get_height()
        value = normalizers.normalizeGlyphHeight(value)
        return value

    def _set_base_height(self, value):
        value = normalizers.normalizeGlyphHeight(value)
        self._set_height(value)

    def _get_height(self):
        """
        This must return an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_height(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    bottomMargin = dynamicProperty(
        "base_bottomMargin",
        """
        The glyph's bottom margin.

            >>> glyph.bottomMargin
            35
            >>> glyph.bottomMargin = 45
        """
    )

    def _get_base_bottomMargin(self):
        value = self._get_bottomMargin()
        value = normalizers.normalizeGlyphBottomMargin(value)
        return value

    def _set_base_bottomMargin(self, value):
        value = normalizers.normalizeGlyphBottomMargin(value)
        self._set_bottomMargin(value)

    def _get_bottomMargin(self):
        """
        This must return an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return 0
        xMin, yMin, xMax, yMax = bounds
        return yMin

    def _set_bottomMargin(self, value):
        """
        value will be an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        diff = value - self.bottomMargin
        self.moveBy((0, diff))
        self.height += diff

    topMargin = dynamicProperty(
        "base_topMargin",
        """
        The glyph's top margin.

            >>> glyph.topMargin
            35
            >>> glyph.topMargin = 45
        """
    )

    def _get_base_topMargin(self):
        value = self._get_topMargin()
        value = normalizers.normalizeGlyphTopMargin(value)
        return value

    def _set_base_topMargin(self, value):
        value = normalizers.normalizeGlyphTopMargin(value)
        self._set_topMargin(value)

    def _get_topMargin(self):
        """
        This must return an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return self.height
        xMin, yMin, xMax, yMax = bounds
        return self.height - yMax

    def _set_topMargin(self, value):
        """
        value will be an int or float.

        XXX define equation

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            self.height = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.height = yMax + value

    # ----
    # Pens
    # ----

    def getPen(self):
        """
        Return a Pen object for modifying the glyph.

            >>> pen = glyph.getPen()
        """
        self.raiseNotImplementedError()

    def getPointPen(self):
        """
        Return a PointPen object for modifying the glyph.

            >>> pointPen = glyph.getPointPen()
        """
        self.raiseNotImplementedError()

    def draw(self, pen, contours=True, components=True):
        """
        Draw the glyph with the given Pen.

            >>> glyph.draw(pen)
            >>> glyph.draw(pen, contours=True, components=False)
        """
        if contours:
            for contour in self:
                contour.draw(pen)
        if components:
            for component in self.components:
                component.draw(pen)

    def drawPoints(self, pen, contours=True, components=True):
        """
        Draw the glyph with the given PointPen.

            >>> glyph.drawPoints(pointPen)
            >>> glyph.drawPoints(pointPen, contours=True, components=False)
        """
        if contours:
            for contour in self:
                contour.drawPoints(pen)
        if components:
            for component in self.components:
                component.drawPoints(pen)

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    def clear(self, contours=True, components=True, anchors=True, guidelines=True, image=True):
        """
        Clear the glyph.

            >>> glyph.clear()

        This clears:

        - contours
        - components
        - anchors
        - guidelines
        - image

        It's possible to selectively turn off the clearing
        of portions of the glyph with the arguments.
        """
        self._clear(contours=contours, components=components, anchors=anchors, guidelines=guidelines, image=image)

    def _clear(self, contours=True, components=True, anchors=True, guidelines=True, image=True):
        """
        Subclasses may override this method.
        """
        if contours:
            self.clearContours()
        if components:
            self.clearComponents()
        if anchors:
            self.clearAnchors()
        if guidelines:
            self.clearGuidelines()
        if image:
            self.clearImage()

    def appendGlyph(self, other, offset=None):
        """
        Append copies of the contours, components,
        anchors and guidelines from other.

            >>> glyph.appendGlyph(otherGlyph)
            >>> glyph.appendGlyph(otherGlyph, (100, 0))

        offset indicates the offset that should
        be applied to the appended data. The default
        is (0, 0).
        """
        if offset is None:
            offset = (0, 0)
        offset = normalizers.normalizeTransformationOffset(offset)
        self._appendGlyph(other, offset)

    def _appendGlyph(self, other, offset=None):
        """
        Subclasses may override this method.
        """
        other = other.copy()
        if offset != (0, 0):
            other.moveBy(offset)
        pen = self.getPointPen()
        other.drawPoints(pen)
        for guideline in other.guidelines:
            self.appendGuideline(
                (guideline.x, guideline.y),
                guideline.angle,
                guideline.name,
                guideline.color
                # XXX the identifier is lost here
            )

    # Contours

    def _setGlyphInContour(self, contour):
        if contour.glyph is None:
            contour.glyph = self

    contours = dynamicProperty(
        "contours",
        """
        An immutable list of contours in the glyph.

            >>> for contour in glyph.contours:
            ...     contour.bounds
            (10, 15, 57, 36)
            (875, 35, 926, 647)
        """
    )

    def _get_contours(self):
        """
        Subclasses may override this method.
        """
        return tuple([self[i] for i in range(len(self))])

    def __len__(self):
        """
        The number of contours in the glyph.

            >>> len(glyph)
            2
        """
        return self._lenContours()

    def _lenContours(self, **kwargs):
        """
        This must return an integer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __iter__(self):
        """
        Iterate through the contours in the glyph.

            >>> for contour in glyph:
            ...     contour.bounds
            (10, 15, 57, 36)
            (875, 35, 926, 647)
        """
        return self._iterContours()

    def _iterContours(self, **kwargs):
        """
        This must return an iterator that returns wrapped contours.

        Subclasses may override this method.
        """
        count = len(self)
        index = 0
        while count:
            yield self[index]
            count -= 1
            index += 1

    def __getitem__(self, index):
        """
        Get the contour located at index from the glyph.

            >>> contour = glyph[0]
        """
        index = normalizers.normalizeContourIndex(index)
        if index >= len(self):
            raise FontPartsError("No contour located at index %d." % index)
        contour = self._getContour(index)
        self._setGlyphInContour(contour)
        return contour

    def _getContour(self, index, **kwargs):
        """
        This must return a wrapped contour.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getContourIndex(self, contour):
        for i, other in enumerate(self.contours):
            if contour == other:
                return i
        raise FontPartsError("The contour could not be found.")

    def appendContour(self, contour, offset=None):
        """
        A copy of the given contour to the glyph.

            >>> contour = glyph.appendContour(contour)
            >>> contour = glyph.appendContour(contour, (100, 0))

        offset indicates the distance that the
        contour should be offset when added to
        the glyph. The default is (0, 0).
        """
        contour = normalizers.normalizeContour(contour)
        if offset is None:
            offset = (0, 0)
        offset = normalizers.normalizeTransformationOffset(offset)
        return self._appendContour(contour, offset)

    def _appendContour(self, contour, offset=None, **kwargs):
        """
        contour will be an object with a drawPoints method.

        offset will be a valid offset (x, y).

        This must return the new contour.

        Subclasses may override this method.
        """
        copy = contour.copy()
        if offset != (0, 0):
            copy.moveBy(offset)
        pointPen = self.getPointPen()
        contour.drawPoints(pointPen)
        return self[-1]

    def removeContour(self, contour):
        """
        Remove the contour from the glyph.

            >>> glyph.removeContour(contour)
            >>> glyph.removeContour(0)

        Contour may be a contour object or a contour index.
        """
        if isinstance(contour, int):
            index = contour
        else:
            index = self._getContourIndex(contour)
        index = normalizers.normalizeContourIndex(index)
        if index >= len(self):
            raise FontPartsError("No contour located at index %d." % index)
        self._removeContour(index)

    def _removeContour(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearContours(self):
        """
        Clear all contours.

            >>> glyph.clearContours()
        """
        self._clearContours()

    def _clearContours(self):
        """
        Subclasses may override this method.
        """
        for i in range(len(self)):
            self.removeContour(-1)

    def removeOverlap(self):
        """
        Perform a remove overlap operation on the contours.

            >>> glyph.removeOverlap()
        """

    def _removeOverlap(self):
        """
        Subclasses must implement this method.
        """
        self.raiseNotImplementedError()

    # Components

    def _setGlyphInComponent(self, component):
        if component.glyph is None:
            component.glyph = self

    components = dynamicProperty(
        "components",
        """
        An immutable list of components in the glyph.

            >>> for component in glyph.components:
            ...     component.baseGlyph
            "A"
            "acute"
        """
    )

    def _get_components(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__components(i) for i in range(self._len__components())])

    def _len__components(self):
        return self._lenComponents()

    def _lenComponents(self, **kwargs):
        """
        This must return an integer indicating
        the number of components in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__components(self, index):
        index = normalizers.normalizeComponentIndex(index)
        if index >= self._len__components():
            raise FontPartsError("No component located at index %d." % index)
        component = self._getComponent(index)
        self._setGlyphInComponent(component)
        return component

    def _getComponent(self, index, **kwargs):
        """
        This must return a wrapped contour.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getComponentIndex(self, component):
        for i, other in enumerate(self.components):
            if component == other:
                return i
        raise FontPartsError("The component could not be found.")

    def appendComponent(self, baseGlyph, offset=None, scale=None):
        """
        Append a new component to the glyph.

            >>> component = glyph.appendComponent("A")
            >>> component = glyph.appendComponent("acute", offset=(20, 200))

        baseGlyph indicates the glyph that the
        component will reference.
        offset indictaes the offset that should
        be defined in the component. The default
        is (0, 0).
        scale indicates the scale that should be
        defined in the component. The default is
        (1.0, 1.0).
        """
        baseGlyph = normalizers.normalizeGlyphName(baseGlyph)
        if self.name == baseGlyph:
            raise FontPartsError("A glyph cannot contain a component referencing itself.")
        if offset is None:
            offset = (0, 0)
        if scale is None:
            scale = (1, 1)
        offset = normalizers.normalizeTransformationOffset(offset)
        scale = normalizers.normalizeTransformationScale(scale)
        ox, oy = offset
        sx, sy = scale
        transformation = (sx, 0, 0, sy, ox, oy)
        return self._appendComponent(baseGlyph, transformation=transformation)

    def _appendComponent(self, baseGlyph, transformation=None, **kwargs):
        """
        baseGlyph will be a valid glyph name.
        The baseGlyph may or may not be in the layer.

        offset will be a valid offset (x, y).
        scale will be a valid scale (x, y).

        This must return the new component.

        Subclasses may override this method.
        """
        pointPen = self.getPointPen()
        pointPen.addComponent(baseGlyph, transformation=transformation)
        return self.components[-1]

    def removeComponent(self, component):
        """
        Remove component from the glyph.

            >>> glyph.removeComponent(component)
            >>> glyph.removeComponent(1)

        component can be a component object or an
        integer representing the component index.
        """
        if isinstance(component, int):
            index = component
        else:
            index = self._getComponentIndex(component)
        index = normalizers.normalizeComponentIndex(index)
        if index >= self._len__components():
            raise FontPartsError("No component located at index %d." % index)
        self._removeComponent(index)

    def _removeComponent(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearComponents(self):
        """
        Clear all components.

            >>> glyph.clearComponents()
        """
        self._clearComponents()

    def _clearComponents(self):
        """
        Subclasses may override this method.
        """
        for i in range(self._len__components()):
            self.removeComponent(-1)

    def decompose(self):
        """
        Decompose all components.

            >>> glyph.decompose()
        """
        self._decompose()

    def _decompose(self):
        """
        Subclasses may override this method.
        """
        for component in self.components:
            component.decompose()

    # Anchors

    def _setGlyphInAnchor(self, anchor):
        if anchor.glyph is None:
            anchor.glyph = self

    anchors = dynamicProperty(
        "anchors",
        """
        An immutable list of anchors in the glyph.

            >>> for anchor in glyph.anchors:
            ...     anchor.name
            "top"
        """
    )

    def _get_anchors(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__anchors(i) for i in range(self._len__anchors())])

    def _len__anchors(self):
        return self._lenAnchors()

    def _lenAnchors(self, **kwargs):
        """
        This must return an integer indicating
        the number of anchors in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__anchors(self, index):
        index = normalizers.normalizeAnchorIndex(index)
        if index >= self._len__anchors():
            raise FontPartsError("No anchor located at index %d." % index)
        anchor = self._getAnchor(index)
        self._setGlyphInAnchor(anchor)
        return anchor

    def _getAnchor(self, index, **kwargs):
        """
        This must return a wrapped anchor.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getAnchorIndex(self, anchor):
        for i, other in enumerate(self.anchors):
            if anchor == other:
                return i
        raise FontPartsError("The anchor could not be found.")

    def appendAnchor(self, name, position, color=None):
        """
        Append a new anchor to the glyph.

            >>> anchor = glyph.appendAnchor("top", (50, 500))
            >>> anchor = glyph.appendAnchor("top", (50, 500), (1, 0, 0, 0.5))

        name indicates the name that should be
        assigned to the anchor.
        position is an (x, y) tuple defining
        the position for the anchor.
        color is None or a color tuple.
        """
        name = normalizers.normalizeAnchorName(name)
        position = normalizers.normalizeCoordinateTuple(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        return self._appendAnchor(name, position=position, color=color)

    def _appendAnchor(self, name, position=None, color=None, **kwargs):
        """
        name will be a valid anchor name.
        position will be a valid position (x, y).
        color will be None or a valid color.

        This must return the new anchor.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeAnchor(self, anchor):
        """
        Remove anchor from the glyph.

            >>> glyph.removeAnchor(anchor)
            >>> glyph.removeAnchor(2)

        anchor can be a anchor object or an
        integer representing the anchor index.
        """
        if isinstance(anchor, int):
            index = anchor
        else:
            index = self._getAnchorIndex(anchor)
        index = normalizers.normalizeAnchorIndex(index)
        if index >= self._len__anchors():
            raise FontPartsError("No anchor located at index %d." % index)
        self._removeAnchor(index)

    def _removeAnchor(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearAnchors(self):
        """
        Clear all anchors.

            >>> glyph.clearAnchors()
        """
        self._clearAnchors()

    def _clearAnchors(self):
        """
        Subclasses may override this method.
        """
        for i in range(self._len__anchors()):
            self.removeAnchor(-1)

    # ----------
    # Guidelines
    # ----------

    def _setGlyphInGuideline(self, guideline):
        if guideline.glyph is None:
            guideline.glyph = self

    guidelines = dynamicProperty(
        "guidelines",
        """
        An immutable list of font-level guidelines.

            >>> for guideline in glyph.guidelines:
            ...     guideline.angle
            0
            45
            90
        """
    )

    def _get_guidelines(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__guidelines(i) for i in range(self._len__guidelines())])

    def _len__guidelines(self):
        return self._lenGuidelines()

    def _lenGuidelines(self, **kwargs):
        """
        This must return an integer indicating
        the number of guidelines in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index):
        index = normalizers.normalizeGuidelineIndex(index)
        if index >= self._len__guidelines():
            raise FontPartsError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setGlyphInGuideline(guideline)
        return guideline

    def _getGuideline(self, index, **kwargs):
        """
        This must return a wrapped guideline.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getGuidelineIndex(self, guideline):
        for i, other in enumerate(self.guidelines):
            if guideline == other:
                return i
        raise FontPartsError("The guideline could not be found.")

    def appendGuideline(self, position, angle, name=None, color=None):
        """
        Append a new guideline to the glyph.

            >>> guideline = glyph.appendGuideline((50, 0), 90)
            >>> guideline = glyph.appendGuideline((0, 540), 0, name="overshoot", color=(0, 0, 0, 0.2))

        position (x, y) indicates the position of the guideline.
        angle indicates the angle of the guideline.
        name indicates the name for the guideline.
        color indicates the color for the guideline.

        """
        position = normalizers.normalizeCoordinateTuple(position)
        angle = normalizers.normalizeGuidelineAngle(angle)
        if name is not None:
            name = normalizers.normalizeGuidelineName(name)
        if color is not None:
            color = normalizers.normalizeColor(color)
        return self._appendGuideline(position, angle, name=name, color=color)

    def _appendGuideline(self, position, angle, name=None, color=None, **kwargs):
        """
        position will be a valid position (x, y).
        angle will be a valida angle.
        name will be a valid guideline name or None.
        color will be a valid color or None .

        This must return the new guideline.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove guideline from the glyph.

            >>> glyph.removeGuideline(guideline)
            >>> glyph.removeGuideline(2)

        guideline can be a guideline object or an
        integer representing the guideline index.
        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(guideline)
        index = normalizers.normalizeGuidelineIndex(index)
        if index >= self._len__guidelines():
            raise FontPartsError("No guideline located at index %d." % index)
        self._removeGuideline(index)

    def _removeGuideline(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearGuidelines(self):
        """
        Clear all guidelines.

            >>> glyph.clearGuidelines()
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        Subclasses may override this method.
        """
        for i in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # ------------------
    # Data Normalization
    # ------------------

    def round(self):
        """
        Round coordinates.

            >>> glyph.round()

        This applies to the following:

        - width
        - height
        - contours
        - components
        - anchors
        - guidelines
        """
        self._round()

    def _round(self):
        """
        Subclasses may override this method.
        """
        self.width = normalizers.normalizeRounding(self.width)
        for contour in self.contours:
            contour.round()
        for component in self.components:
            component.round()
        for anchor in self.anchors:
            anchor.round()
        for guideline in self.guidelines:
            guideline.round()

    def correctDirection(self, trueType=False):
        """
        Correct the direction of the contours in the glyph.

            >>> glyph.correctDirection()
        """
        self._correctDirection(trueType=trueType)

    def _correctDirection(self, trueType=False, **kwargs):
        """
        XXX

        This could be ported from RoboFab, however
        that algorithm is not robust enough. Specifically
        it relies on bounds and hit testing to
        determine nesting.

        XXX
        """
        self.raiseNotImplementedError()

    def autoContourOrder(self):
        """
        Sort the contours based on their centers.

            >>> glyph.autoContourOrder()
        """
        self._autoContourOrder()

    def _autoContourOrder(self, **kwargs):
        """
        XXX

        This can be ported from RoboFab.

        XXX
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        XXX should this apply to the width and height?

        Subclasses may override this method.
        """
        for contour in self.contours:
            contour.transformBy(matrix, origin=origin)
        for component in self.components:
            component.transformBy(matrix, origin=origin)
        for anchor in self.anchors:
            anchor.transformBy(matrix, origin=origin)
        for guideline in self.guidelines:
            guideline.transformBy(matrix, origin=origin)

    # --------------------
    # Interpolation & Math
    # --------------------

    def toMathGlyph(self):
        """
        Returns the glyph as a MathGlyph.

            >>> mg = glyph.toMathGlyph()
        """
        return self._toMathGlyph()

    def _toMathGlyph(self):
        mathGlyph = fontMath.MathGlyph(None)
        pen = mathGlyph.getPointPen()
        self.drawPoints(pen)
        for anchor in self.anchors:
            d = dict(
                x=anchor.x,
                y=anchor.y,
                name=anchor.name,
                identifier=anchor.identifier,
                color=anchor.color
            )
            mathGlyph.anchors.append(d)
        for guideline in self.guidelines:
            d = dict(
                x=guideline.x,
                y=guideline.y,
                angle=guideline.angle,
                name=guideline.name,
                identifier=guideline.identifier,
                color=guideline.color
            )
            mathGlyph.guidelines.append(d)
        image = self.image
        mathGlyph.image = dict(
            # MathGlyph works with image file names, hack
            # around it by using the data as the file name.
            fileName=image.data,
            transformation=image.transformation,
            color=image.color
        )
        mathGlyph.lib = deepcopy(self.lib)
        mathGlyph.name = self.name
        mathGlyph.unicodes = self.unicodes
        mathGlyph.width = self.width
        mathGlyph.height = self.height
        mathGlyph.note = self.note
        return mathGlyph

    def fromMathGlyph(self, mathGlyph):
        """
        Replaces the glyph with the contents of a MathGlyph.

            >>> glyph = glyph.fromMathGlyph(mg)

        mathGlyph is the mathGlyph to put into the current glyph.
        """
        return self._fromMathGlyph(mathGlyph, toThisGlyph=True)

    def _fromMathGlyph(self, mathGlyph, toThisGlyph=False):
        # make the destination
        if toThisGlyph:
            copied = self
            copied.clear()
        else:
            copyClass = self.copyClass
            if copyClass is None:
                copyClass = self.__class__
            copied = copyClass()
        # populate
        pen = copied.getPointPen()
        mathGlyph.drawPoints(pen, filterRedundantPoints=True)
        for anchor in mathGlyph.anchors:
            copied.appendAnchor(
                name=anchor["name"],
                position=(anchor["x"], anchor["y"]),
                color=anchor["color"],
                # XXX identifier is lost
            )
        for guideline in mathGlyph.guidelines:
            copied.appendGuideline(
                position=(guideline["x"], guideline["y"]),
                angle=guideline["angle"],
                name=guideline["name"],
                color=guideline["color"],
                # XXX identifier is lost
            )
        data = mathGlyph.image["fileName"]  # see _toMathGlyph
        if data is not None:
            image = self.image
            image.data = data
            image.transformation = mathGlyph.image["transformation"]
            image.color = mathGlyph.image["color"]
        copied.lib.update(mathGlyph.lib)
        if not toThisGlyph:
            copied.name = mathGlyph.name
            copied.unicodes = mathGlyph.unicodes
        copied.width = mathGlyph.width
        copied.height = mathGlyph.height
        copied.note = mathGlyph.note
        return copied

    def __mul__(self, factor):
        """
        Subclasses may override this method.
        """
        mathGlyph = self._toMathGlyph()
        result = mathGlyph * factor
        copied = self._fromMathGlyph(result)
        return copied

    __rmul__ = __mul__

    def __truediv__(self, factor):
        """
        Subclasses may override this method.
        """
        mathGlyph = self._toMathGlyph()
        result = mathGlyph / factor
        copied = self._fromMathGlyph(result)
        return copied

    # py2 support
    __div__ = __truediv__

    def __add__(self, other):
        """
        Subclasses may override this method.
        """
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph + otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def __sub__(self, other):
        """
        Subclasses may override this method.
        """
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def interpolate(self, factor, minGlyph, maxGlyph, round=True, suppressError=True):
        """
        Interpolate all possible data in the glyph.

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2)
            >>> glyph.interpolate((0.5, 2.0), otherGlyph1, otherGlyph2, round=False)

        The interpolation occurs on a 0 to 1.0 range where minGlyph
        is located at 0 and maxGlyph is located at 1.0.

        factor is the interpolation value. It may be less than 0
        and greater than 1.0. It may be a number (integer, float)
        or a tuple of two numbers. If it is a tuple, the first
        number indicates the x factor and the second number
        indicates the y factor.

        round indicates if the result should be rounded to integers.

        suppressError indicates if incompatible data should be ignored
        or if an error should be raised when such incompatibilities are found.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minGlyph, BaseGlyph):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minGlyph.__class__.__name__))
        if not isinstance(maxGlyph, BaseGlyph):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxGlyph.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minGlyph, maxGlyph, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minGlyph, maxGlyph, round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        minGlyph = minGlyph._toMathGlyph()
        maxGlyph = maxGlyph._toMathGlyph()
        try:
            result = interpolate(minGlyph, maxGlyph, factor)
        except IndexError:
            result = None
        if result is None and not suppressError:
            raise FontPartsError("Glyphs '%s' and '%s' could not be interpolated." % (minGlyph.name, maxGlyph.name))
        if result is not None:
            if round:
                result = result.round()
            self._fromMathGlyph(result, toThisGlyph=True)

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with other.

            >>> compat, report = self.isCompatible(otherFont)
            >>> compat
            False
            >>> report
            [Fatal] The glyphs do not contain the same number of contours.

        Returns a boolean indicating if the glyph is compatible for
        interpolation with other and a string of compatibility notes.
        """
        if not isinstance(other, BaseGlyph):
            raise FontPartsError("Compatibility between an instance of %r and an instance of %r can not be checked." % (self.__class__.__name__, other.__class__.__name__))
        return self._isCompatible(other)

    def _isCompatible(self, other):
        """
        Subclasses may override this method.
        """
        compatable = True
        report = []
        # contour count
        if len(self.contours) != len(other.contours):
            report.append("[Fatal] The glyphs do not contain the same number of contours.")
            compatable = False
        # on curve point count
        for i in range(min(len(self.contours), len(other.contours))):
            selfContour = self[i]
            otherContour = other[i]
            if len(selfContour.segments) != len(otherContour.segments):
                report.append("[Fatal] Contour %d contains a different number of segments." % i)
                compatable = False
        # incompatible components
        selfComponentBases = []
        otherComponentBases = []
        for source, names in ((self, selfComponentBases), (other, otherComponentBases)):
            for component in source.components:
                names.append(component.baseGlyph)
            names.sort()
        if selfComponentBases != otherComponentBases:
            report.append("[Warning] The glyphs do not contain anchors with exactly the same names.")
        # incompatible anchors
        selfAnchorNames = []
        otherAnchorNames = []
        for source, names in ((self, selfAnchorNames), (other, otherAnchorNames)):
            for anchor in source.anchors:
                names.append(anchor.name)
            names.sort()
        if selfAnchorNames != otherAnchorNames:
            report.append("[Warning] The glyphs do not contain components with exactly the same base glyphs.")
        # incompatible guidelines
        if len(self.guidelines) != len(other.guidelines):
            report.append("[Note] The glyphs do not contain the same number of guidelines.")
        # done
        return compatable, "\n".join(report)

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point):
        """
        Determine if point is in the black or white of the glyph.

            >>> glyph.pointInside((40, 65))
            True

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

    bounds = dynamicProperty(
        "bounds",
        """
        The bounds of the glyph: (xMin, yMin, xMax, yMax) or None.

            >>> glyph.bounds
            (10, 30, 765, 643)
        """
    )

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

    # -----------------
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "layers",
        """
        Immutable list of the glyph's layers.

            >>> for glyphLayer in glyph.layers:
            ...     len(glyphLayer)
            3
            2
        """
    )

    def _get_layers(self, **kwargs):
        font = self.font
        if font is None:
            return tuple()
        glyphs = []
        for layer in font.layers:
            if self.name in layer:
                glyphs.append(layer[self.name])
        return tuple(glyphs)

    # get

    def getLayer(self, name, **kwargs):
        """
        Get the glyph layer with name in this glyph.

            >>> glyphLayer = glyph.getLayer("foreground")
        """
        name = normalizers.normalizeLayerName(name)
        return self._getLayer(name, **kwargs)

    def _getLayer(self, name, **kwargs):
        """
        name will be a string, but there may not be a
        layer with a name matching the string. If not,
        a FontPartsError must be raised.

        Subclasses may override this method.
        """
        for glyph in self.layers:
            if glyph.layer.name == name:
                return glyph
        raise FontPartsError("No layer named '%s' in glyph '%s'." % (name, self.name))

    # new

    def newLayer(self, name, **kwargs):
        """
        Make a new layer with name in this glyph.

            >>> glyphLayer = glyph.newLayer("background")

        This is the equivalent of using the newGlyph
        method on a named layer. If the glyph already
        exists in the layer it will be cleared.
        Return the new glyph layer.
        """
        layerName = name
        glyphName = self.name
        layerName = normalizers.normalizeLayerName(layerName)
        for glyph in self.layers:
            if glyph.layer.name == layerName:
                layer = glyph.layer
                layer.removeGlyph(glyphName)
                break
        glyph = self._newLayer(name=layerName, **kwargs)
        layer = self.font.getLayer(layerName)
        # layer._setLayerInGlyph(glyph)
        return glyph

    def _newLayer(self, name, **kwargs):
        """
        name will be a string representing a valid layer
        name. The name will have been tested to make sure
        that no layer in the glyph already has the name.

        This must returned the new glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, layer, **kwargs):
        """
        Remove the layer from the glyph (not the font).

            >>> glyph.removeLayer("background")

        Layer can be a glyph layer or a layer name.
        """
        if not isinstance(layer, basestring):
            layer = layer.layer.name
        layerName = layer
        glyphName = self.name
        layerName = normalizers.normalizeLayerName(layerName)
        found = False
        for glyph in self.layers:
            if glyph.layer.name == layerName:
                found = True
                break
        if found:
            self._removeLayer(layerName, **kwargs)

    def _removeLayer(self, name, **kwargs):
        """
        name will be a valid layer name. It will
        represent an existing layer in the font.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # -----
    # Image
    # -----

    image = dynamicProperty("base_image", "The image for the glyph.")

    def _get_base_image(self):
        image = self._get_image()
        if image.glyph is None:
            image.glyph = self
        return image

    def _get_image(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def addImage(self, path=None, data=None, scale=None, position=None, color=None):
        """
        Set the image in the glyph.

            >>> image = glyph.addImage(path="/path/to/my/image.png", color=(1, 0, 0, 0.5))

        path is a path to an image file.
        data is the raw image data.
        scale (x, y) is the scale of the image (optional).
        position (x, y) is the position of the image (optional).
        color is the color of the image (optional).

        The image data format is not defined. That
        will be environment specific and is handled
        in the Image object.
        """
        if path is not None and data is not None:
            raise FontPartsError("Only path or data may be defined, not both.")
        if scale is None:
            scale = (1, 1)
        if position is None:
            position = (0, 0)
        scale = normalizers.normalizeTransformationScale(scale)
        position = normalizers.normalizeTransformationOffset(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        sx, sy = scale
        ox, oy = position
        transformation = (sx, 0, 0, sy, ox, oy)
        if path is not None:
            if not os.path.exists(path):
                raise FontPartsError("No image located at '%s'." % path)
            f = open(path, "rb")
            data = f.read()
            f.close()
        image = self._addImage(data=data, transformation=transformation, color=color)
        return self.image

    def _addImage(self, data, transformation=None, color=None):
        """
        data will be raw, unnormalized image data.
        Each environment may have different possible
        formats, so this is unspecified.

        trasnformation will be a valid transformation matrix.

        color will be a color tuple or None.

        This must return an Image object. Assigning it
        to the glyph will be handled by the base class.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearImage(self, **kwargs):
        """
        Remove the image from the glyph.

            >>> glyph.clearImage()
        """
        if self.image is not None:
            self._clearImage(**kwargs)

    def _clearImage(self, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Mark color
    # ----

    markColor = dynamicProperty(
        "base_markColor",
        """
        The mark color for the glyph.

            >>> glyph.markColor
            None
            >>> glyph.markColor = (1, 0, 0, 0.5)
        """
    )

    def _get_base_markColor(self):
        value = self._get_markColor()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_markColor(self, value):
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_markColor(value)

    def _get_markColor(self):
        """
        Return the mark color value as a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_markColor(self, value):
        """
        value will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Note
    # ----

    note = dynamicProperty(
        "base_note",
        """
        A note for the glyph as a string or None.

            >>> glyph.note
            None
            >>> glyph.note = "P.B. said this looks 'awesome.'"
        """
    )

    def _get_base_note(self):
        value = self._get_note()
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        return value

    def _set_base_note(self, value):
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        self._set_note(value)

    def _get_note(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_note(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---
    # Lib
    # ---

    lib = dynamicProperty(
        "lib",
        """
        The lib for the glyph.

            >>> glyph.lib["org.robofab.hello"]
            "world"
        """
    )

    def _get_lib(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---
    # API
    # ---

    def isEmpty(self):
        """
        Return a bool indicating the glyph is empty.

        Empty Glyphs has no contours, no components,
        no anchors, no guidelines and an empty lib.

        """
        if self.contours:
            return False
        if self.components:
            return False
        if self.anchors:
            return False
        if self.guidelines:
            return False
        if self.lib:
            return False
        return True

    def readGlyphFromString(self, glifData):
        """
        Reads glif data into a glyph object.

        XML formatting of glif data must follow the
        Unified Font Object specification.
        """
        self._readGlyphFromString(glifData)

    def _readGlyphFromString(self, glifData):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def writeGlyphToString(self, glyphFormatVersion=2):
        """
        Writes glif data to an UFO XML string.

        XML formatting must follow the glyph formating specified by
        the Unified Font Object specification, defaulting to
        glyph format version 2.
        """
        glyphFormatVersion = normalizers.normalizeGlyphFormatVersion(glyphFormatVersion)
        self._writeGlyphToString(glyphFormatVersion)

    def _writeGlyphToString(self, glyphFormatVersion):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()
