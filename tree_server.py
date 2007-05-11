"""
  Server for the simulation.
  
  Author: Christophe Pradal (christophe.pradal@cirad.fr)
"""

class TreeServer(object):

    def __init__( self, client ):
        self.client= client
        self.tree= None

    def run(self):
        self.tree= self.client.run()

    def axes(self,order):
        """
        Return the list of axis_id at a specific order.
        """
        return self.tree.axes(order)

    def polyline(self, axis_id):
        """
        Return a polyline containing points and length.
        """
        return self.tree._properties["polyline"][axis_id]

    def radius(self, axis_id):
        """
        Return a list of radius.
        """
        return self.tree._properties["radius"][axis_id]

    def transformation(self, axis_id):
        """
        Return the transformation between the axis and its parent.
        """
        return self.tree._properties["transformation"][axis_id]

    def has_leaf(self):
        return self.client.has_leaf()

    def leaves(self):
        return self.tree.leaves
    
    # properties
    def _get_max_order(self):
        return self.client.max_order
    
    def _set_max_order(self,max_order):
        raise "max_order is a read only attibute"
        
    max_order=property(_get_max_order, _set_max_order)
    
