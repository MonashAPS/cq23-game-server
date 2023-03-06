from __future__ import annotations

from collections import defaultdict

import pymunk


class IDCounter:
    """Subclassed for GameObject instances so keys are unique and useful."""

    _tracking = defaultdict(lambda: 0)

    @classmethod
    def get_id(cls, id_type: str) -> int:
        cls._tracking[id_type] += 1
        return cls._tracking[id_type]


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

        # Should not use but here for demonstrative purposes.
        self.id = f"BLANK-{IDCounter.get_id('blank')}"

    def is_static(self):
        return self.body_type == pymunk.Body.STATIC

    def apply_damage(self, damage):
        self.hp -= damage
        return self

    def is_destroyed(self):
        return self.hp <= 0
