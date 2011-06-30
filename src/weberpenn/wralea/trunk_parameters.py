import random

from openalea.core import *

from openalea.weberpenn.tree_client import *
from openalea.weberpenn.mtg_client import Weber_MTG
import openalea.weberpenn.tree_server as tree_server
import openalea.weberpenn.tree_geom as tree_geom
import openalea.plantgl.all as pgl
from openalea.mtg.io import read_mtg_file

class WeberPennError(Exception):
    pass

class global_parameters(Node):
    shapes = {"0 - Conical":0,  
              "1 - Spherical":1, 
              "2 - Hemispherical":2, 
              "3 - Cylindrical":3,
              "4 - Tapered cylindrical" :4, 
              "5 - Flame":5,
              "6 - Inverse Conical":6,
              "7 - Tend Flame":7, 
             }

    def __init__(self):
        
        Node.__init__(self)

        shape_ids= self.shapes.keys()
        shape_ids.sort()
        
        inputs=[ {'interface': IEnumStr(shape_ids), 'name': 'shape_id', 'value': '0 - Conical'}, 
                 {'interface': IFloat(0.,1.,step=0.1), 'name': 'base_size', 'value': 0.1},
                 {'interface': IFloat, 'name': 'scale', 'value': 1},
                 {'interface': IFloat, 'name': 'scale_variance', 'value': 0.,'hide':True}, 
                 {'interface': IInt(min=0,max=4), 'name': 'order', 'value': 0}, 
                 {'interface': IFloat(max=1., step=0.01), 'name': 'ratio', 'value': 0.01}, 
                 {'interface': IFloat(min=0., step=0.01), 'name': 'ratio_power', 'value': 1}, 
                 {'interface': IInt(min=0), 'name': 'leaves', 'value': 0}, 
                 {'interface': IFloat, 'name': 'leaf_scale', 'value': 1.}, 
                 {'interface': IFloat, 'name': 'leaf_scale_x', 'value': 1.,'hide':True}, 
                 {'interface': IFloat, 'name': 'lobes', 'value': None,'hide':True}, 
                 {'interface': IFloat, 'name': 'lobes_variance', 'value': None,'hide':True}, 
                 {'interface': IFloat, 'name': 'flare', 'value': None,'hide':True}, 
                 {'interface': IInt, 'name': 'base_split', 'value': 0,'hide':True}]
        [self.add_input(**kwds) for kwds in inputs]
        self.add_output(name='trunk_params')


    def __call__(self, (shape_id, 
                       base_size, 
                       scale, 
                       scale_variance, 
                       order, 
                       ratio, 
                       ratio_power, 
                       leaves, 
                       leaf_scale, 
                       leaf_scale_x, 
                       lobes, 
                       lobes_variance, 
                       flare, 
                       base_split)):
        "Build trunk and global parameters."
        shape_id = self.shapes[shape_id]
        
        return dict((('shape_id', shape_id), 
                    ('base_size', base_size), 
                    ('scale', scale), 
                    ('scale_variance', scale_variance), 
                    ('order', order), 
                    ('ratio', ratio), 
                    ('ratio_power', ratio_power), 
                    ('leaves', leaves), 
                    ('leaf_scale',  leaf_scale), 
                    ('leaf_scale_x',  leaf_scale_x), 
                    ('lobes', lobes), 
                    ('lobes_variance', lobes_variance), 
                    ('flare', flare), 
                    ('base_split', base_split))), 

def order_parameters(length=1.,  length_variance=0.,  
                     curve_res=3,  curve=0.,  curve_variance=0.,  curve_back= 0., 
                     seg_split=0.,  split_angle=0.,  split_angle_variance=0., 
                     down_angle=0.,  down_angle_variance=0., 
                     rotate=0.,  rotate_variance=0.,  branches=5):    
    return dict( length=length,  
                 length_variance=length_variance,  
                 curve_res=curve_res,  
                 curve=curve,  
                 curve_variance=curve_variance,  
                 curve_back= curve_back, 
                 seg_split=seg_split,  
                 split_angle=split_angle,  
                 split_angle_variance=split_angle_variance, 
                 down_angle=down_angle,  
                 down_angle_variance=down_angle_variance, 
                 rotate=rotate,  
                 rotate_variance=rotate_variance,  
                 branches=branches), 

def update_params(local_order, 
                              n_length,  
                              n_seg_split,  
                              n_split_angle,  
                              n_down_angle,  
                              n_curve,  
                              n_rotate,  
                              branches):
    if local_order:
        n_length += [(local_order['length'],  local_order['length_variance'])]
        n_seg_split += [local_order['seg_split']]
        n_split_angle += [(local_order['split_angle'], local_order['split_angle_variance'])]
        n_down_angle += [(local_order['down_angle'], 
                          local_order['down_angle_variance'])]
        n_curve += [(local_order['curve_res'],  
                     local_order['curve'], 
                     local_order['curve_variance'],  
                     local_order['curve_back'])]
        n_rotate += [(local_order['rotate'],  local_order['rotate_variance'])]
        branches += [local_order['branches']]

def tree_parameters(global_params, order0,  order1,  order2,  order3 ):    
    gp = global_params
    if gp is None or order0 is None:
        return 
    
    shape_id = gp['shape_id']
    base_size = gp['base_size']
    scale = (gp['scale'],  gp['scale_variance'])
    order = gp['order']
    leaves = gp['leaves']
    if order >= 4:
        if not leaves:
            order = 3
        else:
            order = 4
    if order == 3 and order3 is None:
        order=2
    if order == 2 and order2 is None:
        order = 1
    if order == 1 and order1 is None:
        order = 0
    
    ratio = gp['ratio']
    ratio_power = gp['ratio_power']
    lobes = (gp['lobes'],  gp['lobes_variance'])
    flare = gp['flare']
    base_split = gp['base_split']
    leaf_scale = gp['leaf_scale']
    leaf_scale_x = gp['leaf_scale_x']
    rotate = [0]*(order+1)
    
    n_length = []
    n_seg_split = []
    n_split_angle = []
    n_down_angle = []
    n_curve = []
    n_rotate = []
    branches = []
    update_params(order0, n_length, n_seg_split, n_split_angle,  n_down_angle,  n_curve,  n_rotate,  branches)
    update_params(order1, n_length, n_seg_split, n_split_angle,  n_down_angle,  n_curve,  n_rotate,  branches)
    update_params(order2, n_length, n_seg_split, n_split_angle,  n_down_angle,  n_curve,  n_rotate,  branches)
    update_params(order3, n_length, n_seg_split, n_split_angle,  n_down_angle,  n_curve,  n_rotate,  branches)

    return TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle,n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate), 

class Species(Node):
    trees = {'Quaking Aspen' : Quaking_Aspen,
             'Black Tupelo' : Black_Tupelo,
             'Black Oak' : Black_Oak}

    def __init__( self ):
        Node.__init__(self)
        _species = self.trees.keys()
        _species.sort()
        
        self.add_input(name='species', interface=IEnumStr(_species), value = 'Black Tupelo' )
        self.add_output(name='trunk_params')
        
    def __call__( self, (t,) ):
        if t:
            return self.trees[t](),

def quaking_aspen():
    return Quaking_Aspen(), 
    
def black_tupelo():
    return Black_Tupelo(), 
    
def black_oak():
    return Black_Oak(), 
    
def weeping_willow():
    return Weeping_Willow()

def weber_penn(parameters, seed, position):
    if not parameters:
        return
    
    random.seed(seed)

    scene = Scene()
    client= Weber_Laws(parameters)
    server= tree_server.TreeServer(client)
    server.run()
    if not position:
        position = pgl.Vector3(0., 0., 0.)
    Vector2 = pgl.Vector2
    p= [Vector2(0.5,0), Vector2( 0,0.5), 
         Vector2(-0.5,0),Vector2(0,-0.5),Vector2(0.5,0)]
    section= pgl.Polyline2D(p)
    
    geom= tree_geom.GeomEngine(server,section,position)
    
    scene= geom.scene('axis', scene)
    
    return scene,

def weber_penn_markov(parameters, seed, position, p0, p1):
    if not parameters:
        return
    
    random.seed(seed)

    scene = Scene()
    client= Markov_Laws(parameters, p0, p1)
    server= tree_server.TreeServer(client)
    server.run()
    if not position:
        position = pgl.Vector3(0., 0., 0.)
    Vector2 = pgl.Vector2
    p= [Vector2(0.5,0), Vector2( 0,0.5), 
         Vector2(-0.5,0),Vector2(0,-0.5),Vector2(0.5,0)]
    section= pgl.Polyline2D(p)
    
    geom= tree_geom.GeomEngine(server,section,position)
    
    scene= geom.scene('axis', scene)
    
    return scene,

def weber_penn_mtg(mtg_file, parameters, seed, position):
    if not parameters or not mtg_file:
        raise WeberPennError("Unable to run the Weber and Penn model without parameters.")
    
    random.seed(seed)

    if isinstance(mtg_file, str):
        g = read_mtg_file(mtg_file)
    else:
        g = mtg_file

    client= Weber_MTG(parameters, g)
    client.run()

    scene = client.plot()
    return scene,

def import_arbaro( filename):
    import openalea.weberpenn.io as io
    if filename:
        return io.read_arbaro_xml(filename)


