from openalea.core import *
 
__name__ = "vplants.weberpenn"
__version__ = '0.1.5'
__license__ = 'CECILL'
__authors__ = 'C. Pradal'
__institutes__ = 'CIRAD/INRIA'
__description__ = 'Construction of geometric tree models from parameters described in Weber and Penn 95.'
__url__ = 'http://openalea.gforge.inria.fr'
 
__editable__ = 'False' 
__icon__ = 'icon.png' 
__alias__ = ["WeberPenn"] # Aliases for compatibitity

__all__ = """
global_param
order_param
tree_param
quaking_aspen
black_tupelo
black_oak
weeping_willow
weber_penn
weber_penn_markov
weber_penn_mtg
species
read_arbaro
""".split()


global_param = Factory(name='global parameters', 
                 description='Global parameters of the weber and Penn model', 
                 category='Simulation', 
                 nodemodule='trunk_parameters',
                 nodeclass='global_parameters',
                 )

order_param = Factory(name='order parameters', 
                   description='Set of parameters for each tree order of the weber and Penn model', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='order_parameters',
                   )

tree_param = Factory(name='tree parameters', 
                   description='Set of parameters of weber and penn model.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='tree_parameters',
                   )

quaking_aspen = Factory(name='quaking aspen', 
                   description='Quaking Aspen parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='quaking_aspen',
                   )

black_tupelo = Factory(name='black tupelo', 
                   description='Black Tupelo parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='black_tupelo',
                   )

black_oak = Factory(name='black oak', 
                   description='Black Oak parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='black_oak',
                   )

weeping_willow = Factory(name='weeping willow', 
                   description='Weeping Willow parameters', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weeping_willow',
                   )

weber_penn = Factory(name='weber and penn', 
                   description='Tree generation from parameters.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn',
                   )

weber_penn_markov = Factory(name='weber and penn (markov)', 
                   description='Tree generation from parameters.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn_markov',
                   )

weber_penn_mtg = Factory(name='weber and penn (mtg)', 
                   description='Geometric solver using Weber and Penn parameters on MTG.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='weber_penn_mtg',
                   )

species = Factory(name='species', 
                   description='Tree parameters for the Weber and Penn model.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='Species',
                   )

read_arbaro = Factory(name='read arbaro xml', 
                   description='Import weber and penn parameters from Arbaro software.', 
                   category='Simulation', 
                   nodemodule='trunk_parameters',
                   nodeclass='import_arbaro',
                   inputs = [dict(name='filename', interface=IFileStr('*.xml')),],
                   )



