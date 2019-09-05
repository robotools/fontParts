from fontParts.base import BaseInfo
from fontParts.fontshell.base import RBaseObject
from fontTools.ttLib import TTFont
import fontTools.ttLib.tables._n_a_m_e
import fontTools.ttLib.tables._h_e_a_d
import fontTools.ttLib.tables._h_h_e_a
import fontTools.ttLib.tables._p_o_s_t
import fontTools.ttLib.tables.O_S_2f_2
import re

class WrappedOTTable(RBaseObject):
    wrappedAttributes = {}

    def _getAttr(self,attr):
      if attr in self.wrappedAttributes:
        return getattr(self.naked(), self.wrappedAttributes[attr])
      return BaseInfo._getAttr(self,attr)

    def _setAttr(self,attr, value):
      if attr in self.wrappedAttributes:
        return setattr(self.naked(), self.wrappedAttributes[attr], value)
      return BaseInfo._setAttr(self,attr, value)

class OTInfo_headTable(WrappedOTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._h_e_a_d
    wrappedAttributes = {
      "unitsPerEm": "unitsPerEm"
    }

class OTInfo_OS2Table(WrappedOTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables.O_S_2f_2
    wrappedAttributes = {
      "xHeight": "sxHeight",
      "capHeight": "sCapHeight",
    }

class OTInfo_hheaTable(WrappedOTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._h_h_e_a
    wrappedAttributes = {
      "ascender": "ascent",
      "descender": "descent"
    }

class OTInfo_postTable(WrappedOTTable, BaseInfo):
    wrapClass = fontTools.ttLib.tables._p_o_s_t
    wrappedAttributes = {
      "italicAngle": "italicAngle",
    }

class OTInfo_nameTable(WrappedOTTable, BaseInfo):
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

    def _get_copyright(self):
      return self.get_name_table_id(["COPYRIGHT"])

    def _get_trademark(self):
      return self.get_name_table_id(["TRADEMARK"])

    def _get_familyName(self):
      return self.get_name_table_id(["PREFERRED_FAMILY", "LEGACY_FAMILY"])

    def _get_styleName(self):
      return self.get_name_table_id(["PREFERRED_SUBFAMILY", "LEGACY_SUBFAMILY"])

    def _get_versionMajor(self):
      v = self.get_name_table_id(["VERSION_STRING"])
      return int(re.search('^Version (\d+)\.(\d+)', v)[1])

    def _get_versionMinor(self):
      v = self.get_name_table_id(["VERSION_STRING"])
      return int(re.search('^Version (\d+)\.(\d+)', v)[2])

class OTInfo(RBaseObject, BaseInfo):
    wrapClass = TTFont
    def _init(self, *args, **kwargs):
        self.tables = [
          OTInfo_nameTable(wrap=kwargs["wrap"]["name"]),
          OTInfo_headTable(wrap=kwargs["wrap"]["head"]),
          OTInfo_hheaTable(wrap=kwargs["wrap"]["hhea"]),
          OTInfo_OS2Table(wrap=kwargs["wrap"]["OS/2"]),
          OTInfo_postTable(wrap=kwargs["wrap"]["post"])
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
