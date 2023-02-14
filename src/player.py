import math
from collections import deque

from gameObjects.tank import Tank
from map import Map


class Player:
    def __init__(self, player_object: Tank, map: Map):
        self.object: Tank = player_object
        self.map: Map = map
        self.path: deque = deque()
        self.target: tuple[int, int] | None = None

        # TODO: setup communication channel with the player's bot

    def tick(self):
        self._traverse_path()

    def request_move(self):
        # supply the relevant gamestate info to the player, then await their move
        pass

    def _traverse_path(self):
        if not self.path:
            self._set_direction(
                (0, 0)
            )  # stop moving the player once the target has been reached
            return
        if (
            tuple(map(math.floor, self.object.body.position)) == self.path[0]
        ):  # pymunk coordinates are floating point nums
            self.path.popleft()
            return
        self.object.move_to_pos(self.path[0])

    def _set_path(self, coord: tuple[int, int]):
        self.path = deque(
            map(
                lambda p: self.map.to_global_coords(*p),
                self.map.path(
                    self.map.from_global_coords(*self.object.body.position),
                    self.map.from_global_coords(*coord),
                ),
            )
        )
        self.target = coord

    def _set_direction(self, direction: tuple[int, int]):
        self.object.set_velocity(direction)
