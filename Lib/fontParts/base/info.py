from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Union,
)

from fontTools.ufoLib import fontInfoAttributesVersion3
from fontTools.ufoLib import validateFontInfoVersion3ValueForAttribute
from fontMath import MathInfo
from fontMath.mathFunctions import setRoundIntegerFunction

from fontParts.base.base import BaseObject, dynamicProperty, interpolate, reference
from fontParts.base import normalizers
from fontParts.base.errors import FontPartsError
from fontParts.base.deprecated import DeprecatedInfo, RemovedInfo
from fontParts.base.annotations import (
    TransformationType,
)

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont


# Notes


class BaseInfo(BaseObject, DeprecatedInfo, RemovedInfo):
    """Represent the basis for an info object."""

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
