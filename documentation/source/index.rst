.. highlight:: python

History
=======

FontParts is based on RoboFab. RoboFab was based on RoboFog. RoboFog was a fork of Fontographer with a built-in Python interpreter. The Fontographer core was wrapped with a lovely Python API. For example, to modify the spacing in all characters ("glyphs" wasn't a standard term back then) in the current font you'd do this::

   font = CurrentFont()

   for character in font:
      character.leftMargin = character.leftMargin + 10
      character.rightMargin = character.rightMargin + 10

When RoboFog could no longer be updated, lots of us designers switched to FontLab. We had *lots* of RoboFog scripts that were critical parts of our workflows and we needed them to work in FontLab right away. FontLab had a built-in Python interpreter, but the API for interacting with the FontLab core was very different from the API in RoboFog. So, a few of us (Erik, Just, Tal) wrote a library called RoboFab that implemented an API that was very similar to the RoboFog API. Designers could take their existing scripts, modify them a tiny bit and they would just work in FontLab. For example, here's how the above script would have been modified::

   from robofab.world import CurrentFont

   font = CurrentFont()

   for character in font:
      character.leftMargin = character.leftMargin + 10
      character.rightMargin = character.rightMargin + 10

This proved to be incredibly useful and it gave us the idea that a universal, environment independent scripting API would be a very good thing to have. So, we extended RoboFab to work in other environments. For example, to get the above script to work outside of any font editor, you would have done this::

   from robofab.world import OpenFont

   font = OpenFont("/path/to/my/font.ufo")

   for character in font:
      character.leftMargin = character.leftMargin + 10
      character.rightMargin = character.rightMargin + 10

Did you notice that the important parts of the script are completely unchanged? Sure, this is a simple two line example, but imagine that you have a suite of tools made of hundreds of thousands of lines of code. *Portable APIs are awesome!!!!!!*

This was very stable and worked reliably for over a decade. New font editors came along. New font formats came along. New ideas came along. RoboFab was not built in a way that made it easy to add all of these new things while making the old things keep working. We tried, hard, to make it work, but it wasn't possible. We decided that the way forward was to start over from scratch. That idea became FontParts.

TL;DR: FontParts is a new implementation of ideas that have worked nearly flawlessly for over two decades.

But why isn't it called RoboFab?
--------------------------------

Good question. Well, it's not 100% compatible with RoboFab, so we couldn't just drop it in place without breaking some working scripts. So, it needed a new name. Erik came up with the name "FontParts" because, you know, it represents parts of fonts.

Design Goals
============

The RoboFog API was quite simple and memorable. FontParts should follow the same model.

* It should be easy to understand. The main users of this API will be typeface designers, not professional coders.
* The objects, methods, arguments and return values should be memorable. We don't want designers to have to spend a lot of time trying to remember how to do basic things.
* It should look Pythonic. Python is a very legible language. That's great, but it can get uglified when ``environmentsStart_wrapping_lowerLevelAPIs``. We want the FontParts API to look like Python code so that it is easy to read.
