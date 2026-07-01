.. highlight:: python
.. module:: fontParts.base

####
Info
####

***********
Description
***********

The :class:`Info <BaseInfo>` object contains all names, numbers, URLs, dimensions, values, etc. that would otherwise clutter up the font object. You don't have to create a :class:`Info <BaseInfo>` object yourself, :class:`Font <BaseFont>` makes one when it is created.

:class:`Info <BaseInfo>` validates any value set for a `Info <BaseInfo>` item, but does not check if the data is sane (i.e., you can set valid but incorrect data).

The :class:`Info <BaseInfo>` object (as any other fontParts object) does not allow to modify mutable containers (like lists) in-place. Always get a value, modify it and then set it back to perform an edit. 

For a list of info attributes, refer to the `UFO fontinfo.plist Specification <https://unifiedfontobject.org/versions/ufo3/fontinfo.plist/#specification>`_.

********
Overview
********

.. autosummary::
    :nosignatures:

    BaseInfo.familyName
    BaseInfo.styleName
    BaseInfo.styleMapFamilyName
    BaseInfo.styleMapStyleName
    BaseInfo.versionMajor
    BaseInfo.versionMinor
    BaseInfo.year
    BaseInfo.copyright
    BaseInfo.trademark
    BaseInfo.unitsPerEm
    BaseInfo.descender
    BaseInfo.xHeight
    BaseInfo.capHeight
    BaseInfo.ascender
    BaseInfo.italicAngle
    BaseInfo.note
    BaseInfo.openTypeHeadCreated
    BaseInfo.openTypeHeadLowestRecPPEM
    BaseInfo.openTypeHeadFlags
    BaseInfo.openTypeHheaAscender
    BaseInfo.openTypeHheaDescender
    BaseInfo.openTypeHheaLineGap
    BaseInfo.openTypeHheaCaretSlopeRise
    BaseInfo.openTypeHheaCaretSlopeRun
    BaseInfo.openTypeHheaCaretOffset
    BaseInfo.openTypeNameDesigner
    BaseInfo.openTypeNameDesignerURL
    BaseInfo.openTypeNameManufacturer
    BaseInfo.openTypeNameManufacturerURL
    BaseInfo.openTypeNameLicense
    BaseInfo.openTypeNameLicenseURL
    BaseInfo.openTypeNameVersion
    BaseInfo.openTypeNameUniqueID
    BaseInfo.openTypeNameDescription
    BaseInfo.openTypeNamePreferredFamilyName
    BaseInfo.openTypeNamePreferredSubfamilyName
    BaseInfo.openTypeNameCompatibleFullName
    BaseInfo.openTypeNameSampleText
    BaseInfo.openTypeNameWWSFamilyName
    BaseInfo.openTypeNameWWSSubfamilyName
    BaseInfo.openTypeOS2WidthClass
    BaseInfo.openTypeOS2WeightClass
    BaseInfo.openTypeOS2Selection
    BaseInfo.openTypeOS2VendorID
    BaseInfo.openTypeOS2Panose
    BaseInfo.openTypeOS2FamilyClass
    BaseInfo.openTypeOS2UnicodeRanges
    BaseInfo.openTypeOS2CodePageRanges
    BaseInfo.openTypeOS2TypoAscender
    BaseInfo.openTypeOS2TypoDescender
    BaseInfo.openTypeOS2TypoLineGap
    BaseInfo.openTypeOS2WinAscent
    BaseInfo.openTypeOS2WinDescent
    BaseInfo.openTypeOS2Type
    BaseInfo.openTypeOS2SubscriptXSize
    BaseInfo.openTypeOS2SubscriptYSize
    BaseInfo.openTypeOS2SubscriptXOffset
    BaseInfo.openTypeOS2SubscriptYOffset
    BaseInfo.openTypeOS2SuperscriptXSize
    BaseInfo.openTypeOS2SuperscriptYSize
    BaseInfo.openTypeOS2SuperscriptXOffset
    BaseInfo.openTypeOS2SuperscriptYOffset
    BaseInfo.openTypeOS2StrikeoutSize
    BaseInfo.openTypeOS2StrikeoutPosition
    BaseInfo.openTypeVheaVertTypoAscender
    BaseInfo.openTypeVheaVertTypoDescender
    BaseInfo.openTypeVheaVertTypoLineGap
    BaseInfo.openTypeVheaCaretSlopeRise
    BaseInfo.openTypeVheaCaretSlopeRun
    BaseInfo.openTypeVheaCaretOffset
    BaseInfo.postscriptFontName
    BaseInfo.postscriptFullName
    BaseInfo.postscriptSlantAngle
    BaseInfo.postscriptUniqueID
    BaseInfo.postscriptUnderlineThickness
    BaseInfo.postscriptUnderlinePosition
    BaseInfo.postscriptIsFixedPitch
    BaseInfo.postscriptBlueValues
    BaseInfo.postscriptOtherBlues
    BaseInfo.postscriptFamilyBlues
    BaseInfo.postscriptFamilyOtherBlues
    BaseInfo.postscriptStemSnapH
    BaseInfo.postscriptStemSnapV
    BaseInfo.postscriptBlueFuzz
    BaseInfo.postscriptBlueShift
    BaseInfo.postscriptBlueScale
    BaseInfo.postscriptForceBold
    BaseInfo.postscriptDefaultWidthX
    BaseInfo.postscriptNominalWidthX
    BaseInfo.postscriptWeightName
    BaseInfo.postscriptDefaultCharacter
    BaseInfo.postscriptWindowsCharacterSet
    BaseInfo.copy
    BaseInfo.font
    BaseInfo.interpolate
    BaseInfo.round
    BaseInfo.update
    BaseInfo.naked
    BaseInfo.changed

*********
Reference
*********

.. autoclass:: BaseInfo

Attributes
==========

.. autoattribute:: BaseInfo.familyName

.. autoattribute:: BaseInfo.styleName

.. autoattribute:: BaseInfo.styleMapFamilyName

.. autoattribute:: BaseInfo.styleMapStyleName

.. autoattribute:: BaseInfo.versionMajor

.. autoattribute:: BaseInfo.versionMinor

.. autoattribute:: BaseInfo.year

.. autoattribute:: BaseInfo.copyright

.. autoattribute:: BaseInfo.trademark

.. autoattribute:: BaseInfo.unitsPerEm

.. autoattribute:: BaseInfo.descender

.. autoattribute:: BaseInfo.xHeight

.. autoattribute:: BaseInfo.capHeight

.. autoattribute:: BaseInfo.ascender

.. autoattribute:: BaseInfo.italicAngle

.. autoattribute:: BaseInfo.note

.. autoattribute:: BaseInfo.openTypeHeadCreated

.. autoattribute:: BaseInfo.openTypeHeadLowestRecPPEM

.. autoattribute:: BaseInfo.openTypeHeadFlags

.. autoattribute:: BaseInfo.openTypeHheaAscender

.. autoattribute:: BaseInfo.openTypeHheaDescender

.. autoattribute:: BaseInfo.openTypeHheaLineGap

.. autoattribute:: BaseInfo.openTypeHheaCaretSlopeRise

.. autoattribute:: BaseInfo.openTypeHheaCaretSlopeRun

.. autoattribute:: BaseInfo.openTypeHheaCaretOffset

.. autoattribute:: BaseInfo.openTypeNameDesigner

.. autoattribute:: BaseInfo.openTypeNameDesignerURL

.. autoattribute:: BaseInfo.openTypeNameManufacturer

.. autoattribute:: BaseInfo.openTypeNameManufacturerURL

.. autoattribute:: BaseInfo.openTypeNameLicense

.. autoattribute:: BaseInfo.openTypeNameLicenseURL

.. autoattribute:: BaseInfo.openTypeNameVersion

.. autoattribute:: BaseInfo.openTypeNameUniqueID

.. autoattribute:: BaseInfo.openTypeNameDescription

.. autoattribute:: BaseInfo.openTypeNamePreferredFamilyName

.. autoattribute:: BaseInfo.openTypeNamePreferredSubfamilyName

.. autoattribute:: BaseInfo.openTypeNameCompatibleFullName

.. autoattribute:: BaseInfo.openTypeNameSampleText

.. autoattribute:: BaseInfo.openTypeNameWWSFamilyName

.. autoattribute:: BaseInfo.openTypeNameWWSSubfamilyName

.. autoattribute:: BaseInfo.openTypeOS2WidthClass

.. autoattribute:: BaseInfo.openTypeOS2WeightClass

.. autoattribute:: BaseInfo.openTypeOS2Selection

.. autoattribute:: BaseInfo.openTypeOS2VendorID

.. autoattribute:: BaseInfo.openTypeOS2Panose

.. autoattribute:: BaseInfo.openTypeOS2FamilyClass

.. autoattribute:: BaseInfo.openTypeOS2UnicodeRanges

.. autoattribute:: BaseInfo.openTypeOS2CodePageRanges

.. autoattribute:: BaseInfo.openTypeOS2TypoAscender

.. autoattribute:: BaseInfo.openTypeOS2TypoDescender

.. autoattribute:: BaseInfo.openTypeOS2TypoLineGap

.. autoattribute:: BaseInfo.openTypeOS2WinAscent

.. autoattribute:: BaseInfo.openTypeOS2WinDescent

.. autoattribute:: BaseInfo.openTypeOS2Type

.. autoattribute:: BaseInfo.openTypeOS2SubscriptXSize

.. autoattribute:: BaseInfo.openTypeOS2SubscriptYSize

.. autoattribute:: BaseInfo.openTypeOS2SubscriptXOffset

.. autoattribute:: BaseInfo.openTypeOS2SubscriptYOffset

.. autoattribute:: BaseInfo.openTypeOS2SuperscriptXSize

.. autoattribute:: BaseInfo.openTypeOS2SuperscriptYSize

.. autoattribute:: BaseInfo.openTypeOS2SuperscriptXOffset

.. autoattribute:: BaseInfo.openTypeOS2SuperscriptYOffset

.. autoattribute:: BaseInfo.openTypeOS2StrikeoutSize

.. autoattribute:: BaseInfo.openTypeOS2StrikeoutPosition

.. autoattribute:: BaseInfo.openTypeVheaVertTypoAscender

.. autoattribute:: BaseInfo.openTypeVheaVertTypoDescender

.. autoattribute:: BaseInfo.openTypeVheaVertTypoLineGap

.. autoattribute:: BaseInfo.openTypeVheaCaretSlopeRise

.. autoattribute:: BaseInfo.openTypeVheaCaretSlopeRun

.. autoattribute:: BaseInfo.openTypeVheaCaretOffset

.. autoattribute:: BaseInfo.postscriptFontName

.. autoattribute:: BaseInfo.postscriptFullName

.. autoattribute:: BaseInfo.postscriptSlantAngle

.. autoattribute:: BaseInfo.postscriptUniqueID

.. autoattribute:: BaseInfo.postscriptUnderlineThickness

.. autoattribute:: BaseInfo.postscriptUnderlinePosition

.. autoattribute:: BaseInfo.postscriptIsFixedPitch

.. autoattribute:: BaseInfo.postscriptBlueValues

.. autoattribute:: BaseInfo.postscriptOtherBlues

.. autoattribute:: BaseInfo.postscriptFamilyBlues

.. autoattribute:: BaseInfo.postscriptFamilyOtherBlues

.. autoattribute:: BaseInfo.postscriptStemSnapH

.. autoattribute:: BaseInfo.postscriptStemSnapV

.. autoattribute:: BaseInfo.postscriptBlueFuzz

.. autoattribute:: BaseInfo.postscriptBlueShift

.. autoattribute:: BaseInfo.postscriptBlueScale

.. autoattribute:: BaseInfo.postscriptForceBold

.. autoattribute:: BaseInfo.postscriptDefaultWidthX

.. autoattribute:: BaseInfo.postscriptNominalWidthX

.. autoattribute:: BaseInfo.postscriptWeightName

.. autoattribute:: BaseInfo.postscriptDefaultCharacter

.. autoattribute:: BaseInfo.postscriptWindowsCharacterSet


Copy
====

.. automethod:: BaseInfo.copy

Parents
=======

.. autoattribute:: BaseInfo.font

Interpolation
=============

.. automethod:: BaseInfo.interpolate

Normalization
=============

.. automethod:: BaseInfo.round

Update
======

.. automethod:: BaseInfo.update

Environment
===========

.. automethod:: BaseInfo.naked
.. automethod:: BaseInfo.changed