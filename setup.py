from setuptools import setup, find_packages
import os, sys
from os.path import join as pj
 
packagename = 'weberpenn'
namespace = 'vplants'


if __name__ == '__main__':
    
    setup(name='VPlants.Weberpenn',
          version='0.6.3',
          author='C. Pradal',
          description='Implementation of the tree model published by Weber and Penn',
          url='',
          license='Cecill',
          
          namespace_packages=['vplants'],
          create_namespaces=True,

          # Packages
          packages=['openalea.weberpenn',
                    'vplants.weberpenn',
                    'vplants.weberpenn.wralea',
                    'vplants.weberpenn.demo'],

          package_dir={'vplants.weberpenn' : 'src/weberpenn',
                       '' : 'src', # hack to use develop command
                       },
          
          # Add package platform libraries if any
          zip_safe = False,

          # Dependencies
          install_requires = ['vplants.plantgl'],
          dependency_links = ['http://openalea.gforge.inria.fr/pi'],

          # entry_points
          entry_points = {
            "vplants.weberpenn": ["weberpenn = openalea.weberpenn.wralea",
                       "demo = openalea.weberpenn.demo",
                       ]
            },

          )


    
