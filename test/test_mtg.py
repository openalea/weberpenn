from openalea.mtg import *
from openalea.weberpenn.mtg_client import *
from openalea.grapheditor import dataflowview
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import warnings
if not QCoreApplication.instance() is None:
    warnings.warn("A QApplication is already running")
else:
    app = QApplication([])
Viewer.start()



def default_mtg():
    g = MTG()
    root = g.add_component(g.root)

    axis0 = [0,0,2,0,1,0,1,0]
    axis1 = [1,0,2,0]
    axis2 = [0,0]

    def add_axis(vid, axis):
        stack = []
        for nb_ramif in axis:
            for i in range(nb_ramif):
                v = g.add_child(vid, edge_type='+')
                stack.append(v)
            vid = g.add_child(vid, edge_type='<')
        return stack

    order1 = add_axis(root, axis0)
    order2 = []
    for vid in order1:
        order2.extend(add_axis(vid, axis1))
    for vid in order2:
        add_axis(vid, axis2)
                
    fat_mtg(g)

    return g

def test1():
    # Build an Tree

    g = default_mtg()
    mtg, index_map = create_mtg_with_axes(g)
    assert len(mtg) == 83
    assert mtg.nb_scales() == 3
    return mtg


def test2():
    g = default_mtg()
    param = Quaking_Aspen()
    wp = Weber_MTG(param, g)
    wp.run()
    return wp


def test4():
    wp = test2()
    wp.plot()
    return wp

def test3():
    p = PglTurtle()
    p.F(10)
    p.down(10)
    p.F(10)
    p.down(-10)
    p.F(10)

    # ramif
    l=3
    phi = 30
    p.push()
    p.rollL(phi)
    p.rollL(0)
    p.down(60)
    p.F(l)
    p.down(10)
    p.F(l)
    p.down(-10)
    p.F(l)
    p.pop()

    p.push()
    p.rollL(phi)
    p.rollL(120)
    p.down(60)
    p.F(l)
    p.down(10)
    p.F(l)
    p.down(-10)
    p.F(l)
    p.pop()

    p.push()
    p.rollL(phi)
    p.rollL(240)
    p.down(60)
    p.F(l)
    p.down(10)
    p.F(l)
    p.down(-10)
    p.F(l)
    p.pop()
    
    p.F(10)
    
    p.stopGC()
    Viewer.display(p.getScene())

def test4():
    from openalea.core import alea
    from openalea.mtg.io import read_mtg_file

    fn = alea.run(('demo.mtg','agraf.mtg'), [])[0]
    g = read_mtg_file(fn)
    param = Quaking_Aspen()
    param.order = 2
    wp = Weber_MTG(param, g)
    wp.run()
 
