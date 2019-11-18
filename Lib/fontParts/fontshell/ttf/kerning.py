import defcon
from fontParts.base import BaseKerning
from fontParts.fontshell.base import RBaseObject
from fontTools.ttLib import TTFont
from fontParts.fontshell.ttf.getKerningPairsFromOTF import OTFKernReader

class TTKerning_kernTable(RBaseObject, BaseKerning):
    def _items(self):
        return self.naked().items()

    def _contains(self, key):
        return key in self.naked()

    def _setItem(self, key, value):
        self.naked()[key] = value

    def _getItem(self, key):
        return self.naked()[key]

    def _delItem(self, key):
        del self.naked()[key]

    def _find(self, pair, default=0):
        return self.naked().find(pair, default)

class TTKerning_GPOSTable(RBaseObject, BaseKerning):
    wrapClass = TTFont
    def _init(self, *args, **kwargs):
        self._wrapped = OTFKernReader(kwargs["wrap"].reader.file.name).kerningPairs

    def _items(self):
        return self.naked().items()

    def _contains(self, key):
        return key in self.naked()

    def _setItem(self, key, value):
        self.raiseNotImplementedError()

    def _getItem(self, key):
        return self.naked()[key]

    def _delItem(self, key):
        del self.naked()[key]

    def _find(self, pair, default=0):
        return self.naked().find(pair, default)
