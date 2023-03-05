from __future__ import annotations

from math import copysign

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter


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
        self.shape._gameobject = self

        self.space.add(self.body, self.shape)

        self.id = f"tank-{IDCounter.get_id('tank')}"

    def move_to_pos(self, coord: tuple[int, int]):
        """This function can be called when the tank needs to be moved to a specific pymunk coordinate.
        The tank's velocity will be set so that it is travelling towards coord.

        Args:
            coord (tuple[int, int]): coordinate to move to
        """
        px, py = self.body.position  # current position
        tx, ty = coord  # target coordinates
        dx = copysign(1, tx - px)  # x direction
        dy = copysign(1, ty - py)  # y direction
        self.set_velocity((dx, dy))

    def set_velocity(self, direction: tuple[float, float]):
        """Set the velocity of the tank.

        Args:
            direction (tuple[float, float]): The direction the tank should move towards (x,y). (1,1) is up and right
        """
        self.body.velocity = (
            direction[0] * config.TANK.VELOCITY,
            direction[1] * config.TANK.VELOCITY,
        )
