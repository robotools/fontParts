|Build Status| |Code Health| |PyPI| |Versions|

FontParts
~~~~~~~~~

An API for interacting with the parts of fonts during the font
development process. FontParts is a strong candidate to replace
`RoboFab <http://robofab.com>`__. The project has a 
`MIT open-source licence <LICENSE>`__.

The documentation is at
`fontparts.readthedocs.io <http://fontparts.readthedocs.io/en/latest/>`__.

*This is a work in progress. We are still working out the API, abstract
implementation, example implementation, test suite and documentation.*

Want to contribute? Great! `These issues need help 
<https://github.com/robofab-developers/fontParts/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`__.
Also, feedback is very much welcome, please open an issue when you run
into something that you wish fontParts did/didn't do.


Installation
~~~~~~~~~~~~

FontParts requires `Python <http://www.python.org/download/>`__ 2.7, 3.4
or later.

The package is listed in the Python Package Index (PyPI), so you can
install it with `pip <https://pip.pypa.io>`__:

.. code:: sh

    pip install fontParts

If you would like to contribute to its development, you can clone the
repository from Github, install the package in 'editable' mode and
modify the source code in place. We recommend creating a virtual
environment, using `virtualenv <https://virtualenv.pypa.io>`__ or
Python 3 `venv <https://docs.python.org/3/library/venv.html>`__ module.

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

Testing
~~~~~~~

Testing is setup so that each environment that includes fontParts
can provides the objects needed to run a common set of tests. 
This makes testing very easy for environments that use fontParts (for
example, see the noneLab 
`test.py <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/nonelab/test.py>`__ 
script), but it means testing is different than other python packages. 

Automated testing of the package is done in the nonelab environment.
nonelab is fontParts for the commandline, implemented with 
`defcon <https://github.com/typesupply/defcon>`__ and is included
as part of the fontParts package.

To run the test suite, you can do:

.. code:: sh

    python Lib/fontParts/nonelab/test.py

To test in other environments, run the test script provided by that environment.

You can also use `tox <https://testrun.org/tox/latest/>`__ to
automatically run tests on different Python versions in isolated virtual
environments.

.. code:: sh

    pip install tox
    tox

Note that when you run ``tox`` without arguments, the tests are executed
for all the environments listed in tox.ini's ``envlist``. In our case,
this includes Python 2.7 and 3.6, so for this to work the ``python2.7``
and ``python3.6`` executables must be available in your ``PATH``.

You can specify an alternative environment list via the ``-e`` option,
or the ``TOXENV`` environment variable:

.. code:: sh

    tox -e py27-nocov
    TOXENV="py36-cov,htmlcov" tox

.. |Code Health| image:: https://landscape.io/github/robofab-developers/fontParts/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/robofab-developers/fontParts/master
.. |Build Status| image:: https://travis-ci.org/robofab-developers/fontParts.svg?branch=master
   :target: https://travis-ci.org/robofab-developers/fontParts
.. |PyPI| image:: https://img.shields.io/pypi/v/fontParts.svg
   :target: https://pypi.org/project/fontParts
.. |Versions| image:: https://img.shields.io/badge/python-2.7%2C%203.6-blue.svg
   :alt: Python Versions