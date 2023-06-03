from __future__ import annotations

from enum import Enum

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter
from util import round_vec2d


class PowerupType(str, Enum):
    HEALTH = "HEALTH"
    DAMAGE = "DAMAGE"
    SPEED = "SPEED"


class Powerup(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        coord: tuple[int, int],
        powerup_type: PowerupType,
        velocity: tuple[float, float] = (0, 0),
    ):
        super().__init__(space, coord, velocity, body_type=pymunk.Body.STATIC)

        self.radius = config.POWERUP.RADIUS
        self.hp = config.POWERUP.HP  # health points

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = config.POWERUP.DENSITY
        self.shape.elasticity = config.POWERUP.ELASTICITY
        self.shape.color = config.POWERUP.COLOR
        self.shape.collision_type = config.COLLISION_TYPE.POWERUP
        self.shape._gameobject = self

        if space:
            self.space.add(self.body, self.shape)

        self.powerup_type = powerup_type
        self.id = f"powerup-{IDCounter.get_id('powerup')}"

    def info(self):
        return {
            "type": self.shape.collision_type,  # this is to let the clients know what type of object this is
            "position": round_vec2d(self.body.position),
            "powerup_type": self.powerup_type,
        }
