import pymunk

from config import config
from gameObjects.game_object import GameObject


class Wall(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        endpoint1: tuple[int, int],
        endpoint2: tuple[int, int],
    ):
        super().__init__(space, (0, 0), body_type=pymunk.Body.STATIC)

        self.radius = config.WALL.RADIUS
        self.HP = config.WALL.HP  # health points

        self.shape = pymunk.Segment(self.body, endpoint1, endpoint2, self.radius)
        self.shape.density = 1
        self.shape.collision_type = config.COLLISION_TYPE.WALL
        self.space.add(self.body, self.shape)
