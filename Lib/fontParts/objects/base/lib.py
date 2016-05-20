import weakref

from .errors import FontPartsError
from .base import BaseDict, dynamicProperty
import validators


class BaseLib(BaseDict):

    keyValidator = validators.validateLibKey
    valueValidator = validators.validateLibValue

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        glyph = self.glyph
        if glyph is not None:
            return glyph
        return self.font

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The lib's parent glyph.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        assert self._font is None
        assert self._glyph is None
        if glyph is not None:
            glyph = weakref.ref(glyph)
        self._glyph = glyph

    # Font

    _font = None

    font = dynamicProperty("font", "The lib's parent font.")

    def _get_font(self):
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(self, font):
        assert self._font is None
        assert self._glyph is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

    # Layer

    layer = dynamicProperty("layer", "The lib's parent layer.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

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
