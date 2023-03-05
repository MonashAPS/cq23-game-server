from __future__ import annotations

from collections import deque

from gameObjects.tank import Tank
from map import Map


class Player:
    def __init__(self, player_object: Tank, map: Map, client_info: dict):
        self.gameobject: Tank = player_object
        self.map: Map = map
        self.target: tuple[int, int] | None = None

        self.client_id = client_info["id"]
        self.client_name = client_info["name"]

        self.action = {"path": deque(), "shoot": None}

    def register_actions(self, actions: dict):
        """register action for the player"""
        created_game_objects = []
        for action in actions:
            if action == "path":
                self._set_path(actions[action])
            if action == "shoot":
                created_game_objects.append(self._shoot_bullet(actions[action]))
        return created_game_objects

    def tick(self):
        """This will be called at every tick."""
        self._traverse_path()

    def request_move(self):
        # supply the relevant gamestate info to the player, then await their move
        pass

    def _traverse_path(self):
        """Move the player through a previously calculated path (self.action["path"]) until the path is complete"""
        if not self.action["path"]:
            self._set_direction(
                (0, 0)
            )  # stop moving the player once the target has been reached
            return
        if (
            sum(
                map(
                    lambda x, y: abs(x - y),
                    self.gameobject.body.position,
                    self.action["path"][0],
                )
            )
            <= 0.3
        ):  # pymunk coordinates are floating point nums
            self.action["path"].popleft()
            return
        self.gameobject.move_to_pos(self.action["path"][0])

    def _set_path(self, coord: tuple[int, int]):
        """calculate and set the path attribute if the target is coord

        Args:
            coord (tuple[int, int]): the target coordinate the function will create a path to
        """
        self.action["path"] = deque(
            map(
                lambda p: self.map.to_global_coords(*p),
                self.map.path(
                    self.map.from_global_coords(*self.gameobject.body.position),
                    self.map.from_global_coords(*coord),
                ),
            )
        )
        self.target = coord

    def _set_direction(self, direction: tuple[int, int]):
        """manually set the direction that the tank should move towards

        Args:
            direction (tuple[int, int]): The direction the tank should move towards (i.e. (x,y)). (1,1) is up and right
        """
        self.gameobject.set_velocity(direction)

    def _shoot_bullet(self, angle: float):
        return self.gameobject.shoot(angle)
