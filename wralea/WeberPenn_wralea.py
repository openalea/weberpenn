
from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = { 'description' :  'Construction of geometric models of trees from parameters', 
    'license': 'CECILL', 
    'url': '', 
    'version': '0.1.0', 
    'authors': 'C. Pradal', 
    'institutes': 'CIRAD'} 
    
    pkg = UserPackage("WeberPenn", metainfo)

    

    nf = Factory(name='global parameters', 
                 description='Global parameters of the weber and Penn model', 
                 category='Simulation', 
                 nodemodule='trunk_parameters',
                 nodeclass='global_parameters',
                 )

    pkg.add_factory( nf )

    nf = Factory(name='order parameters', 
                   description='Set of parameters for each tree order of the weber and Penn model', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='order_parameters',
                   )

    pkg.add_factory( nf )
    
 
    nf = Factory(name='tree parameters', 
                   description='Set of parameters of weber and penn model.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='tree_parameters',
                   )

    pkg.add_factory( nf )
    nf = Factory(name='quaking aspen', 
                   description='Quaking Aspen parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='quaking_aspen',
                   )

    pkg.add_factory( nf )
    nf = Factory(name='black tupelo', 
                   description='Black Tupelo parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='black_tupelo',
                   )

    pkg.add_factory( nf )
    nf = Factory(name='black oak', 
                   description='Black Oak parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='black_oak',
                   )

    pkg.add_factory( nf )
    nf = Factory(name='weeping willow', 
                   description='Weeping Willow parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weeping_willow',
                   )

    pkg.add_factory( nf )
    
    nf = Factory(name='weber and penn', 
                   description='Tree generation from parameters.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn',
                   )

    pkg.add_factory( nf )

    nf = Factory(name='species', 
                   description='Tree parameters for the Weber and Penn model.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='Species',
                   )

    pkg.add_factory( nf )

    nf = Factory(name='read arbaro xml', 
                   description='Import weber and penn parameters from Arbaro software.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='import_arbaro',
                   inputs = [dict(name='filename', interface=IFileStr('*.xml')),],
                   )

    pkg.add_factory( nf )
    pkgmanager.add_package(pkg)
    



