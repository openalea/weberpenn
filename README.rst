.. contents::

==========
WeberPenn
==========

An extension of the Weber and Penn model

=============
Documentation
=============

[...]


=================================================
Installation with Miniconda (Windows, linux, OSX)
=================================================

Miniconda installation
----------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Install conda-build if not already installed
...............................................

.. code:: shell

    conda install conda-build

2. Create virtual environment and activate it
.............................................

.. code:: shell

    conda create --name weberpenn python
    source activate weberpenn

3. Install the openalea.plantgl package
................................................

.. code:: shell

    conda install -c openalea/label/unstable -c openalea vplants.plantgl openalea.visualea openalea.mtg

(Optional) Install several package managing tools :

.. code:: shell

    conda install notebook nose sphinx sphinx_rtd_theme pandoc coverage

Authors
-------

* Christophe    Pradal
