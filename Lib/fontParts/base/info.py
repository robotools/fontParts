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
    """Represent the basis for an info object."""

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

    # has

    def __hasattr__(self, attr: str) -> bool:
        if attr in fontInfoAttributesVersion3:
            return True
        return super(BaseInfo, self).__hasattr__(attr)

    # get

    def __getattribute__(self, attr: str) -> None:
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            value = self._getAttr(attr)
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return value
        return super(BaseInfo, self).__getattribute__(attr)

    def _getAttr(self, attr: str) -> None:
        """
        Subclasses may override this method.

        If a subclass does not override this method,
        it must implement '_get_attributeName' methods
        for all Info methods.
        """
        methodName = f"_get_{attr}"
        if not hasattr(self, methodName):
            raise AttributeError(f"No getter for attribute '{attr}'.")
        method = getattr(self, methodName)
        value = method()
        return value

    # set

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return self._setAttr(attr, value)
        return super(BaseInfo, self).__setattr__(attr, value)

    def _setAttr(self, attr: str, value: Any) -> None:
        """
        Subclasses may override this method.

        If a subclass does not override this method,
        it must implement '_set_attributeName' methods
        for all Info methods.
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
        """
        Round the following attributes to integers:

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
        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        setRoundIntegerFunction(normalizers.normalizeVisualRounding)

        mathInfo = self._toMathInfo(guidelines=False)
        mathInfo = mathInfo.round()
        self._fromMathInfo(mathInfo, guidelines=False)

    # --------
    # Updating
    # --------

    def update(self, other: BaseInfo) -> None:
        """
        Update this object with the values
        from **otherInfo**.
        """
        self._update(other)

    def _update(self, other: BaseInfo) -> None:
        """
        Subclasses may override this method.
        """
        from fontTools.ufoLib import fontInfoAttributesVersion3

        for attr in fontInfoAttributesVersion3:
            if attr == "guidelines":
                continue
            value = getattr(other, attr)
            setattr(self, attr, value)

    # -------------
    # Interpolation
    # -------------

    def toMathInfo(self, guidelines=True) -> MathInfo:
        """
        Returns the info as an object that follows the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.

            >>> mg = font.info.toMathInfo()
        """
        return self._toMathInfo(guidelines=guidelines)

    def fromMathInfo(self, mathInfo, guidelines=True) -> BaseInfo:
        """
        Replaces the contents of this info object with the contents of ``mathInfo``.

            >>> font.fromMathInfo(mg)

        ``mathInfo`` must be an object following the
        `MathInfo protocol <https://github.com/typesupply/fontMath>`_.
        """
        return self._fromMathInfo(mathInfo, guidelines=guidelines)

    def _toMathInfo(self, guidelines=True) -> MathInfo:
        """
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
        """
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
        """
        Interpolate all pairs between minInfo and maxInfo.
        The interpolation occurs on a 0 to 1.0 range where minInfo
        is located at 0 and maxInfo is located at 1.0.

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
        if not isinstance(minInfo, BaseInfo):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {minInfo.__class__.__name__!r}."
            )
        if not isinstance(maxInfo, BaseInfo):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {maxInfo.__class__.__name__!r}."
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
        """
        Subclasses may override this method.
        """

        setRoundIntegerFunction(normalizers.normalizeVisualRounding)

        minInfo = minInfo._toMathInfo()
        maxInfo = maxInfo._toMathInfo()
        result = interpolate(minInfo, maxInfo, factor)
        if result is None and not suppressError:
            raise FontPartsError(
                f"Info from font '{minInfo.font.name}' and font '{maxInfo.font.name}' could not be interpolated."
            )
        if round:
            result = result.round()  # type: ignore[func-returns-value]
        self._fromMathInfo(result)
