# pylint: disable=C0103, C0114
from __future__ import annotations
import os
import glob
from typing import (
    TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
)
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

SortOptionType = Union[str, Callable, CollectionType[Union[str, Callable]]]
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
    "BaseFontList"
]
RegistryType = Dict[str, Optional[Callable[[], BaseTypes]]]
InfoType = Union[str, int, float, bool]


def OpenFonts(
    directory: Optional[Union[str, CollectionType[str]]] = None,
        showInterface: bool = True,
        fileExtensions: Optional[CollectionType[str]] = None
) -> Generator[BaseFont]:
    """
    Open all fonts with the given **fileExtensions** located in
    **directory**. If **directory** is ``None``, a dialog for
    selecting a directory will be opened. **directory** may also
    be a list of directories. If **showInterface** is ``False``,
    the font should be opened without graphical interface. The default
    for **showInterface** is ``True``.

    The fonts are located within the directory using the `glob`
    <https://docs.python.org/library/glob.html>`_ module. The
    patterns are created with ``os.path.join(glob, "*" + fileExtension)``
    for every file extension in ``fileExtensions``. If ``fileExtensions``
    if ``None`` the environment will use its default fileExtensions.

    ::

        from fontParts.world import *

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
    """
    Open font located at **path**. If **showInterface**
    is ``False``, the font should be opened without
    graphical interface. The default for **showInterface**
    is ``True``.

    ::

        from fontParts.world import *

        font = OpenFont("/path/to/my/font.ufo")
        font = OpenFont("/path/to/my/font.ufo", showInterface=False)
    """
    return dispatcher["OpenFont"](pathOrObject=path, showInterface=showInterface)


def NewFont(
        familyName: Optional[str] = None,
        styleName: Optional[str] = None,
        showInterface: bool = True) -> BaseFont:
    """
    Create a new font. **familyName** will be assigned
    to ``font.info.familyName`` and **styleName**
    will be assigned to ``font.info.styleName``. These
    are optional and default to ``None``. If **showInterface**
    is ``False``, the font should be created without
    graphical interface. The default for **showInterface**
    is ``True``.

    ::

        from fontParts.world import *

        font = NewFont()
        font = NewFont(familyName="My Family", styleName="My Style")
        font = NewFont(showInterface=False)
    """
    return dispatcher["NewFont"](
        familyName=familyName, styleName=styleName, showInterface=showInterface
    )


def CurrentFont() -> BaseFont:
    """
    Get the "current" font.
    """
    return dispatcher["CurrentFont"]()


def CurrentGlyph() -> BaseGlyph:
    """
    Get the "current" glyph from :func:`CurrentFont`.

    ::

        from fontParts.world import *

        glyph = CurrentGlyph()
    """
    return dispatcher["CurrentGlyph"]()


def CurrentLayer() -> BaseLayer:
    """
    Get the "current" layer from :func:`CurrentGlyph`.

    ::

        from fontParts.world import *

        layer = CurrentLayer()
    """
    return dispatcher["CurrentLayer"]()


def CurrentContours() -> Tuple[BaseContour, ...]:
    """
    Get the "currently" selected contours from :func:`CurrentGlyph`.

    ::

        from fontParts.world import *

        contours = CurrentContours()

    This returns an immutable list, even when nothing is selected.
    """
    return dispatcher["CurrentContours"]()


def _defaultCurrentContours() -> Tuple[BaseContour, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    return glyph.selectedContours


def CurrentSegments() -> Tuple[BaseSegment, ...]:
    """
    Get the "currently" selected segments from :func:`CurrentContours`.

    ::

        from fontParts.world import *

        segments = CurrentSegments()

    This returns an immutable list, even when nothing is selected.
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
    """
    Get the "currently" selected points from :func:`CurrentContours`.

    ::

        from fontParts.world import *

        points = CurrentPoints()

    This returns an immutable list, even when nothing is selected.
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
    """
    Get the "currently" selected components from :func:`CurrentGlyph`.

    ::

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
    """
    Get the "currently" selected anchors from :func:`CurrentGlyph`.

    ::

        from fontParts.world import *

        anchors = CurrentAnchors()

    This returns an immutable list, even when nothing is selected.
    """
    return dispatcher["CurrentAnchors"]()


def _defaultCurrentAnchors() -> Tuple[BaseAnchor, ...]:
    glyph = CurrentGlyph()
    if glyph is None:
        return ()
    return glyph.selectedAnchors


def CurrentGuidelines() -> Tuple[BaseGuideline, ...]:
    """
    Get the "currently" selected guidelines from :func:`CurrentGlyph`.
    This will include both font level and glyph level guidelines.

    ::

        from fontParts.world import *

        guidelines = CurrentGuidelines()

    This returns an immutable list, even when nothing is selected.
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
    """
    Get a list of all open fonts. Optionally, provide a
    value for ``sortOptions`` to sort the fonts. See
    :meth:`world.FontList.sortBy` for options.

    ::

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
    """
    Get a list with font specific methods.

    ::

        from fontParts.world import *

        fonts = FontList()

    Refer to :class:`BaseFontList` for full documentation.
    """
    l = dispatcher["FontList"]()
    if fonts:
        l.extend(fonts)
    return l


class BaseFontList(list):
    # Sort

    def sortBy(self, sortOptions: SortOptionType, reverse: bool = False) -> None:
        """
        Sort ``fonts`` with the ordering preferences defined
        by ``sortBy``. ``sortBy`` must be one of the following:

        * sort description string
        * :class:`BaseInfo` attribute name
        * sort value function
        * list/tuple containing sort description strings, :class:`BaseInfo`
          attribute names and/or sort value functions
        * ``"magic"``

        Sort Description Strings
        ------------------------

        The sort description strings, and how they modify the sort, are:

        +----------------------+--------------------------------------+
        | ``"familyName"``     | Family names by alphabetical order.  |
        +----------------------+--------------------------------------+
        | ``"styleName"``      | Style names by alphabetical order.   |
        +----------------------+--------------------------------------+
        | ``"isItalic"``       | Italics before romans.               |
        +----------------------+--------------------------------------+
        | ``"isRoman"``        | Romans before italics.               |
        +----------------------+--------------------------------------+
        | ``"widthValue"``     | Width values by numerical order.     |
        +----------------------+--------------------------------------+
        | ``"weightValue"``    | Weight values by numerical order.    |
        +----------------------+--------------------------------------+
        | ``"monospace"``      | Monospaced before proportional.      |
        +----------------------+--------------------------------------+
        | ``"isProportional"`` | Proportional before monospaced.      |
        +----------------------+--------------------------------------+

        ::

            >>> fonts.sortBy(("familyName", "styleName"))


        Font Info Attribute Names
        -------------------------

        Any :class:`BaseFont` attribute name may be included as
        a sort option. For example, to sort by x-height value,
        you'd use the ``"xHeight"`` attribute name.

        ::

            >>> fonts.sortBy("xHeight")


        Sort Value Function
        -------------------

        A sort value function must be a function that accepts
        one argument, ``font``. This function must return
        a sortable value for the given font. For example:

        ::

            >>> def glyphCountSortValue(font):
            >>>   return len(font)
            >>>
            >>> fonts.sortBy(glyphCountSortValue)

        A list of sort description strings and/or sort functions
        may also be provided. This should be in order of most
        to least important. For example, to sort by family name
        and then style name, do this:


        "magic"
        -------

        If "magic" is given for ``sortBy``, the fonts will be
        sorted based on this sort description sequence:

        * ``"familyName"``
        * ``"isProportional"``
        * ``"widthValue"``
        * ``"weightValue"``
        * ``"styleName"``
        * ``"isRoman"``

        ::

            >>> fonts.sortBy("magic")
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
            raise ValueError("sortOptions must be a string, list or function.")
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
            self,
            *attributeValuePairs: Tuple[str, InfoType]
    ) -> BaseFontList:
        """
        Get a list of fonts that match the (attribute, value)
        combinations in ``attributeValuePairs``.

        ::

            >>> subFonts = fonts.getFontsByFontInfoAttribute(("xHeight", 20))
            >>> subFonts = fonts.getFontsByFontInfoAttribute(("xHeight", 20), ("descender", -150))

        This will return an instance of :class:`BaseFontList`.
        """
        found = self
        for attr, value in attributeValuePairs:
            found = self._matchFontInfoAttributes(found, (attr, value))
        return found

    def _matchFontInfoAttributes(
            self,
            fonts: BaseFontList,
            attributeValuePair: Tuple[str, InfoType]
    ) -> BaseFontList:
        found = self.__class__()
        attr, value = attributeValuePair
        for font in fonts:
            if getattr(font.info, attr) == value:
                found.append(font)
        return found

    def getFontsByFamilyName(self, familyName: str) -> BaseFontList:
        """
        Get a list of fonts that match ``familyName``.
        This will return an instance of :class:`BaseFontList`.
        """
        return self.getFontsByFontInfoAttribute(("familyName", familyName))

    def getFontsByStyleName(self, styleName: str) -> BaseFontList:
        """
        Get a list of fonts that match ``styleName``.
        This will return an instance of :class:`BaseFontList`.
        """
        return self.getFontsByFontInfoAttribute(("styleName", styleName))

    def getFontsByFamilyNameStyleName(
            self,
            familyName: str,
            styleName: str
    ) -> BaseFontList:
        """
        Get a list of fonts that match ``familyName`` and ``styleName``.
        This will return an instance of :class:`BaseFontList`.
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
        pathOrObject: Optional[Union[str, BaseFont]] = None,
            showInterface: bool = True) -> fontshell.RFont:
        return fontshell.RFont(pathOrObject=pathOrObject, showInterface=showInterface)

    dispatcher["OpenFont"] = _fontshellRFont
    dispatcher["RFont"] = _fontshellRFont

    # NewFont

    def _fontshellNewFont(
            familyName: Optional[str] = None,
            styleName: Optional[str] = None,
            showInterface: bool = True
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
