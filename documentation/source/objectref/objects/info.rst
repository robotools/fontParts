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

For a list of info attributes, refer to the `UFO fontinfo.plist Specification <https://unifiedfontobject.org/versions/ufo3/fontinfo.plist/#specification>`_.

********
Overview
********

.. autosummary::
    :nosignatures:

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
