from fontParts.base import BaseInfo
from fontParts.fontshell.base import RBaseObject
from fontTools.ttLib import TTFont
import fontTools.ttLib.tables._n_a_m_e
import fontTools.ttLib.tables._h_e_a_d
import fontTools.ttLib.tables._h_h_e_a
import fontTools.ttLib.tables._p_o_s_t
import fontTools.ttLib.tables.O_S_2f_2
import re

class WrappedTTTable(RBaseObject):
    wrappedAttributes = {}

    def _getAttr(self,attr):
      if attr in self.wrappedAttributes:
        return getattr(self.naked(), self.wrappedAttributes[attr])
      return BaseInfo._getAttr(self,attr)

    def _setAttr(self,attr, value):
      if attr in self.wrappedAttributes:
        return setattr(self.naked(), self.wrappedAttributes[attr], value)
      return BaseInfo._setAttr(self,attr, value)

class TTInfo_headTable(WrappedTTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._h_e_a_d
    wrappedAttributes = {
      "unitsPerEm": "unitsPerEm"
    }

class TTInfo_OS2Table(WrappedTTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables.O_S_2f_2
    wrappedAttributes = {
      "xHeight": "sxHeight",
      "capHeight": "sCapHeight",
    }

class TTInfo_hheaTable(WrappedTTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._h_h_e_a
    wrappedAttributes = {
      "ascender": "ascent",
      "descender": "descent"
    }

class TTInfo_postTable(WrappedTTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._p_o_s_t
    wrappedAttributes = {
      "italicAngle": "italicAngle",
    }

class TTInfo_nameTable(WrappedTTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._n_a_m_e

    # Borrowed from fonttools/Snippets/rename-fonts.py
    WINDOWS_ENGLISH_IDS = 3, 1, 0x409
    MAC_ROMAN_IDS = 1, 0, 0

    NAME_IDS = dict(
        COPYRIGHT = 0,
        LEGACY_FAMILY=1,
        LEGACY_SUBFAMILY=2,
        TRUETYPE_UNIQUE_ID=3,
        FULL_NAME=4,
        VERSION_STRING=5,
        POSTSCRIPT_NAME=6,
        TRADEMARK=7,
        PREFERRED_FAMILY=16,
        PREFERRED_SUBFAMILY=17,
        WWS_FAMILY=21,
    )

    def get_name_table_id(self, idlist):
        name_rec = None
        for plat_id, enc_id, lang_id in (self.WINDOWS_ENGLISH_IDS, self.MAC_ROMAN_IDS):
            for name_id in idlist:
                name_rec = self.naked().getName(
                    nameID=self.NAME_IDS[name_id],
                    platformID=plat_id,
                    platEncID=enc_id,
                    langID=lang_id,
                )
                if name_rec is not None:
                    break
            if name_rec is not None:
                break
        if name_rec:
          return name_rec.toUnicode()

    def set_name_table_id(self, idlist, newstring):
        name_rec = None
        for plat_id, enc_id, lang_id in (self.WINDOWS_ENGLISH_IDS, self.MAC_ROMAN_IDS):
            for name_id in idlist:
                self.naked().setName(newstring,
                    nameID=self.NAME_IDS[name_id],
                    platformID=plat_id,
                    platEncID=enc_id,
                    langID=lang_id,
                )

    def _get_copyright(self):
      return self.get_name_table_id(["COPYRIGHT"])
    def _set_copyright(self,s):
      return self.set_name_table_id(["COPYRIGHT"],s)

    def _get_trademark(self):
      return self.get_name_table_id(["TRADEMARK"])
    def _set_trademark(self,s):
      return self.set_name_table_id(["TRADEMARK"],s)

    def _get_familyName(self):
      return self.get_name_table_id(["PREFERRED_FAMILY", "LEGACY_FAMILY"])
    def _set_familyName(self,s):
      return self.set_name_table_id(["PREFERRED_FAMILY", "LEGACY_FAMILY"],s)

    def _get_styleName(self):
      return self.get_name_table_id(["PREFERRED_SUBFAMILY", "LEGACY_SUBFAMILY"])
    def _set_styleName(self,s):
      return self.set_name_table_id(["PREFERRED_SUBFAMILY", "LEGACY_SUBFAMILY"],s)

    def _get_versionMajor(self):
      v = self.get_name_table_id(["VERSION_STRING"])
      if v is None: return 0
      m = re.search('^Version (\d+)\.(\d+)', v)
      if m is None: return 0
      return int(m[1])

    def _set_versionMajor(self,i):
      newstring = "Version %i.%i" % (i, self.versionMinor)
      return self.set_name_table_id(["VERSION_STRING"], newstring)

    def _get_versionMinor(self):
      v = self.get_name_table_id(["VERSION_STRING"])
      if v is None: return 0
      m = re.search('^Version (\d+)\.(\d+)', v)
      if m is None: return 0
      return int(m[2])

    def _set_versionMinor(self,i):
      newstring = "Version %i.%i" % (self.versionMajor, i)
      return self.set_name_table_id(["VERSION_STRING"], newstring)

class TTInfo(RBaseObject, BaseInfo):
    wrapClass = TTFont
    def _init(self, *args, **kwargs):
        self.tables = [
          TTInfo_nameTable(wrap=kwargs["wrap"]["name"]),
          TTInfo_headTable(wrap=kwargs["wrap"]["head"]),
          TTInfo_hheaTable(wrap=kwargs["wrap"]["hhea"]),
          TTInfo_OS2Table(wrap=kwargs["wrap"]["OS/2"]),
          TTInfo_postTable(wrap=kwargs["wrap"]["post"])
        ]

    def _getAttr(self, attr):
        for t in self.tables:
          if hasattr(t, attr) or attr in t.wrappedAttributes:
            return getattr(t, attr)
        return self.raiseNotImplementedError()

    def _setAttr(self, attr, value):
        for t in self.tables:
          if hasattr(t, attr):
            return setattr(t, attr, value)
        return self.raiseNotImplementedError()
