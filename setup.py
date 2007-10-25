from setuptools import setup, find_packages
import os, sys
from os.path import join as pj
 
packagename = 'weberpenn'
namespace = 'openalea'


if __name__ == '__main__':
    
    setup(name='vplants.weberpenn',
          version='0.1',
          author='C. Pradal',
          description='Implementation of the tree model published by Weber and Penn',
          url='',
          license='Cecill',
          
          namespace_packages=['openalea'],
          create_namespaces=True,

          # Packages
          packages=['openalea.weberpenn'],
          package_dir={'openalea.weberpenn' : '',
                       '' : 'build/lib', # hack to use develop command
                       },
          
          # Add package platform libraries if any
          zip_safe = False,

          # Dependencies
          install_requires = ['PlantGL'],
          dependency_links = ['http://openalea.gforge.inria.fr/pi'],
          )


    
