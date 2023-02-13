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

    def set_velocity(self, velocity: tuple[int, int]):
        self.body.velocity = velocity
