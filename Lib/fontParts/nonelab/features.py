import defcon
from fontParts.base import BaseFeatures, FontPartsError
from fontParts.nonelab.base import RBaseObject


class RFeatures(RBaseObject, BaseFeatures):

    wrapClass = defcon.Features

    def _get_text(self):
        return self.naked().text

    def _set_text(self, value):
        self.naked().text = value
