from pygame.math import Vector2
import networkx as nx
from math import copysign, log10
import random

# Constants 
LINK_GAIN = 300
NODE_GAIN = 50000
TEMP_RATE = 1
MIN_DEMOMINATOR = 1

# Defaults
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_NUM_NODES = 7
DEFAULT_NUM_EDGES = 8

# NODE COLORS in RGBA (Left to right): Blue, Indigo, Purple,
#                                      Pink, Yellow, Green.
DEFAULT_NODE_COLORS = ((119, 185, 224, 100),(99, 101, 207, 100),(186, 125, 219, 100),
                       (255, 115, 157, 100),(255, 238, 135, 100),(166, 207, 99, 100))

class force_directed_graph(nx.Graph):
    def __init__(self, num_nodes: int = DEFAULT_NUM_NODES, num_edges: int = DEFAULT_NUM_EDGES, 
                 node_colors: tuple = DEFAULT_NODE_COLORS, 
                 x_range: tuple = ( 0, DEFAULT_WIDTH ), y_range: int = ( 0, DEFAULT_HEIGHT ) ):

        # Initialize Variables
        super().__init__()
        self.temp = 1
        self.x_range = x_range
        self.y_range = y_range

        # Configure graph
        node_list = list( ( v, {'position': self._rand_position(), 'color': random.choice( node_colors ) } ) for v in range( num_nodes ) )
        edge_list = list( ( random.randint(0, num_nodes - 1), random.randint(0, num_nodes - 1) ) for _ in range(num_edges) )
        self.add_nodes_from(node_list)
        self.add_edges_from(edge_list)


    def _get_repulsive_force( self, delta: float ) -> float:
        denominator = max( MIN_DEMOMINATOR, delta**2 )
        denominator *= copysign( 1, delta )
        return( NODE_GAIN / denominator )
    
    def _rand_position( self ) -> Vector2:
        return Vector2( random.randint( self.x_range[0], self.x_range[1] ), 
                        random.randint( self.y_range[0], self.y_range[1] ) )


    def force_directed_graph_step( self ):
        force_vector = Vector2(0, 0)

        for node_1, node_1_data in self.nodes(data=True):
            # Link forces
            for edge in self.edges(node_1):
                delta_x = node_1_data['position'].x - self.nodes[edge[1]]['position'].x
                delta_y = node_1_data['position'].y - self.nodes[edge[1]]['position'].y
                force_vector.x -= delta_x / LINK_GAIN
                force_vector.y -= delta_y / LINK_GAIN

            # Node forces
            for node_2, node_2_data in self.nodes(data=True):
                if node_1 != node_2:
                    delta_x = node_1_data['position'].x - node_2_data['position'].x
                    delta_y = node_1_data['position'].y - node_2_data['position'].y
                    force_vector.x += self._get_repulsive_force( delta_x )
                    force_vector.y += self._get_repulsive_force( delta_y )
                    
            node_1_data['position'].x += self.temp * force_vector.x
            node_1_data['position'].y += self.temp * force_vector.y

            # Clamp Node position
            node_1_data['position'].x = max( self.x_range[0], min(node_1_data['position'].x, self.x_range[1] ) )
            node_1_data['position'].y = max( self.y_range[0], min(node_1_data['position'].y, self.y_range[1] ) )

            # Wall forces
            force_vector.x += self._get_repulsive_force( node_1_data['position'].x - self.x_range[0] )
            force_vector.x += self._get_repulsive_force( node_1_data['position'].x - self.x_range[1] )

            force_vector.y += self._get_repulsive_force( node_1_data['position'].y - self.y_range[0] )
            force_vector.y += self._get_repulsive_force( node_1_data['position'].y - self.y_range[1] )

            node_1_data['position'].x += self.temp * force_vector.x
            node_1_data['position'].y += self.temp * force_vector.y

            self.temp *= TEMP_RATE
                