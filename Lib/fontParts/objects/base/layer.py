import weakref

from .errors import FontPartsError
from .base import BaseObject, dynamicProperty
import validators
from .color import Color


class _BaseGlyphVendor(BaseObject):

    """
    This class exists to provide common glyph
    interaction code to BaseFont and BaseLayer.
    It should not be directly subclassed.
    """

    # -----------------
    # Glyph Interaction
    # -----------------

    def _setLayerInGlyph(self, glyph):
        if glyph.layer is None:
            if isinstance(self, BaseLayer):
                layer = self
            else:
                layer = self.getLayer(self.defaultLayer)
            glyph.layer = layer

    def __len__(self):
        """
        The number of glyphs in the layer.

            >>> len(layer)  # doctest: +SKIP
            256
        """
        return self._len()

    def _len(self, **kwargs):
        """
        This must return an integer.

        Subclasses may override this method.
        """
        return len(self.keys())

    def __iter__(self):
        """
        Iterate through the glyphs in the layer.

            >>> for glyph in layer:  # doctest: +SKIP
            ...     glyph.name       # doctest: +SKIP
            "A"
            "B"
            "C"
        """
        return self._iter()

    def _iter(self, **kwargs):
        """
        This must return an iterator that returns wrapped glyphs.

        Subclasses may override this method.
        """
        names = self.keys()
        while names:
            name = names[0]
            yield self[name]
            names = names[1:]

    def __getitem__(self, name):
        """
        Get the glyph with name from the  layer.

            >>> glyph = layer["A"]  # doctest: +SKIP
        """
        name = validators.validateGlyphName(name)
        if name not in self:
            raise FontPartsError("No glyph named %r." % name)
        glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _getItem(self, name, **kwargs):
        """
        This must return a wrapped glyph.

        name will be a valid glyph name that is in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def keys(self):
        """
        Get a list of all glyphs in the layer of the font.

            >>> layer.keys()  # doctest: +SKIP
            ["B", "C", "A"]

        The order of the glyphs is undefined.
        """
        return self._keys()

    def _keys(self, **kwargs):
        """
        This must return a list of all glyph names in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __contains__(self, name):
        """
        Test if the layer contains a glyph with name.

            >>> "A" in layer  # doctest: +SKIP
            True
        """
        name = validators.validateGlyphName(name)
        return self._contains(name)

    def _contains(self, name, **kwargs):
        """
        This must return an boolean.

        Subclasses may override this method.
        """
        return name in self.keys()

    def newGlyph(self, name):
        """
        Make a new glyph in the layer.

            >>> glyph = layer.newGlyph("A")  # doctest: +SKIP

        The glyph will be returned.
        """
        name = validators.validateGlyphName(name)
        if name in self:
            self.removeGlyph(name)
        glyph = self._newGlyph(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _newGlyph(self, name, **kwargs):
        """
        name will be a string representing a valid glyph
        name. The name will have been tested to make sure
        that no glyph already has the name.

        This must returned the new glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def removeGlyph(self, name):
        """
        Remove the glyph with name from the layer.

            >>> layer.removeGlyph("A")  # doctest: +SKIP

        """
        name = validators.validateGlyphName(name)
        if name not in self:
            raise FontPartsError("No glyph with the name %r exists." % name)
        self._removeGlyph(name)

    def _removeGlyph(self, name, **kwargs):
        """
        name will be a valid glyph name. It will
        represent an existing glyph in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def insertGlyph(self, glyph, name=None):
        """
        Insert a new glyph into the layer.

            >>> glyph = layer.insertGlyph(otherGlyph, name="A")  # doctest: +SKIP

        The glyph will be returned.

        name indicates the name that should be assigned to
        the glyph after insertion. If name is not given,
        the glyph's original name must be used. If the glyph
        does not have a name, an error must be raised.

        This does not insert the given glyph object. Instead,
        a new glyph is created and the data from the given
        glyph is recreated in the new glyph.

        The following data is recreated from the given glyph:

        - width
        - height
        - unicodes
        - note
        - lib
        - contours
        - components
        - anchors
        - guidelines
        """
        name = validators.validateGlyphName(name)
        if name is None:
            name = glyph.name
        if name in self:
            self.removeGlyph(name)
        return self._insertGlyph(glyph, name=name)

    def _insertGlyph(self, glyph, name, **kwargs):
        """
        Insert the data from glyph into a new glyph with name.
        This must returned the new glyph.

        Subclasses may override this method.
        """
        dest = self.newGlyph(name)
        dest.appendGlyph(glyph)
        dest.width = glyph.width
        dest.height = glyph.height
        dest.unicodes = glyph.unicodes
        dest.note = glyph.note
        dest.lib.update(glyph.lib.copy())
        if glyph.image is not None:
            dest.image = glyph.image.copy()
        return dest

    # --------------------
    # Legacy Compatibility
    # --------------------

    has_key = __contains__


class BaseLayer(_BaseGlyphVendor):

    # ----
    # Copy
    # ----

    copyAttributes = (
        "name",
        "color",
        "lib"
    )

    def copy(self):
        """
        Copy the layer into a new layer that does not
        belong to a font.

            >>> copiedLayer = layer.copy()  # doctest: +SKIP

        This will copy:

        - name
        - color
        - lib
        - glyphs
        """
        return super(BaseFont, self).copy()

    def copyData(self, source):
        super(BaseLayer, self).copyData(source)
        for name in source.keys():
            glyph = self.newGlyph(name)
            glyph.copyData(source[name])

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.font

    # Font

    _font = None

    font = dynamicProperty(
        "font",
        """
        The layer's parent font.

            >>> font = layer.font  # doctest: +SKIP
        """
        )

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

    # --------------
    # Identification
    # --------------

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the layer.

            >>> layer.name          # doctest: +SKIP
            "foreground"
            >>> layer.name = "top"  # doctest: +SKIP
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = validators.validateLayerName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        value = validators.validateLayerName(value)
        existing = self.font.layerOrder
        if value in existing:
            raise FontPartsError("A layer with the name %r already exists." % value)
        self._set_name(value)

    def _get_name(self):
        """
        Get the name of the layer.
        This must return a unicode string or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value, **kwargs):
        """
        Set the name of the layer.
        This will be a unicode string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty(
        "base_color",
        """
        The layer's color.

            >>> layer.color                   # doctest: +SKIP
            None
            >>> layer.color = (1, 0, 0, 0.5)  # doctest: +SKIP
        """
)

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = validators.validateColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = validators.validateColor(value)
        self._set_color(value)

    def _get_color(self):
        """
        Get the color of the layer.
        This must return a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value, **kwargs):
        """
        Set the color of the layer.
        This will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    lib = dynamicProperty(
        "lib",
        """
        The layer's lib object.

            >>> layer.lib["org.robofab.hello"]  # doctest: +SKIP
            "world"
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers.

            >>> layer.round()  # doctest: +SKIP

        This is the equivalent of calling the round method on:

        - all glyphs in the layer
        """
        self._round()

    def _round(self):
        """
        Subclasses may override this method.
        """
        for glyph in self:
            glyph.round()

    def autoUnicodes(self):
        """
        Use heuristics to set Unicode values in all glyphs.

            >>> layer.autoUnicodes()  # doctest: +SKIP

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        Subclasses may override this method.
        """
        for glyph in self:
            glyph.autoUnicodes()

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minLayer, maxLayer, round=True, suppressError=True):
        """
        Interpolate all possible data in the layer.

            >>> layer.interpolate(0.5, otherLayer1, otherLayer2)                      # doctest: +SKIP
            >>> layer.interpolate((0.5, 2.0), otherLayer1, otherLayer2, round=False)  # doctest: +SKIP

        The interpolation occurs on a 0 to 1.0 range where minLayer
        is located at 0 and maxLayer is located at 1.0.

        factor is the interpolation value. It may be less than 0
        and greater than 1.0. It may be a number (integer, float)
        or a tuple of two numbers. If it is a tuple, the first
        number indicates the x factor and the second number
        indicates the y factor.

        round indicates if the result should be rounded to integers.

        suppressError indicates if incompatible data should be ignored
        or if an error should be raised when such incompatibilities are found.
        """
        factor = validators.validateInterpolationFactor(factor)
        if not isinstance(minLayer, BaseLayer):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minLayer.__class__.__name__))
        if not isinstance(maxLayer, BaseLayer):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxLayer.__class__.__name__))
        round = validators.validateBoolean(round)
        suppressError = validators.validateBoolean(suppressError)
        self._interpolate(factor, minLayer, maxLayer, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minLayer, maxLayer, round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        for glyphName in self.keys():
            del self[glyphName]
        for glyphName in minLayer.keys():
            if glyphName not in maxLayer:
                continue
            minGlyph = minLayer[glyphName]
            maxGlyph = maxLayer[glyphName]
            dstGlyph = self.newGlyph(glyphName)
            dstGlyph.interpolate(factor, minGlyph, maxGlyph, round=round, suppressError=suppressError)

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with other.

            >>> compat, report = self.isCompatible(otherLayer)  # doctest: +SKIP
            >>> compat                                          # doctest: +SKIP
            False
            >>> report                                          # doctest: +SKIP
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        Returns a boolean indicating if the layer is compatible for
        interpolation with other and a string of compatibility notes.
        """
        if not isinstance(other, BaseLayer):
            raise FontPartsError("Compatibility between an instance of %r and an instance of %r can not be checked." % (self.__class__.__name__, other.__class__.__name__))
        return self._isCompatible(other)

    def _isCompatible(self, other):
        """
        Subclasses may override this method.
        """
        fatal = False
        report = []
        # incompatible glyphs
        if sorted(self.keys()) != sorted(other.keys()):
            report.append("[Warning] The layers do not contain the same glyphs.")
        # test glyphs
        for glyphName in sorted(self.keys()):
            if glyphName not in other:
                continue
            selfGlyph = self[glyphName]
            otherGlyph = other[glyphName]
            f, r = selfGlyph.isCompatible(otherGlyph)
            if f:
                fatal = True
            if r:
                r = "\n" + glyphName + ":\n" + r
                report.append(r)
        return fatal, "\n".join(report)
