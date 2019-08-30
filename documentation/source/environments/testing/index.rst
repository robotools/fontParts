
#######
Testing
#######

.. _implementing-testing:

A test suite is provided to test any implementation, either subclassed from the base objects or implemented independently. The suite has been designed to be environment and format agnostic. Environment developers only need to implement a function that provides objects for testing and a simple Python script that sends the function to the test suite.

Testing an environment
======================

The main thing that an environment needs to implement is the test object generator. This should create an object for the requested class identifier. ::

   def MyAppObjectGenerator(classIdentifier):
       unrequested = []
       obj = myApp.foo.bar.something.hi(classIdentifier)
       return obj, unrequested

If an environment does not allow orphan objects, parent objects may create the parent objects and store them in a list. The function must return the generated objects and the list of unrequested objects (or an empty list if no parent objects were generated).

The class identifiers are as follows:

* font
* info
* groups
* kerning
* features
* lib
* layer
* glyph
* contour
* segment
* bpoint
* point
* component
* anchor
* image
* guideline

Once an environment has developed this function, all that remains is to pass the function to the test runner::

   from fontParts.test import testEnvironment

   if __name__ == "__main__":
       testEnvironment(MyAppObjectGenerator)

This can then be executed and the report will be printed.

.. :note::

It is up to each environment to ensure that the bridge from the environment's native objects to the fontParts wrappers is working properly. This has to be done on an environment by environment basis since the native objects are not consistently implemented.