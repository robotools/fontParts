.. highlight:: python
.. module:: fontParts.base.normalizers

###########
Normalizers
###########

*******
Kerning
*******

.. autofunction:: normalizeKerningKey
.. autofunction:: normalizeKerningValue

******
Groups
******

.. autofunction:: normalizeGroupKey
.. autofunction:: normalizeGroupValue

********
Features
********

.. autofunction:: normalizeFeatureText

***
Lib
***

.. autofunction:: normalizeLibKey
.. autofunction:: normalizeLibValue

******
Layers
******

.. autofunction:: normalizeLayerOrder
.. autofunction:: normalizeDefaultLayer
.. autofunction:: normalizeDefaultLayerName
.. autofunction:: normalizeLayerName

******
Glyphs
******

.. autofunction:: normalizeGlyph
.. autofunction:: normalizeGlyphOrder

Identification
==============

.. autofunction:: normalizeGlyphName
.. autofunction:: normalizeGlyphUnicodes
.. autofunction:: normalizeGlyphUnicode

Metrics
=======

.. autofunction:: normalizeGlyphWidth
.. autofunction:: normalizeGlyphLeftMargin
.. autofunction:: normalizeGlyphRightMargin
.. autofunction:: normalizeGlyphHeight
.. autofunction:: normalizeGlyphBottomMargin
.. autofunction:: normalizeGlyphTopMargin

********
Contours
********

.. autofunction:: normalizeContourIndex
.. autofunction:: normalizeContour

******
Points
******

.. autofunction:: normalizePointType
.. autofunction:: normalizePointName

********
Segments
********

.. autofunction:: normalizeSegmentType

*******
BPoints
*******

.. autofunction:: normalizeBPointType

**********
Components
**********

.. autofunction:: normalizeComponentIndex
.. autofunction:: normalizeComponentScale

*******
Anchors
*******

.. autofunction:: normalizeAnchorIndex
.. autofunction:: normalizeAnchorName

****
Note
****

.. autofunction:: normalizeGlyphNote

**********
Guidelines
**********

.. autofunction:: normalizeGuideline
.. autofunction:: normalizeGuidelineIndex
.. autofunction:: normalizeGuidelineAngle
.. autofunction:: normalizeGuidelineName

*******
Generic
*******

.. autofunction:: normalizeInternalObjectType

Positions
=========

.. autofunction:: normalizeX
.. autofunction:: normalizeY
.. autofunction:: normalizeCoordinateTuple
.. autofunction:: normalizeBoundingBox

Identification
==============

.. autofunction:: normalizeIndex
.. autofunction:: normalizeIdentifier
.. autofunction:: normalizeColor

Interpolation
=============

.. autofunction:: normalizeInterpolationFactor

Transformations
===============

.. autofunction:: normalizeTransformationMatrix
.. autofunction:: normalizeTransformationOffset
.. autofunction:: normalizeTransformationRotationAngle
.. autofunction:: normalizeTransformationSkewAngle
.. autofunction:: normalizeTransformationScale

Files
=====

.. autofunction:: normalizeFilePath
.. autofunction:: normalizeFileFormatVersion

Standard
========

.. autofunction:: normalizeBoolean
.. autofunction:: normalizeVisualRounding

