import random
import os
from vplants.weberpenn.tree_client import *
from vplants.weberpenn import tree_client
from vplants.weberpenn import tree_server
from vplants.weberpenn import tree_geom
from openalea.plantgl.all import *

viewer = Viewer
p = [Vector2(0.5, 0), Vector2(0, 0.5), Vector2(-0.5, 0), Vector2(0, -0.5),
     Vector2(0.5, 0)]
section = Polyline2D(p)

p = [tree_client.Quaking_Aspen(),
     tree_client.Black_Tupelo(),
     tree_client.Black_Oak(),
     tree_client.Weeping_Willow()]
p1, p2, p3, p4 = p


def f(param, section=section, position=Vector3(), scene=Scene()):
    # param.leaves= 0
    client = tree_client.Weber_Laws(param)
    server = tree_server.TreeServer(client)
    server.run()
    geom = tree_geom.GeomEngine(server, section, position)
    # scene= geom.scene('point', scene)
    scene = geom.scene('axis', scene)
    return scene


scenes = []
for param in p:
    param.leaves = 0
    param.order -= 1
    s = f(param, section)
    scenes.append(s)

"""
seed=range(1,10)
for s in seed:
    random.seed(s)
    i= s-1
    x,y= i/3, i%3
    scene=f(p,section,Vector3(x*5,y*5,0), scene)
    
def plot(scenes):
    for i in range(9):
        viewer.display(scenes[i])
        viewer.question("next","next")

def plot(seeds):
    for seed in seeds:
        random.seed(seed)
        viewer.display(f(p1))
        viewer.question("next","%d"%seed)

def save_shrub(seeds):
    for seed in seeds:
        random.seed(seed)
        s=f(p)
        name= "shrub_seed%d.geom"%seed
        s.save(name)
        print "File saved %s"%name

"""
"""
##############################################
def Shrub():
    shape_id= 2
    base_size= 0.1
    scale= (4,1) 
    order= 3
    ratio= 0.018
    ratio_power= 1.3
    lobes= (5,0.1)
    flare= 1.2
    base_split= 0
    n_length= [(1,0),(0.8,0.1),(0.4,0.1),(0.4,0) ]
    n_seg_split= [0.4,0.2,0.1,0]
    n_split_angle= [(10,0),(10,10),(10,10),(0,0)]
    #n_down_angle= [(40, 10), (40, 0), (10, 10)]
    n_down_angle= [(70, 10), (0, 20), (10, 10)]
    #n_curve= [(10, -5, 40, 10), (10, -5, 10, 10), (10, -10, 0, 10), (1, 0, 0, 0)]
    #n_curve= [(5,0,-10,10),(3,10,60,30),(10,10,30,150),(1,0,0,0)]
    n_curve= [(5,5,0,10),(3,-60,30,20),(10,-10,30,50),(1,0,0,0)]
    n_rotate=[(140, 0), (140, 0), (77, 0)]
    branches=[20,30,10]
    leaves= 50
    leaf_scale= 0.12
    leaf_scale_x= 0.66

    return tree_client.TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle,n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x)
p= Shrub()
scene= Scene()


def foug():
    shape_id= 0
    base_size= 0.2
    scale= (1.,0.1) 
    order= 3
    ratio= 0.02
    ratio_power= 1.1
    lobes= (5,0.07)
    flare= 0.6
    base_split= 0
    n_length= [(1,0),(0.4,0),(.3,0),(0,0) ]
    n_seg_split= []
    n_split_angle= []
    n_down_angle= [(70,1),(70,1),(0,0)]
    n_curve= [(3,10,0,20),(3,10,0,20),(3,10,0,25),(1,0,0,0)]
    n_rotate=[(180,0),(180,0),(180,0)]
    branches=[16,20,10]
    leaves= 10
    leaf_scale= 0.3
    leaf_scale_x= 1
    rotate= [0,90,90,0]

    return tree_client.TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle, n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate)
    
class Fougere(tree_client.Weber_Laws):
    def __init__(self, param):
        tree_client.Weber_Laws.__init__(self,param)

    def get_branches( self, order, nb_nodes, branching= None ):

        assert nb_nodes > 0
        
        b=[ i%2 for i in xrange(nb_nodes)]

        b[0]= 0
        b[-1]=0
        if order == 1:
            b[1]=0
        return b

    def get_leaves(self, n, axis_id):

        order= self.max_order
        
        pid= self.tree._parent[axis_id]
        offset= self.tree._properties["offset"][axis_id]

        if pid != self.prev_parent_id:
            self.prev_parent_id= pid
            self.rotate[order]= self.param.rotate[order]
        
        poly= self.tree._properties["polyline"][axis_id]
        length= self.tree._properties["length"][pid]
        length_axis= self.tree._properties["length"][axis_id]
        lengthes= self.tree._properties["offset_length"][axis_id]
        l_offset= self.tree._properties["offset_length"][pid][offset]

        ppoly= Poly( poly, length_axis, lengthes )
        pts, tgts= ppoly.points(n)

        len_child_max= value(self.param.n_length[-1])
        total_len= len_child_max *(length-0.6*l_offset)

        down= self.param.n_down_angle[-1]
        down_angle= 0

        if down[1] >= 0:
            down_angle= value(down)
        else:
            ratio= (length -l_offset) / (length * (1-self.param.base_size))
            downV= down[1]* shape_ratio(0,1-2*shape_ratio(0,ratio))
            down_angle= value( (down[0], downV) )
        
        rotate= self.param.n_rotate[-1]

        
        #r_down= axisRotation(Vector3(1,0,0),radians(angle))
        ppid= self.tree._parent[pid]
        poffset= self.tree._properties["offset"][pid]
        pl_offset= self.tree._properties["offset_length"][ppid][poffset]
        plength= self.tree._properties["length"][ppid]

        leaves= []
        for i, pt in enumerate(pts):
            ratio= (length -l_offset) / (length * (1-self.param.base_size))
            ratio*=1-pow(pl_offset/plength*(1-self.param.base_size),self.param.ratio_power)
            
            #print ratio
            tgt= tgts[i]
            
            self.rotate[order]+= value(rotate)
            self.rotate[order]= self.rotate[order] % 360
            a,e,r= radians(self.rotate[order]), radians(down_angle),angle(Vector3(0,0,1),tgt)
            euler= eulerRotationZYX(Vector3(r,e,a))
            t_parent= Matrix3(self.tree._properties["transform"][pid])

            m= t_parent*euler
            ls, ls_x= self.param.leaf_scale,self.param.leaf_scale_x
            leaves.append( Leaf(pt,m, ratio*ls,ls_x ) )

            self.rotate[order]+= value(rotate)
            self.rotate[order]= self.rotate[order] % 360
            a,e,r= radians(self.rotate[order]), radians(down_angle),angle(Vector3(0,0,1),tgt)
            euler= eulerRotationZYX(Vector3(r,e,a))
            t_parent= Matrix3(self.tree._properties["transform"][pid])

            m= t_parent*euler
            ls, ls_x= self.param.leaf_scale,self.param.leaf_scale_x
            leaves.append( Leaf(pt,m, ls*ratio,ls_x ) )
            
            
        return leaves



def fougere(p):
    return Fougere(p)

def my_leaf():
    l= tree_geom.bezier_leaf()
    leaf= AxisRotated(Vector3(0,0,1),pi/2.,l)
    leaf.name="myleaf"
    return leaf


def f( param, section=section, position= Vector3(), scene= Scene() ):
    client= fougere(param)
    server= tree_server.TreeServer(client)
    server.run()
    geom= tree_geom.GeomEngine(server,section,position,tree_geom.green, my_leaf())
    #scene= geom.scene('point', scene)
    scene= geom.scene('axis', scene)
    return scene


seeds= [15,22,24,25]
for i in range(4):
    x= i/2
    y= i%2
    pos= Vector3(20*x,20*y,0)
    random.seed(seeds[i])
    scene=f(p1,section,pos,scene)

"""
