from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter
from util import round_vec2d


class Bullet(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        tank_id: str,
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
        self.tank_id = tank_id

    def info(self):
        return {
            "type": self.shape.collision_type,  # this is to let the clients know what type of object this is
            "tank_id": self.tank_id,
            "position": round_vec2d(self.body.position),
            "velocity": round_vec2d(self.body.velocity),
            "damage": self.damage,
        }
