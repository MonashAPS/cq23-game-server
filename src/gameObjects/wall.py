import pymunk

from config import config
from gameObjects.game_object import GameObject


class Wall(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        endpoint1: tuple[int, int],
        endpoint2: tuple[int, int],
        is_destructible: bool = False,
    ):
        super().__init__(space, (0, 0), body_type=pymunk.Body.STATIC)

        self.is_destructible = is_destructible
        self.radius = config.WALL.RADIUS

        if is_destructible:
            self.hp = config.WALL.HP  # health points
            color = config.WALL.DESTRUCTIBLE_COLOR
            collision_type = config.COLLISION_TYPE.DESTRUCTIBLE_WALL
        else:
            self.hp = float("inf")  # health points
            color = config.WALL.COLOR
            collision_type = config.COLLISION_TYPE.WALL

        self.shape = pymunk.Segment(self.body, endpoint1, endpoint2, self.radius)
        self.shape.density = config.WALL.DENSITY
        self.shape.elasticity = config.WALL.ELASTICITY
        self.shape.color = color
        self.shape.collision_type = collision_type

        self.space.add(self.body, self.shape)
