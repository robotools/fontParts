.. highlight:: python
.. module:: fontParts.base

####
Info
####

***********
Description
***********

The :class:`Info <BaseInfo>` object contains all names, numbers, URLs, dimensions, values, etc. that would otherwise clutter up the font object. You don't have to create a :class:`Info <BaseInfo>` object yourself, :class:`Font <BaseFont>` makes one when it is created.

:class:`Info <BaseInfo>` doesn’t check the validity of the entries, it just provides storage or access to them.

********
Overview
********

.. autosummary::
    :nosignatures:

    BaseInfo.copy
    BaseInfo.font
    BaseInfo.interpolate
    BaseInfo.round
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

Environment
===========

.. automethod:: BaseInfo.naked
.. automethod:: BaseInfo.changed
