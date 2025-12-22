import random
import os
from openalea.weberpenn.tree_client import *
from openalea.weberpenn import tree_client
from openalea.weberpenn import tree_server
from openalea.weberpenn import tree_geom
from openalea.plantgl.all import *

def test_polyline():
    param = tree_client.Quaking_Aspen()

    #points = [Vector2(0.5, 0), Vector2(0, 0.5), Vector2(-0.5, 0), Vector2(0, -0.5), Vector2(0.5, 0)]
    
    #section = Polyline2D(points)

    client = tree_client.Weber_Laws(param)
    server = tree_server.TreeServer(client)
    server.run()
    geom = tree_geom.GeomEngine(server, section=None)
    polylines = geom.polylines()
    return polylines
    

