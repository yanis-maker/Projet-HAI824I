.. _contributing:

*********************************
Contributing to py_stringmatching
*********************************

.. contents:: Table of contents:
   :local:

This document is adapted from `pandas how to contribute guidelines <http://pandas.pydata.org/pandas-docs/stable/contributing.html>`_ for *py_stringmatching* package. 

Where to start?
===============

All contributions, bug reports, bug fixes, documentation improvements,
enhancements and ideas are welcome.

If you are simply looking to start working with the *py_stringmatching* codebase, navigate to the
`GitHub "issues" tab <https://github.com/anhaidgroup/py_stringmatching/issues>`_ and start looking through
interesting issues.

Or maybe through using *py_stringmatching* you have an idea of your own or are looking for something
in the documentation and thinking 'this can be improved'...you can do something
about it!

Feel free to ask questions on the `mailing list
<https://groups.google.com/forum/#!forum/py_stringmatching>`_

Bug reports and enhancement requests
====================================

Bug reports are an important part of making *py_stringmatching* more stable.  Having a complete bug report
will allow others to reproduce the bug and provide insight into fixing. We use GitHub issue tracker to track bugs. It is important that you provide the exact version of *py_stringmatching* where the bug is found. Trying the bug-producing code out on the *master* branch is often a worthwhile exercise to confirm the bug still exists.  It is also worth searching existing bug reports and pull requests to see if the issue has already been reported and/or fixed.

Bug reports must:

#. Include a short, self-contained Python snippet reproducing the problem.
   You can format the code nicely by using `GitHub Flavored Markdown
   <http://github.github.com/github-flavored-markdown/>`_::

      ```python
      >>> import py_stringmatching as sm
      >>> tfidf = sm.TfIdf(...)
      ...
      ```

#. Include the full version string of *py_stringmatching*. You can find the version as follows::

      >>> import py_stringmatching as sm
      >>> sm.__version__

#. Explain why the current behavior is wrong/not desired and what you expect instead.

The issue will then show up to the *py_stringmatching* community and be open to comments/ideas from others.

Working with the code
=====================

Now that you have an issue you want to fix, enhancement to add, or documentation to improve,
you need to learn how to work with GitHub and the *py_stringmatching* code base.

Version control, Git, and GitHub
--------------------------------

To the new user, working with Git is one of the more daunting aspects of contributing to *py_stringmatching*.
It can very quickly become overwhelming, but sticking to the guidelines below will help keep the process
straightforward and mostly trouble free.  As always, if you are having difficulties please
feel free to ask for help.

The code is hosted on `GitHub <https://www.github.com/anhaidgroup/py_stringmatching>`_. To
contribute you will need to sign up for a `free GitHub account
<https://github.com/signup/free>`_. We use `Git <http://git-scm.com/>`_ for
version control to allow many people to work together on the project.

Some great resources for learning Git:

* the `GitHub help pages <http://help.github.com/>`_.
* the `NumPy's documentation <http://docs.scipy.org/doc/numpy/dev/index.html>`_.
* Matthew Brett's `Pydagogue <http://matthew-brett.github.com/pydagogue/>`_.

Getting started with Git
------------------------

`GitHub has instructions <http://help.github.com/set-up-git-redirect>`__ for installing git,
setting up your SSH key, and configuring git.  All these steps need to be completed before
you can work seamlessly between your local repository and GitHub.

.. _contributing.forking:

Forking
-------

You will need your own fork to work on the code. Go to the `py_stringmatching project
page <https://github.com/anhaidgroup/py_stringmatching>`_ and hit the ``Fork`` button. You will
want to clone your fork to your machine::

    git clone git@github.com:<your-user-name>/py_stringmatching.git <local-repo-name>
    cd <local-repo-name>
    git remote add upstream git://github.com/anhaidgroup/py_stringmatching.git

This creates the directory `local-repo-name` and connects your repository to
the upstream (main project) *py_stringmatching* repository.

The testing suite will run automatically on Travis-CI once your pull request is
submitted.  However, if you wish to run the test suite on a branch prior to
submitting the pull request, then Travis-CI needs to be hooked up to your
GitHub repository.  Instructions for doing so are `here
<http://about.travis-ci.org/docs/user/getting-started/>`__.

Creating a branch
-----------------

You want your master branch to reflect only production-ready code, so create a
feature branch for making your changes. For example::

    git branch new_feature
    git checkout new_feature

The above can be simplified to::

    git checkout -b new_feature

This changes your working directory to the *new_feature* branch.  Keep any
changes in this branch specific to one bug or feature so it is clear
what the branch brings to *py_stringmatching*. You can have many new features
and switch in between them using the git checkout command.

To update this branch, you need to retrieve the changes from the master branch::

    git fetch upstream
    git rebase upstream/master

This will replay your commits on top of the lastest py_stringmatching git master.  If this
leads to merge conflicts, you must resolve them before submitting your pull
request.  If you have uncommitted changes, you will need to ``stash`` them prior
to updating.  This will effectively store your changes and they can be reapplied
after updating.

.. _contributing.dev_env:

Creating a development environment
----------------------------------

An easy way to create a *py_stringmatching* development environment is as follows.

- Install either :ref:`Anaconda <install.anaconda>` or :ref:`miniconda <install.miniconda>`
- Make sure that you have :ref:`cloned the repository <contributing.forking>`
- ``cd`` to the *py_stringmatching* source directory

Tell conda to create a new environment, named ``py_stringmatching_dev``, or any other name you would like
for this environment, by running::

      conda create -n py_stringmatching_dev --file build_tools/requirements_dev.txt


For a python 3 environment::

      conda create -n py_stringmatching_dev python=3 --file build_tools/requirements_dev.txt

.. warning::

   If you are on Windows, see :ref:`here for a fully compliant Windows environment <contributing.windows>`.

This will create the new environment, and not touch any of your existing environments,
nor any existing python installation. It will install all of the basic dependencies of
*py_stringmatching*, as well as the development and testing tools. If you would like to install
other dependencies, you can install them as follows::

      conda install -n py_stringmatching_dev numpy

.. To install *all* py_stringmatching dependencies you can do the following::

..     conda install -n py_stringmatching_dev --file build_tools/requirements_all.txt

To work in this environment, Windows users should ``activate`` it as follows::

      activate py_stringmatching_dev

Mac OSX / Linux users should use::

      source activate py_stringmatching_dev

You will then see a confirmation message to indicate you are in the new development environment.

To view your environments::

      conda info -e

To return to your home root environment in Windows::

      deactivate

To return to your home root environment in OSX / Linux::

      source deactivate

See the full conda docs `here <http://conda.pydata.org/docs>`__.

At this point you can easily do an *in-place* install, as detailed in the next section.

.. _contributing.windows:

Creating a Windows development environment
------------------------------------------

To build on Windows, you need to have compilers installed to build the extensions. You will need to install the appropriate Visual Studio compilers; the most recent is VS 2019.

To obtain VS 2019, you can download and install the `Visual Studio 2019 Community Edition <https://visualstudio.microsoft.com/downloads/>`__.

Here are some references and blogs:

- https://blogs.msdn.microsoft.com/pythonengineering/2016/04/11/unable-to-find-vcvarsall-bat/
- https://github.com/conda/conda-recipes/wiki/Building-from-Source-on-Windows-32-bit-and-64-bit
- https://cowboyprogrammer.org/building-python-wheels-for-windows/
- https://blog.ionelmc.ro/2014/12/21/compiling-python-extensions-on-windows/
- https://support.enthought.com/hc/en-us/articles/204469260-Building-Python-extensions-with-Canopy

.. _contributing.getting_source:

Making changes
--------------

Before making your code changes, it is often necessary to build the code that was
just checked out. Specifically, you need build the C extensions in-place by running::

      python setup.py build_ext --inplace

If you startup the Python interpreter in the *py_stringmatching* source directory you will call the built C extensions.

.. _contributing.documentation:

Contributing to the documentation
=================================

If you're not the developer type, contributing to the documentation is still
of huge value. You don't even have to be an expert on
*py_stringmatching* to do so! Something as simple as rewriting small passages for clarity
as you reference the docs is a simple but effective way to contribute. The
next person to read that passage will be in your debt!

In fact, there are sections of the docs that are worse off after being written
by experts. If something in the docs doesn't make sense to you, updating the
relevant section after you figure it out is a simple way to ensure it will
help the next person.

.. contents:: Documentation:
   :local:


About the *py_stringmatching* documentation
-------------------------------------------

The documentation is written in **reStructuredText**, which is almost like writing
in plain English, and built using `Sphinx <http://sphinx.pocoo.org/>`__. The
Sphinx Documentation has an excellent `introduction to reST
<http://sphinx.pocoo.org/rest.html>`__. Review the Sphinx docs to perform more
complex changes to the documentation as well.

Some other important things to know about the docs:

- The *py_stringmatching* documentation consists of two parts: the docstrings in the code
  itself and the docs in this folder ``py_stringmatching/docs/``.

  The docstrings provide a clear explanation of the usage of the individual
  functions, while the documentation in this folder consists of tutorial-like
  overviews per topic together with some other information (what's new,
  installation, etc).

- The docstrings follow the **Google Docstring Standard**. This standard specifies the format of
  the different sections of the docstring. See `this document
  <http://www.sphinx-doc.org/en/stable/ext/example_google.html>`_
  for a detailed explanation, or look at some of the existing functions to
  extend it in a similar manner.

- The tutorial makes use of the `ipython directive
  <http://matplotlib.org/sampledoc/ipython_directive.html>`_ sphinx extension.
  This directive lets you put code in the documentation which will be run
  during the doc build. For example::

      .. ipython:: python

          x = 2
          x**3

  will be rendered as::

      In [1]: x = 2

      In [2]: x**3
      Out[2]: 8

  Almost all code examples in the docs are run (and the output saved) during the
  doc build. This approach means that code examples will always be up to date,
  but it does make the doc building a bit more complex.


How to build the *py_stringmatching* documentation
---------------------------------------------------

Requirements
~~~~~~~~~~~~

To build the *py_stringmatching* docs there are some extra requirements: you will need to
have ``sphinx`` and ``ipython`` installed.

It is easiest to :ref:`create a development environment <contributing.dev_env>`, then install::

      conda install -n py_stringmatching_dev sphinx sphinx_rtd_theme ipython

Building the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

So how do you build the docs? Navigate to your local
``py_stringmatching/docs/`` directory in the console and run::

    make html

Then you can find the HTML output in the folder ``py_stringmatching/docs/_build/html/``.

If you want to do a full clean build, do::

    make clean html


.. _contributing.dev_docs:


Contributing to the code base
=============================

.. contents:: Code Base:
   :local:

Code standards
--------------
*py_stringmatching* follows `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_.

Please try to maintain backward compatibility. *py_stringmatching* has lots of users with lots of
existing code, so don't break it if at all possible.  If you think breakage is required,
clearly state why as part of the pull request.  Also, be careful when changing method
signatures and add deprecation warnings where needed.

Writing tests
-------------
Adding tests is one of the most common requests after code is pushed to *py_stringmatching*.  Therefore,
it is worth getting in the habit of writing tests ahead of time so this is never an issue.

Unit testing
~~~~~~~~~~~~~
Like many packages, *py_stringmatching* uses the `standard ``unittest``
testing library <https://docs.python.org/3/library/unittest.html>`_.

All tests should go into the ``tests`` subdirectory of the specific package.
This folder contains many current examples of tests, and we suggest looking to these for
inspiration.

The tests can then be run directly inside your Git clone (without having to
install *py_stringmatching*) by typing::

    python3 -m unittest


Performance testing
~~~~~~~~~~~~~~~~~~~
Performance matters and it is worth considering whether your code has introduced
performance regressions.  *py_stringmatching* uses
`asv <https://github.com/spacetelescope/asv>`_ for performance testing.
The benchmark test cases are all found in the ``benchmarks`` directory.  asv
supports both python2 and python3.

To install asv::

    pip install git+https://github.com/spacetelescope/asv

If you need to run a benchmark, run the following from your clone directory::

    asv run

This command uses ``conda`` by default for creating the benchmark environments.

Information on how to write a benchmark and how to use asv can be found in the
`asv documentation <http://asv.readthedocs.org/en/latest/writing_benchmarks.html>`_.


Contributing your changes to *py_stringmatching*
================================================

Committing your code
--------------------

Finally, commit your changes to your local repository with an explanatory message.

The following defines how a commit message should be structured.  Please reference the
relevant GitHub issues in your commit message using GH1234 or #1234.  Either style
is fine, but the former is generally preferred:

    * a subject line with `< 80` chars.
    * One blank line.
    * Optionally, a commit message body.

Now you can commit your changes in your local repository::

    git commit -m

Combining commits
-----------------

If you have multiple commits, you may want to combine them into one commit, often
referred to as "squashing" or "rebasing".  This is a common request by package maintainers
when submitting a pull request as it maintains a more compact commit history.  To rebase
your commits::

    git rebase -i HEAD~#

Where # is the number of commits you want to combine.  Then you can pick the relevant
commit message and discard others.

To squash to the master branch do::

    git rebase -i master

Use the ``s`` option on a commit to ``squash``, meaning to keep the commit messages,
or ``f`` to ``fixup``, meaning to merge the commit messages.

Then you will need to push the branch (see below) forcefully to replace the current
commits with the new ones::

    git push origin new_feature -f


Pushing your changes
--------------------

When you want your changes to appear publicly on your GitHub page, push your
forked feature branch's commits::

    git push origin new_feature

Here ``origin`` is the default name given to your remote repository on GitHub.
You can see the remote repositories::

    git remote -v

If you added the upstream repository as described above you will see something
like::

    origin  git@github.com:<yourname>/py_stringmatching.git (fetch)
    origin  git@github.com:<yourname>/py_stringmatching.git (push)
    upstream        git://github.com/anhaidgroup/py_stringmatching.git (fetch)
    upstream        git://github.com/anhaidgroup/py_stringmatching.git (push)

Now your code is on GitHub, but it is not yet a part of the *py_stringmatching* project.  For that to
happen, a pull request needs to be submitted on GitHub.

Review your code
----------------

When you're ready to ask for a code review, file a pull request. Before you do, once
again make sure that you have followed all the guidelines outlined in this document
regarding code style, tests, performance tests, and documentation. You should also
double check your branch changes against the branch it was based on:

#. Navigate to your repository on GitHub -- https://github.com/<your-user-name>/py_stringmatching
#. Click on ``Branches``
#. Click on the ``Compare`` button for your feature branch
#. Select the ``base`` and ``compare`` branches, if necessary. This will be ``master`` and
   ``new_feature``, respectively.

Finally, make the pull request
------------------------------

If everything looks good, you are ready to make a pull request.  A pull request is how
code from a local repository becomes available to the GitHub community and can be looked
at and eventually merged into the master version.  This pull request and its associated
changes will eventually be committed to the master branch and available in the next
release.  To submit a pull request:

#. Navigate to your repository on GitHub
#. Click on the ``Pull Request`` button
#. You can then click on ``Commits`` and ``Files Changed`` to make sure everything looks
   okay one last time
#. Write a description of your changes.
#. Click ``Send Pull Request``.

This request then goes to the repository maintainers, and they will review
the code. If you need to make more changes, you can make them in
your branch, push them to GitHub, and the pull request will be automatically
updated.  Pushing them to GitHub again is done by::

    git push -f origin new_feature

This will automatically update your pull request with the latest code and restart the
Travis-CI tests.

Delete your merged branch (optional)
------------------------------------

Once your feature branch is accepted into upstream, you'll probably want to get rid of
the branch. First, merge upstream master into your branch so git knows it is safe to
delete your branch::

    git fetch upstream
    git checkout master
    git merge upstream/master

Then you can just do::

    git branch -d new_feature

Make sure you use a lower-case ``-d``, or else git won't warn you if your feature
branch has not actually been merged.

The branch will still exist on GitHub, so to delete it there do::

    git push origin --delete new_feature
