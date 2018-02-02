import fontMath
from ufoLib import fontInfoAttributesVersion3, validateFontInfoVersion3ValueForAttribute
from fontParts.base.errors import FontPartsError
from fontParts.base.base import BaseObject, dynamicProperty, interpolate, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedInfo, RemovedInfo



class BaseInfo(BaseObject, DeprecatedInfo, RemovedInfo):

    copyAttributes = set(fontInfoAttributesVersion3)
    copyAttributes.remove("guidelines")
    copyAttributes = tuple(copyAttributes)

    def _reprContents(self):
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

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

    font = dynamicProperty("font", "The info's parent font.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None or self._font() == font
        if font is not None:
            font = reference(font)
        self._font = font

    # ----------
    # Validation
    # ----------

    def _validateFontInfoAttributeValue(self, attr, value):
        valid = validateFontInfoVersion3ValueForAttribute(attr, value)
        if not valid:
            raise FontPartsError("Invalid value %s for attribute '%s'." % (value, attr))
        return value

    # ----------
    # Attributes
    # ----------

    # has

    def __hasattr__(self, attr):
        if attr in fontInfoAttributesVersion3:
            return True
        return super(BaseInfo, self).__hasattr__(attr)

    # get

    def __getattribute__(self, attr):
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            value = self._getAttr(attr)
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return value
        return super(BaseInfo, self).__getattribute__(attr)

    def _getAttr(self, attr):
        """
        Subclasses may override this method.

        If a subclass does not override this method,
        it must implement '_get_attributeName' methods
        for all Info methods.
        """
        meth = "_get_%s" % attr
        if not hasattr(self, meth):
            raise AttributeError("No getter for attribute '%s'." % attr)
        meth = getattr(self, meth)
        value = meth()
        return value

    # set

    def __setattr__(self, attr, value):
        if attr != "guidelines" and attr in fontInfoAttributesVersion3:
            if value is not None:
                value = self._validateFontInfoAttributeValue(attr, value)
            return self._setAttr(attr, value)
        return super(BaseInfo, self).__setattr__(attr, value)

    def _setAttr(self, attr, value):
        """
        Subclasses may override this method.

        If a subclass does not override this method,
        it must implement '_set_attributeName' methods
        for all Info methods.
        """
        meth = "_set_%s" % attr
        if not hasattr(self, meth):
            raise AttributeError("No setter for attribute '%s'." % attr)
        meth = getattr(self, meth)
        meth(value)

    # -------------
    # Normalization
    # -------------

    def round(self):
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

    def _round(self, **kwargs):
        """
        Subclasses may override this method.
        """
        mathInfo = self._toMathInfo(guidelines=False)
        mathInfo = mathInfo.round()
        self._fromMathInfo(mathInfo, guidelines=False)

    # -------------
    # Interpolation
    # -------------

    def _toMathInfo(self, guidelines=True):
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
                    color=guideline.color
                )
                self.guidelines.append(d)
        info = fontMath.MathInfo(self)
        del self.guidelines
        return info

    def _fromMathInfo(self, mathInfo, guidelines=True):
        self.guidelines = []
        mathInfo.extractInfo(self)
        font = self.font
        if guidelines:
            for guideline in self.guidelines:
                font.appendGuideline(
                    position=(guideline["x"], guideline["y"]),
                    angle=guideline["angle"],
                    name=guideline["name"],
                    color=guideline["color"]
                    # XXX identifier is lost
                )
        del self.guidelines

    def interpolate(self, factor, minInfo, maxInfo, round=True, suppressError=True):
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
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minInfo.__class__.__name__))
        if not isinstance(maxInfo, BaseInfo):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxInfo.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minInfo, maxInfo, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minInfo, maxInfo, round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        minInfo = minInfo._toMathInfo()
        maxInfo = maxInfo._toMathInfo()
        result = interpolate(minInfo, maxInfo, factor)
        if round:
            result = result.round()
        self._fromMathInfo(result)
