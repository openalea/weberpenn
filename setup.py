# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
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

namespace = 'openalea'
packages=find_packages('src')
package_dir={'': 'src'}

if __name__ == '__main__':

    setup(name=name,
          version=version,
          author=authors,
          description=description,
          url=url,
          license=license,

          namespace_packages=[namespace],

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
