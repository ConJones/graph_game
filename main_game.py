import pygame
from pygame.locals import *
import sys

# Global Constants
HEIGHT = 450
WIDTH = 400
FPS = 60

def main():
    # Local Variables

    # Initialize Variables
    pygame.init()
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) 
    vec = pygame.math.Vector2 

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        displaysurface.fill((0,0,0))
        
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()
