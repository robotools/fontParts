# pylint: disable=C0103, C0114
from __future__ import annotations
import os
import glob
from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
from collections.abc import Generator
from types import FunctionType

from fontParts.base.annotations import T, CollectionType

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.contour import BaseContour
    from fontParts.base.segment import BaseSegment
    from fontParts.base.point import BasePoint
    from fontParts.base.component import BaseComponent
    from fontParts.base.anchor import BaseAnchor
    from fontParts.base.guideline import BaseGuideline

SortOptionType = Union[str, FunctionType, CollectionType[Union[str, FunctionType]]]
BaseTypes = Union[
    "BaseFont",
    "BaseGlyph",
    "BaseLayer",
    "BaseContour",
    "BaseSegment",
    "BasePoint",
    "BaseComponent",
    "BaseAnchor",
    "BaseGuideline",
    "BaseFontList",
]
RegistryType = Dict[str, Optional[Callable[[], BaseTypes]]]
InfoType = Union[str, int, float, bool]


def OpenFonts(
    directory: Optional[Union[str, CollectionType[str]]] = None,
    showInterface: bool = True,
    fileExtensions: Optional[CollectionType[str]] = None,
) -> Generator[BaseFont]:
    """Open all fonts located in the specified directories.

    The fonts are located within the directory using the :mod:`glob` module.
    The patterns are created with ``os.path.join(directory, "*" + fileExtension)``
    for every file extension in `fileExtensions`.

    :param directory: The optional directory :class:`str` or the :class:`list`
        or :class:`tuple`  of directories to search for fonts. If :obj:`None` (default),
        a dialog for selecting a directory will be opened.
    :param showInterface: A :class:`bool` indicating whether to show the graphical
        interface. If :obj:`False`, the font should be opened without a graphical
        interface. Defaults to :obj:`True`.
    :param fileExtensions: The optional file extensions to search for as a :class:`list`
        or :class:`tuple` of :class:`str` items. If :obj:`None` (default), the default
        file extensions will be used.
    :return: A :class:`generator` yielding the opened fonts.

    Example::

        from fontParts.world import OpenFonts

        fonts = OpenFonts()
        fonts = OpenFonts(showInterface=False)

    """
    from fontParts.ui import GetFileOrFolder

    directories: CollectionType[str]
    if fileExtensions is None:
        fileExtensions = dispatcher["OpenFontsFileExtensions"]()
    if directory is None:
        directory = GetFileOrFolder(allowsMultipleSelection=True)
    elif isinstance(directory, str):
        directories = [directory]
    else:
        directories = directory
    if directories:
        globPatterns = []
        for directory in directories:
            if not fileExtensions:
                continue
            if os.path.splitext(directory)[-1] in fileExtensions:
                globPatterns.append(directory)
            elif not os.path.isdir(directory):
                pass
            else:
                for ext in fileExtensions:
                    globPatterns.append(os.path.join(directory, "*" + ext))
        paths = []
        for pattern in globPatterns:
            paths.extend(glob.glob(pattern))
        for path in paths:
            yield OpenFont(path, showInterface=showInterface)


def OpenFont(path: str, showInterface: bool = True) -> BaseFont:
    """Open font located at the specified path.

    :param path: The path to the font file to be opened as a :class:`str`
    :param showInterface: A :class:`bool` indicating whether to show the graphical
        interface. If :obj:`False`, the font should be opened without a graphical
        interface. Defaults to :obj:`True`.
    :return: The newly opened :class:`BaseFont` instance.

    Example::

        from fontParts.world import OpenFont

        font = OpenFont("/path/to/my/font.ufo")
        font = OpenFont("/path/to/my/font.ufo", showInterface=False)

    """
    return dispatcher["OpenFont"](pathOrObject=path, showInterface=showInterface)


def NewFont(
    familyName: Optional[str] = None,
    styleName: Optional[str] = None,
    showInterface: bool = True,
) -> BaseFont:
    """Create a new font.

    :param familyName: The optional :attr:`BaseInfo.familyName` to apply to the font as
        a :class:`str`.
    :param styleName: The optional :attr:`BaseInfo.styleName` to apply to the font as
        a :class:`str`.
    :param showInterface: A :class:`bool` indicating whether to show the graphical
        interface. If :obj:`False`, the font should be opened without a graphical
        interface. Defaults to :obj:`True`.
    :return: The newly created :class:`BaseFont` instance.

    Example::

        from fontParts.world import *

        font = NewFont()
        font = NewFont(familyName="My Family", styleName="My Style")
        font = NewFont(showInterface=False)

    """
    return dispatcher["NewFont"](
        familyName=familyName, styleName=styleName, showInterface=showInterface
    )


def CurrentFont() -> BaseFont:
    """Get the currently active font.

    :return: A :class:`BaseFont` subclass instance representing the currently active
        font.

    """
    return dispatcher["CurrentFont"]()


def CurrentGlyph() -> BaseGlyph:
    """Get the currently active glyph from :func:`CurrentFont`.

    :return: A :class:`BaseGlyph` subclass instance representing the currently active
        glyph.

    Example::

        from fontParts.world import *

        glyph = CurrentGlyph()
    """
    return dispatcher["CurrentGlyph"]()


def CurrentLayer() -> BaseLayer:
    """Get the currently active layer from :func:`CurrentGlyph`.

    :return: A :class:`BaseLayer` subclass instance representing the currently active
        glyph layer.

    Example::

        from fontParts.world import *

        layer = CurrentLayer()

    """
    return dispatcher["CurrentLayer"]()


def CurrentContours() -> Tuple[BaseContour, ...]:
    """Get the currently selected contours from :func:`CurrentGlyph`.

    :return: A :class:`tuple` of :class:`BaseContour` subclass instances representing
        the currently selected glyph contours.

    Example::

        from fontParts.world import *

        contours = CurrentContours()

    """
    return dispatcher["CurrentContours"]()


def _defaultCurrentContours() -> Tuple[BaseContour, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    return glyph.selectedContours


def CurrentSegments() -> Tuple[BaseSegment, ...]:
    """Get the currently selected segments from :func:`CurrentContours`.

    :return: A :class:`tuple` of :class:`BaseSegments` subclass instances representing
        the currently selected contour segments.

    Example::

        from fontParts.world import *

        segments = CurrentSegments()

    """
    return dispatcher["CurrentSegments"]()


def _defaultCurrentSegments() -> Tuple[BaseSegment, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    segments = []
    for contour in glyph.selectedContours:
        segments.extend(contour.selectedSegments)
    return tuple(segments)


def CurrentPoints() -> Tuple[BasePoint, ...]:
    """Get the currently selected points from :func:`CurrentContours`.

    :return: A :class:`tuple` of :class:`BasePoint` subclass instances representing
        the currently selected contour points.

    Example::

        from fontParts.world import *

        points = CurrentPoints()

    """
    return dispatcher["CurrentPoints"]()


def _defaultCurrentPoints() -> Tuple[BasePoint, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    points = []
    for contour in glyph.selectedContours:
        points.extend(contour.selectedPoints)
    return tuple(points)


def CurrentComponents() -> Tuple[BaseComponent, ...]:
    """Get the currently selected components from :func:`CurrentGlyph`.

    :return: A :class:`tuple` of :class:`BaseComponent` subclass instances representing
        the currently selected glyph components.

    Example::

        from fontParts.world import *

        components = CurrentComponents()

    This returns an immutable list, even when nothing is selected.
    """
    return dispatcher["CurrentComponents"]()


def _defaultCurrentComponents() -> Tuple[BaseComponent, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    return glyph.selectedComponents


def CurrentAnchors() -> Tuple[BaseAnchor, ...]:
    """Get the currently selected anchors from :func:`CurrentGlyph`.

    :return: A :class:`tuple` of :class:`BaseAnchor` subclass instances representing
        the currently selected glyph anchors.

    Example::

        from fontParts.world import *

        anchors = CurrentAnchors()

    """
    return dispatcher["CurrentAnchors"]()


def _defaultCurrentAnchors() -> Tuple[BaseAnchor, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    return glyph.selectedAnchors


def CurrentGuidelines() -> Tuple[BaseGuideline, ...]:
    """Get the currently selected guidelines from :func:`CurrentGlyph`.

    This will include both font level and glyph level guidelines.

    :return: A :class:`tuple` of :class:`BaseGuideline` subclass instances representing
        the currently selected guidelines.

    Example::

        from fontParts.world import *

        guidelines = CurrentGuidelines()

    """
    return dispatcher["CurrentGuidelines"]()


def _defaultCurrentGuidelines() -> Tuple[BaseGuideline, ...]:
    guidelines = []
    font = CurrentFont()
    if font is not None:
        guidelines.extend(font.selectedGuidelines)
    glyph = CurrentGlyph()
    if glyph is not None:
        guidelines.extend(glyph.selectedGuidelines)
    return tuple(guidelines)


def AllFonts(sortOptions: Optional[CollectionType[str]] = None) -> BaseFontList:
    """Get a list of all open fonts.

    Optionally, provide a value for `sortOptions` to sort the fonts. See
    :meth:`BaseFontList.sortBy` for options.

    :param sortOptions: The optional :class:`list` or :class:`tuple` of :class:`str`
        sort options to apply to the list. Defaults to :obj:`None`.
    :return: A :class:`BaseFontList` instance representing all open fonts.

    Example::

        from fontParts.world import *

        fonts = AllFonts()
        for font in fonts:
            # do something

        fonts = AllFonts("magic")
        for font in fonts:
            # do something

        fonts = AllFonts(["familyName", "styleName"])
        for font in fonts:
            # do something

    """
    fontList = FontList(dispatcher["AllFonts"]())
    if sortOptions is not None:
        fontList.sortBy(sortOptions)
    return fontList


def RFont(path: Optional[str] = None, showInterface: bool = True) -> fontshell.RFont:
    return dispatcher["RFont"](pathOrObject=path, showInterface=showInterface)


def RGlyph() -> fontshell.RGlyph:
    return dispatcher["RGlyph"]()


# ---------
# Font List
# ---------


def FontList(fonts: Optional[Iterable[T]] = None):
    """Get a list with font-specific methods.

    :return: A :class:`BaseFontList` instance.

    Example::

        from fontParts.world import *

        fonts = FontList()

    Refer to :class:`BaseFontList` for full documentation.
    """
    list = dispatcher["FontList"]()
    if fonts:
        list.extend(fonts)
    return list


class BaseFontList(list):
    """Represent a :class:`list` with font-specific methods."""

    # Sort

    def sortBy(self, sortOptions: SortOptionType, reverse: bool = False) -> None:
        """Sort items according to specified options.

        Sorting options may be defined as follows:

        - A :ref:`sort description <sort-descriptions>` as a :class:`str`
        - A :ref:`font info attribute name` <info-attributes` as a :class:`str`
        - A custom `sort value function <sort-value-function>`
        - A :class:`list` or :class:`tuple` containing a mix of any of the above
        - The special keyword ``"magic"`` (see :ref:`magic-sorting`)


        .. _sort-descriptions:

        Sort Descriptions
        -----------------

        The following string-based sort descriptions determine sorting behavior:

        +----------------------+--------------------------------------+
        | Sort Description     | Effect                               |
        +======================+======================================+
        | ``"familyName"``     | Sort by family name (A-Z).           |
        +----------------------+--------------------------------------+
        | ``"styleName"``      | Sort by style name (A-Z).            |
        +----------------------+--------------------------------------+
        | ``"isItalic"``       | Sort italics before romans.          |
        +----------------------+--------------------------------------+
        | ``"isRoman"``        | Sort romans before italics.          |
        +----------------------+--------------------------------------+
        | ``"widthValue"``     | Sort by width value (low-high).      |
        +----------------------+--------------------------------------+
        | ``"weightValue"``    | Sort by weight value (low-high).     |
        +----------------------+--------------------------------------+
        | ``"monospace"``      | Sort monospaced before proportional. |
        +----------------------+--------------------------------------+
        | ``"isProportional"`` | Sort proportional before monospaced. |
        +----------------------+--------------------------------------+


        .. _info-attributes:

        Font Info Attribute Names
        -------------------------

        Any attribute of :class:`BaseInfo` may be used as a sorting criterion.
        For example, sorting by x-height value can be achieved using the
        attribute name ``"xHeight"``.


        .. _sort-value-function:

        Sort Value Function
        -------------------

        A sort value function is a :class:`Callable` that takes a single
        argument, `font`, and returns a sortable value. Example::

            def glyph_count_sort(font):
                return len(font)


            fonts.sortBy(glyph_count_sort)

        A :class:`list` or :class:`tuple` of sort descriptions and/or sort functions
        may be provided to specify sorting precedence, from most to least important.


        .. _magic-sorting:

        Magic Sorting
        -------------

        If ``"magic"`` is specified, fonts are sorted using the following
        sequence of criteria:

        #. ``"familyName"``
        #. ``"isProportional"``
        #. ``"widthValue"``
        #. ``"weightValue"``
        #. ``"styleName"``
        #. ``"isRoman"``


        :param sortOptions: The sorting option(s), given as a single :class:`str`,
            :class:`FunctionType`, or a :class:`list` or :class:`tuple` of several.
        :param reverse: Whether to reverse the sort order. Defaults to :obj:`False`.
        :raises TypeError: If `sortOptions` is not a :class:`str`,
            :class:`FunctionType`, :class:`list` or :class:`tuple`.
        :raises ValueError:
            - If `sortOptions` does not conatain any sorting options.
            - If `sortOptions` contains an unrecognized value or value item.

        Example::

            from fontParts.world import AllFonts

            fonts = AllFonts()
            fonts.sortBy("familyName")
            fonts.sortBy(["familyName", "styleName"])
            fonts.sortBy("magic")
            fonts.sortBy(lambda font: len(font))

        """
        valueGetters = dict(
            familyName=_sortValue_familyName,
            styleName=_sortValue_styleName,
            isRoman=_sortValue_isRoman,
            isItalic=_sortValue_isItalic,
            widthValue=_sortValue_widthValue,
            weightValue=_sortValue_weightValue,
            isProportional=_sortValue_isProportional,
            isMonospace=_sortValue_isMonospace,
        )
        if isinstance(sortOptions, str) or isinstance(sortOptions, FunctionType):
            sortOptions = [sortOptions]
        if not isinstance(sortOptions, (list, tuple)):
            raise TypeError("sortOptions must be a string, list or function.")
        if not sortOptions:
            raise ValueError("At least one sort option must be defined.")
        if sortOptions == ["magic"]:
            sortOptions = [
                "familyName",
                "isProportional",
                "widthValue",
                "weightValue",
                "styleName",
                "isRoman",
            ]
        sorter = []
        for originalIndex, font in enumerate(self):
            sortable = []
            for valueName in sortOptions:
                value = None
                if isinstance(valueName, FunctionType):
                    value = valueName(font)
                elif isinstance(valueName, str):
                    if valueName in valueGetters:
                        value = valueGetters[valueName](font)
                    elif hasattr(font.info, valueName):
                        value = getattr(font.info, valueName)
                else:
                    raise ValueError(f"Unknown sort option: {repr(valueName)}")
                sortable.append(value)
            sortable.append(originalIndex)
            sortable.append(font)
            sorter.append(tuple(sortable))
        sorter.sort()
        fonts = [i[-1] for i in sorter]
        del self[:]
        self.extend(fonts)
        if reverse:
            self.reverse()

    # Search

    def getFontsByFontInfoAttribute(
        self, *attributeValuePairs: Tuple[str, InfoType]
    ) -> BaseFontList:
        r"""Get a list of fonts that match the specified attribute-value pairs.

        This method filters fonts based on one or more ``(attribute, value)`` pairs.
        When multiple pairs are provided, only fonts that satisfy all conditions are
        included.

        :param \*attributeValuePairs: The attribute-value pairs to search
            for as :class:`tuple` instances, each containing a font attribute name
            as a :class:`str` and the expected value.
        :return: A :class:`BaseFontList` instance containing the matching fonts.

        Example::

            >>> subFonts = fonts.getFontsByFontInfoAttribute(("xHeight", 20))
            >>> subFonts = fonts.getFontsByFontInfoAttribute(("xHeight", 20), ("descender", -150))

        """
        found = self
        for attr, value in attributeValuePairs:
            found = self._matchFontInfoAttributes(found, (attr, value))
        return found

    def _matchFontInfoAttributes(
        self, fonts: BaseFontList, attributeValuePair: Tuple[str, InfoType]
    ) -> BaseFontList:
        found = self.__class__()
        attr, value = attributeValuePair
        for font in fonts:
            if getattr(font.info, attr) == value:
                found.append(font)
        return found

    def getFontsByFamilyName(self, familyName: str) -> BaseFontList:
        """Get a list of fonts that match the provided family name.

        :param familyName: The :attr:`BaseInfo.familyName` to search for as
            a :class:`str`.
        :return: A :class:`BaseFontList` instance containing the matching fonts.

        """
        return self.getFontsByFontInfoAttribute(("familyName", familyName))

    def getFontsByStyleName(self, styleName: str) -> BaseFontList:
        """Get a list of fonts that match the provided style name.

        :param styleName: The :attr:`BaseInfo.styleName` to search for as
            a :class:`str`.
        :return: A :class:`BaseFontList` instance containing the matching fonts.

        """
        return self.getFontsByFontInfoAttribute(("styleName", styleName))

    def getFontsByFamilyNameStyleName(
        self, familyName: str, styleName: str
    ) -> BaseFontList:
        """Get a list of fonts that match the provided family name and style name.

        :param familyName: The :attr:`BaseInfo.familyName` to search for as
            a :class:`str`.
        :param styleName: The :attr:`BaseInfo.styleName` to search for as
            a :class:`str`.
        :return: A :class:`BaseFontList` instance containing the matching fonts.

        """
        return self.getFontsByFontInfoAttribute(
            ("familyName", familyName), ("styleName", styleName)
        )


def _sortValue_familyName(font: BaseFont) -> str:
    """
    Returns font.info.familyName.
    """
    value = font.info.familyName
    if value is None:
        value = ""
    return value


def _sortValue_styleName(font: BaseFont) -> str:
    """
    Returns font.info.styleName.
    """
    value = font.info.styleName
    if value is None:
        value = ""
    return value


def _sortValue_isRoman(font: BaseFont) -> int:
    """
    Returns 0 if the font is roman.
    Returns 1 if the font is not roman.
    """
    italic = _sortValue_isItalic(font)
    if italic == 1:
        return 0
    return 1


def _sortValue_isItalic(font: BaseFont) -> int:
    """
    Returns 0 if the font is italic.
    Returns 1 if the font is not italic.
    """
    info = font.info
    styleMapStyleName = info.styleMapStyleName
    if styleMapStyleName is not None and "italic" in styleMapStyleName:
        return 0
    if info.italicAngle not in (None, 0):
        return 0
    return 1


def _sortValue_widthValue(font: BaseFont) -> int:
    """
    Returns font.info.openTypeOS2WidthClass.
    """
    value = font.info.openTypeOS2WidthClass
    if value is None:
        value = -1
    return value


def _sortValue_weightValue(font: BaseFont) -> int:
    """
    Returns font.info.openTypeOS2WeightClass.
    """
    value = font.info.openTypeOS2WeightClass
    if value is None:
        value = -1
    return value


def _sortValue_isProportional(font: BaseFont) -> int:
    """
    Returns 0 if the font is proportional.
    Returns 1 if the font is not proportional.
    """
    monospace = _sortValue_isMonospace(font)
    if monospace == 1:
        return 0
    return 1


def _sortValue_isMonospace(font: BaseFont) -> int:
    """
    Returns 0 if the font is monospace.
    Returns 1 if the font is not monospace.
    """
    if font.info.postscriptIsFixedPitch:
        return 0
    if not len(font):
        return 1
    testWidth = None
    for glyph in font:
        if testWidth is None:
            testWidth = glyph.width
        else:
            if testWidth != glyph.width:
                return 1
    return 0


# ----------
# Dispatcher
# ----------


class _EnvironmentDispatcher:
    def __init__(self, registryItems: CollectionType[str]) -> None:
        self._registry: RegistryType = {item: None for item in registryItems}

    def __setitem__(self, name: str, func: Optional[Callable]) -> None:
        self._registry[name] = func

    def __getitem__(self, name: str) -> Callable:
        func = self._registry[name]
        if func is None:
            raise NotImplementedError
        return func


dispatcher = _EnvironmentDispatcher(
    [
        "OpenFontsFileExtensions",
        "OpenFont",
        "NewFont",
        "AllFonts",
        "CurrentFont",
        "CurrentGlyph",
        "CurrentLayer",
        "CurrentContours",
        "CurrentSegments",
        "CurrentPoints",
        "CurrentComponents",
        "CurrentAnchors",
        "CurrentGuidelines",
        "FontList",
        "RFont",
        "RLayer",
        "RGlyph",
        "RContour",
        "RPoint",
        "RAnchor",
        "RComponent",
        "RGuideline",
        "RImage",
        "RInfo",
        "RFeatures",
        "RGroups",
        "RKerning",
        "RLib",
    ]
)

# Register the default functions.

dispatcher["CurrentContours"] = _defaultCurrentContours
dispatcher["CurrentSegments"] = _defaultCurrentSegments
dispatcher["CurrentPoints"] = _defaultCurrentPoints
dispatcher["CurrentComponents"] = _defaultCurrentComponents
dispatcher["CurrentAnchors"] = _defaultCurrentAnchors
dispatcher["CurrentGuidelines"] = _defaultCurrentGuidelines
dispatcher["FontList"] = BaseFontList

# -------
# fontshell
# -------

try:
    from fontParts import fontshell

    # OpenFonts

    dispatcher["OpenFontsFileExtensions"] = lambda: [".ufo"]

    # OpenFont, RFont

    def _fontshellRFont(
        pathOrObject: Optional[Union[str, BaseFont]] = None, showInterface: bool = True
    ) -> fontshell.RFont:
        return fontshell.RFont(pathOrObject=pathOrObject, showInterface=showInterface)

    dispatcher["OpenFont"] = _fontshellRFont
    dispatcher["RFont"] = _fontshellRFont

    # NewFont

    def _fontshellNewFont(
        familyName: Optional[str] = None,
        styleName: Optional[str] = None,
        showInterface: bool = True,
    ) -> fontshell.RFont:
        font = fontshell.RFont(showInterface=showInterface)
        if familyName is not None:
            font.info.familyName = familyName
        if styleName is not None:
            font.info.styleName = styleName
        return font

    dispatcher["NewFont"] = _fontshellNewFont

    # RLayer, RGlyph, RContour, RPoint, RAnchor, RComponent, RGuideline, RImage, RInfo, RFeatures, RGroups, RKerning, RLib

    dispatcher["RLayer"] = fontshell.RLayer
    dispatcher["RGlyph"] = fontshell.RGlyph
    dispatcher["RContour"] = fontshell.RContour
    dispatcher["RPoint"] = fontshell.RPoint
    dispatcher["RAnchor"] = fontshell.RAnchor
    dispatcher["RComponent"] = fontshell.RComponent
    dispatcher["RGuideline"] = fontshell.RGuideline
    dispatcher["RImage"] = fontshell.RImage
    dispatcher["RInfo"] = fontshell.RInfo
    dispatcher["RFeatures"] = fontshell.RFeatures
    dispatcher["RGroups"] = fontshell.RGroups
    dispatcher["RKerning"] = fontshell.RKerning
    dispatcher["RLib"] = fontshell.RLib

except ImportError:
    pass
