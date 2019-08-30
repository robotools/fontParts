.. highlight:: python
.. module:: fontParts.base

#########
Component
#########

***********
Description
***********

A component can be a part of a glyph, and it is a reference to another glyph in the same font. With components you can make glyphs depend on other glyphs. Changes to the base glyph will reflect in the component as well.

The parent of a component is usually a glyph. Components can be decomposed: they replace themselves with the actual outlines from the base glyph. When that happens, the link between the original and the component is broken: changes to the base glyph will no longer reflect in the glyph that had the component.

********
Overview
********

Parents
=======

.. autosummary::
    :nosignatures:

    BaseComponent.glyph
    BaseComponent.layer
    BaseComponent.font

Copy
====

.. autosummary::
    :nosignatures:

    BaseComponent.copy

Identification
==============

.. autosummary::
    :nosignatures:

    BaseComponent.identifier
    BaseComponent.index

Attributes
==========

.. autosummary::
    :nosignatures:

    BaseComponent.baseGlyph
    BaseComponent.transformation
    BaseComponent.offset
    BaseComponent.scale

Queries
=======

.. autosummary::
    :nosignatures:

    BaseComponent.bounds
    BaseComponent.pointInside

Pens and Drawing
================

.. autosummary::
    :nosignatures:

    BaseComponent.draw
    BaseComponent.drawPoints

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseComponent.transformBy
    BaseComponent.moveBy
    BaseComponent.scaleBy
    BaseComponent.rotateBy
    BaseComponent.skewBy

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseComponent.decompose
    BaseComponent.round

Environment
===========

.. autosummary::
    :nosignatures:

    BaseComponent.naked
    BaseComponent.changed

*********
Reference
*********

.. autoclass:: BaseComponent

Parents
=======

.. autoattribute:: BaseComponent.glyph
.. autoattribute:: BaseComponent.layer
.. autoattribute:: BaseComponent.font

Copy
====

.. automethod:: BaseComponent.copy

Identification
==============

.. autoattribute:: BaseComponent.identifier
.. autoattribute:: BaseComponent.index

Attributes
==========

.. autoattribute:: BaseComponent.baseGlyph
.. autoattribute:: BaseComponent.transformation
.. autoattribute:: BaseComponent.offset
.. autoattribute:: BaseComponent.scale

Queries
=======

.. autoattribute:: BaseComponent.bounds
.. automethod:: BaseComponent.pointInside

Pens and Drawing
================

.. automethod:: BaseComponent.draw
.. automethod:: BaseComponent.drawPoints

Transformations
===============

.. automethod:: BaseComponent.transformBy
.. automethod:: BaseComponent.moveBy
.. automethod:: BaseComponent.scaleBy
.. automethod:: BaseComponent.rotateBy
.. automethod:: BaseComponent.skewBy

Normalization
=============

.. automethod:: BaseComponent.decompose
.. automethod:: BaseComponent.round

Environment
===========

.. automethod:: BaseComponent.naked
.. automethod:: BaseComponent.changed
