from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject


class Tank(GameObject):
    def __init__(
        self, space: pymunk.Space, coord: tuple[int, int], velocity: tuple[int, int]
    ):
        super().__init__(space, coord, velocity)

        self.dims = (
            config.TANK.DIM_MULT[0] * config.GRID_SCALING,
            config.TANK.DIM_MULT[1] * config.GRID_SCALING,
        )
        self.hp = config.TANK.HP  # health points

        self.shape = pymunk.Poly.create_box(self.body, self.dims)
        self.shape.density = config.TANK.DENSITY
        self.shape.collision_type = config.COLLISION_TYPE.TANK
        self.space.add(self.body, self.shape)

    def move_to_pos(self, coord: tuple[int, int]):
        px, py = self.body.position  # current position
        tx, ty = coord  # target coordinates
        dx = 1 - ((tx - px) <= 0)  # x direction
        dy = 1 - ((ty - py) <= 0)  # y direction
        self.set_velocity((dx, dy))

    def set_velocity(self, direction: tuple[int, int]):
        self.body.velocity = (
            direction[0] * config.TANK.VELOCITY,
            direction[1] * config.TANK.VELOCITY,
        )
