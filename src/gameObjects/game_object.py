import pymunk


class GameObject:
    def __init__(
        self, space: pymunk.Space, coord: tuple[int, int], velocity: tuple[int, int]
    ):
        self.space = space

        self.body = pymunk.Body()
        self.body.position = coord
        self.body.velocity = velocity
