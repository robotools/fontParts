import weakref

from .errors import FontPartsError
from .base import BaseDict, dynamicProperty
import validators


class BaseGroups(BaseDict):

    keyValidator = validators.validateGroupKey
    valueValidator = validators.validateGroupValue

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

    font = dynamicProperty("font", "The groups' parent font.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

	# ---------
	# Searching
	# ---------

    def findGlyph(self, glyphName):
        """
        Return a list of all groups contianing glyphName.
        """
        glyphName = validators.validateGlyphName(glyphName)
        groupNames = self._findGlyph(glyphName)
        groupNames = [self.keyValidator(groupName) for groupName in groupNames]
        return groupNames

    def _findGlyph(self, glyphName):
        """
        Subclasses may override this method.
        """
        found = []
        for groupName, groupList in self.items():
            if glyphName in groupList:
                found.append(groupName)
        return found

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
