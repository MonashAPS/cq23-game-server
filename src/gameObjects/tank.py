import pygame
import pymunk

from config import config
from gameObjects.game_object import GameObject
from utils import convert_to_pygame_coord


class Tank(GameObject):
    def __init__(
        self, space: pymunk.Space, coord: tuple[int, int], velocity: tuple[int, int]
    ):
        super().__init__(space, coord, velocity)

        self.dims = config.TANK.DIMS
        self.HP = config.TANK.HP  # health points

        self.shape = pymunk.Poly.create_box(self.body, self.dims)
        self.space.add(self.body, self.shape)

    def draw(
        self, pygame_display: pygame.surface.Surface, color=pygame.Color("orange")
    ):
        pygame.draw.rect(
            pygame_display,
            color,
            pygame.Rect(
                convert_to_pygame_coord(
                    self.body.position, pygame_display.get_height()
                ),
                self.dims,
            ),
        )
