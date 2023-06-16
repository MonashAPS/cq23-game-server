from __future__ import annotations

from math import copysign, cos, radians, sin, sqrt

import pymunk

from config import config
from gameObjects.bullet import Bullet
from gameObjects.game_object import GameObject, IDCounter
from gameObjects.powerup import Powerup, PowerupType
from replay import ReplayManager
from util import round_vec2d


class Tank(GameObject):
    def __init__(
        self, space: pymunk.Space, coord: tuple[int, int], velocity: tuple[float, float]
    ):
        super().__init__(space, coord, velocity)

        self.dims = (
            config.TANK.DIM_MULT[0] * config.GRID_SCALING,
            config.TANK.DIM_MULT[1] * config.GRID_SCALING,
        )
        self.hp = config.TANK.HP  # health points

        self.shape = pymunk.Poly.create_box(body=self.body, size=self.dims, radius=0)
        self.shape.density = config.TANK.DENSITY
        self.shape.collision_type = config.COLLISION_TYPE.TANK
        self.shape._gameobject = self

        self.space.add(self.body, self.shape)

        # multiplier for velocity
        self.velocity_mult = 1

        # the tank determines the damage for a bullet. this value changes when powerups are activated
        self.bullet_damage = config.BULLET.DAMAGE

        # prevent tanks from rotating. moment has to be set after the body is added to the space
        self.body.moment = float("inf")

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
            direction[0] * config.TANK.VELOCITY * self.velocity_mult,
            direction[1] * config.TANK.VELOCITY * self.velocity_mult,
        )

    def shoot(self, angle: float, replay_manager: ReplayManager):
        angle_radians = radians(angle)
        bullet = Bullet(
            space=self.space,
            coord=tuple(
                map(
                    lambda tank, safe_space, offset: tank + offset + safe_space,
                    self.body.position,
                    (0, 0),
                    (
                        cos(angle_radians) * (self.get_radius() + config.BULLET.RADIUS),
                        sin(angle_radians) * (self.get_radius() + config.BULLET.RADIUS),
                    ),
                )
            ),
            velocity=(
                cos(angle_radians) * config.BULLET.VELOCITY,
                sin(angle_radians) * config.BULLET.VELOCITY,
            ),
            damage=self.bullet_damage,
        )

        return bullet

    def get_radius(self):
        return sqrt((self.dims[0] / 2) ** 2 + (self.dims[1] / 2) ** 2)

    def info(self):
        return {
            "type": self.shape.collision_type,  # this is to let the clients know what type of object this is
            "position": round_vec2d(self.body.position),
            "velocity": round_vec2d(self.body.velocity),
            "hp": "inf" if self.hp == float("inf") else self.hp,
        }

    def apply_powerup(self, powerup: Powerup):
        if powerup.powerup_type == PowerupType.HEALTH:
            self.hp += config.POWERUP.HP_BOOST
        elif powerup.powerup_type == PowerupType.SPEED:
            self.velocity_mult = config.POWERUP.SPEED_BOOST
        elif powerup.powerup_type == PowerupType.DAMAGE:
            self.bullet_damage = config.POWERUP.BULLET_BOOST
