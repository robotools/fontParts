import os
import fontMath
from fontTools.misc.py23 import basestring
from fontParts.base.errors import FontPartsError
from fontParts.base.base import dynamicProperty
from fontParts.base.layer import _BaseGlyphVendor
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedFont, RemovedFont


class BaseFont(_BaseGlyphVendor, DeprecatedFont, RemovedFont):

    """
    A font object. This object is almost always
    created with one of the font functions in
    :ref:`fontparts-world`.
    """

    def __init__(self, pathOrObject=None, showInterface=True):
        """
        When constructing a font, the object can be created
        in a new file, from an existing file or from a native
        object. This is defined with the **pathOrObjectArgument**.
        If **pathOrObject** is a string, the string must represent
        an existing file. If **pathOrObject** is an instance of the
        environment's unwrapped native font object, wrap it with
        FontParts. If **pathOrObject** is None, create a new,
        empty font. If **showInterface** is ``False``, the font
        should be created without graphical interface. The default
        for **showInterface** is ``True``.
        """
        super(BaseFont, self).__init__(pathOrObject=pathOrObject, showInterface=showInterface)

    def _reprContents(self):
        contents = [
            "'%s %s'" % (self.info.familyName, self.info.styleName),
        ]
        if self.path is not None:
            contents.append("path=%r" % self.path)
        return contents

    def __hash__(self):
        """
        Allow font object to be used as a key
        in a dictionary.
        
        Subclasses may override this method.
        """
        return id(self.naked())

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
        Copy the font into a new font. ::

            >>> copiedFont = font.copy()

        This will copy:

        * info
        * groups
        * kerning
        * features
        * lib
        * layers
        * layerOrder
        * defaultLayer
        * glyphOrder
        * guidelines
        """
        return super(BaseFont, self).copy()

    def copyData(self, source):
        """
        Copy data from **source** into this font.
        Refer to :meth:`BaseFont.copy` for a list
        of values that will be copied.
        """
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
        Initialize this object. This should wrap a native font
        object based on the values for **pathOrObject**:

        +--------------------+---------------------------------------------------+
        | None               | Create a new font.                                |
        +--------------------+---------------------------------------------------+
        | string             | Open the font file located at the given location. |
        +--------------------+---------------------------------------------------+
        | native font object | Wrap the given object.                            |
        +--------------------+---------------------------------------------------+

        If **showInterface** is ``False``, the font should be
        created without graphical interface.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # path

    path = dynamicProperty(
        "base_path",
        """
        The path to the file this object represents. ::

            >>> print font.path
            "/path/to/my/font.ufo"
        """
    )

    def _get_base_path(self):
        path = self._get_path()
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        return path

    def _get_path(self, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.path`.

        This must return a :ref:`type-string` defining the
        location of the file or ``None`` indicating that the
        font does not have a file representation. If the
        returned value is not ``None`` it will be normalized
        with :func:`normalizers.normalizeFilePath`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # save

    def save(self, path=None, showProgress=False, formatVersion=None):
        """
        Save the font to **path**.

            >>> font.save()
            >>> font.save("/path/to/my/font-2.ufo")

        If **path** is None, use the font's original location.
        The file type must be inferred from the file extension
        of the given path. If no file extension is given, the
        environment may fall back to the format of its choice.
        **showProgress** indicates if a progress indicator should
        be displayed during the operation. Environments may or may
        not implement this behavior. **formatVersion** indicates
        the format version that should be used for writing the given
        file type. For example, if 2 is given for formatVersion
        and the file type being written if UFO, the file is to
        be written in UFO 2 format. This value is not limited
        to UFO format versions. If no format version is given,
        the original format version of the file should be preserved.
        If there is no original format version it is implied that
        the format version is the latest version for the file
        type as supported by the environment.

        .. note::

           Environments may define their own rules governing when
           a file should be saved into its original location and
           when it should not. For example, a font opened from a
           compiled OpenType font may not be written back into
           the original OpenType font.
        """
        if path is None and self.path is None:
            raise FontPartsError("The font cannot be saved because no file location has been given.")
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        showProgress = bool(showProgress)
        if formatVersion is not None:
            formatVersion = normalizers.normalizeFileFormatVersion(formatVersion)
        self._save(path=path, showProgress=showProgress, formatVersion=formatVersion)

    def _save(self, path=None, showProgress=False, formatVersion=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.save`. **path** will be a
        :ref:`type-string` or ``None``. If **path**
        is not ``None``, the value will have been
        normalized with :func:`normalizers.normalizeFilePath`.
        **showProgress** will be a ``bool`` indicating if
        the environment should display a progress bar
        during the operation. Environments are not *required*
        to display a progress bar even if **showProgess**
        is ``True``. **formatVersion** will be :ref:`type-int-float`
        or ``None`` indicating the file format version
        to write the data into. It will have been normalized
        with :func:`normalizers.normalizeFileFormatVersion`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # close

    def close(self, save=False):
        """
        Close the font.

            >>> font.close()

        **save** is a boolean indicating if the font
        should be saved prior to closing. If **save**
        is ``True``, the :meth:`BaseFont.save` method
        will be called. The default is ``False``.
        """
        if save:
            self.save()
        self._close()

    def _close(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.close`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # generate

    def generateFormatToExtension(self, format, fallbackFormat):
        """
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
        return formatToExtension.get(format, fallbackFormat)

    def generate(self, format, path=None, **kwargs):
        """
        Generate the font to another format.

            >>> font.generate("otfcff")
            >>> font.generate("otfcff", "/path/to/my/font.otf")

        **format** defines the file format to output. These are the
        standard format identifiers:

        %s

        Environments are not required to support all of these
        and environments may define their own format types.
        **path** defines the location where the new file should
        be created. If a file already exists at that location,
        it will be overwritten by the new file. If **path** defines
        a directory, the file will be output as the current
        file name, with the appropriate suffix for the format,
        into the given directory. If no **path** is given, the
        file will be output into the same directory as the source
        font with the file named with the current file name,
        with the appropriate suffix for the format.
        """

        if format is None:
            raise FontPartsError("The format must be defined when generating.")
        elif not isinstance(format, basestring):
            raise FontPartsError("The format must be defined as a string.")
        ext = self.generateFormatToExtension(format, "." + format)
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
        path = normalizers.normalizeFilePath(path)
        return self._generate(format=format, path=path, **kwargs)

    generate.__doc__ %= generateFormatToExtension.__doc__

    def _generate(self, format, path, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.generate`. **format** will be a
        :ref:`type-string` defining the output format.
        Refer to the :meth:`BaseFont.generate` documentation
        for the standard format identifiers. If the value
        given for **format** is not supported by the environment,
        the environment must raise :exc:`FontPartsError`.
        **path** will be a :ref:`type-string` defining the
        location where the file should be created. It
        will have been normalized with :func:`normalizers.normalizeFilePath`.

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
        The font's :class:`BaseInfo` object.

            >>> font.info.familyName
            "My Family"
        """
    )

    def _get_base_info(self):
        info = self._get_info()
        info.font = self
        return info

    def _get_info(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.info`. This must return an
        instance of a :class:`BaseInfo` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # groups

    groups = dynamicProperty(
        "base_groups",
        """
        The font's :class:`BaseGroups` object.

            >>> font.groups["myGroup"]
            ["A", "B", "C"]
        """
    )

    def _get_base_groups(self):
        groups = self._get_groups()
        groups.font = self
        return groups

    def _get_groups(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.groups`. This must return
        an instance of a :class:`BaseGroups` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # kerning

    kerning = dynamicProperty(
        "base_kerning",
        """
        The font's :class:`BaseKerning` object.

            >>> font.kerning["A", "B"]
            -100
        """
    )

    def _get_base_kerning(self):
        kerning = self._get_kerning()
        kerning.font = self
        return kerning

    def _get_kerning(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.kerning`. This must return
        an instance of a :class:`BaseKerning` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # features

    features = dynamicProperty(
        "base_features",
        """
        The font's :class:`BaseFeatures` object.

            >>> font.features.text
            "include(features/substitutions.fea);"
        """
    )

    def _get_base_features(self):
        features = self._get_features()
        features.font = self
        return features

    def _get_features(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.features`. This must return
        an instance of a :class:`BaseFeatures` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # lib

    lib = dynamicProperty(
        "base_lib",
        """
        The font's :class:`BaseLib` object.

            >>> font.lib["org.robofab.hello"]
            "world"
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.lib`. This must return an
        instance of a :class:`BaseLib` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "base_layers",
        """
        The font's :class:`BaseLayer` objects.

            >>> for layer in font.layers:
            ...     layer.name
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
        This is the environment implementation of
        :attr:`BaseFont.layers`. This must return an
        :ref:`type-immutable-list` containing
        instances of :class:`BaseLayer` subclasses.
        The items in the list should be in the order
        defined by :attr:`BaseFont.layerOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # order

    layerOrder = dynamicProperty(
        "base_layerOrder",
        """
        A list of layer names indicating order of the layers in the font.

            >>> font.layerOrder = ["My Layer 2", "My Layer 1"]
            >>> font.layerOrder
            ["My Layer 2", "My Layer 1"]
        """
    )

    def _get_base_layerOrder(self):
        value = self._get_layerOrder()
        value = normalizers.normalizeLayerOrder(value, self)
        return list(value)

    def _set_base_layerOrder(self, value):
        value = normalizers.normalizeLayerOrder(value, self)
        self._set_layerOrder(value)

    def _get_layerOrder(self, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.layerOrder`. This must return an
        :ref:`type-immutable-list` defining the order of
        the layers in the font. The contents of the list
        must be layer names as :ref:`type-string`. The
        list will be normalized with :func:`normalizers.normalizeLayerOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_layerOrder(self, value, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.layerOrder`. **value** will
        be a **list** of :ref:`type-string` representing
        layer names. The list will have been normalized
        with :func:`normalizers.normalizeLayerOrder`.

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

            >>> font.defaultLayer = "My Layer 2"
            >>> font.defaultLayer
            "My Layer 2"
        """
    )

    def _get_base_defaultLayer(self):
        value = self._get_defaultLayer()
        value = normalizers.normalizeDefaultLayer(value, self)
        return value

    def _set_base_defaultLayer(self, value):
        value = normalizers.normalizeDefaultLayer(value, self)
        self._set_defaultLayer(value)

    def _get_defaultLayer(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayer`. Return the name
        of the default layer as a :ref:`type-string`.
        The name will be normalized with
        :func:`normalizers.normalizeDefaultLayer`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_defaultLayer(self, value, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayer`. **value**
        will be a :ref:`type-string`. It will have
        been normalized with :func:`normalizers.normalizeDefaultLayer`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # get

    def getLayer(self, name):
        """
        Get the :class:`BaseLayer` with **name**.

            >>> layer = font.getLayer("My Layer 2")
        """
        name = normalizers.normalizeLayerName(name)
        layer = self._getLayer(name)
        self._setFontInLayer(layer)
        return layer

    def _getLayer(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.getLayer`. **name** will
        be a :ref:`type-string`. It will have been
        normalized with :func:`normalizers.normalizeLayerName`.
        This must return an instance of :class:`BaseLayer`.
        If a layer with **name** does not exist, a
        :exc:`FontPartsError` must be raised.

        XXX don't require the subclass to test for existence. do that in getLayer.

        Subclasses may override this method.
        """
        for layer in self.layers:
            if layer.name == name:
                return layer
        raise FontPartsError("No layer with the name '%s' exists." % name)

    # new

    def newLayer(self, name, color=None):
        """
        Make a new layer with **name** and **color**.
        **name** must be a :ref:`type-string` and
        **color** must be a :ref:`type-color` or ``None``.

            >>> layer = font.newLayer("My Layer 3")

        The will return the newly created
        :class:`BaseLayer`.
        """
        name = normalizers.normalizeLayerName(name)
        if name in self.layerOrder:
            layer = self.getLayer(name)
            if color is not None:
                layer.color = color
            return layer
        if color is not None:
            color = normalizers.normalizeColor(color)
        layer = self._newLayer(name=name, color=color)
        self._setFontInLayer(layer)
        return layer

    def _newLayer(self, name, color, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.newLayer`. **name** will be
        a :ref:`type-string` representing a valid
        layer name. The value will have been normalized
        with :func:`normalizers.normalizeLayerName` and
        **name** will not be the same as the name of
        an existing layer. **color** will be a
        :ref:`type-color` or ``None``. If the value
        is not ``None`` the value will have been
        normalized with :func:`normalizers.normalizeColor`.
        This must return an instance of a :class:`BaseLayer`
        subclass that represents the new layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, name):
        """
        Remove the layer with **name** from the font.

            >>> font.removeLayer("My Layer 3")
        """
        name = normalizers.normalizeLayerName(name)
        if name not in self.layerOrder:
            raise FontPartsError("No layer with the name '%s' exists." % name)
        self._removeLayer(name)

    def _removeLayer(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.removeLayer`. **name** will
        be a :ref:`type-string` defining the name
        of an existing layer. The value will have
        been normalized with :func:`normalizers.normalizeLayerName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Glyph Interaction
    # -----------------

    # base implementation overrides

    def _getItem(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.__getitem__`. **name** will
        be a :ref:`type-string` defining an existing
        glyph in the default layer. The value will
        have been normalized with :func:`normalizers.normalizeGlyphName`.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer[name]

    def _keys(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.keys`. This must return an
        :ref:`type-immutable-list` of all glyph names
        in the default layer.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer.keys()

    def _newGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.newGlyph`. **name** will be
        a :ref:`type-string` representing a valid
        glyph name. The value will have been tested
        to make sure that an existing glyph in the
        default layer does not have an identical name.
        The value will have been normalized with
        :func:`normalizers.normalizeGlyphName`. This
        must return an instance of :class:`BaseGlyph`
        representing the new glyph.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        # clear is False here because the base newFont
        # that has called this method will have already
        # handled the clearing as specified by the caller.
        return layer.newGlyph(name, clear=False)

    def _removeGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.removeGlyph`. **name** will
        be a :ref:`type-string` representing an
        existing glyph in the default layer. The
        value will have been normalized with
        :func:`normalizers.normalizeGlyphName`.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        layer.removeGlyph(name)

    # order

    glyphOrder = dynamicProperty(
        "base_glyphOrder",
        """
        The preferred order of the glyphs in the font.

            >>> font.glyphOrder
            ["C", "B", "A"]
            >>> font.glyphOrder = ["A", "B", "C"]
        """
    )

    def _get_base_glyphOrder(self):
        value = self._get_glyphOrder()
        value = normalizers.normalizeGlyphOrder(value)
        return value

    def _set_base_glyphOrder(self, value):
        value = normalizers.normalizeGlyphOrder(value)
        self._set_glyphOrder(value)

    def _get_glyphOrder(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.glyphOrder`. This must return
        an :ref:`type-immutable-list` containing glyph
        names representing the glyph order in the font.
        The value will be normalized with
        :func:`normalizers.normalizeGlyphOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_glyphOrder(self, value):
        """
        This is the environment implementation of
        :attr:`BaseFont.glyphOrder`. **value** will
        be a list of :ref:`type-string`. It will
        have been normalized with
        :func:`normalizers.normalizeGlyphOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers.

            >>> font.round()

        This is the equivalent of calling the round method on:

        * info
        * kerning
        * the default layer
        * font-level guidelines

        This applies only to the default layer.
        """
        self._round()

    def _round(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.round`.

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

            >>> font.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.

        This applies only to the default layer.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.autoUnicodes`.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
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
        An :ref:`type-immutable-list` of font-level :class:`BaseGuideline` objects.

            >>> for guideline in font.guidelines:
            ...     guideline.angle
            0
            45
            90
        """
    )

    def _get_guidelines(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.guidelines`. This must
        return an :ref:`type-immutable-list` of
        :class:`BaseGuideline` objects.

        Subclasses may override this method.
        """
        return tuple([self._getitem__guidelines(i) for i in range(self._len__guidelines())])

    def _len__guidelines(self):
        return self._lenGuidelines()

    def _lenGuidelines(self, **kwargs):
        """
        This must return an integer indicating
        the number of font-level guidelines
        in the font.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index):
        index = normalizers.normalizeGuidelineIndex(index)
        if index >= self._len__guidelines():
            raise FontPartsError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setFontInGuideline(guideline)
        return guideline

    def _getGuideline(self, index, **kwargs):
        """
        This must return a :class:`BaseGuideline` object.
        **index** will be a valid **index**.

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

            >>> guideline = font.appendGuideline((50, 0), 90)
            >>> guideline = font.appendGuideline((0, 540), 0, name="overshoot", color=(0, 0, 0, 0.2))

        **position** must be a :ref:`type-coordinate`
        indicating the position of the guideline.
        **angle** indicates the :ref:`type-angle` of
        the guideline. **name** indicates the name
        for the guideline. This must be a :ref:`type-string`
        or ``None``. **color** indicates the color for
        the guideline. This must be a :ref:`type-color`
        or ``None``. This will return the newly created
        :class:`BaseGuidline` object.
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
        This is the environment implementation of
        :meth:`BaseFont.appendGuideline`. **position**
        will be a valid :ref:`type-coordinate`. **angle**
        will be a valid angle. **name** will be a valid
        :ref:`type-string` or ``None``. **color** will
        be a valid :ref:`type-color` or ``None``.
        This must return the newly created
        :class:`BaseGuideline` object.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove **guideline** from the font.

            >>> font.removeGuideline(guideline)
            >>> font.removeGuideline(2)

        **guideline** can be a guideline object or
        an integer representing the guideline index.
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
        This is the environment implementation of
        :meth:`BaseFont.removeGuideline`. **index**
        will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearGuidelines(self):
        """
        Clear all guidelines.

            >>> font.clearGuidelines()
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.clearGuidelines`.

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

            >>> font.interpolate(0.5, otherFont1, otherFont2)
            >>> font.interpolate((0.5, 2.0), otherFont1, otherFont2, round=False)

        The interpolation occurs on a 0 to 1.0 range where **minFont**
        is located at 0 and **maxFont** is located at 1.0. **factor**
        is the interpolation value. It may be less than 0 and greater
        than 1.0. It may be a :ref:`type-int-float` or a tuple of
        two :ref:`type-int-float`. If it is a tuple, the first
        number indicates the x factor and the second number indicates
        the y factor. **round** indicates if the result should be
        rounded to integers. **suppressError** indicates if incompatible
        data should be ignored or if an error should be raised when
        such incompatibilities are found.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minFont, BaseFont):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minFont.__class__.__name__))
        if not isinstance(maxFont, BaseFont):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxFont.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minFont, maxFont, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minFont, maxFont, round=True, suppressError=True):
        """
        This is the environment implementation of
        :meth:`BaseFont.interpolate`.

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
        Evaluate interpolation compatibility with **other**.

            >>> compat, report = self.isCompatible(otherFont)
            >>> compat
            False
            >>> report
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        This will return a ``bool`` indicating if the font is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        if not isinstance(other, BaseFont):
            raise FontPartsError("Compatibility between an instance of %r and an instance of %r can not be checked." % (self.__class__.__name__, other.__class__.__name__))
        return self._isCompatible(other)

    def _isCompatible(self, other):
        """
        This is the environment implementation of
        :meth:`BaseFont.isCompatible`.

        Subclasses may override this method.
        """
        compatable = True
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
            if not f:
                compatable = False
            if r:
                header = layerName
                marker = "-" * len(layerName)
                r = "\n" + header + "\n" + marker + "\n" + r
                report.append(r)
        return compatable, "\n".join(report)

    # -------
    # mapping
    # -------

    def getReverseComponentMapping(self):
        """
        Create a dictionary of unicode -> [glyphname, ...] mappings.
        All glyphs are loaded. Note that one glyph can have multiple unicode values,
        and a unicode value can have multiple glyphs pointing to it.
        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer.getReverseComponentMapping()

    def getCharacterMapping(self):
        """
        Get a reversed map of component references in the font.
        {
        'A' : ['Aacute', 'Aring']
        'acute' : ['Aacute']
        'ring' : ['Aring']
        etc.
        }
        """
        return self._getCharacterMapping()

    def _getCharacterMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getCharacterMapping`.

        Subclasses may override this method.
        """
        layer = self.getLayer(self.defaultLayer)
        return layer.getCharacterMapping()
