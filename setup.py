# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, sys
from os.path import join as pj


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

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
          create_namespaces=True,

          # Packages
          packages=packages,

          package_dir=package_dir,

          # Add package platform libraries if any
          zip_safe = False,

          # Add package platform libraries if any
          include_package_data=True,
          package_data = {'' : [ '*.png'],},

          # Dependencies
          install_requires = [],
          dependency_links = ['http://openalea.gforge.inria.fr/pi'],

          # entry_points
          entry_points = {
            "wralea": ["weberpenn = openalea.weberpenn.wralea",
                       "demo = openalea.weberpenn.demo",
                       ]
            },
          )
