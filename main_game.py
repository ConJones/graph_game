import pygame
from pygame.locals import *
import sys
import random

# Global Constants
WIDTH = 1920
HEIGHT = 1080
FPS = 1

def main():
    # Local Variables
    color_node = ((119, 185, 224),(99, 101, 207),(186, 125, 219),(255, 115, 157),(255, 238, 135),(166, 207, 99))

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
        
        displaysurface.fill((51, 51, 51))

        for dot in range(400):       
            coords = (WIDTH*random.random(),HEIGHT*random.random())

            pygame.draw.line(displaysurface, (255,255,255), coords, (WIDTH*random.random(),HEIGHT*random.random()), 1)

            pygame.draw.circle(displaysurface, random.choice(color_node), coords, 5)

            

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()
