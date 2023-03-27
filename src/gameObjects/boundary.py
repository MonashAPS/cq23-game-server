from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter


class Boundary(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        p1: tuple[int, int],
        p2: tuple[int, int],
        is_closing_boundary: bool = False,
    ):
        segment_no = 4  # number of segments for the boundary

        self.shape = [None for _ in range(segment_no)]
        self.body: list[pymunk.Body] = []

        for vel in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if is_closing_boundary:
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                body.velocity = tuple(
                    map(lambda x: x * config.CLOSING_BOUNDARY.VELOCITY, vel)
                )
            else:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (0, 0)
            self.body.append(body)

        if is_closing_boundary:
            self.id = f"closing_boundary-{IDCounter.get_id('closing_boundary')}"
            color = config.CLOSING_BOUNDARY.COLOR
            collision_type = config.COLLISION_TYPE.CLOSING_BOUNDARY
        else:
            self.id = f"boundary-{IDCounter.get_id('boundary')}"
            color = config.BOUNDARY.COLOR
            collision_type = config.COLLISION_TYPE.BOUNDARY

        self.hp = float("inf")

        verts = [
            p1,
            (p1[0], p2[1]),
            p2,
            (p2[0], p1[1]),
        ]

        for i in range(segment_no):
            shape = pymunk.Segment(self.body[i], verts[i], verts[(i + 1) % 4], 2)
            shape.density = config.BOUNDARY.DENSITY
            shape.elasticity = config.BOUNDARY.ELASTICITY
            shape.color = color
            shape.collision_type = collision_type
            shape._boundary_coords = verts[i]
            shape._gameobject = self

            self.shape[i] = shape
            space.add(self.body[i], shape)
