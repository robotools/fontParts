# pylint: disable=C0103, W0613
from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any, Generic, List, Optional, Tuple, Type, Union

from fontTools import ufoLib
from fontParts.base.errors import FontPartsError
from fontParts.base.base import dynamicProperty, InterpolationMixin
from fontParts.base.layer import _BaseGlyphVendor
from fontParts.base import normalizers
from fontParts.base.compatibility import FontCompatibilityReporter
from fontParts.base.deprecated import DeprecatedFont, RemovedFont
from fontParts.base.annotations import (
    CharacterMappingType,
    CollectionType,
    IntFloatType,
    QuadrupleCollectionType,
    PairCollectionType,
    TransformationType,
    KerningDictType,
    ReverseComponentMappingType,
)

if TYPE_CHECKING:
    from fontParts.base.info import BaseInfo
    from fontParts.base.groups import BaseGroups
    from fontParts.base.kerning import BaseKerning
    from fontParts.base.features import BaseFeatures
    from fontParts.base.lib import BaseLib
    from fontParts.base.layer import BaseLayer
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.guideline import BaseGuideline


class BaseFont(_BaseGlyphVendor, InterpolationMixin, DeprecatedFont, RemovedFont):
    """Represent the basis for a font object.

    Instances of this class are almost always created with one of the
    font functions in :ref:`fontParts.world`.

    This class will be instantiated in different ways depending on
    the value type of the `pathOrObject` parameter.

    :param pathOrObject: The source for initializing the font.
        If :obj:`None`, a new, empty font will be created. If
        a :class:`str` representing the path to an existing file,
        the class will open and read the file at this path. If an
        instance of the environment's unwrapped native font object,
        it will be wrapped with FontParts. Defaults to :obj:`None`.
    :param showInterface: Whether to display the graphical
        interface. Defaults to :obj:`True`.

    """

    def __init__(
        self,
        pathOrObject: Optional[Union[str, "BaseFont"]] = None,
        showInterface: bool = True,
    ) -> None:
        super(BaseFont, self).__init__(
            pathOrObject=pathOrObject, showInterface=showInterface
        )

    def _reprContents(self) -> List[str]:
        contents: List[str] = [f"'{self.info.familyName} {self.info.styleName}'"]
        if self.path is not None:
            contents.append(f"path={self.path!r}")
        return contents

    # ----
    # Copy
    # ----

    copyAttributes: Tuple[str, ...] = (
        "info",
        "groups",
        "kerning",
        "features",
        "lib",
        "layerOrder",
        "defaultLayerName",
        "glyphOrder",
    )

    def copy(self) -> BaseFont:
        """Copy data from the the current font into a new font.

        This will copy:

        - :attr:`~BaseFont.info`
        - :attr:`~BaseFont.groups`
        - :attr:`~BaseFont.kerning`
        - :attr:`~BaseFont.features`
        - :attr:`~BaseFont.lib`
        - :attr:`~BaseFont.layers`
        - :attr:`~BaseFont.layerOrder`
        - :attr:`~BaseFont.defaultLayerName`
        - :attr:`~BaseFont.glyphOrder`
        - :attr:`~BaseFont.guidelines`

        :return: A new :class:`BaseFont` instance with the same
            attributes as the current instance.

        Example::

            >>> copiedFont = font.copy()

        """
        return super(BaseFont, self).copy()

    def copyData(self, source: BaseFont) -> None:
        """Copy data from another font instance.

        Refer to :meth:`BaseFont.copy` for a list of values that will be
        copied.

        :param source: The source :class:`BaseFont` instance from which
            to copy data.

        Example::

            >>> sourceFont = MyFont('path/to/source.ufo')
            >>> font.copyData(sourceFont)

        """
        # set the default layer name
        self.defaultLayer.name = source.defaultLayerName
        for layerName in source.layerOrder:
            if layerName in self.layerOrder:
                layer = self.getLayer(layerName)
            else:
                layer = self.newLayer(layerName)
            layer.copyData(source.getLayer(layerName))
        for guideline in source.guidelines:
            self.appendGuideline(guideline=guideline)
        super(BaseFont, self).copyData(source)

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(
        self,
        pathOrObject: Optional[Union[str, BaseFont]],
        showInterface: bool,
        **kwargs: Any,
    ) -> None:
        r"""Initialize the native font object.

        This method is the environment implementation
        of :meth:`BaseFont.__init__`. It will wrap a native font
        object based on the value type of the `pathOrObject` parameter.

        :param pathOrObject: The source for initializing the font. Options are:

            +--------------------+---------------------------------------------------+
            | Type               | Description                                       |
            +--------------------+---------------------------------------------------+
            | :obj:`None`        | Create a new font.                                |
            | :class:`str`       | Open the font file located at the given location. |
            | native font object | Wrap the given object.                            |
            +--------------------+---------------------------------------------------+

        :param showInterface: Whether to display the graphical
            interface.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # path

    path: dynamicProperty = dynamicProperty(
        "base_path",
        """Get the path to the font file.

        This property is read-only.

        :return: A :class:`str` defining the location of the file
            or :obj:`None` to indicate that the font does not have a
            file representation.

        Example::

            >>> print(font.path)
            "/path/to/my/font.ufo"

        """,
    )

    def _get_base_path(self) -> Optional[str]:
        path: Optional[str] = self._get_path()
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        return path

    def _get_path(self, **kwargs: Any) -> Optional[str]:  # type: ignore[return]
        r"""Get the path to the native font file.

        This method is the environment implementation
        of :attr:`BaseFont.path`.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`str` defining the location of the file
            or :obj:`None` to indicate that the font does not have a
            file representation. If the value is not :obj:`None` it will
            be normalized with :func:`normalizers.normalizeFilePath`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # save

    def save(
        self,
        path: Optional[str] = None,
        showProgress: bool = False,
        formatVersion: Optional[int] = None,
        fileStructure: Optional[str] = None,
    ) -> None:
        """Save the font to the specified path.

        :param path: The path to which the font should be saved.
            If :obj:`None`, the font is saved to its original location.
            The file type is inferred from the file extension of the
            path. If no extension is given, the environment may use a
            default format. Defaults to :obj:`None`.
        :param showProgress: Whether to display a progress bar during
            the operation. Environments may or may not implement this
            behavior. Defaults to :obj:`False`.
        :param formatVersion: The format version to use when saving the
            file. For example, a `formatVersion` of 2 will save the file
            in UFO 2 format. If :obj:`None`, the original format version
            will be preserved, or the latest version supported by the
            environment will be used if no original version exists.
            Defaults to :obj:`None`.
        :param fileStructure: The file structure for saving UFO formats.
            Can be :obj:`None`, which uses the existing file structure
            or the default structure for unsaved fonts; ``'package'``,
            which is the default structure; or ``'zip'``, which saves
            the font as a ``.ufoz`` file. Defaults to :obj:`None`.

        :raises IOError: If no file location is given in either the
            `path` parameter or the :attr:`BaseFont.path` attribute.

        .. note::

            Environments may define their own rules regarding when a
            file should be saved to its original location versus a new
            location. For example, a font opened from a compiled
            OpenType font may not be saved back into the original
            OpenType file.

        Example::

            >>> font.save()
            >>> font.save("/path/to/my/font-2.ufo")

        """
        if path is None and self.path is None:
            raise IOError(
                ("The font cannot be saved because no file location has been given.")
            )
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        showProgress = bool(showProgress)
        if formatVersion is not None:
            formatVersion = normalizers.normalizeFileFormatVersion(formatVersion)
        if fileStructure is not None:
            fileStructure = normalizers.normalizeFileStructure(fileStructure)
        self._save(
            path=path,
            showProgress=showProgress,
            formatVersion=formatVersion,
            fileStructure=fileStructure,
        )

    def _save(
        self,
        path: Optional[str],
        showProgress: bool,
        formatVersion: Optional[int],
        fileStructure: Optional[str],
        **kwargs: Any,
    ) -> None:
        r"""Save the native font to the specified path.

        This is the environment implementation of :meth:`BaseFont.save`.

        :param path: The file path to save the data to. If not :obj:`None`, the value
            will have been normalized with :func:`normalizers.normalizeFilePath`.
        :param showProgress: Whether to display a progress bar during the
            operation. Environments are not required to display a progress bar
            even if value is :obj:`True`.
        :param formatVersion: The file format version to write the data into.
            If not :obj:`None`, the value will have been normalized
            with :func:`normalizers.normalizeFileFormatVersion`.
        :param fileStructure: The file structure to use.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # close

    def close(self, save: bool = False) -> None:
        """Close the font.

        :param save: Whether to save the font before closing.
            Defaults to :obj:`False`

        Example::

            >>> font.close()
            >>> font.close(save=True)

        """
        if save:
            self.save()
        self._close()

    def _close(self, **kwargs: Any) -> None:
        r"""Close the native font.

        This is the environment implementation
        of :meth:`BaseFont.close`.

        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # generate

    @staticmethod
    def generateFormatToExtension(format: str, fallbackFormat: str) -> str:
        """Return the file extension for the given format identifier.

        This method maps format identifiers to file extensions. If the
        provided `format` is not in the map, the method returns the
        `fallbackFormat`.

        :param format: The format identifier to map to a file extension. Options are:

        +--------------------+-------------------------------------------------------+
        | Format             | Description                                           |
        +--------------------+-------------------------------------------------------+
        | ``'mactype1'``     | Mac Type 1 font (generates suitcase  and LWFN file)   |
        | ``'macttf'``       | Mac TrueType font (generates suitcase)                |
        | ``'macttdfont'``   | Mac TrueType font (generates suitcase with data fork) |
        | ``'otfcff'``       | PS OpenType (CFF-based) font (OTF)                    |
        | ``'otfttf'``       | PC TrueType/TT OpenType font (TTF)                    |
        | ``'pctype1'``      | PC Type 1 font (binary/PFB)                           |
        | ``'pcmm'``         | PC MultipleMaster font (PFB)                          |
        | ``'pctype1ascii'`` | PC Type 1 font (ASCII/PFA)                            |
        | ``'pcmmascii'``    | PC MultipleMaster font (ASCII/PFA)                    |
        | ``'ufo1'``         | UFO format version 1                                  |
        | ``'ufo2'``         | UFO format version 2                                  |
        | ``'ufo3'``         | UFO format version 3                                  |
        | ``'unixascii'``    | UNIX ASCII font (ASCII/PFA)                           |
        +--------------------+-------------------------------------------------------+

        :param fallbackFormat: The extension to return if `format` is
            unrecognized.
        :return: The corresponding file extension for the `format`
            identifier or the `fallbackFormat` if the format is
            unrecognized.

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

    def generate(
        self, format: str, path: Optional[str] = None, **environmentOptions: Any
    ) -> None:
        r"""Generate the font in another format.

        This method converts the font to the specified format and saves
        it to the specified path. Standard format identifiers can be
        found in :attr:`BaseFont.generateFormatToExtension`.

        Environments may support additional keyword arguments in this
        method. For example, if the tool allows decomposing components
        during generation, this can be specified with an additional
        keyword argument.

        :param format: The file format identifier for the output.
        :param path: The location to save the generated file. If not
            provided, the file will be saved in the same directory as
            the source font, with the current file name and the
            appropriate suffix for the format. If a directory is
            specified, the file will be saved with the current file
            name and the appropriate suffix for the format. If a file
            already exists at that location, it will be overwritten.
        :param \**environmentOptions: Additional keyword arguments for
            environment-specific options.
        :raises ValueError: If `format` is not defined.
        :raises TypeError: If `format` is not a :class:`str`.
        :raises UserWarning: If an unsupported environment option is
            passed.
        :raises IOError: If the output path is not defined and the
            source font does not have a path.

        Example::

            >>> font.generate("otfcff")
            >>> font.generate("otfcff", "/path/to/my/font.otf")

        """
        import warnings

        if format is None:
            raise ValueError("The format must be defined when generating.")
        elif not isinstance(format, str):
            raise TypeError("The format must be defined as a string.")
        env = {}
        for key, value in environmentOptions.items():
            valid = self._isValidGenerateEnvironmentOption(key)
            if not valid:
                warnings.warn(
                    f"The {key} argument is not supported in this environment.",
                    UserWarning,
                )
            env[key] = value
        environmentOptions = env
        ext = self.generateFormatToExtension(format, "." + format)
        if path is None and self.path is None:
            raise IOError(
                ("The file cannot be generated because an output path was not defined.")
            )
        elif path is None:
            path = os.path.splitext(self.path)[0]
            path += ext
        elif os.path.isdir(path):
            if self.path is None:
                raise IOError(
                    (
                        "The file cannot be generated because "
                        "the file does not have a path."
                    )
                )
            fileName = os.path.basename(self.path)
            fileName += ext
            path = os.path.join(path, fileName)
        path = normalizers.normalizeFilePath(path)
        return self._generate(
            format=format, path=path, environmentOptions=environmentOptions
        )

    @staticmethod
    def _isValidGenerateEnvironmentOption(name: str) -> bool:
        """Validate if the environment option is supported.

        Any unknown keyword arguments given to :meth:`BaseFont.generate`
        are passed to this method. `name` is the name used for the
        argument. Environments may evaluate if `name` is a supported
        option.

        :param name: The name of the environment option to validate.
        :return: :obj:`True` if the environment option is supported,
            otherwise :obj:`False`.

        .. note::

            Subclasses may override this method.

        """
        return False

    def _generate(
        self,
        format: str,
        path: Optional[str],
        environmentOptions: dict,
        **kwargs: object,
    ) -> None:
        """Generate the native font in another format.

        This is the environment implementation
        of :meth:`BaseFont.generate`. Refer to
        the :attr:`BaseFont.generateFormatToExtension` documentation
        for the standard format identifiers.

        :param format: The output format identifier. If the value given
            for `format` is not supported by the environment,
            the environment must raise :exc:`FontPartsError`.
        :param path: The location where the generated file should be
            saved. The value will have been normalized
            with :func:`normalizers.normalizeFilePath`.
        :param environmentOptions: A dictionary of environment-specific
            options. These options are validated
            with :meth:`BaseFont._isValidGenerateEnvironmentOption` and
            the given values. These values are not passed through any
            normalization functions.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # info

    info: dynamicProperty = dynamicProperty(
        "base_info",
        """Get the font's info object.

        This property is read-only.

        :return: An instance of the :class:`BaseInfo` class.

        Example::

            >>> font.info.familyName
            "My Family"

        """,
    )

    def _get_base_info(self) -> BaseInfo:
        info: BaseInfo = self._get_info()
        info.font = self
        return info

    def _get_info(self) -> BaseInfo:  # type: ignore[return]
        """Get the native font's info object.

        This is the environment implementation of :attr:`BaseFont.info`.

        :return: An instance of a :class:`BaseInfo` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # groups

    groups: dynamicProperty = dynamicProperty(
        "base_groups",
        """Get the font's groups object.

        This property is read-only.

        :return: An instance of the :class:`BaseGroups` class.

        Example::

            >>> font.groups["myGroup"]
            ["A", "B", "C"]

        """,
    )

    def _get_base_groups(self) -> BaseGroups:
        groups: BaseGroups = self._get_groups()
        groups.font = self
        return groups

    def _get_groups(self) -> BaseGroups:  # type: ignore[return]
        """Get the native font's groups object.

        This is the environment implementation
        of :attr:`BaseFont.groups`.

        :return: an instance of a :class:`BaseGroups` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # kerning

    kerning: dynamicProperty = dynamicProperty(
        "base_kerning",
        """Get the font's kerning object.

        This property is read-only.

        :return: An instance of the :class:`BaseKerning` class.

        Example::

            >>> font.kerning["A", "B"]
            -100

        """,
    )

    def _get_base_kerning(self) -> BaseKerning:
        kerning: BaseKerning = self._get_kerning()
        kerning.font = self
        return kerning

    def _get_kerning(self) -> BaseKerning:  # type: ignore[return]
        """Get the native font's kerning object.

        This is the environment implementation
        of :attr:`BaseFont.kerning`.

        :return: An instance of a :class:`BaseKerning` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def getFlatKerning(self) -> KerningDictType:
        """Get the font's kerning as a flat dictionary.

        :return: A :class:`dict` of the font's :class:`BaseKerning` keys
            mapped to their respective values.

        """
        return self._getFlatKerning()

    def _getFlatKerning(self) -> KerningDictType:
        """Get the native font's kerning as a flat dictionary.

        This is the environment implementation of
        :meth:`BaseFont.getFlatKerning`.

        :return: A :class:`dict` of the font's :class:`BaseKerning`
            subclass keys mapped to their respective values.

        .. note::

            Subclasses may override this method.

        """
        kernOrder = {
            (True, True): 0,  # group group
            (True, False): 1,  # group glyph
            (False, True): 2,  # glyph group
            (False, False): 3,  # glyph glyph
        }

        def kerningSortKeyFunc(pair):
            g1, g2 = pair
            g1grp = g1.startswith("public.kern1.")
            g2grp = g2.startswith("public.kern2.")
            return (kernOrder[g1grp, g2grp], pair)

        flatKerning = dict()
        kerning = self.kerning
        groups = self.groups

        for pair in sorted(self.kerning.keys(), key=kerningSortKeyFunc):
            kern_value = kerning[pair]
            (left, right) = pair
            if left.startswith("public.kern1."):
                left = groups.get(left, [])
            else:
                left = [left]

            if right.startswith("public.kern2."):
                right = groups.get(right, [])
            else:
                right = [right]

            for right_glyph in right:
                for left_glyph in left:
                    flatKerning[(left_glyph, right_glyph)] = kern_value

        return flatKerning

    # features

    features: dynamicProperty = dynamicProperty(
        "base_features",
        """Get the font's features object.

        This property is read-only.

        :return: An instance of the :class:`BaseFeatures` class.

        Example::

            >>> font.features.text
            "include(features/substitutions.fea);"

        """,
    )

    def _get_base_features(self) -> BaseFeatures:
        features: BaseFeatures = self._get_features()
        features.font = self
        return features

    def _get_features(self) -> BaseFeatures:  # type: ignore[return]
        """Get the native font's features object.

        This is the environment implementation of
        :attr:`BaseFont.features`.

        :return: An instance of a :class:`BaseFeatures` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # lib

    lib: dynamicProperty = dynamicProperty(
        "base_lib",
        """Get the font's lib object.

        This property is read-only.

        :return: An instance of the :class:`BaseLib` class.

        Example::

            >>> font.lib["org.robofab.hello"]
            "world"

        """,
    )

    def _get_base_lib(self) -> BaseLib:
        lib: BaseLib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self) -> BaseLib:  # type: ignore[return]
        """Get the native font's lib object.

        This is the environment implementation of :attr:`BaseFont.lib`.

        :return: An instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # tempLib

    tempLib: dynamicProperty = dynamicProperty(
        "base_tempLib",
        """Get the font's temporary lib object.

        This property is read-only.

        This property provides access to a temporary instance of
        the :class:`BaseLib` class, used for storing data that should
        not be persisted. It is similar to :attr:`BaseFont.lib`, except
        that its contents will not be saved when calling
        the :meth:`BaseFont.save` method.

        :return: A temporary instance of the :class:`BaseLib` class.

        Example::

            >>> font.tempLib["org.robofab.hello"]
            "world"

        """,
    )

    def _get_base_tempLib(self) -> BaseLib:
        lib: BaseLib = self._get_tempLib()
        lib.font = self
        return lib

    def _get_tempLib(self) -> BaseLib:  # type: ignore[return]
        """Get the native font's temporary lib object.

        This is the environment implementation
        of :attr:`BaseFont.tempLib`.

        :return: A temporary instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -----------------
    # Layer Interaction
    # -----------------

    layers: dynamicProperty = dynamicProperty(
        "base_layers",
        """Get the font's layer objects.

        This property is read-only.

        :return: A :class:`tuple` containing instances of
            the :class:`BaseLayer` class.

        Example::

            >>> for layer in font.layers:
            ...     layer.name
            "My Layer 1"
            "My Layer 2"

        """,
    )

    def _get_base_layers(self) -> Tuple[BaseLayer, ...]:
        layers: Tuple[BaseLayer, ...] = self._get_layers()
        for layer in layers:
            self._setFontInLayer(layer)
        return tuple(layers)

    def _get_layers(self, **kwargs: Any) -> Tuple[BaseLayer, ...]:  # type: ignore[return]
        r"""Get the native font's layer objects.

        This is the environment implementation of
        :attr:`BaseFont.layers`.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`tuple` containing instances
            of the :class:`BaseLayer` subclass. The items  should be in
            the order defined by :attr:`BaseFont.layerOrder`.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # order

    layerOrder: dynamicProperty = dynamicProperty(
        "base_layerOrder",
        """Get or set the order of the layers in the font.

        The value must be a :class:`list` or :class:`tuple` of layer
        names as :class:`str` reflecting the desired order of the
        font's :class:`BaseLayer` objects.

        :return: A :class:`tuple` of layer names as :class:`str` in
            their defined order.

        Example::

            >>> font.layerOrder = ["My Layer 2", "My Layer 1"]
            >>> font.layerOrder
            ("My Layer 2", "My Layer 1")

        """,
    )

    def _get_base_layerOrder(self) -> Tuple[str, ...]:
        value: CollectionType[str] = self._get_layerOrder()
        value = normalizers.normalizeLayerOrder(value, self)
        return value

    def _set_base_layerOrder(self, value: CollectionType[str]) -> None:
        value = normalizers.normalizeLayerOrder(value, self)
        self._set_layerOrder(value)

    def _get_layerOrder(self, **kwargs: Any) -> Tuple[str, ...]:  # type: ignore[return]
        r"""Get the order of the layers in the native font.

        This is the environment implementation of the
        :attr:`BaseFont.layerOrder` property getter.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`list` of layer names in their defined order.
            The value will be normalized with :func:`normalizers.normalizeLayerOrder`.
        :raises NotImplementedError: If the method has not
            beenoverridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_layerOrder(self, value: CollectionType[str], **kwargs: Any) -> None:
        r"""Set the order of the layers in the native font.

        This is the environment implementation of the
        :attr:`BaseFont.layerOrder` property setter.

        :param value: A :class:`list` or :class:`tuple` of layer names
            reflecting the desired order of the font's :class:`BaseLayer` objects.
            The value will have been normalized
            with :func:`normalizers.normalizeLayerOrder`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # default layer

    def _setFontInLayer(self, layer: BaseLayer) -> None:
        if layer.font is None:
            layer.font = self

    defaultLayerName: dynamicProperty = dynamicProperty(
        "base_defaultLayerName",
        """Get or set the name of the font's default layer.

        The value must be name of the desired default :class`BaseLayer`
        instance as a :class:`str`.

        :return: The name of the current default :class`BaseLayer`
            instance.

        Example::

            >>> font.defaultLayerName = "My Layer 2"
            >>> font.defaultLayerName
            "My Layer 2"

        """,
    )

    def _get_base_defaultLayerName(self) -> str:
        value = self._get_defaultLayerName()
        value = normalizers.normalizeDefaultLayerName(value, self)
        return value

    def _set_base_defaultLayerName(self, value: str) -> None:
        value = normalizers.normalizeDefaultLayerName(value, self)
        self._set_defaultLayerName(value)

    def _get_defaultLayerName(self) -> str:  # type: ignore[return]
        """Get the name of the native font's default layer.

        This is the environment implementation of
        :attr:`BaseFont.defaultLayerName` property getter.
        :return: The name of the current default :class`BaseLayer`
            subclass instance. The value will be normalized
            with :func:`normalizers.normalizeDefaultLayerName`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_defaultLayerName(self, value: str, **kwargs: Any) -> None:
        r"""Set the name of the native font's default layer.

        This is the environment implementation of
        :attr:`BaseFont.defaultLayerName` property setter.
        :param value: The name of the desired default :class`BaseLayer`
            subclass instance. The name will have been normalized
            with :func:`normalizers.normalizeDefaultLayerName`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    defaultLayer: dynamicProperty = dynamicProperty(
        "base_defaultLayer",
        """Get or set the font's default layer.

        The value must be the desired default :class:`BaseLayer` instance.

        :return: The current default :class:`BaseLayer` instance.

        Example::

            >>> layer = font.defaultLayer
            >>> font.defaultLayer = otherLayer

        """,
    )

    def _get_base_defaultLayer(self) -> BaseLayer:
        layer: BaseLayer = self._get_defaultLayer()
        layer = normalizers.normalizeLayer(layer)
        return layer

    def _set_base_defaultLayer(self, layer: BaseLayer) -> None:
        layer = normalizers.normalizeLayer(layer)
        self._set_defaultLayer(layer)

    def _get_defaultLayer(self) -> BaseLayer:
        """Get the native font's default layer.

        This is the environment implementation of the
        :attr:`BaseFont.defaultLayer` property getter.

        :return: The default :class:`BaseLayer` subclass instance.
            The value will be normalized with :func:`normalizers.normalizeLayer`.

        .. important::

            Subclasses must override this method.

        """
        name = self.defaultLayerName
        layer = self.getLayer(name)
        return layer

    def _set_defaultLayer(self, value: BaseLayer) -> None:
        """Set the native font's default layer.

        This is the environment implementation of the
        :attr:`BaseFont.defaultLayer` property setter.

        :param value: The desired default :class:`BaseLayer` subclass
            instance. The value will have been normalized
            with :func:`normalizers.normalizeLayer`.

        .. important::

            Subclasses must override this method.

        """
        self.defaultLayerName = value.name

    # get

    def getLayer(self, name: str) -> BaseLayer:
        """Get the named layer from the font.

        :param name: The name of the :class:`BaseLayer` instance to
            retrieve.
        :return: The specified :class:`Baselayer` instance.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        Example::

            >>> font.getLayer("My Layer 2")
            <Layer 'My Layer 2' at 0x...>

        """
        name = normalizers.normalizeLayerName(name)
        if name not in self.layerOrder:
            raise ValueError(f"No layer with the name '{name}' exists.")
        layer = self._getLayer(name)
        self._setFontInLayer(layer)
        return layer

    def _getLayer(self, name: str, **kwargs: Any) -> BaseLayer:
        r"""Get the named layer from the native font.

        This is the environment implementation of
        :meth:`BaseFont.getLayer`.

        :param name: The name of the :class:`BaseLayer` subclass
            instance to retrieve.
        :param \**kwargs: Additional keyword arguments.
        :return: The specified :class:`BaseLayer` subclass instance. The value
            will have been normalized with :func:`normalizers.normalizeLayerName`
            and verified as an existing layer.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        .. note::

            Subclasses may override this method.

        """
        for layer in self.layers:
            if layer.name == name:
                return layer
        raise ValueError(f"No layer with the name '{name}' exists.")

    # new

    def newLayer(
        self, name: str, color: Optional[QuadrupleCollectionType[IntFloatType]] = None
    ) -> BaseLayer:
        """Create a new layer in the font.

        :param name: The name of the new layer to create.
        :param color: The color value to assign to the new layer.
            Defaults to :obj:`None`.
        :return: A newly created :class:`BaseLayer` instance.

        Example::

            >>> layer = font.newLayer("My Layer 3")

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

    def _newLayer(  # type: ignore[return]
        self,
        name: str,
        color: Optional[QuadrupleCollectionType[IntFloatType]],
        **kwargs: Any,
    ) -> BaseLayer:
        r"""Create a new layer in the native font.

        This is the environment implementation of
        :meth:`BaseFont.newLayer`.

        :param name: The name of the new layer to create. The value must
            be unique to the font and will have been normalized
            with :func:`normalizers.normalizeLayerName`.
        :param color: The color value to assign to the new layer. If the
            value is not :obj:`None`, it will have been normalized with
            :func:`normalizers.normalizeColor`.
        :param \**kwargs: Additional keyword arguments.
        :return: A newly created :class:`BaseLayer` subclass instance.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, name: str) -> None:
        """Remove the specified layer from the font.

        :param name: The name of the layer to remove.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        Example::

            >>> font.removeLayer("My Layer 3")

        """
        name = normalizers.normalizeLayerName(name)
        if name not in self.layerOrder:
            raise ValueError(f"No layer with the name '{name}' exists.")
        self._removeLayer(name)

    def _removeLayer(self, name: str, **kwargs: Any) -> None:
        r"""Remove the specified layer from the native font.

        This is the environment implementation of
        :meth:`BaseFont.removeLayer`.

        :param name: The name of the layer to remove. The value will have been
            normalized with :func:`normalizers.normalizeLayerName`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # insert

    def insertLayer(self, layer: BaseLayer, name: Optional[str] = None) -> BaseLayer:
        """Insert a specified layer into the font.

        This method will not insert a layer directly, but rather create
        a new :class:`BaseLayer` instance containing the data from
        `layer`. The data inserted from `layer` is the same data as
        documented in :meth:`BaseLayer.copy`.

        :param layer: The :class:`BaseLayer` instance to insert.
        :param name: The name to assign to the new layer after
            insertion. If value is :obj:`None`, the origninal name will
            be used. Defaults to :obj:`None`.
        :return: The newly inserted :class:`BaseLayer` instance.

        Example::

            >>> layer = font.insertLayer(otherLayer, name="layer 2")

        """
        if name is None:
            name = layer.name
        normalizedName = normalizers.normalizeLayerName(name)
        if normalizedName in self:
            self.removeLayer(normalizedName)
        return self._insertLayer(layer, name=normalizedName)

    def _insertLayer(self, layer: BaseLayer, name: str, **kwargs: Any) -> BaseLayer:
        r"""Insert a specified layer into the native font.

        This is the environment implementation of :meth:`BaseFont.insertLayer`.

        An environment must not insert `layer` directly, but rather copy
        it's data to a new layer.

        :param layer: A layer object with the attributes  necessary for
            copying as defined in :meth:`BaseLayer.copy`.
        :param name: The name to assign to the new layer after
            insertion. The value will have been normalized
            with :func:`normalizers.normalizeLayerName` and tested to
            make sure that it is unique to the font.
        :param \**kwargs: Additional keyword arguments.
        :return: The newly inserted :class:`BaseLayer` subclass instance.

        .. note::

            Subclasses may override this method.

        """
        if name != layer.name and layer.name in self.layerOrder:
            layer = layer.copy()
            layer.name = name
        dest = self.newLayer(name)
        dest.copyData(layer)
        return dest

    # duplicate

    def duplicateLayer(self, layerName: str, newLayerName: str) -> BaseLayer:
        """Duplicate the specified layer in the font.

        This method creates a new :class:`BaseLayer` instance. It copies
        data from the layer named `layerName` into this new instance,
        assigns it the name specified by `newLayerName`, and then
        inserts the new layer into the font.

        :param layerName: The name of the layer to duplicate.
        :param newLayerName: The new name to assign to the duplicated
            layer.
        :return: The newly duplicated :class:`BaseLayer` instance.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        Example::

            >>> layer = font.duplicateLayer("layer 1", "layer 2")

        """
        layerOrder = self.layerOrder
        layerName = normalizers.normalizeLayerName(layerName)
        if layerName not in layerOrder:
            raise ValueError(f"No layer with the name '{layerName}' exists.")
        newLayerName = normalizers.normalizeLayerName(newLayerName)
        if newLayerName in layerOrder:
            raise ValueError(f"A layer with the name '{newLayerName}' already exists.")
        newLayer = self._duplicateLayer(layerName, newLayerName)
        newLayer = normalizers.normalizeLayer(newLayer)
        return newLayer

    def _duplicateLayer(self, layerName: str, newLayerName: str) -> BaseLayer:
        """Duplicate the specified layer in the native font.

        This is the environment implementation
        of :meth:`BaseFont.duplicateLayer`.

        :param layerName: The name of the layer to duplicate. The value
            will have been normalized
            with :func:`normalizers.normalizeLayerName` and tested to
            make sure that it already exists in the font.
        :param newLayerName: The new name to assign to the duplicated
            layer. The value will have been normalized
            with :func:`normalizers.normalizeLayerName` and tested to
            make sure that it does not already exist in the font.
        :return: The newly duplicated :class:`BaseLayer` subclass
            instance.

        .. note::

            Subclasses may override this method.

        """
        newLayer = self.getLayer(layerName).copy()
        return self.insertLayer(newLayer, newLayerName)

    def swapLayerNames(self, layerName: str, otherLayerName: str) -> None:
        """Swap the names of two specific layers in the font.

        This method assigns the name `layerName` to the layer currently
        named `otherLayerName` and assigns the name `otherLayerName` to
        the layer currently named `layerName`.

        :param layerName: The name of one layer.
        :param otherNAme: The name of the other layer.
        :raises ValueError: If no layer with the given `layerName` or
            `otherLayerName` exists in the font.

        Example::

            >>> font.swapLayerNames("before drawing revisions",
            ...                     "after drawing revisions")

        """
        layerOrder = self.layerOrder
        layerName = normalizers.normalizeLayerName(layerName)
        if layerName not in layerOrder:
            raise ValueError(f"No layer with the name '{layerName}' exists.")
        otherLayerName = normalizers.normalizeLayerName(otherLayerName)
        if otherLayerName not in layerOrder:
            raise ValueError(f"No layer with the name '{otherLayerName}' exists.")
        self._swapLayerNames(layerName, otherLayerName)

    def _swapLayerNames(self, layerName: str, otherLayerName: str) -> None:
        """Swap the names of two specific layers in the native font.

        This is the environment implementation
        of :meth:`BaseFont.swapLayerNames`.

        Both `layerName` and `otherLayerName` will have been normalized
        with :func:`normalizers.normalizeLayerName` and tested to make
        sure they already exist in the font.

        :param layerName: The name of one layer.
        :param otherName: The name of the other layer.

        .. note::

            Subclasses may override this method.

        """
        import random

        layer1 = self.getLayer(layerName)
        layer2 = self.getLayer(otherLayerName)
        # make a temporary name and assign it to
        # the first layer to prevent two layers
        # from having the same name at once.
        layerOrder = self.layerOrder
        for _ in range(50):
            # shout out to PostScript unique IDs
            tempLayerName = str(random.randint(4000000, 4999999))
            if tempLayerName not in layerOrder:
                break
        else:
            raise FontPartsError(
                "Couldn't find a temporary layer name after 50 tries. "
                "Sorry. Please try again."
            )
        layer1.name = tempLayerName
        # now swap
        layer2.name = layerName
        layer1.name = otherLayerName

    # -----------------
    # Glyph Interaction
    # -----------------

    # base implementation overrides

    def _getItem(self, name: str, **kwargs: Any) -> BaseGlyph:
        r"""Get the specified glyph from the native default layer.

        This is the environment implementation of
        :meth:`BaseFont.__getitem__`.

        :param name: The name of the glyph to retrieve from the default layer.
            The value will have been normalized
            with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :return: the specified instance of a :class:`BaseGlyph`
            subclass.

         .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        return layer[name]

    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:
        r"""Get a list of all glyph names in the native default layer.

        This is the environment implementation of :meth:`BaseFont.keys`.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`tuple` of glyph names as :class:`str`.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        return layer.keys()

    def _newGlyph(self, name: str, **kwargs: Any) -> BaseGlyph:
        r"""Create a new glyph in the native default layer.

        This is the environment implementation of :meth:`BaseFont.newGlyph.

        :param name: The name to assign to the new glyph. The value will
            have been normalized
            with :func:`normalizers.normalizeGlyphName` and verified as
            unique within the default layer.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseGlyph subclass representing
            the new glyph.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        # clear is False here because the base newFont
        # that has called this method will have already
        # handled the clearing as specified by the caller.
        return layer.newGlyph(name, clear=False)

    def _removeGlyph(self, name: str, **kwargs: Any) -> None:
        r"""Remove the specified glyph from the default layer.

        .. deprecated::

            Use :meth:`BaseFont.__delitem__` instead.

        This is the environment implementation of
        :meth:`BaseFont.removeGlyph`.

        :param name: The name of the glyph to remove. The value will be
            normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        layer.removeGlyph(name)

    def __setitem__(self, name: str, glyph: BaseGlyph) -> BaseGlyph:
        """Insert the specified glyph into the font.

        Example::

            >>> glyph = font["A"] = otherGlyph

        This will not insert a glyph directly, but rather create
        a new :class:`BaseGlyph` instance containing the data from
        `glyph`. The data inserted from `glyph` is the same data as
        documented in :meth:`BaseGlyph.copy`.

        On a font level, :attr:`.glyphOrder` will be preserved if
            the `name` is already present.

        :param name: The name to assign to the new glyph after
            insertion.
        :param glyph: The layer :class:`BaseGlyph` instance to insert.
        :return: The newly inserted :class:`BaseGlyph` instance.

        """
        name = normalizers.normalizeGlyphName(name)
        if name in self:
            # clear the glyph here if the glyph exists
            dest = self._getItem(name)
            dest.clear()
        return self._insertGlyph(glyph, name=name, clear=False)

    # order

    glyphOrder: dynamicProperty = dynamicProperty(
        "base_glyphOrder",
        """Get or set the order of the glyphs in the font.

        The value must be a :class:`list` or :class:`tuple` of glyph names
        reflecting the desired order of the font's :class:`BaseGlyph` objects.

        :return: A :class:`tuple` of glyph names in their defined order.

        Example::

            >>> font.glyphOrder
            ["C", "B", "A"]
            >>> font.glyphOrder = ("A", "B", "C")

        """,
    )

    def _get_base_glyphOrder(self) -> Tuple[str, ...]:
        value = self._get_glyphOrder()
        value = normalizers.normalizeGlyphOrder(value)
        return value

    def _set_base_glyphOrder(self, value: CollectionType[str]) -> None:
        value = normalizers.normalizeGlyphOrder(value)
        self._set_glyphOrder(value)

    def _get_glyphOrder(self) -> Tuple[str, ...]:  # type: ignore[return]
        r"""Get the order of the glyphs in the native font.

        This is the environment implementation of the
        :attr:`BaseFont.glyphrOrder` property getter.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`tuple` of layer names in their defined order.
            The value will be normalized with :func:`normalizers.normalizeGlyphOrder`.
        :raises NotImplementedError: If the method has not
            beenoverridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_glyphOrder(self, value: CollectionType[str]) -> None:
        r"""Set the order of the glyphs in the native font.

        This is the environment implementation of the
        :attr:`BaseFont.glyphrOrder` property setter.

        :param value: A :class:`list` of glyph names reflecting the
            desired order of the font's :class:`BaseGlyph` objects.
            The value will have been normalized
            with :func:`normalizers.normalizeGlyphOrder`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self) -> None:
        """Round all appropriate font data to integers.

        This method applies only to the glyphs in the default layer
        of the font. It is the equivalent of calling the :meth:`round`
        method on:

        - :attr:`info`
        - :attr:`kerning`
        - :attr:`defaultLayer`
        - :attr:`guidelines`

        Example::

            >>> font.round()

        """
        self._round()

    def _round(self) -> None:
        """Round all appropriate native font data to integers.

        This is the environment implementation of :meth:`BaseFont.round`.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        layer.round()
        self.info.round()
        self.kerning.round()
        for guideline in self.guidelines:
            guideline.round()

    def autoUnicodes(self) -> None:
        """Use heuristics to set Unicode values in all font glyphs.

        This method applies only to the glyphs in the default layer
        of the font. Environments will define their own heuristics for
        automatically determining values.

        Example::

            >>> font.autoUnicodes()

        """
        self._autoUnicodes()

    def _autoUnicodes(self) -> None:
        """Use heuristics to set Unicode values in all native font glyphs.

        This is the environment implementation of
        :meth:`BaseFont.autoUnicodes`.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        layer.autoUnicodes()

    # ----------
    # Guidelines
    # ----------

    def _setFontInGuideline(self, guideline):
        if guideline.font is None:
            guideline.font = self

    guidelines: dynamicProperty = dynamicProperty(
        "guidelines",
        """Get the font-level guideline objects.

        This property is read-only.

        :return: A :class:`tuple` containing instances of
            the :class:`BaseGuideline` class.

            >>> for guideline in font.guidelines:
            ...     guideline.angle
            0
            45
            90

        """,
    )

    def _get_guidelines(self) -> Tuple[BaseGuideline, ...]:
        """Get the native font-level guideline objects.

        This is the environment implementation of
        :attr:`BaseFont.guidelines`.

        :return: A :class:`tuple` containing instances
            of the :class:`BaseGuideline` subclass.

        .. note::

            Subclasses may override this method.

        """
        return tuple(
            self._getitem__guidelines(i) for i in range(self._len__guidelines())
        )

    def _len__guidelines(self) -> int:
        return self._lenGuidelines()

    def _lenGuidelines(self, **kwargs: Any) -> int:  # type: ignore[return]
        r"""Return the number of font-level guidelines in the native font.

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` indicating the number of font-level
            :class:`BaseGuideline` subclass instances in the font.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index: int) -> BaseGuideline:
        normalizedIndex = normalizers.normalizeIndex(index)
        if normalizedIndex is None or normalizedIndex >= self._len__guidelines():
            raise ValueError(f"No guideline located at index {normalizedIndex}.")
        guideline = self._getGuideline(normalizedIndex)
        self._setFontInGuideline(guideline)
        return guideline

    def _getGuideline(self, index: int, **kwargs: Any) -> BaseGuideline:  # type: ignore[return]
        r"""Return the guideline at the given index.

        :param index: The index of the guideline.
        :param \**kwargs: Additional keyword arguments.

        :return: An instance of a :class:`BaseGuideline` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getGuidelineIndex(self, guideline: BaseGuideline) -> int:
        for i, other in enumerate(self.guidelines):
            if guideline == other:
                return i
        raise FontPartsError("The guideline could not be found.")

    def appendGuideline(
        self,
        position: Optional[PairCollectionType[IntFloatType]] = None,
        angle: Optional[IntFloatType] = None,
        name: Optional[str] = None,
        color: Optional[QuadrupleCollectionType[IntFloatType]] = None,
        guideline: Optional[BaseGuideline] = None,
    ) -> BaseGuideline:
        """Append a new guideline to the font.

        This method will create a new :class:`BaseGuideline` with the
        provided values. Values may be copied from
        the specified `guideline` or passed individually to the
        appropriate parameters.

        :param position: The optional position for the guideline as
            a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param angle: The optional angle for the guideline as
            a :class:`float`. Defaults to :obj:`None`.
        :param name: The optional name for the guideline as
            a :class:`str`. Defaults to :obj:`None`.
        :param color: The optional color for the guideline as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :param guideline: The optional :class:`BaseGuideline` instance
            from which to copy values. If `position`, `angle`, `name`,
            or `color` are specified, those values will be used instead.
            Defaults to :obj:`None`.
        :return: The newly appended instance of
            the :class:`BaseGuideline` class.

        Example::

            >>> guideline = font.appendGuideline((50, 0), 90)
            >>> guideline = font.appendGuideline((0, 540), 0, name="overshoot",
            ... color=(0, 0, 0, 0.2))

        """
        identifier = None
        if guideline is not None:
            normalizedGuideline = normalizers.normalizeGuideline(guideline)
            if position is None:
                position = normalizedGuideline.position
            if angle is None:
                angle = normalizedGuideline.angle
            if name is None:
                name = normalizedGuideline.name
            if color is None:
                color = normalizedGuideline.color
            if normalizedGuideline.identifier is not None:
                existing = set(
                    [g.identifier for g in self.guidelines if g.identifier is not None]
                )
                if normalizedGuideline.identifier not in existing:
                    identifier = normalizedGuideline.identifier
        if position is not None:
            position = normalizers.normalizeCoordinateTuple(position)
        else:
            raise ValueError("Position cannot be None.")
        if angle is not None:
            angle = normalizers.normalizeRotationAngle(angle)
        if name is not None:
            name = normalizers.normalizeGuidelineName(name)
        if color is not None:
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
        newGuideline = self._appendGuideline(
            position, angle, name=name, color=color, identifier=identifier
        )
        newGuideline.font = self
        return newGuideline

    def _appendGuideline(  # type: ignore[return]
        self,
        position: PairCollectionType[IntFloatType],
        angle: Optional[float],
        name: Optional[str],
        color: Optional[QuadrupleCollectionType[IntFloatType]],
        **kwargs: Any,
    ) -> BaseGuideline:
        r"""Append a new guideline to the native font.

        This is the environment implementation of
        :meth:`BaseFont.appendGuideline`.

        :param position: The position for the guideline as
            a :ref:`type-coordinate`.
        :param angle: The angle for the guideline as a :class:`float`.
        :param name: The name for the guideline as a :class:`str`.
        :param color: The color for the guideline as a :ref:`type-color`.
        :param \**kwargs: Additional keyword arguments.
        :return: The newly appended instance of
            the :class:`BaseGuideline` subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline: Union[int, BaseGuideline]) -> None:
        """Remove a guideline from the font.

        :param guideline: A :class:`BaseGuideline` object or an integer
            representing a :attr:`BaseGuideline.index`.
        :raises: ValueError if no guideline is found at the given `index`.

        Example::

            >>> font.removeGuideline(guideline)
            >>> font.removeGuideline(2)

        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(guideline)
        normalizedIndex = normalizers.normalizeIndex(index)
        # Avoid mypy conflict with normalizeIndex -> Optional[int]
        if normalizedIndex is None:
            return
        if normalizedIndex >= self._len__guidelines():
            raise ValueError(f"No guideline located at index {normalizedIndex}.")
        self._removeGuideline(normalizedIndex)

    def _removeGuideline(self, index: int, **kwargs: Any) -> None:
        """Remove the guideline at the specified index.

        This is the environment implementation of
        :meth:`BaseFont.removeGuideline`.

        :param index: The index of the guideline to remove.
        :raises NotImplementedError: If the method has not been overridden
            by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearGuidelines(self) -> None:
        """Clear all guidelines in the font.

        Example::

            >>> font.clearGuidelines()

        """
        self._clearGuidelines()

    def _clearGuidelines(self) -> None:
        """Clear all guidelines in the native font.

        This is the environment implementation of
        :meth:`BaseFont.clearGuidelines`.

        .. note::

            Subclasses may override this method.

        """
        for _ in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # -------------
    # Interpolation
    # -------------

    def interpolate(
        self,
        factor: TransformationType,
        minFont: BaseFont,
        maxFont: BaseFont,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """Interpolate all possible data in the font.

        The interpolation occurs on a 0 to 1.0 range between `minFont`
        and `maxFont`, using the specified `factor`.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minFont: The :class:`BaseFont` instance corresponding to the 0.0
            position in the interpolation.
        :param maxFont: The :class:`BaseFont` instance corresponding to the 1.0
            position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minFont` or `maxFont` are not instances
            of :class:`BaseFont`.

        Example::

            >>> font.interpolate(0.5, otherFont1, otherFont2)
            >>> font.interpolate((0.5, 2.0), otherFont1, otherFont2, round=False)

        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minFont, BaseFont):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {minFont.__class__.__name__!r}."
            )
        if not isinstance(maxFont, BaseFont):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {maxFont.__class__.__name__!r}."
            )
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(
            factor, minFont, maxFont, round=round, suppressError=suppressError
        )

    def _interpolate(
        self,
        factor: TransformationType,
        minFont: BaseFont,
        maxFont: BaseFont,
        round: bool,
        suppressError: bool,
    ) -> None:
        """Interpolate all possible data in the native font.

        This is the environment implementation of :meth:`BaseFont.interpolate`.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minFont: The :class:`BaseFont` subclass instance
            corresponding to the 0.0 position in the interpolation.
        :param maxFont: The :class:`BaseFont` subclass instance
            corresponding to the 1.0 position in the interpolation.
        :param round: A boolean indicating whether the result should
            be rounded to integers.
        :param suppressError: A boolean indicating whether to ignore
            incompatible data or raise an error when such incompatibilities
            are found.
        :raises TypeError: If `minFont` or `maxFont` are not instances
            of :class:`BaseFont`.

        .. note::

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
            dstLayer.interpolate(
                factor, minLayer, maxLayer, round=round, suppressError=suppressError
            )
        if self.layerOrder:
            if ufoLib.DEFAULT_LAYER_NAME in self.layerOrder:
                self.defaultLayer = self.getLayer(ufoLib.DEFAULT_LAYER_NAME)
            else:
                self.defaultLayer = self.getLayer(self.layerOrder[0])
        # kerning and groups
        self.kerning.interpolate(
            factor,
            minFont.kerning,
            maxFont.kerning,
            round=round,
            suppressError=suppressError,
        )
        # info
        self.info.interpolate(
            factor, minFont.info, maxFont.info, round=round, suppressError=suppressError
        )

    compatibilityReporterClass = FontCompatibilityReporter

    def isCompatible(
        self, other: BaseFont, cls=None
    ) -> Tuple[bool, FontCompatibilityReporter]:
        """Evaluate interpolation compatibility with another font.

        This method will return a :class:`bool` indicating if the font is
        compatible for interpolation with `other`, and a :class:`str`
        containing compatibility notes.

        :param other: The other :class:`BaseFont` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.FontCompatibilityReporter` instance.

        Example::

            >>> compatible, report = self.isCompatible(otherFont)
            >>> compatible
            False
            >>> report
            [Fatal] Glyph: "test1" + "test2"
            [Fatal] Glyph: "test1" contains 1 contours | "test2" contains 2 contours

        """
        return super(BaseFont, self).isCompatible(other, BaseFont)

    def _isCompatible(
        self, other: BaseFont, reporter: FontCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native font.

        This is the environment implementation of :meth:`BaseFont.isCompatible`.

        :param other: The other :class:`BaseFont` subclass instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.

        """
        font1 = self
        font2 = other

        # incompatible guidelines
        guidelines1 = set(font1.guidelines)
        guidelines2 = set(font2.guidelines)
        if len(guidelines1) != len(guidelines2):
            reporter.warning = True
            reporter.guidelineCountDifference = True
        if len(guidelines1.difference(guidelines2)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromFont2 = list(
                guidelines1.difference(guidelines2)
            )
        if len(guidelines2.difference(guidelines1)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingInFont1 = list(
                guidelines2.difference(guidelines1)
            )
        # incompatible layers
        layers1 = set(font1.layerOrder)
        layers2 = set(font2.layerOrder)
        if len(layers1) != len(layers2):
            reporter.warning = True
            reporter.layerCountDifference = True
        if len(layers1.difference(layers2)) != 0:
            reporter.warning = True
            reporter.layersMissingFromFont2 = list(layers1.difference(layers2))
        if len(layers2.difference(layers1)) != 0:
            reporter.warning = True
            reporter.layersMissingInFont1 = list(layers2.difference(layers1))
        # test layers
        for layerName in sorted(layers1.intersection(layers2)):
            layer1 = font1.getLayer(layerName)
            layer2 = font2.getLayer(layerName)
            layerCompatibility = layer1.isCompatible(layer2)[1]
            if layerCompatibility.fatal or layerCompatibility.warning:
                if layerCompatibility.fatal:
                    reporter.fatal = True
                if layerCompatibility.warning:
                    reporter.warning = True
                reporter.layers.append(layerCompatibility)

    # -------
    # mapping
    # -------

    def getReverseComponentMapping(self) -> ReverseComponentMappingType:
        """Get a reversed map of all component references in the font.

        This method creates a :class:`dict` mapping each component glyph
        name in the font to a :class:`tuple` containing the composite
        glyph names that include the comoponent.

        :return: A :class:`dict` of component glyph names mapped to
            tuples of composite glyph names.

        Example::

            >>> mapping = font.getReverseComponentMapping()
            >>> mapping
            {'A': ('Aacute', 'Aring'), 'acute': ('Aacute',),
            'ring': ('Aring',)  , ...}

        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self) -> ReverseComponentMappingType:
        """Get a reversed map of all component references in the font.

        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        return layer.getReverseComponentMapping()

    def getCharacterMapping(self) -> CharacterMappingType:
        """Get the font's character mapping.

        This method creates a :class:`dict` mapping Unicode values to
        tuples of glyph names. Each Unicode value corresponds to one or
        more glyphs, and the glyph names represent these glyphs in the
        mapping.

        .. note::

            One glyph can have multiple unicode values, and a unicode value can
            have multiple glyphs pointing to it.

        :return: A :class:`dict` mapping Unicode values to :class:`tuple` of
            glyph names.

        Example::

            >>> mapping = font.getCharacterMapping()
            >>> mapping
            {65: ('A', 'A.alt'), 66: ('B',),
            67: ('C', 'C.alt', 'C.swash') , ...}

        """
        return self._getCharacterMapping()

    def _getCharacterMapping(self) -> CharacterMappingType:
        """Get the native font's character mapping.

        This is the environment implementation of
        :meth:`BaseFont.getCharacterMapping`.

        :return: A :class:`dict` mapping Unicode values to :class:`tuple` of
            glyph names.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. note::

            Subclasses may override this method.

        """
        layer = self.defaultLayer
        return layer.getCharacterMapping()

    # ---------
    # Selection
    # ---------

    # layers

    selectedLayers: dynamicProperty = dynamicProperty(
        "base_selectedLayers",
        """Get or set the selected glyph layers in the default font layer.

        :param value: The :class:`list` of :class:`BaseLayer` instances
            to select.
        :return: A :class:`tuple` of currently selected :class:`BaseLayer`
            instances.

        Getting selected layer objects::

            >>> for layer in layer.selectedLayers:
            ...     layer.color = (1, 0, 0, 0.5)

        Setting selected layer objects::

            >>> layer.selectedLayers = someLayers

        """,
    )

    def _get_base_selectedLayers(self) -> Tuple[BaseLayer, ...]:
        selected = tuple(
            normalizers.normalizeLayer(layer) for layer in self._get_selectedLayers()
        )
        return selected

    def _get_selectedLayers(self) -> Tuple[BaseLayer, ...]:
        """Get the selected glyph layers in the native default font layer.

        This is the environment implementation of
        the :attr:`BaseFont.selectedLayers` property getter.

        :return: A :class:`tuple` of currently selected :class:`BaseLayer`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizeLayer`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.layers)

    def _set_base_selectedLayers(self, value: List[BaseLayer]) -> None:
        normalized = [normalizers.normalizeLayer(layer) for layer in value]
        self._set_selectedLayers(normalized)

    def _set_selectedLayers(self, value: List[BaseLayer]) -> None:
        """Set the selected glyph layers in the native default font layer.

        This is the environment implementation of
        the :attr:`BaseFont.selectedLayers` property setter.

        :param value: The :class:`list` of :class:`BaseLayer` instances
            to select. Each value item will have been normalized
            with :func:`normalizers.normalizeLayer`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.layers, value)

    selectedLayerNames: dynamicProperty = dynamicProperty(
        "base_selectedLayerNames",
        """Get or set the selected glyph layer names in the default font layer.

        :param value: The :class:`list` of layer names representing
            the :class:`BaseLayer` instances to select.
        :return: A :class:`tuple` of layer names representing the currently
            selected :class:`BaseLayer` instances.

        Getting selected layer names::

            >>> for name in layer.selectedLayerNames:
            ...     print(name)

        Setting selected layer names:

            >>> layer.selectedLayerNames = ["A", "B", "C"]

        """,
    )

    def _get_base_selectedLayerNames(self) -> Tuple[str, ...]:
        selected = tuple(
            normalizers.normalizeLayerName(name)
            for name in self._get_selectedLayerNames()
        )
        return selected

    def _get_selectedLayerNames(self) -> Tuple[str, ...]:
        """Get the selected glyph layer names in the native font layer.

        This is the environment implementation of
        the :attr:`BaseFont.selectedLayerNames` property getter.

        :return: A :class:`tuple` of layer names representing the currently
            selected :class:`BaseLayer` instances. Each value item will be
            normalized with :func:`normalizers.normalizeLayerName`.

        .. note::

            Subclasses may override this method.

        """
        return tuple(layer.name for layer in self.selectedLayers)

    def _set_base_selectedLayerNames(self, value: List[str]) -> None:
        normalized = [normalizers.normalizeLayerName(name) for name in value]
        self._set_selectedLayerNames(normalized)

    def _set_selectedLayerNames(self, value: List[str]) -> None:
        """Set the selected glyph layer names in the native font layer.

        This is the environment implementation of
        the :attr:`BaseFont.selectedLayerNames` property setter.

        :param value: The :class:`list` of layer names representing
            the :class:`BaseLayer` instances to select. Each value item will
            have been normalized with :func:`normalizers.normalizeLayerName`.

        .. note::

            Subclasses may override this method.

        """
        select = [self.layers(name) for name in value]
        self.selectedLayers = select

    # guidelines

    selectedGuidelines: dynamicProperty = dynamicProperty(
        "base_selectedGuidelines",
        """Get or set the selected guidelines in the font.

        :param value: The :class:`list` of either :class:`BaseGuideline` instances
            to select or their corresponding indexes.
        :return: A :class:`tuple` of currently selected :class:`BaseGuideline`
            instances.

        Getting selected guideline objects::

            >>> for guideline in font.selectedGuidelines:
            ...     guideline.color = (1, 0, 0, 0.5)

        Setting selected guideline objects::

            >>> font.selectedGuidelines = someGuidelines

        Setting also supports guideline indexes::

            >>> font.selectedGuidelines = [0, 2]

        """,
    )

    def _get_base_selectedGuidelines(self) -> Tuple[BaseGuideline, ...]:
        selected = tuple(
            normalizers.normalizeGuideline(guideline)
            for guideline in self._get_selectedGuidelines()
        )
        return selected

    def _get_selectedGuidelines(self) -> Tuple[BaseGuideline, ...]:
        """Get the selected guidelines in the native font.

        This is the environment implementation of
        the :attr:`BaseFont.selectedGuidelines` property getter.

        :return: A :class:`tuple` of currently selected :class:`BaseGuideline`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizeGuideline`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.guidelines)

    def _set_base_selectedGuidelines(
        self, value: List[Union[BaseGuideline, int]]
    ) -> None:
        normalized = []
        for guideline in value:
            normalizedGuideline: Union[BaseGuideline, int]
            if isinstance(guideline, int):
                normalizedIndex = normalizers.normalizeIndex(guideline)
                # Avoid mypy conflict with normalizeIndex -> Optional[int]
                if normalizedIndex is None:
                    continue
                normalizedGuideline = normalizedIndex
            else:
                normalizedGuideline = normalizers.normalizeGuideline(guideline)

            normalized.append(normalizedGuideline)
        self._set_selectedGuidelines(normalized)

    def _set_selectedGuidelines(self, value: List[Union[BaseGuideline, int]]) -> None:
        """Set the selected guidelines in the native font.

        This is the environment implementation of
        the :attr:`BaseFont.selectedGuidelines` property setter.

        :param value: The :class:`list` of :class:`BaseGuideline` instances to
            select. Each value item will have been normalized
            with :func:`normalizers.normalizeGuideline`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.guidelines, value)
