A Mini Python Project
=====================

Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 20. Example 1.

This example shows some of the directory structure of a larger Python project.

The tests can be run as follows::

    PYTHONPATH=Chapter_20/src pytest Chapter_20

The documentation can be built as follows::

    cd docs
    PYTHONPATH=../src make html
