def OpenFont(path=None, showInterface=True):
    return dispatcher["OpenFont"](path=path, showInterface=showInterface)

def NewFont(familyName=None, styleName=None, showInterface=True):
    return dispatcher["NewFont"](familyName=familyName, styleName=styleName, showInterface=showInterface)

def CurrentFont():
    return dispatcher["CurrentFont"]()

def CurrentGlyph():
    return dispatcher["CurrentGlyph"]()

def AllFonts():
    """
    XXX

    This needs to be a special list with the
    additional methods as defined in RoboFont.

    XXX
    """
    return dispatcher["CurrentGlyph"]()

def RFont(path=None, showInterface=True):
    return dispatcher["RFont"](path=path, showInterface=showInterface)

# ----------
# Dispatcher
# ----------

class _EnvironmentDispatcher(object):

    def __init__(self):
        self._registry = {
            "OpenFont" : None,
            "NewFont" : None,
            "CurrentFont" : None,
            "CurrentGlyph" : None,
            "AllFonts" : None,
            "RFont" : None,
            "RGlyph" : None
        }

    def __setitem__(self, name, func):
        self._registry[name] = func

    def __getitem__(self, name):
        func = self._registry[name]
        if func is None:
            raise NotImplementedError
        return func

dispatcher = _EnvironmentDispatcher()

# -------
# NoneLab
# -------

from .objects import nonelab

try:
    from .objects import nonelab

    # OpenFont, RFont

    def _NoneLabRFont(path=None, showInterface=True):
        return nonelab.RFont(pathOrObject=path, showInterface=showInterface)

    dispatcher["OpenFont"] = _NoneLabRFont
    dispatcher["RFont"] = _NoneLabRFont

    # NewFont

    def _NoneLabNewFont(familyName=None, styleName=None, showInterface=True):
        font = nonelab.RFont(showInterface=showInterface)
        if familyName is not None:
            font.info.familyName = familyName
        if styleName is not None:
            font.info.styleName = styleName
        return font

    dispatcher["NewFont"] = _NoneLabNewFont

except ImportError:
    pass
