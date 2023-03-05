from __future__ import annotations

import pymunk


class GameObject:
    def __init__(
        self,
        space: pymunk.Space,
        coord: tuple[int, int],
        velocity: tuple[float, float] = (0, 0),
        body_type=pymunk.Body.DYNAMIC,
    ):
        self.space = space
        self.hp = float("inf")

        self.body_type = body_type
        self.body = pymunk.Body(body_type=self.body_type)
        self.body.position = coord
        self.body.velocity = velocity

        self.shape = None

    def is_static(self):
        return self.body_type == pymunk.Body.STATIC

    def apply_damage(self, damage):
        self.hp -= damage
        return self

    def is_destroyed(self):
        return self.hp <= 0
