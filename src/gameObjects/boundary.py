from __future__ import annotations

import pymunk

from config import config
from gameObjects.game_object import GameObject, IDCounter
from util import round_vec2d


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

        self.verts = [
            p1,
            (p1[0], p2[1]),
            p2,
            (p2[0], p1[1]),
        ]

        for i in range(segment_no):
            shape = pymunk.Segment(
                self.body[i], self.verts[i], self.verts[(i + 1) % 4], 2
            )
            shape.density = config.BOUNDARY.DENSITY
            shape.elasticity = config.BOUNDARY.ELASTICITY
            shape.color = color
            shape.collision_type = collision_type
            shape._boundary_coords = self.verts[i]
            shape._gameobject = self

            self.shape[i] = shape
            space.add(self.body[i], shape)

    def get_vertices(self):
        pos = [
            [x.position[0] + self.verts[i][0], x.position[1] + self.verts[i][1]]
            for i, x in enumerate(self.body)
        ]
        return list(
            map(
                round_vec2d,
                [
                    [pos[0][0], pos[3][1]],
                    [pos[0][0], pos[1][1]],
                    [pos[2][0], pos[1][1]],
                    [pos[2][0], pos[3][1]],
                ],
            )
        )

    def info(self):
        return {
            "type": self.shape[
                0
            ].collision_type,  # this is to let the clients know what type of object this is
            "position": self.get_vertices(),
            "velocity": [x.velocity for x in self.body],
            "hp": "inf" if self.hp == float("inf") else self.hp,
        }
