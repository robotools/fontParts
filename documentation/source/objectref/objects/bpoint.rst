.. highlight:: python
.. module:: fontParts.base

######
bPoint
######

***********
Description
***********

The :class:`bPoint <BaseBPoint>` is a point object which mimics the old “Bezier Point” from RoboFog. It has attributes for :attr:`bcpIn <BaseBPoint.bcpIn>`, anchor, bcpOut and type. The coordinates in bcpIn and bcpOut are relative to the position of the anchor. For instance, if the bcpIn is 20 units to the left of the anchor, its coordinates would be (-20,0), regardless of the coordinates of the anchor itself. Also: bcpIn will be (0,0) when it is “on top of the anchor”, i.e. when there is no bcp it will still have a value. The parent of a bPoint is usually a :class:`Contour <BaseContour>`.



********
Overview
********

Parents
=======

.. autosummary::
    :nosignatures:

    BaseBPoint.contour
    BaseBPoint.glyph
    BaseBPoint.layer
    BaseBPoint.font

Identification
==============

.. autosummary::
    :nosignatures:

    BaseBPoint.index

Attributes
==========

.. autosummary::
    :nosignatures:

    BaseBPoint.type

Points
======

.. autosummary::
    :nosignatures:

    BaseBPoint.anchor
    BaseBPoint.bcpIn
    BaseBPoint.bcpOut

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseBPoint.transformBy
    BaseBPoint.moveBy
    BaseBPoint.scaleBy
    BaseBPoint.rotateBy
    BaseBPoint.skewBy

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseBPoint.round

Environment
===========

.. autosummary::
    :nosignatures:

    BaseBPoint.naked
    BaseBPoint.changed


*********
Reference
*********

.. autoclass:: BaseBPoint

Parents
=======

.. autoattribute:: BaseBPoint.contour
.. autoattribute:: BaseBPoint.glyph
.. autoattribute:: BaseBPoint.layer
.. autoattribute:: BaseBPoint.font

Identification
==============

.. autoattribute:: BaseBPoint.index

Attributes
==========

.. autoattribute:: BaseBPoint.type

Points
======

.. autoattribute:: BaseBPoint.anchor
.. autoattribute:: BaseBPoint.bcpIn
.. autoattribute:: BaseBPoint.bcpOut

Transformations
===============

.. automethod:: BaseBPoint.transformBy
.. automethod:: BaseBPoint.moveBy
.. automethod:: BaseBPoint.scaleBy
.. automethod:: BaseBPoint.rotateBy
.. automethod:: BaseBPoint.skewBy

Normalization
=============

.. automethod:: BaseBPoint.round

Environment
===========

.. automethod:: BaseBPoint.naked
.. automethod:: BaseBPoint.changed
