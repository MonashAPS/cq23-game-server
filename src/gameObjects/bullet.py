import pymunk

from config import config
from gameObjects.game_object import GameObject


class Bullet(GameObject):
    def __init__(
        self, space: pymunk.Space, coord: tuple[int, int], velocity: tuple[int, int]
    ):
        super().__init__(space, coord, velocity)

        self.radius = config.BULLET.RADIUS
        self.HP = config.BULLET.HP  # health points

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.color = config.BULLET.COLOR
        self.shape.collision_type = config.COLLISION_TYPE.BULLET

        self.space.add(self.body, self.shape)
