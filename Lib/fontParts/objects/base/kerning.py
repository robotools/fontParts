import weakref
import fontMath

from .errors import FontPartsError
from .base import BaseDict, dynamicProperty, interpolate
import validators


class BaseKerning(BaseDict):

    keyValidator = validators.validateKerningKey
    valueValidator = validators.validateKerningValue

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

    font = dynamicProperty("font", "The kerning's parent font.")

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
    # Transformation
    # --------------

    def scaleBy(self, value):
        """
        Scale all kernng pairs by value.
        """
        value = validators.validateTransformationScale(value)
        self._scale(value)

    def _scale(self, value):
        """
        Subclasses may override this method.
        """
        value = value[0]
        for k, v in self.items():
            v *= value
            self[key] = v

    # -------------
    # Normalization
    # -------------

    def round(self, multiple=1):
        """
        Round the kerning pair values to increments of multiple.
        """
        if not isinstance(multiple, int):
            raise FontPartsError("The round multiple must be an int not %s." % multiple.__class__.__name__)
        self._round(multiple)

    def _round(self, multiple=1):
        """
        Subclasses may override this method.
        """
        for pair, value in self.items():
            value = int(round(value / float(multiple))) * multiple
            self[pair] = value

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minKerning, maxKerning, round=True, suppressError=True):
        """
        Interpolate all pairs between minKerning and maxKerning.
        The interpolation occurs on a 0 to 1.0 range where minKerning
        is located at 0 and maxKerning is located at 1.0.

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
        if not isinstance(minKerning, BaseKerning):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, minKerning.__class__.__name__))
        if not isinstance(maxKerning, BaseKerning):
            raise FontPartsError("Interpolation to an instance of %r can not be performed from an instance of %r." % (self.__class__.__name__, maxKerning.__class__.__name__))
        round = validators.validateBoolean(round)
        suppressError = validators.validateBoolean(suppressError)
        self._interpolate(factor, minKerning, maxKerning, round=round, suppressError=suppressError)

    def _interpolate(self, factor, minKerning, maxKerning, round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        minKerning = fontMath.MathKerning(kerning=minKerning, groups=minKerning.font.groups)
        maxKerning = fontMath.MathKerning(kerning=maxKerning, groups=maxKerning.font.groups)
        result = interpolate(minKerning, maxKerning, factor)
        if round:
            result.round()
        self.clear()
        result.extractKerning(self.font)


    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, key):
        del self[key]

    def asDict(self):
        d = {}
        for k, v in self.items():
            d[k] = v
        return d
