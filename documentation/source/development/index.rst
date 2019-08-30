.. highlight:: python

####################
Developing FontParts
####################

You want to help with developing FontParts? Yay!

We are mostly focused on documenting the objects and building a test suite. We'll eventually need bits of code here and there. If you have an idea for a new API or want to discuss one of the testing APIs, cool.

.. _developing-proposals:

*********
Proposals
*********

Want to suggest a new font part for FontParts? It's best to do this as an issue on the `FontParts GitHub <http://github.com/robofab-developers/fontParts/issues>`_ repository. Please present why you think this needs to be added. Before you do so, please make sure you understand the goals of the project, the existing API and so on.

.. _developing-bug-reports:


***********
Bug Reports
***********

Notice a bug when using FontParts? Is it a bug in a specific application? If so, please report the bug to the application developer. If it's not specific to a particular application, please open an issue on GitHub or, if you really can't `open an issue on GitHub <https://github.com/robofab-developers/fontParts/issues>`_, send a message to the `RoboFab mailing list <https://groups.google.com/forum/#!forum/robofab>`_


.. _developing-coding:

******
Coding
******

Take a look at the `open issues <https://github.com/robofab-developers/fontParts/issues>`_ and see if there is anything there that you want to work on. Please try to follow the general coding style of the library so that everything has the same level of readability.

This library follows much of PEP8, with a couple of exceptions. You’ll see camelCase. We like camelCase. The standard line length is also 90 characters. If possible, try to keep lines to 80, but 90 comes in handy occasionally. You’ll also notice that some builtin names are redefined in as variables in methods. It’s impossible not to use ``type`` in a package dealing with fonts.

*********************
Writing Documentation
*********************

We really need help with adding the formatted documentation strings to the base objects. The API documentation is generated from those. Here's a :doc:`style guide <documenting>`. Please look at the `Documentation project <https://github.com/robofab-developers/fontParts/projects/2>`_ on GitHub and see if there is anything you want to work on. If there is, ask to be assigned to that issue, and then follow the style guide. A good place to look for examples of the object documentation is the `glyph object <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/base/glyph.py>`_.

**********
Test Suite
**********

We also really need help in finishing up the test suite. You can see what needs to be done in the `Tests project <https://github.com/robofab-developers/fontParts/projects/1>`_ on GitHub. Pick something you want to write tests for and ask to be assigned to that issue. More information about writing tests is :doc:`here <testing>`.
