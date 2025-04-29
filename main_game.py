import pygame
from pygame.locals import *
from pygame import draw
import sys
import networkx as nx
import random

# Global Constants
WIDTH = 1920
HEIGHT = 1080
NODE_RADIUS = 20
SCREEN_EDGE_BUFFER = NODE_RADIUS + 10
FPS = 144

NUM_NODES = 10
NUM_EDGES = 20

# NODE COLORS in RGBA (Left to right): Blue, Indigo, Purple,
#                                      Pink, Yellow, Green.
NODE_COLORS = ((119, 185, 224, 100),(99, 101, 207, 100),(186, 125, 219, 100),
               (255, 115, 157, 100),(255, 238, 135, 100),(166, 207, 99, 100))

# Classes

# Functions
def rand_position():
    return ( random.randint(SCREEN_EDGE_BUFFER, WIDTH - SCREEN_EDGE_BUFFER), 
            random.randint(SCREEN_EDGE_BUFFER, HEIGHT - SCREEN_EDGE_BUFFER) )

def rand_graph() -> nx.Graph:
    node_list = ( ( v, {'position': rand_position(), 'color': random.choice(NODE_COLORS) } ) for v in range(NUM_NODES) )
    edge_list = ( ( random.randint(0, NUM_NODES - 1), random.randint(0, NUM_NODES - 1) ) for _ in range(NUM_EDGES) )
    graph = nx.Graph()

    # Initialize Variables
    graph.add_nodes_from(node_list)
    graph.add_edges_from(edge_list)

    return graph

# Main
def main():
    # Local Variables
    graph = rand_graph()

    # Radius of the circle of influence for player.
    player_influence_radius = 15

    # Initialize Variables
    pygame.init()
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    transparency_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    vec = pygame.math.Vector2 

    # Main loop
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                graph = rand_graph()
                player_influence_radius = player_influence_radius * 1.25

        # Render
        transparency_surface.fill((51,51,51,0))
        displaysurface.fill((51,51,51))

        for edge in graph.edges:
            draw.aaline(displaysurface, (255, 255, 255), graph.nodes[edge[0]]['position'], graph.nodes[edge[1]]['position'], 1 )

        # Sphere of Influence Generation
        for _, node_data in graph.nodes(data=True):
            draw.circle( transparency_surface, color=(node_data['color'][0], node_data['color'][1], node_data['color'][2], 50), center=node_data['position'], radius=player_influence_radius)
        
        for _, node_data in graph.nodes(data=True):
            draw.circle( displaysurface, color=node_data['color'], center=node_data['position'], radius=NODE_RADIUS)
        
        # Draws the second transparency_surface overtop the displaysurface.
        displaysurface.blit(transparency_surface, (0,0))

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()
