"""
  3D Scene Maker from a tree and its specifications.
  
  Author: Christophe Pradal (christophe.pradal@cirad.fr)
"""

from openalea.plantgl.all import (BezierPatch, Discretizer, Viewer, Scene,
                                  Shape, Material,
                                  Color3,
                                  Extrusion,
                                  Polyline, Point2Array, Point4Matrix, PointSet,
                                  Vector2, angle,
                                  AxisRotated,
                                  Oriented, Translated, Scaled, Vector3,
                                  EulerRotated,
                                  Vector4)

brown = Material(Color3(120, 60, 10))
green = Material(Color3(4, 69, 4), diffuse=0.768116,
                 specular=Color3(116, 116, 116))
green.name = "green_leaf"


def bezier_leaf():
    l = []
    l.append([Vector4(-0.00170203, 0.00487903, -0.00155362, 1),
              Vector4(-0.00946124, 0.0267487, 0.00857975, 1),
              Vector4(-0.0145598, 0.0310762, 0.0565383, 1),
              Vector4(-0.00422035, 0.0237428, 0.101953, 1)])
    l.append([Vector4(3.9604e-05, 0.0019996, 5.60056e-06, 1),
              Vector4(-0.00466331, 0.00703859, 0.0339818, 1),
              Vector4(-0.00868596, 0.00523895, 0.076457, 1),
              Vector4(0.00379859, 0.00943444, 0.154352, 1)])
    l.append([Vector4(-3.9604e-05, -0.0019996, -5.60056e-06, 1),
              Vector4(-0.00493527, 0.00263947, 0.0352765, 1),
              Vector4(-0.00867663, 0.00259947, 0.0760139, 1),
              Vector4(0.00447972, 0.00923447, 0.156651, 1)])
    l.append([Vector4(-0.00218137, -0.00475904, 0.000459084, 1),
              Vector4(-0.0120507, -0.0206578, 0.0115464, 1),
              Vector4(-0.0150292, -0.0230562, 0.0604107, 1),
              Vector4(-0.00608397, -0.0102688, 0.102558, 1)])
    
    matrix = Point4Matrix(4, 4)
    for i, row in enumerate(l):
        for j, pt in enumerate(row):
            pt = pt * 9
            pt.w = 1
            matrix[i, j] = pt
    
    leaf = BezierPatch(matrix, 4, 4)

    leaf.name = 'leaf'
    return leaf


class GeomEngine(object):
    """
    Construct a scene graph from a computed tree.
    """

    def __init__(self, server, section, position=Vector3(0, 0, 0), color=brown,
                 leaf=None):
        self.server = server
        self.color = color
        self.section = section
        self.leaf = leaf
        if not leaf:
            self.leaf = bezier_leaf()
        self._shapes = []
        self.position = position

    def scene(self, view="axis", scene=None):
        """
        Compute a scene from a tree squeleton.

        view='axis', 'node', 'polyline' or 'point'
        view specify if we compute a shape by axis, a shape by node
        or just a polyline.
        """
        if not scene:
            scene = Scene()

        server = self.server

        max_order = server.max_order

        for order in range(max_order):
            self.axes(order, view)

        if server.has_leaf():
            if view not in ['point']:
                self.leaves()
        else:
            self.axes(max_order, view)

        map(lambda x: scene.add(x), self._shapes)
        return scene

    def axes(self, order, view="axis"):

        server = self.server
        axes = server.axes(order)
        for axis_id in axes:
            # if order > 3:
            #    break
            polyline = server.polyline(axis_id)
            radius = server.radius(axis_id)
            
            # Compute the shape
            shapes_axis = self.shapes(view, polyline, radius)
            self._shapes.extend(shapes_axis)

    def leaves(self, color=green):

        server = self.server
        leaves = server.leaves()
        leaf = self.leaf
        # map( lambda x: scene.add(self.leaf_shape(x,color,leaf)), leaves )
        map(lambda x: self._shapes.append(self.leaf_shape(x, color, leaf)),
            leaves)

    def leaf_shape(self, leaf, color, shape):

        s = shape
        # t= Transform4()
        # t.scale(Vector3(leaf.leaf_scale_x,leaf.leaf_scale,leaf.leaf_scale))
        # t.rotate(leaf.matrix)
        # t.translate(leaf.point+self.position)
        # t.transform(s.pointList)
        # normal= leaf.matrix*Vector3(0,0,1)

        s = Scaled(Vector3(leaf.leaf_scale_x, leaf.leaf_scale, leaf.leaf_scale),
                   s)
        
        x = leaf.matrix * Vector3(1, 0, 0)
        y = leaf.matrix * Vector3(0, 1, 0)

        s = Oriented(x, y, s)
        # a, e, r= uniform(-pi, pi), uniform(-pi,pi),uniform(-pi,pi)
        # s= EulerRotated(a,e,r, s)

        t = Translated(leaf.point + self.position, s)
        return Shape(t, color)

    def shapes(self, scale, polyline, radius):
        """
        Compute the geometric objects from the spec.
        scale= 'polyline': tree skeleton is made by polylines.
        scale= 'axis': tree skeleton is made by generalized cylinder.
        scale= 'cylinder': tree skeleton is made by cylinders.
        scale= 'point': tree skeleton is made by set of points.
        """
        p = polyline
        if scale == 'polyline':
            if self.position != Vector3(0, 0, 0):
                polyline = Translated(self.position, p)
            else:
                polyline = p

            return [Shape(polyline, self.color)]

        elif scale == 'axis' or scale == 'point':
            n = len(p)
            taper = 0.9
            if n > 1:
                step = taper * (98 / 100.) / float(n)
            else:
                return []
            r = [Vector2(radius * (1. - i * step), radius * (1. - i * step)) for
                 i in range(n)]
            sweep = Extrusion(polyline, self.section, Point2Array(r))
            sweep = Translated(self.position, sweep)

            if scale == 'point':
                d = Discretizer()
                sweep.apply(d)
                points = d.getDiscretization()
                return [Shape(PointSet(points.pointList), self.color)]
            else:
                return [Shape(sweep, self.color)]

        elif scale == 'cylinder':
            sweeps = []

            n = len(polyline)
            taper = 0.9
            if n > 1:
                step = taper / float(n)
            else:
                return []

            r = [Vector2(radius * (1. - i * step), radius * (1. - i * step)) for
                 i in range(n)]

            for i in range(n - 1):
                p1, p2 = polyline[i] + self.position, polyline[
                    i + 1] + self.position
                r1, r2 = r[i], r[i + 1]
                local_r = Point2Array([Vector2(r1), Vector2(r2)])
                sweep = Extrusion(Polyline([p1, p2]), self.section, local_r)
                sweeps.append(Shape(sweep, self.color))
            return sweeps
