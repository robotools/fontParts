|Build Status| |Appveyor| |Coverage| |Codacy| |PyPI| |Versions|

FontParts
~~~~~~~~~

An API for interacting with the parts of fonts during the font
development process. FontParts is the replacement for
`RoboFab <http://robofab.com>`__. The project has a
`MIT open-source licence <LICENSE>`__.

The documentation is at
`fontparts.readthedocs.io <http://fontparts.readthedocs.io/en/latest/>`__.

*This is a work in progress. We are still working out the API, abstract
implementation, example implementation, test suite and documentation.*

Want to contribute?
-------------------

Thank you! Please see the `CONTRIBUTING.rst <https://github.com/robofab-developers/fontParts/blob/master/CONTRIBUTING.rst>`_ file for a guide on how to help.

Also, feedback is very much welcome, please open an issue when you run
into something that you wish fontParts did/didn't do.


Installation
~~~~~~~~~~~~

FontParts requires `Python <http://www.python.org/download/>`__ 3.6 or later.

The package is listed in the Python Package Index (PyPI), so you can
install it with `pip <https://pip.pypa.io>`__:

.. code:: sh

    pip install fontParts

If you would like to contribute to its development, you can clone the
repository from Github, install the package in 'editable' mode and
modify the source code in place. We recommend creating a virtual
environment, using `virtualenv <https://virtualenv.pypa.io>`__ or `venv <https://docs.python.org/3/library/venv.html>`__ module.

.. code:: sh

    # download the source code to 'fontParts' folder
    git clone https://github.com/robofab-developers/fontParts.git
    cd fontParts

    # create new virtual environment called e.g. 'fontParts-venv', or anything you like
    python -m virtualenv fontParts-venv

    # source the `activate` shell script to enter the environment (Un\*x); to exit, just type `deactivate`
    . fontParts-venv/bin/activate

    # to activate the virtual environment in Windows `cmd.exe`, do
    fontParts-venv\Scripts\activate.bat

    # install in 'editable' mode
    pip install -e .

Roadmap
~~~~~~~

We are currently working towards the 1.0 release.

* **0.8** Initial releases. Python 2 & 3.
* **0.9** Python 3 only.
* **1.0** Documentation and testing complete.
* **1.5** Removal of ``Deprecated``. Released 1 year after 1.0.

Testing
~~~~~~~

Testing is setup so that each environment that includes fontParts
can provides the objects needed to run a common set of tests.
This makes testing very easy for environments that use fontParts (for
example, see the fontshell
`test.py <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/fontshell/test.py>`__
script), but it means testing is different than other python packages.

Automated testing of the package is done in the fontshell environment.
fontshell is fontParts for the commandline, implemented with
`defcon <https://github.com/typesupply/defcon>`__ and is included
as part of the fontParts package.

Before you can run the test suite you’ll need to install the test dependencies:

.. code:: sh

    pip install -r dev-requirements.txt

To run the test suite you can do:

.. code:: sh

    python Lib/fontParts/fontshell/test.py

To test in other environments, run the test script provided by that environment.

You can also use `tox <https://testrun.org/tox/latest/>`__ to
automatically run tests on different Python versions in isolated virtual
environments.

.. code:: sh

    pip install tox
    tox

Note that when you run ``tox`` without arguments, the tests are executed
for all the environments listed in tox.ini's ``envlist``. In our case,
this is Python 3.6, so for this to work the ``python3.6`` executables must
be available in your ``PATH``.

You can specify an alternative environment list via the ``-e`` option,
or the ``TOXENV`` environment variable:

.. code:: sh

    tox -e py27-nocov
    TOXENV="py36-cov,htmlcov" tox

.. |Build Status| image:: https://travis-ci.org/robotools/fontParts.svg?branch=master
   :target: https://travis-ci.org/robotools/fontParts
.. |PyPI| image:: https://img.shields.io/pypi/v/fontParts.svg
   :target: https://pypi.org/project/fontParts
.. |Versions| image:: https://img.shields.io/badge/python-3.6%2C%203.7-blue.svg
   :alt: Python Versions
.. |Coverage| image:: https://codecov.io/gh/robotools/fontParts/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/robotools/fontParts
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/f99cc7af19964717b67a79ebf1523234
   :target: https://www.codacy.com/app/fontParts/fontParts?utm_source=github.com&amp;utm_campaign=Badge_Grade
.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/3x64dg9nbaiwl965/branch/master?svg=true
   :target: https://ci.appveyor.com/project/robotools/fontparts/
