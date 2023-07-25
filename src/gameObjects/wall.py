from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter
from util import round_vec2d


class Wall(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        coord: tuple[int, int],
        is_destructible: bool = False,
    ):
        super().__init__(space, coord, body_type=pymunk.Body.STATIC)

        self.is_destructible = is_destructible

        if is_destructible:
            self.hp = config.WALL.DESTRUCTIBLE_HP  # health points
            color = config.WALL.DESTRUCTIBLE_COLOR
            collision_type = config.COLLISION_TYPE.DESTRUCTIBLE_WALL
        else:
            self.hp = float("inf")  # health points
            color = config.WALL.COLOR
            collision_type = config.COLLISION_TYPE.WALL

        self.dims = (
            config.WALL.DIM_MULT[0] * config.GRID_SCALING,
            config.WALL.DIM_MULT[1] * config.GRID_SCALING,
        )

        self.shape = pymunk.Poly.create_box(
            body=self.body, size=self.dims, radius=config.WALL.RADIUS
        )

        self.shape.density = config.WALL.DENSITY
        self.shape.elasticity = config.WALL.ELASTICITY
        self.shape.color = color
        self.shape.collision_type = collision_type
        self.shape._gameobject = self

        self.space.add(self.body, self.shape)

        self.id = f"wall-{IDCounter.get_id('wall')}"

    def info(self):
        info = {
            "type": self.shape.collision_type,  # this is to let the clients know what type of object this is
            "position": round_vec2d(self.body.position),  # bottom left vertex for walls
        }
        if self.hp != float("inf"):
            info["hp"] = self.hp

        return info
