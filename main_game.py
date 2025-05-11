import pygame
from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
import sys
import networkx as nx
import force_directed_graph as fdg

# Global Constants
WIDTH = 1920
HEIGHT = 1080
NODE_RADIUS = 20
SCREEN_EDGE_BUFFER = NODE_RADIUS + 10
FPS = 144
CREATE_INFLUENCE = False
NUM_NODES = 4
NUM_EDGES = 4

# NODE COLORS in RGBA (Left to right): Blue, Indigo, Purple,
#                                      Pink, Yellow, Green.
NODE_COLORS = ((119, 185, 224, 100),(99, 101, 207, 100),(186, 125, 219, 100),
               (255, 115, 157, 100),(255, 238, 135, 100),(166, 207, 99, 100))

# Functions

# Main
def main():
    # Local Variables
    graph = fdg.force_directed_graph( NUM_NODES, NUM_EDGES, NODE_COLORS )

    # Radius of the circle of influence for player.
    player_influence_radius = 15

    # Initialize Variables
    pygame.init()
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    transparency_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

    # Main loop
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                graph = fdg.force_directed_graph( NUM_NODES, NUM_EDGES, NODE_COLORS )

        # Update Spring graph
        graph.force_directed_graph_step()

        # Render
        transparency_surface.fill((51,51,51,0))
        displaysurface.fill((51,51,51))

        for edge in graph.edges:
            draw.aaline(displaysurface, (255, 255, 255), graph.nodes[edge[0]]['position'], graph.nodes[edge[1]]['position'], 1 )

        # Sphere of Influence Generation
        if CREATE_INFLUENCE:
            player_influence_radius = player_influence_radius * 1.25
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
