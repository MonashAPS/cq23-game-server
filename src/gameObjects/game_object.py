import pymunk


class GameObject:
    def __init__(
        self,
        space: pymunk.Space,
        coord: tuple[int, int],
        velocity: tuple[int, int] = (0, 0),
        body_type=pymunk.Body.DYNAMIC,
    ):
        self.space = space

        self.body_type = body_type
        self.body = pymunk.Body(body_type=self.body_type)
        self.body.position = coord
        self.body.velocity = velocity

    def is_static(self):
        return self.body_type == pymunk.Body.STATIC