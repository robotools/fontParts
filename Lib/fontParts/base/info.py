from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from fontTools.ufoLib import fontInfoAttributesVersion3
from fontTools.ufoLib import validateFontInfoVersion3ValueForAttribute
from fontMath import MathInfo
from fontMath.mathFunctions import setRoundIntegerFunction

from fontParts.base.base import BaseObject, dynamicProperty, interpolate, reference
from fontParts.base import normalizers
from fontParts.base.errors import FontPartsError
from fontParts.base.deprecated import DeprecatedInfo, RemovedInfo
from fontParts.base.annotations import TransformationType

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont


class BaseInfo(BaseObject, DeprecatedInfo, RemovedInfo):
    """Represent the basis for a font info object."""

    familyName: str
    """Family name."""

    styleName: str
    """Style name."""

    styleMapFamilyName: str
    """Family name used for bold, italic and bold italic style mapping."""

    styleMapStyleName: str
    """Style map style.

    The possible values are *regular*, *italic*, *bold* and *bold italic*.
    These are case sensitive."""

    versionMajor: int
    """Major version."""

    versionMinor: int
    """Minor version."""

    year: int
    """The year the font was created.

    This attribute is deprecated as of version 2. It's presence should not
    be relied upon by applications. However, it may occur in a font's info
    so applications should preserve it if present."""

    copyright: str
    """Copyright statement."""

    trademark: str
    """Trademark statement."""

    unitsPerEm: Union[int, float]
    """Units per em."""

    descender: Union[int, float]
    """Descender value."""

    xHeight: Union[int, float]
    """x-height value."""

    capHeight: Union[int, float]
    """Cap height value."""

    ascender: Union[int, float]
    """Ascender value."""

    italicAngle: Union[int, float]
    """Italic angle."""

    note: str
    """Arbitrary note about the font."""

    openTypeHeadCreated: str
    """Creation date.

    Expressed as a string of the format "YYYY/MM/DD HH:MM:SS". "YYYY/MM/DD"
    is year/month/day. The month should be in the range 1-12 and the day
    should be in the range 1-end of month. "HH:MM:SS" is hour:minute:second.
    The hour should be in the range 0:23. The minute and second should each
    be in the range 0-59."""

    openTypeHeadLowestRecPPEM: Union[int, float]
    """Smallest readable size in pixels.

    Corresponds to the OpenType head table lowestRecPPEM field."""

    openTypeHeadFlags: list[int]
    """A list of bit numbers indicating the flags.

    The bit numbers are listed in the OpenType head specification.
    Corresponds to the OpenType head table flags field."""

    openTypeHheaAscender: Union[int, float]
    """Ascender value.

    Corresponds to the OpenType hhea table Ascender field."""

    openTypeHheaDescender: Union[int, float]
    """Descender value.

    Corresponds to the OpenType hhea table Descender field."""

    openTypeHheaLineGap: Union[int, float]
    """Line gap value.

    Corresponds to the OpenType hhea table LineGap field."""

    openTypeHheaCaretSlopeRise: int
    """Caret slope rise value.

    Corresponds to the OpenType hhea table caretSlopeRise field."""

    openTypeHheaCaretSlopeRun: int
    """Caret slope run value.

    Corresponds to the OpenType hhea table caretSlopeRun field."""

    openTypeHheaCaretOffset: Union[int, float]
    """Caret offset value.

    Corresponds to the OpenType hhea table caretOffset field."""

    openTypeNameDesigner: str
    """Designer name.

    Corresponds to the OpenType name table name ID 9."""

    openTypeNameDesignerURL: str
    """URL for the designer.

    Corresponds to the OpenType name table name ID 12."""

    openTypeNameManufacturer: str
    """Manufacturer name.

    Corresponds to the OpenType name table name ID 8."""

    openTypeNameManufacturerURL: str
    """Manufacturer URL.

    Corresponds to the OpenType name table name ID 11."""

    openTypeNameLicense: str
    """License text.

    Corresponds to the OpenType name table name ID 13."""

    openTypeNameLicenseURL: str
    """URL for the license.

    Corresponds to the OpenType name table name ID 14."""

    openTypeNameVersion: str
    """Version string.

    Corresponds to the OpenType name table name ID 5."""

    openTypeNameUniqueID: str
    """Unique ID string.

    Corresponds to the OpenType name table name ID 3."""

    openTypeNameDescription: str
    """Description of the font.

    Corresponds to the OpenType name table name ID 10."""

    openTypeNamePreferredFamilyName: str
    """Preferred family name.

    Corresponds to the OpenType name table name ID 16."""

    openTypeNamePreferredSubfamilyName: str
    """Preferred subfamily name.

    Corresponds to the OpenType name table name ID 17."""

    openTypeNameCompatibleFullName: str
    """Compatible full name.

    Corresponds to the OpenType name table name ID 18."""

    openTypeNameSampleText: str
    """Sample text.

    Corresponds to the OpenType name table name ID 20."""

    openTypeNameWWSFamilyName: str
    """WWS family name.

    Corresponds to the OpenType name table name ID 21."""

    openTypeNameWWSSubfamilyName: str
    """WWS Subfamily name.

    Corresponds to the OpenType name table name ID 22."""

    openTypeOS2WidthClass: int
    """Width class value.

    Must be in the range 1-9. Corresponds to the OpenType OS/2 table
    usWidthClass field."""

    openTypeOS2WeightClass: int
    """Weight class value.

    Must be a positive integer. Corresponds to the OpenType OS/2 table
    usWeightClass field."""

    openTypeOS2Selection: list[int]
    """A list of bit numbers indicating the bits that should be set in fsSelection.

    The bit numbers are listed in the OpenType OS/2 specification.
    Corresponds to the OpenType OS/2 table selection field. **Note:** Bits 0
    (italic), 5 (bold) and 6 (regular) should not be set here. These bits
    should be taken from the generic *styleMapStyleName* attribute."""

    openTypeOS2VendorID: str
    """Four character identifier for the creator of the font.

    Corresponds to the OpenType OS/2 table achVendID field."""

    openTypeOS2Panose: list[int]
    """The list should contain 10 integers that represent the setting for each category in the Panose specification.

    The integers correspond with the option numbers in each of the Panose
    categories. This corresponds to the OpenType OS/2 table Panose field."""

    openTypeOS2FamilyClass: list[int]
    """Two integers representing the IBM font class and font subclass of the font.

    The first number, representing the class ID, should be in the range
    0-14. The second number, representing the subclass, should be in the
    range 0-15. The numbers are listed in the OpenType OS/2 specification.
    Corresponds to the OpenType OS/2 table sFamilyClass field."""

    openTypeOS2UnicodeRanges: list[int]
    """A list of bit numbers that are supported Unicode ranges in the font.

    The bit numbers are listed in the OpenType OS/2 specification.
    Corresponds to the OpenType OS/2 table ulUnicodeRange1, ulUnicodeRange2,
    ulUnicodeRange3 and ulUnicodeRange4 fields."""

    openTypeOS2CodePageRanges: list[int]
    """A list of bit numbers that are supported code page ranges in the font.

    The bit numbers are listed in the OpenType OS/2 specification.
    Corresponds to the OpenType OS/2 table ulCodePageRange1 and
    ulCodePageRange2 fields."""

    openTypeOS2TypoAscender: Union[int, float]
    """Ascender value.

    Corresponds to the OpenType OS/2 table sTypoAscender field."""

    openTypeOS2TypoDescender: Union[int, float]
    """Descender value.

    Corresponds to the OpenType OS/2 table sTypoDescender field."""

    openTypeOS2TypoLineGap: Union[int, float]
    """Line gap value.

    Corresponds to the OpenType OS/2 table sTypoLineGap field."""

    openTypeOS2WinAscent: Union[int, float]
    """Ascender value.

    Corresponds to the OpenType OS/2 table usWinAscent field."""

    openTypeOS2WinDescent: Union[int, float]
    """Descender value.

    Corresponds to the OpenType OS/2 table usWinDescent field."""

    openTypeOS2Type: list[int]
    """A list of bit numbers indicating the embedding type.

    The bit numbers are listed in the OpenType OS/2 specification.
    Corresponds to the OpenType OS/2 table fsType field."""

    openTypeOS2SubscriptXSize: Union[int, float]
    """Subscript horizontal font size.

    Corresponds to the OpenType OS/2 table ySubscriptXSize field."""

    openTypeOS2SubscriptYSize: Union[int, float]
    """Subscript vertical font size.

    Corresponds to the OpenType OS/2 table ySubscriptYSize field."""

    openTypeOS2SubscriptXOffset: Union[int, float]
    """Subscript x offset.

    Corresponds to the OpenType OS/2 table ySubscriptXOffset field."""

    openTypeOS2SubscriptYOffset: Union[int, float]
    """Subscript y offset.

    Corresponds to the OpenType OS/2 table ySubscriptYOffset field."""

    openTypeOS2SuperscriptXSize: Union[int, float]
    """Superscript horizontal font size.

    Corresponds to the OpenType OS/2 table ySuperscriptXSize field."""

    openTypeOS2SuperscriptYSize: Union[int, float]
    """Superscript vertical font size.

    Corresponds to the OpenType OS/2 table ySuperscriptYSize field."""

    openTypeOS2SuperscriptXOffset: Union[int, float]
    """Superscript x offset.

    Corresponds to the OpenType OS/2 table ySuperscriptXOffset field."""

    openTypeOS2SuperscriptYOffset: Union[int, float]
    """Superscript y offset.

    Corresponds to the OpenType OS/2 table ySuperscriptYOffset field."""

    openTypeOS2StrikeoutSize: Union[int, float]
    """Strikeout size.

    Corresponds to the OpenType OS/2 table yStrikeoutSize field."""

    openTypeOS2StrikeoutPosition: Union[int, float]
    """Strikeout position.

    Corresponds to the OpenType OS/2 table yStrikeoutPosition field."""

    openTypeVheaVertTypoAscender: Union[int, float]
    """Ascender value.

    Corresponds to the OpenType vhea table vertTypoAscender field."""

    openTypeVheaVertTypoDescender: Union[int, float]
    """Descender value.

    Corresponds to the OpenType vhea table vertTypoDescender field."""

    openTypeVheaVertTypoLineGap: Union[int, float]
    """Line gap value.

    Corresponds to the OpenType vhea table vertTypoLineGap field."""

    openTypeVheaCaretSlopeRise: int
    """Caret slope rise value.

    Corresponds to the OpenType vhea table caretSlopeRise field."""

    openTypeVheaCaretSlopeRun: int
    """Caret slope run value.

    Corresponds to the OpenType vhea table caretSlopeRun field."""

    openTypeVheaCaretOffset: Union[int, float]
    """Caret offset value.

    Corresponds to the OpenType vhea table caretOffset field."""

    postscriptFontName: str
    """Name to be used for the *FontName* field in Type 1/CFF table."""

    postscriptFullName: str
    """Name to be used for the *FullName* field in Type 1/CFF table."""

    postscriptSlantAngle: Union[int, float]
    """Artificial slant angle."""

    postscriptUniqueID: int
    """A unique ID number as defined in the Type 1/CFF specification."""

    postscriptUnderlineThickness: Union[int, float]
    """Underline thickness value.

    Corresponds to the Type 1/CFF/post table UnderlineThickness field."""

    postscriptUnderlinePosition: Union[int, float]
    """Underline position value.

    Corresponds to the Type 1/CFF/post table UnderlinePosition field."""

    postscriptIsFixedPitch: bool
    """Indicates if the font is monospaced.

    A compiler could calculate this automatically, but the designer may wish
    to override this setting. This corresponds to the Type 1/CFF
    isFixedPitched field"""

    postscriptBlueValues: list[int]
    """A list of up to 14 integers or floats specifying the values that should be in the Type 1/CFF BlueValues field.

    This list must contain an even number of integers following the rules
    defined in the Type 1/CFF specification."""

    postscriptOtherBlues: list[int]
    """A list of up to 10 integers or floats specifying the values that should be in the Type 1/CFF OtherBlues field.

    This list must contain an even number of integers following the rules
    defined in the Type 1/CFF specification."""

    postscriptFamilyBlues: list[int]
    """A list of up to 14 integers or floats specifying the values that should be in the Type 1/CFF FamilyBlues field.

    This list must contain an even number of integers following the rules
    defined in the Type 1/CFF specification."""

    postscriptFamilyOtherBlues: list[int]
    """A list of up to 10 integers or floats specifying the values that should be in the Type 1/CFF FamilyOtherBlues field.

    This list must contain an even number of integers following the rules
    defined in the Type 1/CFF specification."""

    postscriptStemSnapH: list[int]
    """List of horizontal stems sorted in increasing order.

    Up to 12 integers or floats are possible. This corresponds to the Type
    1/CFF StemSnapH field."""

    postscriptStemSnapV: list[int]
    """List of vertical stems sorted in increasing order.

    Up to 12 integers or floats are possible. This corresponds to the Type
    1/CFF StemSnapV field."""

    postscriptBlueFuzz: Union[int, float]
    """BlueFuzz value.

    This corresponds to the Type 1/CFF BlueFuzz field."""

    postscriptBlueShift: Union[int, float]
    """BlueShift value.

    This corresponds to the Type 1/CFF BlueShift field."""

    postscriptBlueScale: Union[int, float]
    """BlueScale value.

    This corresponds to the Type 1/CFF BlueScale field."""

    postscriptForceBold: bool
    """Indicates how the Type 1/CFF ForceBold field should be set."""

    postscriptDefaultWidthX: Union[int, float]
    """Default width for glyphs."""

    postscriptNominalWidthX: Union[int, float]
    """Nominal width for glyphs."""

    postscriptWeightName: str
    """A string indicating the overall weight of the font.

    This corresponds to the Type 1/CFF Weight field. It should be in sync
    with the openTypeOS2WeightClass value."""

    postscriptDefaultCharacter: str
    """The name of the glyph that should be used as the default character in PFM files."""

    postscriptWindowsCharacterSet: int
    """The Windows character set.

    The values are defined below."""

    fontInfoAttributes = set(fontInfoAttributesVersion3)
    fontInfoAttributes.remove("guidelines")
    copyAttributes = tuple(fontInfoAttributes)

    def _reprContents(self) -> List[str]:
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Font

    _font: Optional[Callable[[], BaseFont]] = None

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get  or set the info's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the info
            or :obj:`None`.
        :raises AssertionError: If attempting to set the font when it
            has already been set.

        Example::

            >>> font = info.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(
        self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]
    ) -> None:
        if self._font is not None and self._font != font:
            raise AssertionError("font for info already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # ----------
    # Validation
    # ----------

    @staticmethod
    def _validateFontInfoAttributeValue(attr: str, value: Any):
        valid = validateFontInfoVersion3ValueForAttribute(attr, value)
        if not valid:
            raise ValueError(f"Invalid value {value} for attribute '{attr}'.")
        return value

    # ----------
    # Attributes
    # ----------

    # get

    def __getattribute__(self, attr: str) -> Any:
        """Get the value of the specified font info attribute.

        Attributes listed in :const:`fonttools.ufolib.fontInfoAttributesVersion3` are
        retrieved by calling a corresponding ``_get_<attr>`` method via
        :meth:`_getAttr`. The value is validated before being returned.

        :param attr: The name of the attribute to retrieve.
        :return: The value of the specified attribute.
        :raises ValueError: if the value of `attr` is invalid.

        """
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            value = self._getAttr(attr)
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return value
        return super(BaseInfo, self).__getattribute__(attr)

    def _getAttr(self, attr: str) -> Any:
        """Get the value of the specified native font info attribute.

        This is the environment implementation of :meth:`BaseInfo.__getattribute__`.

        :param attr: The name of the attribute to retrieve.
            The value will be validated by
            :func:`fonttools.ufolib.validateFontInfoVersion3ValueForAttribute`
        :return: The value of the specified attribute.
        :raises AttributeError: If no getter is defined for `attr`.
        :raises ValueError: if the value of `attr` is invalid.

        .. note::

            Subclasses may override this method.

            If a subclass does not override this method, it must implement
            ``_get_<attr>`` methods for all :class:`BaseInfo` methods.

        """
        methodName = f"_get_{attr}"
        try:
            method = object.__getattribute__(self, methodName)
        except AttributeError:
            raise AttributeError(f"No getter for attribute '{attr}'.")
        return method()

    # set

    def __setattr__(self, attr: str, value: Any) -> None:
        """Set the value of the specified font info attribute.

        Attributes listed in :const:`fonttools.ufolib.fontInfoAttributesVersion3` are
        set by validating the value and calling a corresponding ``_set_<attr>`` method
        via :meth:`_setAttr`.

        :param attr: The name of the attribute to set.
        :param value: The value to set for `attr`.
        :raises ValueError: if the value of `attr` is invalid.

        """
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return self._setAttr(attr, value)
        return super(BaseInfo, self).__setattr__(attr, value)

    def _setAttr(self, attr: str, value: Any) -> None:
        """Set the value of the specified native font info attribute.

        This is the environment implementation of :meth:`BaseInfo.__setattr__`.

        :param attr: The name of the attribute to set.
            The value will have been validated by
            :func:`fonttools.ufolib.validateFontInfoVersion3ValueForAttribute`
        :param value: The value to set for `attr`.
        :raises AttributeError: If no setter is defined for `attr`.
        :raises ValueError: if the value of `attr` is invalid.

        .. note::

            Subclasses may override this method.

            If a subclass does not override this method, it must implement
            ``_set_<attr>`` methods for all :class:`BaseInfo` methods.

        """
        methodName = f"_set_{attr}"
        if not hasattr(self, methodName):
            raise AttributeError(f"No setter for attribute '{attr}'.")
        method = getattr(self, methodName)
        method(value)

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """Round the following attributes to the nearest integer:

        - unitsPerEm
        - descender
        - xHeight
        - capHeight
        - ascender
        - openTypeHeadLowestRecPPEM
        - openTypeHheaAscender
        - openTypeHheaDescender
        - openTypeHheaLineGap
        - openTypeHheaCaretSlopeRise
        - openTypeHheaCaretSlopeRun
        - openTypeHheaCaretOffset
        - openTypeOS2WidthClass
        - openTypeOS2WeightClass
        - openTypeOS2TypoAscender
        - openTypeOS2TypoDescender
        - openTypeOS2TypoLineGap
        - openTypeOS2WinAscent
        - openTypeOS2WinDescent
        - openTypeOS2SubscriptXSize
        - openTypeOS2SubscriptYSize
        - openTypeOS2SubscriptXOffset
        - openTypeOS2SubscriptYOffset
        - openTypeOS2SuperscriptXSize
        - openTypeOS2SuperscriptYSize
        - openTypeOS2SuperscriptXOffset
        - openTypeOS2SuperscriptYOffset
        - openTypeOS2StrikeoutSize
        - openTypeOS2StrikeoutPosition
        - openTypeVheaVertTypoAscender
        - openTypeVheaVertTypoDescender
        - openTypeVheaVertTypoLineGap
        - openTypeVheaCaretSlopeRise
        - openTypeVheaCaretSlopeRun
        - openTypeVheaCaretOffset
        - postscriptSlantAngle
        - postscriptUnderlineThickness
        - postscriptUnderlinePosition
        - postscriptBlueValues
        - postscriptOtherBlues
        - postscriptFamilyBlues
        - postscriptFamilyOtherBlues
        - postscriptStemSnapH
        - postscriptStemSnapV
        - postscriptBlueFuzz
        - postscriptBlueShift
        - postscriptDefaultWidthX
        - postscriptNominalWidthX

        Example::

            >>> info.round()

        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        """Round selected native attributes to the nearest integer.

        This is the environment implementation of :meth:`BaseInfo.round`.

        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        setRoundIntegerFunction(normalizers.normalizeVisualRounding)

        mathInfo = self._toMathInfo(guidelines=False)
        mathInfo = mathInfo.round()
        self._fromMathInfo(mathInfo, guidelines=False)

    # --------
    # Updating
    # --------

    def update(self, other: BaseInfo) -> None:  # type: ignore[override]
        """Update the current info object with the values from another.

        :param other: A :class:`BaseInfo` to update this info object with.

        Example::

            >>> info.update(newInfo)

        """
        self._update(other)

    def _update(self, other: BaseInfo) -> None:
        """Update the current native info object with the values from another.

        This is the environment implementation of :meth:`BaseInfo.update`.

        :param other: A :class:`BaseInfo` to update this info object with.

        .. note::

            Subclasses may override this method.

        """

        for attr in fontInfoAttributesVersion3:
            if attr == "guidelines":
                continue
            value = getattr(other, attr)
            setattr(self, attr, value)

    # -------------
    # Interpolation
    # -------------

    def toMathInfo(self, guidelines=True) -> MathInfo:
        """Return this info as an object conforming to the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.

        :param guidelines: Whether to replace guidelines. Defaults to :obj:`True`.

        Example::

            >>> mg = font.info.toMathInfo()

        """
        return self._toMathInfo(guidelines=guidelines)

    def fromMathInfo(self, mathInfo, guidelines=True) -> None:
        """Replace the contents of this info object with that of `mathInfo`.

        :param mathInfo: An object conforming to the `MathInfo protocol
            <https://github.com/typesupply/fontMath>`_, containing the replacement
            values.
        :param guidelines: Whether to replace guidelines. Defaults to :obj:`True`.

        Example::

            >>> font.fromMathInfo(mg)

        """
        self._fromMathInfo(mathInfo, guidelines=guidelines)

    def _toMathInfo(self, guidelines=True) -> MathInfo:
        """Return this native info as an object conforming to the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.

        This is the environment implementation of :meth:`BaseInfo.toMathInfo`.

        :param guidelines: Whether to replace guidelines. Defaults to :obj:`True`.

        .. note::

            Subclasses may override this method.

        """

        # A little trickery is needed here because MathInfo
        # handles font level guidelines. Those are not in this
        # object so we temporarily fake them just enough for
        # MathInfo and then move them back to the proper place.
        self.guidelines = []
        if guidelines:
            for guideline in self.font.guidelines:
                d = dict(
                    x=guideline.x,
                    y=guideline.y,
                    angle=guideline.angle,
                    name=guideline.name,
                    identifier=guideline.identifier,
                    color=guideline.color,
                )
                self.guidelines.append(d)
        info = MathInfo(self)
        del self.guidelines
        return info

    def _fromMathInfo(self, mathInfo, guidelines=True) -> None:
        """Replace the contents of this native info object with that of `mathInfo`.

        This is the environment implementation of :meth:`BaseInfo.fromMathInfo`.

        :param mathInfo: An object conforming to the `MathInfo protocol
            <https://github.com/typesupply/fontMath>`_, containing the replacement
            values.
        :param guidelines: Whether to replace guidelines. Defaults to :obj:`True`.

        .. note::

            Subclasses may override this method.

        """
        mathInfo.extractInfo(self)
        font = self.font
        if guidelines:
            for guideline in mathInfo.guidelines:
                font.appendGuideline(
                    position=(guideline["x"], guideline["y"]),
                    angle=guideline["angle"],
                    name=guideline["name"],
                    color=guideline["color"],
                    # XXX identifier is lost
                )

    def interpolate(
        self,
        factor: TransformationType,
        minInfo: BaseInfo,
        maxInfo: BaseInfo,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """Interpolate all possible data in the current info object.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minInfo: The :class:`BaseInfo` instance corresponding to the
            0.0 position in the interpolation.
        :param maxInfo: The :class:`BaseInfo` instance corresponding to the
            1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minInfo` or `maxInfo` are not instances
            of :class:`BaseInfo`.

        Example::

            >>> info.interpolate(0.5, otherInfo1, otherInfo2)
            >>> info.interpolate((0.5, 2.0), otherInfo1, otherInfo2, round=False)

        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minInfo, BaseInfo):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not "
                f"be performed from an instance of {minInfo.__class__.__name__!r}."
            )
        if not isinstance(maxInfo, BaseInfo):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not "
                f"be performed from an instance of {maxInfo.__class__.__name__!r}."
            )
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(
            factor, minInfo, maxInfo, round=round, suppressError=suppressError
        )

    def _interpolate(
        self,
        factor: TransformationType,
        minInfo: BaseInfo,
        maxInfo: BaseInfo,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """ "Interpolate all possible data in the current native info object.

        This is the environment implementation of :meth:`BaseInfo.interpolate`.

        Subclasses may override this method.
        """

        setRoundIntegerFunction(normalizers.normalizeVisualRounding)

        minInfo = minInfo._toMathInfo()
        maxInfo = maxInfo._toMathInfo()
        result: Optional[MathInfo] = interpolate(minInfo, maxInfo, factor)
        if result is None:
            if not suppressError:
                raise FontPartsError(
                    f"Info from font '{minInfo.font.name}' and font '{maxInfo.font.name}' "
                    "could not be interpolated."
                )
            return

        if round:
            result = result.round()
        self._fromMathInfo(result)
