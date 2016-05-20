import weakref

from .errors import FontPartsError
from .base import BaseObject, dynamicProperty
import validators


class BaseFeatures(BaseObject):

    copyAttributes = ("text",)

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

    font = dynamicProperty("font", "The features' parent font.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

	# ----
	# Text
	# ----

    text = dynamicProperty("base_text", ".fea formatted text representing the features.")

    def _get_base_text(self):
        value = self._get_text()
        if value is not None:
            value = validators.validateFeatureText(value)
        return value

    def _set_base_text(self, value):
        if value is not None:
            value = validators.validateFeatureText(value)
        self._set_text(value)

    def _get_text(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_text(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()
