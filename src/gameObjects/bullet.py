from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter


class Bullet(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        coord: tuple[int, int],
        velocity: tuple[float, float],
        damage: int = config.BULLET.DAMAGE,
    ):
        super().__init__(space, coord, velocity)

        self.radius = config.BULLET.RADIUS
        self.hp = config.BULLET.HP  # health points

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = config.BULLET.DENSITY
        self.shape.elasticity = config.BULLET.ELASTICITY
        self.shape.color = config.BULLET.COLOR
        self.shape.collision_type = config.COLLISION_TYPE.BULLET
        self.shape._gameobject = self

        self.space.add(self.body, self.shape)

        self.damage = damage

        self.id = f"bullet-{IDCounter.get_id('bullet')}"

    def info(self):
        return {
            "type": self.shape.collision_type,  # this is to let the clients know what type of object this is
            "position": self.body.position,
            "velocity": self.body.velocity,
            "hp": "inf" if self.hp == float("inf") else self.hp,
        }
