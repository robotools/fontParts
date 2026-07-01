.. highlight:: python
.. module:: fontParts.base

########
Features
########

***********
Description
***********

Features is text in the `Adobe Font Development Kit <http://www.adobe.com/devnet/opentype/afdko.html>`_ for OpenType `.fea syntax <http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html>`_ that describes the OpenType features of your font. The `OpenType Cookbook <http://opentypecookbook.com>`_ is a great place to start learning how to write features. Your features must be self-contained; for example, any glyph or mark classes must be defined within the file. No assumption should be made about the validity of the syntax, and FontParts does not check the validity of the syntax.

.. note:: It is important to note that the features file may contain data that is a duplicate of or data that is in conflict with the data in :class:`BaseKerning`, :class:`BaseGroups`, and :class:`BaseInfo`. Synchronization is up to the user and application developers.

::

    font = CurrentFont()
    print(font.features)

********
Overview
********

.. autosummary::
    :nosignatures:

    BaseFeatures.copy
    BaseFeatures.font
    BaseFeatures.text

*********
Reference
*********

.. autoclass:: BaseFeatures

Copy
====

.. automethod:: BaseFeatures.copy

Parents
=======

.. autoattribute:: BaseFeatures.font

Attributes
==========

.. autoattribute:: BaseFeatures.text
