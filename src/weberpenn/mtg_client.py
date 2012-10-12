"""
  Simulation client.
  The client
  
  Author: Christophe Pradal (christophe.pradal@cirad.fr)
"""

from openalea.plantgl.all import *
import openalea.plantgl.all as PlantGL
from  openalea.plantgl.all import (Vector3, Point3Array, Polyline, 
Translation, axisRotation, Matrix3, Matrix4, Transform4,
Index3Array,Index3, TriangleSet, eulerRotationZYX,eulerRotationXYZ, angle)
from random import randint, uniform
from math import degrees, radians, sin, pi, atan2
import random

from openalea.weberpenn.tree_client import *
from openalea.mtg import *
from openalea.mtg.traversal import pre_order


##############################################################################

class GeometryParameters(object):
    def __init__(self):
        # Total length of an element
        self.length = None
        # Position of an element on its parent axis
        self.offset = None
        # Insertion angle or curvature
        self.down = None
        # Phylloxis angle to be used only on the axes.
        # This is used only before branching
        self.rotate = None
        # Rotation angle
        self.roll = None
        # Top radius if node or bottom radius if axis
        self.radius = None

        

class Weber_MTG(Weber_Laws):
    """ Apply Weber and Penn Laws on a MTG graph.

    First we consider that there is no geometric properties on the MTG.
    Method:
        - Tree extraction at the finest scale.
        - Insertion of an upper scale at axe level to store local properties.
        - Traverse the axes in a pre_order way (lower order axes before higher ones.)
        - for each axes:
            - compute the curvature for interior vertex
            - compute the length of the axe and of the nodes plus the offset
            - compute the radius for the axe and for each nodes
            - compute the phyllotaxie and the insertion angle (down angle)
            
    """
    def __init__(self, param, mtg):
        """ Solve all geometric parameters on a MTG using the Weber and Penn model.
        :Parameters:
            - param: Parameters of the Weber and Penn model
            - mtg: a multiscale tree graph 
        """
        self._mtg = mtg
        self.param = param
        self.g, self.index_map = create_mtg_with_axes(mtg)
        self.max_order= param.order
        self.frame = {}

    def run(self):
        ''' Compute the geometric parameters on the MTG.
        '''
        root_id = self.get_trunk()
        for axis_id in pre_order(self.g, root_id):
            if axis_id != root_id:
                self.get_stem(axis_id)

    def get_trunk(self):
        g = self.g
        axis_id = g.components_iter(g.root).next()

        self.get_stem(axis_id)
        return axis_id

    def get_stem(self, axis_id):
        self.create_frames(axis_id)
        self.get_curvature(axis_id)
        self.get_length(axis_id)
        self.get_transformation(axis_id)
        self.get_radius(axis_id)

    def create_frames(self, vid):
        g = self.g
        frames = self.frame
        frames.setdefault(vid, GeometryParameters())
        for v in g.components_iter(vid):
            frames.setdefault(v, GeometryParameters())

    def get_curvature(self, vid):
        """ Compute the curvature of an axis.
        Add and/or update the frame for each interior nodes.
        """
        g = self.g
        assert g.scale(vid) == 1
        order = self._get_order(vid)
        nb_nodes = g.nb_components(vid) +1

        curvature = super(Weber_MTG, self).get_curvature(order,nb_nodes)
        components = g.components(vid)
        assert len(curvature) == len(components) -1

        for i, v in enumerate(components):
            if i != 0:
                self.frame[v].down = curvature[i-1]

    def get_length(self, vid):
        """ Compute the length of each elements of an axis.
        """
        g = self.g
        order = self._get_order(vid)
        nb_nodes = g.nb_components(vid) + 1
        frames = self.frame

        if order == 0:
            nb_base_nodes = 0
            for v in g.components(vid):
                nb_base_nodes+=1
                if g.nb_children(v) > 1:
                    break

            total_len= value(self.param.scale) * value(self.param.n_length[0])
            base= total_len*self.param.base_size/nb_base_nodes
            crown_len= (total_len - base) / (nb_nodes - nb_base_nodes -1)
            l= [base]*(nb_base_nodes)+ [ crown_len ]*(nb_nodes-nb_base_nodes-1)

        else:
            # pid is the parent axis to vid
            pid = g.parent(vid)
            root_id = g.components_iter(vid).next()
            offset_id = g.parent(root_id)
            assert g.complex(offset_id) == pid

            parent_len = frames[pid].length
            assert parent_len is not None
            d = frames[offset_id].offset
            len_child_max= value(self.param.n_length[order])

            if order == 1:
                sid=self.param.shape_id
                ratio= (parent_len -d) / (parent_len * (1-self.param.base_size))
                total_len= parent_len *len_child_max * shape_ratio( sid, ratio )

            else:
                total_len= len_child_max *(parent_len-0.6*d)

            l= total_len / (nb_nodes-1)
            l= [l]*(nb_nodes-1)

        assert len(l) == nb_nodes - 1
        # Update the frames...
        frames[vid].length = total_len
        
        offset_length = 0
        for i,v in enumerate(g.components_iter(vid)):
            length = l[i]
            offset_length+= length
            frames[v].length = length
            frames[v].offset = offset_length

    def get_transformation(self, vid):
        """ Compute insertion angle or down angle and phyllotaxis.
        """
        g = self.g
        order = self._get_order(vid)
        nb_nodes = g.nb_components(vid) + 1
        frames = self.frame
        edge_type = g.property('edge_type')

        r = 0
        if order == 0:
            rotate= value(self.param.n_rotate[order])
            frames[vid].rotate = rotate
            for v in g.components_iter(vid):

                et = [c for c in g.children(v) if edge_type.get(c) == '+']
                n = len(et)
                roll = 0
                for c in et:
                    roll += 360./n
                    frames.setdefault(c, GeometryParameters()).roll = roll
                    r = (r+rotate) %360
                    frames[v].rotate = r

            return

        pid = g.parent(vid)
        root_id = g.components_iter(vid).next()
        offset_id = g.parent(root_id)

        down= self.param.n_down_angle[order]
        down_angle= 0
        
        if down[1] > 0:
            down_angle= value(down)
        else:

            parent_len= frames[pid].length
            d= frames[offset_id].offset

            ratio= (parent_len -d) / (parent_len * (1-self.param.base_size))
            
            downV= down[1]* shape_ratio(0,1-2*shape_ratio(0,ratio))
            down_angle= value( (down[0], downV) )

        frames[root_id].down = down_angle

        rotate= value(self.param.n_rotate[order-1])

        frames[vid].rotate = rotate
        for v in g.components_iter(vid):
            r = (r+rotate) %360
            frames[v].rotate = r
            
            et = [c for c in g.children(v) if edge_type.get(c, '/') == '+']
            n = len(et)
            roll = 0
            for c in et:
                roll += 360./n
                frames.setdefault(c, GeometryParameters()).roll = roll


    def get_radius(self, vid):
        g = self.g
        order = self._get_order(vid)
        nb_nodes = g.nb_components(vid) + 1
        frames = self.frame

        taper = 0.9
        if order == 0:
            length = frames[vid].length
            radius = length * self.param.ratio
        else:
            # pid is the parent axis to vid
            pid = g.parent(vid)
            root_id = g.components(vid).next()
            offset_id = g.parent(root_id)
            parent_len = frames[pid].length
            parent_radius = frames[pid].radius
            ratio_power= self.param.ratio_power

            length= d = frames[offset_id].offset
            taper = 0.9
            power = 1-taper*min(1., length/parent_len)
            radius= parent_radius * pow(power,ratio_power)

        frames[vid].radius = radius
        step = taper / float(nb_nodes)
        for i, v in enumerate(g.components(vid)):
            frames[v].radius = radius*(1-(i+1)*step)

    def _get_order(self, vid):
        """ Get the order of a node, and check if it is not out of the max order parameter.
        """ 
        order = self.g.order(vid)
        max_order = self.param.order
        return min(order, max_order)

    def plot(self):

        g = self.g
        frames = self.frame
        edge_type = g.property('edge_type')

        p = PglTurtle()
        #p.startGC()

        root = g.roots_iter(scale=2).next()

        min_length = min([f.length for f in frames.itervalues() if f.length and f.length >0])
        for vid in pre_order_turtle(g, root, p):
            down = frames[vid].down 
            down = 0 if down is None else down 
            l = max(frames[vid].length, min_length)

            if edge_type.get(vid) == '+':
                # 1. phi /
                # 2. insertion angle (+, -)
                # 3. F
                pid = g.parent(vid)
                radius = frames[vid].radius
                phi = frames[pid].rotate
                phi = 0 if phi is None else phi
                roll = frames[vid].roll
                roll = 0 if roll is None else roll


                p.push()
                p.scale(radius)
                p.rollL(phi)
                p.rollL(roll)
                p.down(down)
                p.F(l)
            else:
                radius = frames[vid].radius
                p.scale(radius)
                p.down(down)
                p.F(l)

        
        #p.stopGC()
        #Viewer.display(p.getScene())
        return p.getScene()

def pre_order_turtle(tree, vtx_id, turtle):
    # 1. select first '+' edges
    edge_type = tree.property('edge_type')
    successor = []
    yield vtx_id
    for vid in tree.children(vtx_id):
        if edge_type.get(vid) == '<':
            successor.append(vid)
            continue
        for node in pre_order_turtle(tree, vid, turtle):
            yield node
        turtle.pop()

    # 2. select then '<' edges
    for vid in successor:
        for node in pre_order_turtle(tree, vid, turtle):
            yield node

def create_mtg_with_axes(g):
    """ Construct a MTG from the finest scale of an existing MTG.
    Insert a scale which represent axes.
    """

    max_scale = g.max_scale()
    tree_root = g.roots_iter(scale=max_scale).next()
    colors = {}

    edge_type = g.property('edge_type')
    colors[2] = g.vertices(scale=max_scale)
    colors[1] = [vid for vid, edge in edge_type.iteritems() if edge=='+' and g.scale(vid) == max_scale]
    colors[1].insert(0,tree_root)

    mtg, new_map = colored_tree(g, colors)

    return mtg, new_map

    
