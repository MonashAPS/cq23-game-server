from __future__ import annotations

import math
import typing as t
from collections import deque

import exceptions
from config import config
from gameObjects.tank import Tank
from map import Map


class Player:
    def __init__(self, player_object: Tank, map: Map, client_info: dict):
        self.gameobject: Tank = player_object
        self.gameobject.id = (
            f"tank-{client_info['id']}"  # Override tank id to have client id
        )

        self.map: Map = map
        self.target: tuple[int, int] | None = None

        self.client_id = client_info["id"]
        self.client_name = client_info["name"]
        self.shoot_cooldown = 0

        self.action = {"path": deque(), "move": False}

    def register_actions(self, actions: t.Optional[dict]) -> t.List:
        """
        register action for the player.
        called at every communication tick.
        """
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        created_game_objects = []
        # dismiss the actions if path and move have been set at the same time
        if actions is None or ("path" in actions and "move" in actions):
            return created_game_objects
        for action in actions:
            if action == "path":
                self._set_path(actions[action])
            if action == "move":
                self._move(actions[action])
            if action == "shoot" and self.shoot_cooldown == 0:
                self.shoot_cooldown = config.BULLET.SHOOT_COOLDOWN
                created_game_objects.append(self._shoot_bullet(angle=actions[action]))
        return created_game_objects

    def tick(self):
        """This will be called at every tick."""
        if not self.action["move"]:
            self._traverse_path()

    def _move(self, angle: float):
        # remove path if manual move is used
        self.action["path"] = deque()

        if angle == -1:
            self.action["move"] = False
        else:
            self.action["move"] = True

            # the magnitude of the vector should be square root of 2
            angle_radians = math.radians(angle)
            self._set_direction(
                (
                    math.sqrt(2) * math.cos(angle_radians),
                    math.sqrt(2) * math.sin(angle_radians),
                )
            )

    def _set_distance_to_target(self):
        self.distance_to_target = sum(
            map(
                lambda a, b: abs(a - b),
                self.gameobject.body.position,
                self.action["path"][0],
            )
        )

    def _traverse_path(self):
        """Move the player through a previously calculated path (self.action["path"]) until the path is complete"""
        if not self.action["path"]:
            self._set_direction(
                (0, 0)
            )  # stop moving the player once the target has been reached
            return
        last_distance_to_target = self.distance_to_target
        self._set_distance_to_target()

        if last_distance_to_target < self.distance_to_target:
            if self.action["path"]:
                self.gameobject.move_to_pos(self.action["path"][0])
        elif self.distance_to_target <= 1:
            self.action["path"].popleft()
            if self.action["path"]:
                self.gameobject.move_to_pos(self.action["path"][0])

    def _set_path(self, coord: tuple[int, int]):
        """calculate and set the path attribute if the target is coord

        Args:
            coord (tuple[int, int]): the target coordinate the function will create a path to
        """
        self.action["move"] = False

        if not coord:
            self.action["path"] = deque()
            return
        try:
            self.action["path"] = deque(
                map(
                    lambda p: self.map.to_global_coords(*p),
                    self.map.path(
                        self.map.from_global_coords(*self.gameobject.body.position),
                        self.map.from_global_coords(*coord),
                    ),
                )
            )
            if len(self.action["path"]) > 0:
                self.action["path"].popleft()
            if self.action["path"]:
                self.gameobject.move_to_pos(self.action["path"][0])
                self._set_distance_to_target()
        except exceptions.CoordinateError:
            # TODO: client input coordinates were out of bounds.
            # The server shouldn't care about coordinates being out of bounds because the game has boundaries.
            self.action["path"] = deque()

        self.target = coord

    def _set_direction(self, direction: tuple[int, int]):
        """manually set the direction that the tank should move towards

        Args:
            direction (tuple[int, int]): The direction the tank should move towards (i.e. (x,y)). (1,1) is up and right
        """
        self.gameobject.set_velocity(direction)

    def _shoot_bullet(self, angle: float):
        return self.gameobject.shoot(angle=angle)
