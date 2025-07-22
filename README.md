# Package Name
[![Docs](https://readthedocs.org/projects/weberpenn/badge/?version=latest)](https://weberpenn.readthedocs.io/)
[![Build Status](https://github.com/openalea/weberpenn/actions/workflows/conda-package-build.yml/badge.svg?branch=master)](https://github.com/openalea/weberpenn/actions/workflows/conda-package-build.yml?query=branch%3Amaster)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License--CeCILL-C-blue)](https://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/weberpenn/badges/version.svg)](https://anaconda.org/openalea3/weberpenn)
## Description

# WeberPenn

An extension of the Weber and Penn model

# Tutorial

see visualea tutorial on [https://openalea.readthedocs.io/en/latest/tutorials/visualea/weberpenn.html#](https://openalea.readthedocs.io/en/latest/tutorials/visualea/weberpenn.html#)

# Installation with Miniconda (Windows, linux, OSX)

## Miniconda installation

Follow official website instruction to install miniconda :

<http://conda.pydata.org/miniconda.html>

### 1. Create a conda environment and activate it


# for user
```commandline
mamba create -n myenv -c openalea3 -c conda-forge openalea.weberpenn
```

# for developer, in an existing environment
```shell
git clone https://github.com/openalea/weberpenn.git
cd weberpenn
mamba install --only-deps -c openalea3 -c conda-forge openalea.weberpenn
pip install -e .[options]
```
[options] is optional, and allows to install additional dependencies 
defined in the [project.optional-dependencies] section of your 
pyproject.toml file (usually "dev", or "doc", ...)

For maintainer that need clean isolated env, or to start development (i.e. before first build)

```commandline
mamba env create -f ./conda/environment.yml
```

## Authors

-   Christophe Pradal
