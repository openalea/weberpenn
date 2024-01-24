# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages
import os, sys
from os.path import join as pj

name = 'OpenAlea.Weberpenn'
pkg_name = 'openalea.weberpenn'
description = 'Implementation of the tree model published by Weber and Penn'
long_description= 'Implementation of the tree model published by Weber and Penn'
authors = 'Christophe Pradal'
authors_email = 'christophe.pradal@cirad.fr'
url = 'https://github.com/openalea/weberpenn'
license='Cecill-C'

_version = {}
with open("src/openalea/weberpenn/version.py") as fp:
    exec(fp.read(), _version)
version = _version["__version__"]

namespace = 'openalea'
packages=find_namespace_packages(where='src', include=['openalea.*'])
package_dir={'': 'src'}

if __name__ == '__main__':

    setup(name=name,
          version=version,
          author=authors,
          description=description,
          url=url,
          license=license,

          # Packages
          packages=packages,

          package_dir=package_dir,

          # Add package platform libraries if any
          zip_safe = False,

          # Add package platform libraries if any
          include_package_data=True,
          package_data = {'' : [ '*.png'],},

          # Dependencies
          setup_requires = ['openalea.deploy'],

          # entry_points
          entry_points = {
            "wralea": ["weberpenn = openalea.weberpenn.wralea",
                       "demo = openalea.weberpenn.demo",
                       ]
            },
          )
