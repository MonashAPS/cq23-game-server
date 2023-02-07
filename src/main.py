import pygame
import pymunk

from config import config
from gameObjects.tank import Tank


def run_pygame():
    pygame.init()

    # Set up the drawing window
    display = pygame.display.set_mode(config.MAP.DIMS)

    # example tank
    tank = Tank(space, (200, 200), (50, 50))

    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        display.fill((255, 255, 255))

        # Draw a tank
        tank.draw(display)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


def run_pymunk():
    # example tank
    tank = Tank(space, (200, 200), (50, 50))
    tank.body.position = (201, 201)


if __name__ == "__main__":
    # setup pymunk
    space = pymunk.Space()

    if True:  # run game in pygame
        run_pygame()
    else:
        run_pymunk()
