# -*- coding: utf-8 -*-
__revision__ = "$Id$"

from setuptools import setup, find_packages
import os, sys
from os.path import join as pj


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)

for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

if __name__ == '__main__':

    setup(name=name,
          version=version,
          author=authors,
          description=description,
          url=url,
          license=license,

          namespace_packages=['vplants'],
          create_namespaces=True,

          # Packages
          packages=['openalea', 'openalea.weberpenn',
                    'vplants.weberpenn',
                    'vplants.weberpenn.wralea',
                    'vplants.weberpenn.demo'],

          package_dir={'vplants.weberpenn' : 'src/weberpenn',
                       '' : 'src', # hack to use develop command
                       },

          # Add package platform libraries if any
          zip_safe = False,

          # Add package platform libraries if any
          include_package_data=True,
          package_data = {'' : [ '*.png'],},

          # Dependencies
          install_requires = ['vplants.plantgl'],
          dependency_links = ['http://openalea.gforge.inria.fr/pi'],

          # entry_points
          entry_points = {
            "wralea": ["weberpenn = vplants.weberpenn.wralea",
                       "demo = vplants.weberpenn.demo",
                       ]
            },
          )
