=========================
Contributing to fontParts
=========================

Thanks for being interested in helping out with fontParts, we really appreciate it! 🎉👍

Below is a short guide to what we need help with, where to find both documentation about helping, and where to find examples to model when writing code or documentation.

Like anything in fontParts, if you see something that needs improvement/isn’t clear/could be added to, you can submit pull requests for this document.

**Right now we need the most help with writing tests and writing documentation.**

-----------------
Table of contents
-----------------

1. `Contributing with Issues`_

2. `I just have a question!`_

3. `Contributing Tests`_

    a) `What should I install to write tests?`_
    b) `How do I know what tests to write?`_

4. `Contributing Documentation`_

5. `Creating a fork & a pull request`_

    a) `Creating a fork`_
    b) `Creating a branch`_
    c) `Keeping your working branch in sync`_
    d) `Making a pull request`_

6. `Style and other notes`_


------------------------
Contributing with Issues
------------------------

There are three ways you can help with `issues <https://github.com/robofab-developers/fontParts/issues>`_.

#. **Opening an issue for discussion.** Have you hit a bug? Does something not make sense? Is there a feature you would like so see? Open an `issue <https://github.com/robotools/fontParts/issues/new>`_!

#. **Helping out figuring out issues.** If you have experience with an issue, you can contribute further test cases or domain knowledge to the discussion to help move the issue along.

#. **Fixing the issue.** Either show that the issue isn’t a problem or contribute a pull request that fixes the issue.

One can view all the issues that we’d love help with by searching for `Help Wanted <https://github.com/robofab-developers/fontParts/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_ in the issues.


-----------------------
I just have a question!
-----------------------

If you have a question about fontParts that doesn’t make sense as an issue, open a . Please read the documentation first to see if your question is answered (as the documentation is still being written, it may not be).


------------------
Contributing Tests
------------------

Oh man, thank you! Writing test cases is like kerning, sometimes it’s really soothing, sometimes it feels like it might just not end. Any test case that you want to contribute is one less that someone needs to write, so we really thank you for your interest here.

To start, you’ll see a list of all that needs to be done on the `Tests Project <https://github.com/robofab-developers/fontParts/projects/1>`_ on GitHub. Each object that needs tests has an issue where one can discuss the tests, ask questions about what should be done, and (hopefully) where you will volunteer to take ownership of writing tests for that object.

If you want to take ownership for testing an object, just say so on the issue and we’ll add you as a contributor and assign that issue to you.

Our tests are written with Python’s unittest framework, if you’ve not used it before, browsing the `documentation for unittest <https://docs.python.org/2/library/unittest.html>`_ will be helpful to understand what’s going on.

How to write tests for fontParts is covered in the fontParts documentation, in `Testing <http://fontparts.readthedocs.io/en/latest/development/testing.html>`_.

A good place to start looking to see examples for how to write the tests is in the `test_glyph.py <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/test/test_glyph.py>`_ and `test_component.py <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/test/test_component.py>`_ files.


What should I install to write tests?
-------------------------------------

Having both ``tox`` and ``coverage`` installed locally are great aids to writing tests.

`Tox <https://pypi.org/project/tox/>`_ is installed via: ::

  pip install tox

Once ``tox`` is installed, you can run the tests for fontParts by just typing ``tox`` on the command line when you are in the fontParts directory.

``tox`` is set up to test fontParts in Python 2.7, 3.5, 3.6, and PyPy. It’s likely that you don’t have all of those versions installed on your machine (looking at you pypy). Don’t worry about testing errors for python versions that aren’t installed. If you don’t have a version of Python 3 installed, you should install version 3.6. On the MacOS, it’s easiest to do via `Homebrew <https://brew.sh>`_, but whatever you are most comfortable with will likely be OK.

`Coverage <https://pypi.org/project/coverage/>`_ is installed via: ::

    pip install coverage

After installing it, run: ::

    coverage run Lib/fontParts/fontshell/test.py
    coverage html

And a folder named **htmlcov** containing a bunch of files will be created. Open the file named **index.html** in that folder. This will allow you to get an update of the coverage before you push out a commit.

You can also check if the tests run on Python 3 by using ``coverage3`` instead of ``coverage`` (the former invokes ``python3`` whereas the latter calls up ``python``).

``tox`` is also set up to run the coverage tests, so if you have Python 3.6 installed, each time you run ``tox`` it will update the **htmlcov** folder for you.

**Note:** Coverage is great for showing what lines of code may be missed, and is a good yardstick to measure your progress. However, it can’t and doesn’t know everything that may go wrong, so you will need to think about the object you are writing tests for and have a logical plan for what might go wrong & what to then test.

How do I know what tests to write?
----------------------------------

Check the `Codecov page for fontParts base <https://codecov.io/gh/robofab-developers/fontParts/tree/master/Lib/fontParts/base>`_ to see which lines of the code are still not being hit by tests.

Because the automated tests are run in ``fontshell``, a good starting point for writing tests is to get coverage to 100% on the `fontshell version <https://codecov.io/gh/robofab-developers/fontParts/tree/master/Lib/fontParts/fontshell>`_ of the object, and then determine what other tests need to be added to get 100% on the base files.

Do not worry about testing ``repr``.


--------------------------
Contributing Documentation
--------------------------

We want fontParts to have clear, easy to follow documentation. This library is aimed at working typeface designers who want to script some of their work flow. Easy to follow documentation is a big part of making that as pleasant and easy as possible.

Like Tests, there is a `Documentation <https://github.com/robofab-developers/fontParts/projects/2>`_ project on GitHub with a bunch of issues for specific things that need to be written. Each issue is where you can ask questions about writing documentation for that thing and hopefully volunteer to be in charge of writing the documentation for that issue. If you want to take ownership for writing a piece of the documentation, just say so on the issue and we’ll add you as a contributor and assign that issue to you.

There are four types of things that we need help with in the documentation:

#. **Design**. We’d love to have the standard Sphinx CSS redone. This is a great opportunity for someone who is handy with HTML/CSS. We do have a logo that is forthcoming.

#. **Writing introduction**. RoboFab had a bunch of really good introductory documentation that we want to port over.

#. **Writing object documentation**. The main part of the documentation happens in the code for each object. This is nearly done, but there are several objects that currently don’t have full documentation.

#. **Checking written documentation**. We need to double check the Object documentation that has been written to be sure what we didn’t later add a method/attribute that needs documentation.

Our documentation is written with reStructeredText markup. The `Quick reStructredText Primer <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ is a good reference to the markup style.

fontParts has a `style guide and howto <http://fontparts.readthedocs.io/en/latest/development/documenting.html>`_ for documentation, before starting please give it a read.

A good example of the Object documentation can be found in the `Glyph <https://github.com/robofab-developers/fontParts/blob/master/Lib/fontParts/base/glyph.py>`_ object.


--------------------------------
Creating a fork & a pull request
--------------------------------

Wait, “pull request”?!

Don’t worry, though it can be a bit confusing at the start, changes to the code should be made via pull requests on the GitHub repository for fontParts.

To do so, you’ll first need a GitHub account. If you don’t have one, you can
`sign up <https://github.com/join>`_ for one for free.

Creating a fork
---------------

Once you have a GitHub account, you’ll want to fork the project `on GitHub <https://github.com/robofab-developers/fontParts>`_ and then clone your fork locally. Do so on the command line with: ::

  git clone git@github.com:username/fontParts.git
  cd fontParts
  git remote add upstream https://github.com/robofab-developers/fontParts.git
  git fetch upstream

After doing this, it’s a good idea to at least install `tox <https://pypi.org/project/tox/>`_ for local testing. See “`What should I install to write tests?`_” for how to install ``tox``.

Creating a branch
-----------------

Once you have your fork set up, it’s time to make changes to the code or documentation. To do so, create a branch of the code for the work you’re about to do. This is done by typing the following on the command line. (note: **my-branch** should be a logical name for the code that you want to change) ::

  git checkout -b my-branch -t upstream/master

Make your changes, committing to your branch as things make sense. Keep your commit messages descriptive and as short as is needed to describe your changes.

Keeping your working branch in sync
-----------------------------------

As you work, it’s a good idea to “rebase” your branch after a commit to keep the bits that you aren’t changing in sync with the main repository. You do this by typing the following on the command line ::

  git fetch upstream
  git rebase upstream/master


Making a pull request
---------------------

Once you are done with your changes, you can create a pull request to merge your changes into fontParts. You do this by first pushing your working code to your fork on GitHub. This is done with (note: **my-branch** should be whatever you named your branch, not **my-branch**) ::

  git push origin my-branch

Then on GitHub you’ll open a pull request (`more info <https://help.github.com/articles/creating-a-pull-request/>`_). Please make your description of the pull request easy to understand.

You may receive feedback on your pull request. As you make changes to the code based on the feedback, after you commit those changes locally, do the following on the command line to add the new changes to your pull request and GitHub will take care of the rest. ::

  git push origin my-branch

After your pull request is accepted, you can delete your branch with ::

  git branch -d my-branch

After doing so, it’s a good idea to then pull from the main repository to be sure that you have all the updated code ::

  git pull


---------------------
Style and other notes
---------------------

The style guide and other notes about developing fontParts is found `here <http://fontparts.readthedocs.io/en/latest/development/index.html>`_ in the documentation.
