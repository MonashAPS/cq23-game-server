from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

import pymunk

from communicator import Communicator
from config import config
from gameObjects.boundary import Boundary
from gameObjects.tank import Tank
from map import Map
from player import Player


class Game:
    def __init__(self, space: pymunk.Space, map: Map):
        self.space = space
        self.map = map
        self.game_objects = list(self.map.create_game_objects(self.space))

        self.comms = Communicator()
        tanks = filter(lambda go: isinstance(go, Tank), self.game_objects)
        self.players = {
            client_info["id"]: Player(tank, map, client_info)
            for tank, client_info in zip(tanks, self.comms.client_info)
        }

        # create map boundary
        self.boundary = Boundary(
            self.space,
            self.map.to_global_coords(-0.5, -0.5),
            self.map.to_global_coords(
                self.map.map_height - 0.5, self.map.map_width - 0.5
            ),
        )
        self.closing_boundary = Boundary(
            self.space,
            self.map.to_global_coords(-0.5, -0.5),
            self.map.to_global_coords(
                self.map.map_height - 0.5, self.map.map_width - 0.5
            ),
            is_closing_boundary=True,
        )
        self.game_objects.append(self.boundary)

        self.add_collision_handlers()

    def add_collision_handlers(self):
        """register all collision handlers in the pymunk space"""
        collision_groups: list[tuple[int, int, Callable | None]] = [
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.WALL, None),
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.DESTRUCTIBLE_WALL, None),
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.TANK, None),
            (config.COLLISION_TYPE.BOUNDARY, config.COLLISION_TYPE.TANK, None),
            (config.COLLISION_TYPE.BOUNDARY, config.COLLISION_TYPE.BULLET, None),
            (
                config.COLLISION_TYPE.CLOSING_BOUNDARY,
                config.COLLISION_TYPE.BULLET,
                None,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.TANK,
                self.damage_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.BULLET,
                self.damage_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.DESTRUCTIBLE_WALL,
                self.damage_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.WALL,
                self.damage_collision_handler,
            ),
            (
                config.COLLISION_TYPE.CLOSING_BOUNDARY,
                config.COLLISION_TYPE.TANK,
                self.closing_boundary_collision_handler,
            ),
        ]

        for coltype_a, coltype_b, handler in collision_groups:
            collision_handler = self.space.add_collision_handler(coltype_a, coltype_b)
            if handler:
                collision_handler.post_solve = handler

    def closing_boundary_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        """collision handler for collisions with the closing boundary

        Args:
            arbiter (pymunk.Arbiter): pymunk provided arg
            space (pymunk.Space): pymunk provided arg
            data (_type_): pymunk provided arg
        """

        for shape in arbiter.shapes:
            if shape._gameobject.apply_damage(
                config.CLOSING_BOUNDARY.DAMAGE
            ).is_destroyed():
                self.space.remove(shape, shape.body)
                self.game_objects.remove(
                    shape._gameobject
                )  # remove reference to game object

    def damage_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        """collision handler for collisions that would cause HP loss to an object

        Args:
            arbiter (pymunk.Arbiter): pymunk provided arg
            space (pymunk.Space): pymunk provided arg
            data (_type_): pymunk provided arg
        """

        for shape in arbiter.shapes:
            if shape._gameobject.apply_damage(config.BULLET.DAMAGE).is_destroyed():
                # TODO: remove the destroyed object from the map
                if shape.collision_type == config.COLLISION_TYPE.DESTRUCTIBLE_WALL:
                    self.map.register_wall_broken(shape._wall_coords)
                self.space.remove(shape, shape.body)
                self.game_objects.remove(
                    shape._gameobject
                )  # remove reference to game object

    def handle_client_response(self):
        message = self.comms.get_message()
        for client_id in message:
            self.game_objects.extend(  # keep the reference to any object created
                self.players[client_id].register_actions(message[client_id])
            )

    def tick(self):
        """called at every tick"""
        self._play_turn()
        if self._is_terminal():
            self.comms.terminate_game()
            return True
        return False

    def _play_turn(self):
        for player in self.players.values():
            player.tick()

    def _is_terminal(self):
        active_players = 0
        for player in self.players.values():
            if player.gameobject.hp > 0:
                active_players += 1
        if active_players > 1:
            return False
        return True

    def results(self):
        results = defaultdict(list)
        for playerId, player in self.players.items():
            if player.gameobject.hp > 0:
                results["victor"].append(playerId)
            else:
                results["vanquished"].append(playerId)
        return results
