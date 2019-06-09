# About

This is Hyde, a web UX for the Gkeyll code. The goal of the project is
to provide a web-drive UX for Gkeyll that allows editing input files,
running code, doing viz and maintaining notes. Also provided are a
source code browser.

# Documentation

Documentation is available at [ReadTheDocs](http://gkeyll.rtfd.io).

# Dependencies and Installation

Hyde requires the following packages:

 * postgkyl
 * flask
 * zeromq
 * redis

You can install Hyder directly through Conda (all dependencies will be
downloaded and installed automatically):

~~~~~~~
conda install -c gkyl hyde
~~~~~~~

Conda package manager can be obtained ether through the full
[Anaconda](https://www.continuum.io/downloads) distribution or the
lightweight [Miniconda](https://conda.io/miniconda.html)

# License

See [Gkyl License](http://gkyl.readthedocs.io/en/latest/license.html) for usage conditions.

# Developer guidelines

* Since Python 3 has now all the vital parts Hyde only works with
  Python 3.

* Hyde loosely follow the Python style conventions in PEP 8. Python
  package `pep8` provides a useful
  [tool](https://pypi.python.org/pypi/pep8) to check the code. One
  exceptions the usage of camelNames instead of underscore_names.

