from __future__ import annotations

import math
import typing as t
from collections import deque

import exceptions
from gameObjects.tank import Tank
from map import Map
from replay import ReplayManager


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

        self.action = {"path": deque(), "move": False}

    def register_actions(
        self, actions: t.Optional[dict], replay_manager: ReplayManager
    ) -> t.List:
        """register action for the player"""
        created_game_objects = []
        # dismiss the actions if path and move have been set at the same time
        if actions is None or ("path" in actions and "move" in actions):
            return created_game_objects
        for action in actions:
            if action == "path":
                self._set_path(actions[action])
            if action == "move":
                self._move(actions[action])
            if action == "shoot":
                created_game_objects.append(
                    self._shoot_bullet(
                        angle=actions[action], replay_manager=replay_manager
                    )
                )
        return created_game_objects

    def tick(self):
        """This will be called at every tick."""
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

    def _traverse_path(self):
        """Move the player through a previously calculated path (self.action["path"]) until the path is complete"""
        if self.action["move"]:
            return
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

    def _shoot_bullet(self, angle: float, replay_manager: ReplayManager):
        return self.gameobject.shoot(angle=angle, replay_manager=replay_manager)
