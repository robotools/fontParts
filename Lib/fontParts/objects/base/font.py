import os
import fontMath

from .errors import FontPartsError
from .base import BaseObject, dynamicProperty
from .layer import _BaseGlyphVendor
import validators


class BaseFont(_BaseGlyphVendor):

    def __init__(self, pathOrObject=None, showInterface=True):
        """
        if pathOrObject is a string, open the file located at
        path. The type of files that can be opened will be
        defined by the environment. If pathOrObject is a font
        object to be wrapped, wrap it. If pathOrObject is
        None, create a new font.

        showInterface indicates if the user interface
        should be opened or not. Environments may or may not
        implement this behavior.
        """
        super(BaseFont, self).__init__(pathOrObject=pathOrObject, showInterface=showInterface)

    # ----
    # Copy
    # ----

    copyAttributes = (
        "info",
        "groups",
        "kerning",
        "features",
        "lib",
        "layerOrder",
        "defaultLayer",
        "glyphOrder"
    )

    def copy(self):
        """
        Copy the font into a new font.

            >>> copiedFont = font.copy()  # doctest: +SKIP

        This will copy:

        - info
        - groups
        - kerning
        - features
        - lib
        - layers
        - layerOrder
        - defaultLayer
        - glyphOrder
        - guidelines
        """
        return super(BaseFont, self).copy()

    def copyData(self, source):
        for layerName in source.layerOrder:
            if layerName in self.layerOrder:
                layer = self.getLayer(layerName)
            else:
                layer = self.newLayer(layerName)
            layer.copyData(source.getLayer(layerName))
        for sourceGuideline in self.guidelines:
            selfGuideline = self.appendGuideline((0, 0), 0)
            selfGuideline.copyData(sourceGuideline)
        super(BaseFont, self).copyData(source)

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(self, pathOrObject=None, showInterface=True, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # path

    path = dynamicProperty(
        "base_path",
        """
        The path to the file this object represents.

            >>> print font.path  # doctest: +SKIP
            "/path/to/my/font.ufo"
        """
    )

    def _get_base_path(self):
        path = self._get_path()
        if path is not None:
            path = validators.validateFilePath(path)
        return path

    def _get_path(self, **kwargs):
        """
        This must return a string defining the location of the
        file or None indicating that the file does not exist.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # save

    def save(self, path=None, showProgress=False, formatVersion=None):
        """
        Save the font to path.

            >>> font.save()                          # doctest: +SKIP
            >>> font.save("/path/to/my/font-2.ufo")  # doctest: +SKIP

        If path is None, use the font's original location. The
        file type must be inferred from the file extension on
        the given path. If no file extension is given, the
        environment may fall back to the format of its choice.

        showProgress indicates if a progress indicator should be
        displayed during the operation. Environments may or may not
        implement this behavior.

        formatVersion indicates the format version that should
        be used for writing the given file type. For example, if
        2 is given for formatVersion and the file type being written
        if UFO, the file is to be written in UFO 2 format. This
        value is not limited to UFO format versions. If no
        format version is given, the original format version of
        the file should be preserved. If there is no original
        format version it is implied that the format version
        is the latest version for the file type as supported
        by the environment.

        Environments may define their own rules governing when
        a file should be saved into its original location and
        when it should not. For example, a font opened from a
        compiled OpenType font may not be written back into
        the original OpenType font.
        """
        if path is None and self.path is None:
            raise FontPartsError("The font cannot be saved because no file location has been given.")
        if path is not None:
            path = validators.validateFilePath(path)
        showProgress = bool(showProgress)
        if formatVersion is not None:
            formatVersion = validators.validatorFileFormatVersion(formatVersion)
        self._save(path=path, showProgress=showProgress, formatVersion=formatVersion)

    def _save(self, path=None, showProgress=False, formatVersion=None, **kwargs):
        """
        Refer to the public save method for argument documentation.

        path will be a unicode string or None.
        showProgress will be a boolean.
        formatVersion will be an integer, float or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # close

    def close(self, save=False):
        """
        Close the font.

            >>> font.close()  # doctest: +SKIP

        If save is True, call the save method
        is called with no arguments.
        """
        if save:
            self.save()
        self._close()

    def _close(self, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # generate

    def generate(self, format, path=None):
        """
        Generate the font to another format.

            >>> font.generate("otfcff")                          # doctest: +SKIP
            >>> font.generate("otfcff", "/path/to/my/font.otf")  # doctest: +SKIP

        format defines the file format to output. These are the
        standard format identifiers.

        +--------------+--------------------------------------------------------------------+
        | mactype1     | Mac Type 1 font (generates suitcase  and LWFN file)                |
        +--------------+--------------------------------------------------------------------+
        | macttf       | Mac TrueType font (generates suitcase)                             |
        +--------------+--------------------------------------------------------------------+
        | macttdfont   | Mac TrueType font (generates suitcase with resources in data fork) |
        +--------------+--------------------------------------------------------------------+
        | otfcff       | PS OpenType (CFF-based) font (OTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | otfttf       | PC TrueType/TT OpenType font (TTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | pctype1      | PC Type 1 font (binary/PFB)                                        |
        +--------------+--------------------------------------------------------------------+
        | pcmm         | PC MultipleMaster font (PFB)                                       |
        +--------------+--------------------------------------------------------------------+
        | pctype1ascii | PC Type 1 font (ASCII/PFA)                                         |
        +--------------+--------------------------------------------------------------------+
        | pcmmascii    | PC MultipleMaster font (ASCII/PFA)                                 |
        +--------------+--------------------------------------------------------------------+
        | ufo1         | UFO format version 1                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo2         | UFO format version 2                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo3         | UFO format version 3                                               |
        +--------------+--------------------------------------------------------------------+
        | unixascii    | UNIX ASCII font (ASCII/PFA)                                        |
        +--------------+--------------------------------------------------------------------+

        Environments are not required to support all of these.
        Environments may define their own format types.

        path defines the location where the new file should
        be located. If path defines a directory, the file should
        be output as the current file name, with the appropriate
        suffix for the format, into the given directory. If no path
        is given, the file will be output into the same directory
        as the source font with the file named with the current
        file name, with the appropriate suffix for the format.
        """
        formatToExtension = dict(
            # mactype1=None,
            macttf=".ttf",
            macttdfont=".dfont",
            otfcff=".otf",
            otfttf=".ttf",
            # pctype1=None,
            # pcmm=None,
            # pctype1ascii=None,
            # pcmmascii=None,
            ufo1=".ufo",
            ufo2=".ufo",
            ufo3=".ufo",
            unixascii=".pfa",
        )
        if format is None:
            raise FontPartsError("The format must be defined when generating.")
        elif not isinstance(format, basestring):
            raise FontPartsError("The format must be defined as a string.")
        ext = formatToExtension.get(format, "." + format)
        if path is None and self.path is None:
            raise FontPartsError("The file cannot be generated because an output path was not defined.")
        elif path is None:
            path = os.path.splitext(self.path)[0]
            path += ext
        elif os.path.isdir(path):
            if self.path is None:
                raise FontPartsError("The file cannot be generated because the file does not have a path.")
            fileName = os.path.basename(self.path)
            fileName += ext
            path = os.path.join(path, fileName)
        path = validators.validateFilePath(path)
        self._generate(format=format, path=path)

    def _generate(self, format, path, **kwargs):
        """
        format will be a string defining the output format.
        path will be the path to output to.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # info

    info = dynamicProperty(
        "base_info",
        """
        The font's info object.

            >>> font.info.familyName  # doctest: +SKIP
            "My Family"
        """
    )

    def _get_base_info(self):
        info = self._get_info()
        info.font = self
        return info

    def _get_info(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # groups

    groups = dynamicProperty(
        "base_groups",
        """
        The font's groups object.

            >>> font.groups["myGroup"]  # doctest: +SKIP
            ["A", "B", "C"]
        """
    )

    def _get_base_groups(self):
        groups = self._get_groups()
        groups.font = self
        return groups

    def _get_groups(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # kerning

    kerning = dynamicProperty(
        "base_kerning",
        """
        The font's kerning object.

            >>> font.kerning["A", "B"]  # doctest: +SKIP
            -100
        """
    )

    def _get_base_kerning(self):
        kerning = self._get_kerning()
        kerning.font = self
        return kerning

    def _get_kerning(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # features

    features = dynamicProperty(
        "base_features",
        """
        The font's features object.

            >>> font.features.text  # doctest: +SKIP
            "include(features/substitutions.fea);"
        """
    )

    def _get_base_features(self):
        features = self._get_features()
        features.font = self
        return features

    def _get_features(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # lib

    lib = dynamicProperty(
        "base_lib",
        """
        The font's lib object.

            >>> font.lib["org.robofab.hello"]  # doctest: +SKIP
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
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "base_layers",
        """
        The font's layer objects.

            >>> for layer in font.layers:  # doctest: +SKIP
            ...     layer.name             # doctest: +SKIP
            "My Layer 1"
            "My Layer 2"
        """
    )

    def _get_base_layers(self):
        layers = self._get_layers()
        for layer in layers:
            self._setFontInLayer(layer)
        return tuple(layers)

    def _get_layers(self, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # order

    layerOrder = dynamicProperty(
        "base_layerOrder",
        """
        A list of layer names indicating order of the layers in the font.

            >>> font.layerOrder = ["My Layer 2", "My Layer 1"]  # doctest: +SKIP
            >>> font.layerOrder                                 # doctest: +SKIP
            ["My Layer 2", "My Layer 1"]
        """
    )

    def _get_base_layerOrder(self):
        value = self._get_layerOrder()
        value = validators.validateLayerOrder(value, self)
        return list(value)

    def _set_base_layerOrder(self, value):
        value = validators.validateLayerOrder(value, self)
        self._set_layerOrder(value)

    def _get_layerOrder(self, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_layerOrder(self, value, **kwargs):
        """
        value will be a list of layer names.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # default layer

    def _setFontInLayer(self, layer):
        if layer.font is None:
            layer.font = self

    defaultLayer = dynamicProperty(
        "base_defaultLayer",
        """
        The name of the font's default layer.

            >>> font.defaultLayer = "My Layer 2"  # doctest: +SKIP
            >>> font.defaultLayer                 # doctest: +SKIP
            "My Layer 2"
        """
    )

    def _get_base_defaultLayer(self):
        value = self._get_defaultLayer()
        value = validators.validateDefaultLayer(value, self)
        return value

    def _set_base_defaultLayer(self, value):
        value = validators.validateDefaultLayer(value, self)
        self._set_defaultLayer(value)

    def _get_defaultLayer(self):
        """
        Return the name of the default layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_defaultLayer(self, value, **kwargs):
        """
        value will be a string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # get

    def getLayer(self, name):
        """
        Get the layer with name.

            >>> layer = font.getLayer("My Layer 2")  # doctest: +SKIP
        """
        name = validators.validateLayerName(name)
        layer = self._getLayer(name)
        self._setFontInLayer(layer)
        return layer

    def _getLayer(self, name, **kwargs):
        """
        name will be a string, but there may not be a
        layer with a name matching the string. If not,
        a FontPartsError must be raised.

        Subclasses may override this method.
        """
        for layer in self.layers:
            if layer.name == name:
                return layer
        raise FontPartsError("No layer with the name %r exists." % name)

    # new

    def newLayer(self, name, color=None):
        """
        Make a new layer with name and color.

            >>> layer = font.newLayer("My Layer 3")  # doctest: +SKIP

        The will return the new layer.
        """
        name = validators.validateLayerName(name)
        if name in self.layerOrder:
            raise FontPartsError("A layer with the name %r already exists." % name)
        if color is not None:
            color = validators.validateColor(color)
        layer = self._newLayer(name=name, color=color)
        self._setFontInLayer(layer)
        return layer

    def _newLayer(self, name, color, **kwargs):
        """
        name will be a string representing a valid layer
        name. The name will have been tested to make sure
        that no layer already has the name.

        color will be a color tuple.

        This must returned the new layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, name):
        """
        Remove the layer with name from the font.

            >>> font.removeLayer("My Layer 3")  # doctest: +SKIP
        """
        name = validators.validateLayerName(name)
        if name not in self.layerOrder:
            raise FontPartsError("No layer with the name %r exists." % name)
        self._removeLayer(name)

    def _removeLayer(self, name, **kwargs):
        """
        name will be a valid layer name. It will
        represent an existing layer in the font.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Glyph Interaction
    # -----------------

    # base implementation overrides

    def _getItem(self, name, **kwargs):
        """
        This must return a wrapped glyph.

        name will be a valid glyph name that is in the layer.

        Subclasses may override this method. The base
        implementation delegates this method to the
        default layer.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer[name]

    def _keys(self):
        """
        This must return a list of all glyph names in the layer.

        Subclasses may override this method. The base
        implementation delegates this method to the
        default layer.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer.keys()

    def _newGlyph(self, name, **kwargs):
        """
        name will be a string representing a valid glyph
        name. The name will have been tested to make sure
        that no glyph already has the name.

        This must returned the new glyph.

        Subclasses may override this method. The base
        implementation delegates this method to the
        default layer.
        """
        layer = self.getLayer(self.defaultLayer)
        # clear is False here because the base newFont
        # that has called this method will have already
        # handled the clearning as specified by the caller.
        return layer.newGlyph(name)

    def _removeGlyph(self, name, **kwargs):
        """
        name will be a valid glyph name. It will
        represent an existing glyph in the layer.

        Subclasses may override this method. The base
        implementation delegates this method to the
        default layer.
        """
        layer = self.getLayer(self.defaultLayer)
        layer.removeGlyph(name)

    # order

    glyphOrder = dynamicProperty(
        "base_glyphOrder",
        """
        The preferred order of the glyphs in the font.

            >>> font.glyphOrder                    # doctest: +SKIP
            ["C", "B", "A"]
            >>> font.glyphOrder = ["A", "B", "C"]  # doctest: +SKIP
        """
    )

    def _get_base_glyphOrder(self):
        value = self._get_glyphOrder()
        value = validators.validateGlyphOrder(value)
        return value

    def _set_base_glyphOrder(self, value):
        value = validators.validateGlyphOrder(value)
        self._set_glyphOrder(value)

    def _get_glyphOrder(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_glyphOrder(self, value):
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

            >>> font.round()  # doctest: +SKIP

        This is the equivalent of calling the round method on:

        - info
        - kerning
        - the default layer
        - font-level guidelines

        This applies only to the default layer.
        """
        self._round()

    def _round(self):
        """
        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        layer.round()
        self.info.round()
        self.kerning.round()
        for guideline in self.guidelines():
            guideline.round()

    def autoUnicodes(self):
        """
        Use heuristics to set Unicode values in all glyphs.

            >>> font.autoUnicodes()  # doctest: +SKIP

        Environments will define their own heuristics for
        automatically determining values.

        This applies only to the default layer.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer())
        layer.autoUnicodes()

    # ----------
    # Guidelines
    # ----------

    def _setFontInGuideline(self, guideline):
        if guideline.font is None:
            guideline.font = self

    guidelines = dynamicProperty(
        "guidelines",
        """
        An immutable list of font-level guidelines.

            >>> for guideline in font.guidelines:  # doctest: +SKIP
            ...     guideline.angle                # doctest: +SKIP
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
        index = validators.validateGuidelineIndex(index)
        if index >= self._len__guidelines():
            raise FontPartsError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setFontInGuideline(guideline)
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
        Append a new guideline to the font.

            >>> guideline = font.appendGuideline((50, 0), 90)                                          # doctest: +SKIP
            >>> guideline = font.appendGuideline((0, 540), 0, name="overshoot", color=(0, 0, 0, 0.2))  # doctest: +SKIP

        position (x, y) indicates the position of the guideline.
        angle indicates the angle of the guideline.
        name indicates the name for the guideline.
        color indicates the color for the guideline.
        """
        position = validators.validateCoordinateTuple(position)
        angle = validators.validateGuidelineAngle(angle)
        if name is not None:
            name = validators.validateGuidelineName(name)
        if color is not None:
            color = validators.validateColor(color)
        return self._appendGuideline(position, angle, name=name, color=color)

    def _appendGuideline(self, position, angle, name=None, color=None, **kwargs):
        """
        position will be a valid position (x, y).
        angle will be a valida angle.
        name will be a valid guideline name or None.
        color will be None or a valid color.

        This must return the new guideline.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove guideline from the font.

            >>> font.removeGuideline(guideline)  # doctest: +SKIP
            >>> font.removeGuideline(2)          # doctest: +SKIP

        guideline can be a guideline object or an
        integer representing the guideline index.
        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(anchor)
        index = validators.validateGuidelineIndex(index)
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

            >>> font.clearGuidelines()  # doctest: +SKIP
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        Subclasses may override this method.
        """
        for i in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minFont, maxFont, round=True, suppressError=True):
        """
        Interpolate all possible data in the font.

            >>> font.interpolate(0.5, otherFont1, otherFont2)                      # doctest: +SKIP
            >>> font.interpolate((0.5, 2.0), otherFont1, otherFont2, round=False)  # doctest: +SKIP

        The interpolation occurs on a 0 to 1.0 range where minFont
        is located at 0 and maxFont is located at 1.0.

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
        if not isinstance(minFont, BaseFont):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minFont.__class__.__name__))
        if not isinstance(maxFont, BaseFont):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxFont.__class__.__name__))
        round = validators.validateBoolean(round)
        suppressError = validators.validateBoolean(suppressError)
        self._interpolate(factor, minFont, maxFont, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minFont, maxFont, round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        # layers
        for layerName in self.layerOrder:
            self.removeLayer(layerName)
        for layerName in minFont.layerOrder:
            if layerName not in maxFont.layerOrder:
                continue
            minLayer = minFont.getLayer(layerName)
            maxLayer = maxFont.getLayer(layerName)
            dstLayer = self.newLayer(layerName)
            dstLayer.interpolate(factor, minLayer, maxLayer, round=round, suppressError=suppressError)
        # kerning and groups
        self.kerning.interpolate(factor, minFont.kerning, maxFont.kerning, round=round, suppressError=suppressError)
        # info
        self.info.interpolate(factor, minFont.info, maxFont.info, round=round, suppressError=suppressError)

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with other.

            >>> compat, report = self.isCompatible(otherFont)  # doctest: +SKIP
            >>> compat                                         # doctest: +SKIP
            False
            >>> report                                         # doctest: +SKIP
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        Returns a boolean indicating if the font is compatible for
        interpolation with other and a string of compatibility notes.
        """
        if not isinstance(other, BaseFont):
            raise FontPartsError("Compatibility between an instance of %r and an instance of %r can not be checked." % (self.__class__.__name__, other.__class__.__name__))
        return self._isCompatible(other)

    def _isCompatible(self, other):
        """
        Subclasses may override this method.
        """
        fatal = False
        report = []
        # incompatible guidelines
        if len(self.guidelines) != len(other.guidelines):
            report.append("[Note] The glyphs do not contain the same number of guidelines.")
        # incompatible layers
        if sorted(self.layerOrder) != sorted(other.layerOrder):
            report.append("[Warning] The fonts do not contain the same layers.")
        # test layers
        for layerName in sorted(self.layerOrder):
            selfLayer = self.getLayer(layerName)
            otherLayer = other.getLayer(layerName)
            f, r = selfLayer.isCompatible(otherLayer)
            if f:
                fatal = True
            if r:
                header = layerName
                marker = "-" * len(layerName)
                r = "\n" + header + "\n" + marker + "\n" + r
                report.append(r)
        return fatal, "\n".join(report)
