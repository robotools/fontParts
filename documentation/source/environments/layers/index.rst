######
Layers
######

There are two primary layer models in the font world:

- font level layers: In this model, all glyphs have the same layers. A good example of this is a chromatic font.
- glyph level layers: In this model, individual glyphs may have their own unique layers.

fontParts supports both of these models. Both fonts and glyphs have fully developed layer APIs::

    font = CurrentFont()
    foregroundLayer = font.getLayer("foreground")
    backgroundLayer = font.getLayer("background")

    glyph = font["A"]
    foregroundGlyph = glyph.getLayer("foreground")
    backgroundGlyph = glyph.getLayer("background")

A font-level layer is a font-like object. Essentially, a layer has the same glyph management behavior as a font::

    font = CurrentFont()
    foreground = font.getLayer("foreground")
    glyph = foreground.newGlyph("A")

A glyph-level layer is identical to a glyph object::

    font = CurrentFont()
    glyph = font["A"]
    foreground = glyph.getLayer("foreground")
    background = glyph.getLayer("background")

When a scripter is addressing a font or glyph without specifying a specific layer, the action is performed on the "default" (or primary) layer. For example, in the original Fontographer there were two layers: foreground and background. The foreground was the primary layer and it contained the primary data that would be compiled into a font binary. In multi-layered glyph editing environments, designers can specify which layer should be considered primary. This layer is the "default" layer in fontParts. Thus::

    font = CurrentFont()
    glyph1 = font["A"]
    glyph2 = font.newGlyph("B")

The `glyph1` object will reference the A's "foreground" layer and the "foreground" layer will contain a new glyph named "B".

fontParts delegates the implementation to the environment subclasses. Given that an environment can only support font-level layers *or* glyph-level layers, the following algorithms can be used to simulate the model that the environment doesn't support.

Simulating glyph-level layers.
==============================

1. Get the parent font.
2. Iterate through all of the font's layers.
3. If the glyph's name is in the layer, grab the glyph from the layer.
4. Return all found glyphs.

Simulating font-level layers.
=============================

1. Iterate over all glyphs.
2. For every layer in the glyph, create a global mapping of layer name to glyphs containing a layer with the same name.
