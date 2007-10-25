"""
  Simulation client.
  The client
  
  Author: Christophe Pradal (christophe.pradal@cirad.fr)
"""

from openalea.plantgl.all import *
import openalea.plantgl.all as PlantGL
from  openalea.plantgl.all import Vector3, Point3Array, Polyline, Translation, axisRotation, \
     Matrix3, Matrix4, Transform4,Index3Array,Index3, TriangleSet, \
     eulerRotationZYX,eulerRotationXYZ, angle
from random import randint, uniform
from math import degrees, radians, sin, pi
import random
from markov import Markov

debug=0

class Tree(object):
    """
    Tree data structure
    """
    def __init__(self):

        # id
        self.root= 0
        self._node_id= 0
        self._axis_id= 0
        
        # axis -> node
        self._parent= {}
        #self._axis= {}

        # node -> axis
        self._children= {}

        # node -> offset in axis
        #self._offset= {}

        # axis property ( order, polyline, radius, transform)
        self._properties= { "order" : {},
                            "polyline" : {},
                            "radius" : {},
                            "offset" : {},
                            "length" : {},
                            "offset_length":{},
                            "transform":{}}

        self._order_axes= {}
        self.leaves= []

    def axes( self, order ):
        return self._order_axes[order]
    
    def axis_id( self ):
        self._axis_id+= 1
        return self._axis_id

    def node_id(self):
        self._node_id+= 1
        return self._node_id

    def __str__(self):
        s= "parent: %s\n"%str(self._parent)
        s+= "children: %s\n"% str(self._children)
        s+= "properties: %s\n"% str(self._properties)
        s+= "nb axis: %i\n"% self._axis_id
        s+= "nb nodes: %i\n"% self._node_id

        return s

##############################################################################

class Axis(object):
    
    def __init__( self, parent, offset, nodes,
                  total_length, length, radius, curvature, transform ):
        self.parent= parent
        self.offset= offset
        self.nodes= nodes
        self.total_length= total_length
        self.length= length
        self.radius= radius
        self.curvature= curvature
        self.transform= transform
        self.polyline= None
        if not transform:
            self.transform=Matrix4()

    def __len__(self):
        return len(self.nodes)

    def register(self, order, tree):
        """
        Update the tree data structure with a new axis.
        """
        
        axis_id= tree.axis_id()
        #if self.parent != tree.root:
        #    t= tree._properties["transform"][self.parent]
        #    t= Matrix3(t)*Matrix3(self.transform)
        #    t= Matrix4(t)
        #    t[0,3]= self.transform[0,3]
        #    t[1,3]= self.transform[1,3]
        #    t[2,3]= self.transform[2,3]
        #    self.transform= t

        self.compute_polyline()

        tree._properties["order"].setdefault(axis_id,[]).append(order)
        tree._properties["radius"].setdefault(axis_id,self.radius)
        tree._properties["polyline"].setdefault(axis_id,self.polyline)
        tree._properties["offset"].setdefault(axis_id,self.offset)
        tree._properties["length"].setdefault(axis_id,self.total_length)
        tree._properties["transform"].setdefault(axis_id,self.transform)

        length= 0
        node_length= [0.]
        for l in self.length:
            length+= l
            node_length.append(length)
            
        tree._properties["offset_length"].setdefault(axis_id,node_length)

        tree._order_axes.setdefault(order,[]).append(axis_id)

        # je pense que c'est inutile...
        # axis_id, offset
        tree._parent[axis_id]= self.parent
        tree._children.setdefault(self.parent,[]).append(axis_id)

        return axis_id


    def compute_polyline(self):

        if self.polyline:
            return

        angle= 0
        z= Vector3(0,0,1)
        x= Vector3(1,0,0)
        p1p2= Vector3(0,0,1)
        pt= Vector3()
        pt1= pt+p1p2*self.length[0]
        poly= [pt,pt1]
        pt= pt1
        
        assert len(self.curvature) == len(self.nodes)-2
        
        for i in range( 1, len(self.nodes)-1 ):
            p1p2= rotate_Y(p1p2,self.curvature[i-1])
            pt= pt+ p1p2*self.length[i]
            poly.append(pt)
            
        points= Point3Array(poly)
        if self.transform:
            t= Transform4(self.transform)
            points=t.transform(points)

        self.polyline= Polyline( points )

        


##############################################################################

class Branching(object):
    def __init__(self,axis_id,node_offset,nb_branch):
        self.axis_id= axis_id
        self.offset= node_offset
        self.nb_branch= nb_branch

    def __repr__(self):
        return "Branching(axis_id=%i,offset=%i,nb_branch=%i)"% (self.axis_id,
                                                                self.offset,
                                                                self.nb_branch)
        
##############################################################################

class Leaf(object):

    def __init__( self, point, matrix, leaf_scale, leaf_scale_x ):
        self.point= point
        self.matrix= matrix
        self.leaf_scale= leaf_scale
        self.leaf_scale_x= leaf_scale*leaf_scale_x

    def geom(self):
        x= self.leaf_scale_x/1.5
        y= self.leaf_scale

        points= Point3Array([ Vector3(x/2.,0,0), Vector3(0,x/4.,0), Vector3(0,y-x/4.,0),
                              Vector3(x/2.,y,0), Vector3(x,y-x/4.,0), Vector3(x,x/4.,0)])
        indices= Index3Array([ Index3(0,1,5), Index3(1,2,5), Index3(2,3,4),
                               Index3(2,4,5)])

        s= TriangleSet(points, indices)
        return s

            
    

##############################################################################

class Weber_Penn(object):

    def __init__(self,param):
        """
        Base Class of Weber & Penn Tree Simulator.
        """
        
        self.param= param
        self.tree= Tree()
        self.max_order= param.order

        self.stack= []

    def run(self):
        """
        Compute a tree with all geometric properties.
        """
        self.create_trunk()
        for order in range( 1, self.max_order ):
            self.create_stems( order )

        if self.has_leaf():
            self.create_leaves()
        else:
            self.create_stems(self.max_order)
            
        return self.tree

    def create_trunk(self):
        """
        Create a trunk structure.
        """
        # alias
        tree= self.tree

        nb_nodes= self.nb_trunk_nodes()
        axis= self.get_trunk(nb_nodes)
        

        axis_id= axis.register(0,tree)
        
        # axis to create
        self.stack= [ Branching( axis_id, i, n) \
                      for i,n in enumerate(axis.nodes) if n != 0 ]

        if not len(self.stack):
            self.stack= []

        #if not self.stack:
        #    self.max_order= 0
        
    
    def create_stems(self, order):

        stack= []
        
        while self.stack:
            branching= self.stack.pop()

            for i_axis in  range(branching.nb_branch):
                # create axes
                nb_nodes= self.nb_axis_nodes(order, branching)
                axis= self.get_axis(order, nb_nodes,branching)

                axis_id= axis.register(order,self.tree)

                l= [ Branching( axis_id, i, n) \
                     for i,n in enumerate(axis.nodes) if n != 0 ]
                stack.extend(l)
                if len(stack) == 0:
                    stack= []

        self.stack= stack

        #if not self.stack:
        #    self.max_order= order
        

    def create_leaves(self):

        if self.max_order == 0:
            return
        leaves= []
        branches= self.tree._order_axes[self.max_order-1]
        
        for axis_id in branches:

            nb_leaves= self.nb_leaves(axis_id)
            leaves.extend( self.get_leaves(nb_leaves,axis_id) )

        self.tree.leaves= leaves
            
    def has_leaf(self):
        return self.param.leaves


class Weber_Laws( Weber_Penn ):
    """
    Detail implementation of geometrical tree laws
    """

    def __init__(self, param):
        Weber_Penn.__init__(self,param)
        self.rotate= [r for r in param.rotate]
        self.prev_parent_id= 0

    def nb_trunk_nodes(self):
        nb_axes= self.param.n_branches[0]
        return nb_axes+2

    def get_trunk(self,nb_nodes):

        root= self.tree.root
        nodes= self.get_branches(0,nb_nodes)
        curvature= self.get_curvature(0,nb_nodes)
        total_length, length= self.get_length(0,nb_nodes)
        radius= self.get_radius(0,nb_nodes, total_length)
        
        return Axis( root, 0, nodes,
                     total_length, length, radius, curvature, None )

    def nb_axis_nodes( self, order, branching ):
        
        if order >= 3:
            stem_max= 4
        else:
            stem_max= self.param.n_branches[order]
        return max(stem_max,2)
    
    def get_axis(self,order, nb_nodes,branching):

        b= branching
        
        parent_id= branching.axis_id
        if parent_id != self.prev_parent_id:
            self.prev_parent_id= parent_id
            self.rotate[order]= self.param.rotate[order]
            
        offset= branching.offset

        nodes= self.get_branches(order,nb_nodes,b)
        curvature= self.get_curvature(order,nb_nodes,b)
        total_length, length= self.get_length(order,nb_nodes, b)
        radius= self.get_radius( order, nb_nodes, total_length, b)

        transfo= self.get_transformation(order,total_length, b)

        return Axis( parent_id, offset, nodes,
                     total_length, length, radius, curvature, transfo)


    def get_branches( self, order, nb_nodes, branching= None ):

        assert nb_nodes > 0
        b= [1]*nb_nodes
        #b= [ random.randint(0,1) for i in range(nb_nodes) ]
        b[0]= 0
        b [-1]= 0
        
        return b

    def get_curvature( self, order, nb_nodes, branching= None ):
        curve, curveV, curve_back = self.param.n_curve[order][1:]
        if curve_back == 0:
            return [value((curve,curveV))/nb_nodes \
                    for i in range(nb_nodes-2)]
        else:
            n= (nb_nodes-2)/2
            c= []
            for i in range(nb_nodes-2):
                if i < n:
                    c.append( value((curve,curveV)) / n )
                else:
                    c.append( value((curve_back,curveV)) / n )
            return c

    def get_length( self, order, nb_nodes, branching= None ):

        if order == 0:
            total_len= value(self.param.scale) * value(self.param.n_length[0])
            base= total_len*self.param.base_size
            crown_len= (total_len - base) / (nb_nodes-2)
            l= [base]+ [ crown_len ]*(nb_nodes-2)

        else:
            assert( branching )
            pid= branching.axis_id
            parent_len= self.tree._properties["length"][pid]
            poly= self.tree._properties["polyline"][pid]
            offset=branching.offset
            d= self.tree._properties["offset_length"][pid][offset]
            #d= PlantGL.norm(poly[offset]-poly[0])
            len_child_max= value(self.param.n_length[order])

            if order == 1:
                sid=self.param.shape_id
                ratio= (parent_len -d) / (parent_len * (1-self.param.base_size))
                total_len= parent_len *len_child_max * shape_ratio( sid, ratio )

            else:
                total_len= len_child_max *(parent_len-0.6*d)

            l= total_len / (nb_nodes-1)
            l= [l]*(nb_nodes-1)

        assert total_len > 0
        return total_len, l
            

    def get_radius( self, order, nb_nodes, length, branching= None ):

        if order == 0:
            radius= length * self.param.ratio

            return radius
        else: 
            pid= branching.axis_id
            offset= branching.offset
            parent_len= self.tree._properties["length"][pid]
            parent_radius= self.tree._properties["radius"][pid]
            ratio_power= self.param.ratio_power

            length= self.tree._properties["offset_length"][pid][offset]
            
            radius= parent_radius * pow(1-length/parent_len,ratio_power)

        return radius

    def get_transformation( self, order, length, branching ):

        assert(branching)

        pid= branching.axis_id
        poly= self.tree._properties["polyline"][pid]
        t = Matrix3(self.tree._properties["transform"][pid])
        offset=branching.offset

        down= self.param.n_down_angle[order]
        down_angle= 0
        
        if down[1] > 0:
            down_angle= value(down)
        else:

            parent_len= self.tree._properties["length"][pid]
            d= self.tree._properties["offset_length"][pid][offset]

            ratio= (parent_len -d) / (parent_len * (1-self.param.base_size))
            
            downV= down[1]* shape_ratio(0,1-2*shape_ratio(0,ratio))
            down_angle= value( (down[0], downV) )


        rotate= self.param.n_rotate[order-1]

        #todo
        self.rotate[order]+= value(rotate)
        self.rotate[order]= self.rotate[order] % 360

        z= poly[offset]-poly[offset-1]
        z.normalize()
        
        y = t* Vector3(0,1,0)
        x = t* Vector3(1,0,0)
        x.normalize()
        y.normalize()
        
        r_rot= axisRotation(z, radians(self.rotate[order]))
        r_down= axisRotation(y,radians(down_angle))
        new_z = r_rot * r_down * z
        new_y = r_rot * y
        new_x = new_y ^new_z
        transfo = Matrix4(BaseOrientation(new_x, new_y).getMatrix3())

        #transfo = Matrix4(r_rot*r_down*t)
        #x = t * Vector3(1,0,0)
        #r_rot = axisRotation(z, radians(self.rotate[order]))
        #r_down = axisRotation(z^x, radians(down_angle))
        #transfo = Matrix4(r_rot * r_down)

        # FIXME BIG BUG
        #euler = r_rot * r_down
        
        #z_old = t * Vector3(0,0,1)
        #y_old = t * Vector3(0,1,0)
        #z_rot = axisRotation(y_old, angle(z_old, z))
        #x = z_rot * t * Vector3(1,0,0)
        #y = y_old 
        #x.normalize()
        #y.normalize()
        #t = BaseOrientation(x,y).getMatrix3()
        #a,e,r= radians(self.rotate[order]),  radians(down_angle), 0
        #euler= eulerRotationZYX(Vector3(a,e,r))
        #transfo= Matrix4(euler*t)
        #print degrees(a),degrees(e),degrees(r)

        #transfo= Transform4( Matrix4(  euler ) )
        #transfo.translate(poly[offset])

        x,y,z= poly[offset]
        transfo[0,3]= x
        transfo[1,3]= y
        transfo[2,3]= z
        return transfo

    def nb_leaves(self, axis_id):

        leaves= self.param.leaves
        
        pid= self.tree._parent[axis_id]
        offset= self.tree._properties["offset"][axis_id]

        length_parent= self.tree._properties["length"][pid]
        offset_child= self.tree._properties["offset_length"][pid][offset]
        quality= 1

        leaves_per_branch= leaves * shape_ratio(4,offset_child / length_parent)

        return int(leaves_per_branch)

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
        
        leaves= []
        for i, pt in enumerate(pts):
            
            tgt= tgts[i]
            
            self.rotate[order]+= value(rotate)
            self.rotate[order]= self.rotate[order] % 360
            a,e,r= radians(self.rotate[order]), radians(90-down_angle),angle(Vector3(0,0,1),tgt)
            #a,e,r= random.uniform(-pi,pi),random.uniform(-pi,pi),random.uniform(-pi,pi)
            euler= eulerRotationZYX(Vector3(r,e,a))
            t_parent= Matrix3(self.tree._properties["transform"][pid])

            m= t_parent*euler
            
            #debug
            r_rot= axisRotation(tgt, radians(self.rotate[order]))
            r_down= axisRotation(Vector3(1,0,0),radians(down_angle))
            r_tgt= axisRotation(Vector3(1,0,0), angle(Vector3(0,0,1),tgt))
            m= r_rot * r_down * r_tgt
            #nv= r_rot * r_down * tgt
            #debug
            #nv= Vector3(random.random(), random.random(), random.random())
            #nv.normalize()
            ls, ls_x= self.param.leaf_scale,self.param.leaf_scale_x
            leaves.append( Leaf(pt,m, ls,ls_x ) )
            
            
        return leaves

##############################################################################

class Markov_Laws( Weber_Laws):
    """
    Ramification is build form a first order Markov chain rather 
    than from fixed parameters.
    """
    def __init__(self, param, p0 = 0.85, p1 = 0.95):
        Weber_Laws.__init__(self, param)
        self.p0 = p0
        self.p1 = p1
        
    def get_branches( self, order, nb_nodes, branching= None ):

        assert nb_nodes > 0
        m= Markov(self.p0,self.p1)
        b= [m() for i in xrange(nb_nodes)]
        b[0]= 0
        b [-1]= 0
        
        return b

##############################################################################
# Utility functions

class Poly(Polyline):

    def __init__(self, points, length, lengthes):
        PlantGL.Polyline.__init__(self,points)
        self.lengthes = lengthes
        self.length= length

    def points( self, n ):
        step= self.length / float(n)
        pts= []
        tgts= []

        error= step
        previous_length= 0

        #print n+2-len(lengthes)
        for i,l in enumerate(self.lengthes[1:]):

            l-= previous_length
            p1= self[i]
            p2= self[i+1]
            tgt= p2 - p1

            while error <= l:
                pt= tgt*(error / l) + p1

                pts.append(pt)
                #tgt.normalize()
                tgts.append(tgt)

                error+= step
            
            else:
                error-= l

            previous_length+= l

        #print "pt1:", pts[-1], "pt2:", self[len(self)-1]
        #print n, len(pts), len(self)
        map(lambda x: x.normalize(), tgts)
        return pts, tgts


def rotate_X( v, angle ):
    " Rotate a vector V around the x axis."
    mat= PlantGL.axisRotation(Vector3(1,0,0),radians(angle))
    return mat * v

def rotate_Y( v, angle ):
    " Rotate a vector V around the x axis."
    mat= PlantGL.axisRotation(Vector3(0,1,0),radians(angle))
    return mat * v

def value(v):
    return v[0]+uniform(-v[1],v[1])


def shape_ratio( envelop_type, ratio ):
    # Conical
    if envelop_type == 0:
        return 0.2+0.8*ratio
    # Spherical
    elif envelop_type == 1:
        return 0.2 + 0.8 * sin( pi * ratio )
    # Hemispherical
    elif envelop_type == 2:
        return 0.2 + 0.8 * sin( 0.5 * pi * ratio )
    # Cylindrical
    elif envelop_type == 3:
        return 1.
    # Tapered cylindrical
    elif envelop_type == 4:
        return 0.5+0.5*ratio
    # Flame
    elif envelop_type == 5:
        l = 0.01
        if ratio < 0.7:
            return ratio/0.7+l
        else:
            return (1.-ratio)/0.3+l
    # Inverse Conical
    elif envelop_type == 6:
        return 1.-0.8*ratio
    # Tend Flame
    elif envelop_type == 7:
        if ratio < 0.7:
            return 0.5+0.5*ratio/0.7
        else:
            return 0.5+0.5*(1.-ratio)/0.7
    else:
        return ratio


##############################################################################

# TODO:
#  1. Weber & penn
#  2. Fractal (autosimilar)
#  3. Growing MTG


class TreeParameter(object):
    def __init__(self, shape_id, base_size, scale, order, ratio, ratio_power,
                 lobes, flare, base_split, n_length,
                 n_seg_split, n_split_angle, n_down_angle,
                 n_curve, n_rotate, n_branches,
                 leaves, leaf_scale, leaf_scale_x, rotate):

        self.shape_id= shape_id
        self.base_size= base_size
        self.scale= scale
        self.order= order
        self.ratio=ratio
        self.ratio_power=ratio_power
        self.lobes=lobes
        self.flare=flare
        self.base_split=base_split
        self.n_length=n_length
        self.n_seg_split=n_seg_split
        self.n_split_angle=n_split_angle
        self.n_down_angle= n_down_angle
        self.n_curve=n_curve
        self.n_rotate=n_rotate
        self.n_branches=n_branches
        self.leaves= leaves
        self.leaf_scale= leaf_scale
        self.leaf_scale_x= leaf_scale_x
        self.rotate= rotate


# Factory
# see Weber & Penn 96
def Quaking_Aspen():
    shape_id= 7
    base_size= 0.4
    scale= (13,3) 
    order= 3
    ratio= 0.015
    ratio_power= 1.2
    lobes= (5,0.07)
    flare= 0.6
    base_split= 0
    n_length= [(1,0),(0.3,0),(0.6,0),(0,0) ]
    n_seg_split= []
    n_split_angle= []
    n_down_angle= [(0,0),(60,-50),(45,10),(45,10)]
    n_curve= [(3,0,0,20),(5,-40,0,50),(3,-40,0,75),(1,0,0,0)]
    n_rotate=[(140,0),(140,0),(77,0)]
    branches=[50,30,10]
    leaves= 25
    leaf_scale= 0.17
    leaf_scale_x= 1
    rotate=[0]*(order+1)

    return TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle, n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate)

def Black_Tupelo():
    shape_id= 4
    base_size= 0.2
    scale= (23,5) 
    order= 4
    ratio= 0.015
    ratio_power= 1.3
    lobes= (3,0.1)
    flare= 1
    base_split= 0
    n_length= [(1,0),(0.3,0.05),(0.6,0.1),(0.4,0) ]
    n_seg_split= []
    n_split_angle= []
    n_down_angle= [(0,0),(60,-40),(30,10),(45,10)]
    n_curve= [(10,0,0,40),(10,0,0,90),(10,-10,0,150),(1,0,0,0)]
    n_rotate=[(140,0),(140,0),(140,0)]
    branches=[50,25,12]
    leaves= 6
    leaf_scale= 0.3
    leaf_scale_x= 0.5
    rotate=[0]*(order+1)

    return TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle,n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate)

def Weeping_Willow():
    shape_id= 3
    base_size= 0.05
    scale= (15,5) 
    order= 4
    ratio= 0.03
    ratio_power= 2
    lobes= (9,0.03)
    flare= 0.75
    base_split= 2
    n_length= [(0.8,0),(0.5,0.1),(1.5,0),(0.1,0) ]
    n_seg_split= [0.1,0.1,0.2,0]
    n_split_angle= [(3,0),(30,10),(45,20),(0,0)]
    n_down_angle= [(0,0),(20,10),(30,10),(20,10)]
    n_curve= [(8,0,20,120),(10,40,80,90),(6,0,0,0),(1,0,0,0)]
    n_rotate=[(-120,30),(-120,30),(140,0)]
    branches=[25,10,300]
    leaves= 15
    leaf_scale= 0.12
    leaf_scale_x= 0.12
    rotate=[0]*(order+1)

    return TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle,n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate)

def Black_Oak():
    shape_id= 2
    base_size= 0.05
    scale= (10,10) 
    order= 3
    ratio= 0.018
    ratio_power= 1.3
    lobes= (5,0.1)
    flare= 1.2
    base_split= 2
    n_length= [(1,0),(0.8,0.1),(0.2,0.05),(0.4,0) ]
    n_seg_split= [0.4,0.2,0.1,0]
    n_split_angle= [(10,0),(10,10),(10,10),(0,0)]
    n_down_angle= [(0,0),(30,-30),(45,10),(45,10)]
    n_curve= [(8,0,0,90),(10,40,-70,150),(3,0,0,-30),(1,0,0,0)]
    n_rotate=[(80,0),(140,0),(140,0)]
    branches=[40,120,0]
    leaves= 25
    leaf_scale= 0.12
    leaf_scale_x= 0.66
    rotate=[0]*(order+1)

    return TreeParameter( shape_id, base_size, scale, order,
                          ratio, ratio_power, lobes, flare,
                          base_split, n_length,
                          n_seg_split, n_split_angle,n_down_angle,
                          n_curve, n_rotate, branches, leaves, leaf_scale, leaf_scale_x,
                          rotate)

