import pygame
import pymunk
import pymunk.pygame_util

from config import config
from game import Game
from map import Map
from gameObjects.bullet import Bullet
from gameObjects.tank import Tank
from gameObjects.wall import Wall


def run_pygame():
    # PyGame init
    pygame.init()
    m = Map(config.MAP.PATH)
    display = pygame.display.set_mode((m.map_width * config.GRID_SCALING, m.map_height * config.GRID_SCALING))
    clock = pygame.time.Clock()
    FPS = 50
    running = True
    # Physics stuff
    space = pymunk.Space()
    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(display)  # type: ignore

    # example objects
    Game(space)

    objects = list(m.create_game_objects(space))

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        display.fill(pygame.Color("white"))

        # Draw stuff
        space.debug_draw(draw_options)

        state = []
        for x in space.shapes:
            s = f"{x} {x.body.position} {x.body.velocity}"
            state.append(s)

        # Update physics
        space.step(1 / FPS)

        pygame.display.flip()
        clock.tick(FPS)

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
