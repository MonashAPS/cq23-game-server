from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Callable

import pymunk

from communicator import Communicator
from config import config
from gameObjects.boundary import Boundary
from gameObjects.bullet import Bullet
from gameObjects.powerup import Powerup, PowerupType
from gameObjects.tank import Tank
from gameObjects.wall import Wall
from map import Map
from player import Player
from replay import Event, ReplayManager


class Game:
    def __init__(self, space: pymunk.Space, map: Map, replay_manager: ReplayManager):
        self.space = space
        self.map = map
        self.game_objects = list(self.map.create_game_objects(self.space))
        self.replay_manager = replay_manager

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
        self.game_objects.append(self.closing_boundary)

        self.tick_count = 0

        self.add_collision_handlers()
        self.remove_collision_handlers()

        self.send_map_info_to_clients()

    def send_map_info_to_clients(self):
        # self.comms.post_init_world_message(...)
        self.comms.terminate_init_world_sequence()

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
                self.bullet_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.BULLET,
                self.bullet_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.DESTRUCTIBLE_WALL,
                self.bullet_collision_handler,
            ),
            (
                config.COLLISION_TYPE.BULLET,
                config.COLLISION_TYPE.WALL,
                self.bullet_collision_handler,
            ),
            (
                config.COLLISION_TYPE.CLOSING_BOUNDARY,
                config.COLLISION_TYPE.TANK,
                self.closing_boundary_collision_handler,
            ),
            (
                config.COLLISION_TYPE.TANK,
                config.COLLISION_TYPE.POWERUP,
                self.powerup_collision_handler,
            ),
        ]

        for coltype_a, coltype_b, handler in collision_groups:
            collision_handler = self.space.add_collision_handler(coltype_a, coltype_b)
            if handler:
                collision_handler.post_solve = handler

    def remove_collision_handlers(self):
        collision_groups: list[tuple[int, int]] = [
            (config.COLLISION_TYPE.BULLET, config.COLLISION_TYPE.POWERUP)
        ]
        for col_type_a, col_type_b in collision_groups:
            poweup_collision_handler = self.space.add_collision_handler(
                col_type_a, col_type_b
            )
            poweup_collision_handler.post_solve = None
            poweup_collision_handler.pre_solve = None
            poweup_collision_handler.separate = None

    def powerup_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        """collision handler for collisions between tanks and powerups

        Args:
            arbiter (pymunk.Arbiter): pymunk provided arg
            space (pymunk.Space): pymunk provided arg
            data (_type_): pymunk provided arg
        """
        for shape in arbiter.shapes:
            if isinstance(shape._gameobject, Powerup):
                powerup: Powerup = shape._gameobject
                space.remove(shape, shape.body)
                self.game_objects.remove(
                    shape._gameobject
                )  # remove reference to game object

        for shape in arbiter.shapes:
            if isinstance(shape._gameobject, Tank):
                shape._gameobject.apply_powerup(powerup)
                self.replay_manager.add_event(
                    Event.powerup_collected(
                        shape._gameobject.id,
                        shape.body.position,
                        powerup.id,
                        powerup.powerup_type,
                    )
                )

    def register_replay_manager_event(self, shape: pymunk.Shape, event: str):
        if event == "HEALTH_LOSS":
            # record health loss in replay file
            if shape.collision_type == config.COLLISION_TYPE.TANK:
                self.replay_manager.add_event(
                    Event.tank_health_loss(shape._gameobject.id, shape.body.position)
                )
            elif shape.collision_type == config.COLLISION_TYPE.DESTRUCTIBLE_WALL:
                self.replay_manager.add_event(
                    Event.wall_health_loss(
                        shape._gameobject.id, shape.get_vertices()[0]
                    )
                )
        elif event == "DESTRUCTION":
            # record destruction in replay file
            if shape.collision_type == config.COLLISION_TYPE.TANK:
                self.replay_manager.add_event(
                    Event.tank_destroyed(shape._gameobject.id, shape.body.position)
                )
            elif shape.collision_type == config.COLLISION_TYPE.DESTRUCTIBLE_WALL:
                self.replay_manager.add_event(
                    Event.wall_destroyed(shape._gameobject.id, shape.get_vertices()[0])
                )
            elif shape.collision_type == config.COLLISION_TYPE.BULLET:
                self.replay_manager.add_event(
                    Event.bullet_destroyed(shape._gameobject.id, shape.body.position)
                )

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
            self.register_replay_manager_event(shape, "HEALTH_LOSS")
            if shape._gameobject.apply_damage(
                config.CLOSING_BOUNDARY.DAMAGE
            ).is_destroyed():
                space.remove(shape, shape.body)
                self.game_objects.remove(
                    shape._gameobject
                )  # remove reference to game object

                self.register_replay_manager_event(shape, "DESTRUCTION")

    def bullet_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        """collision handler for collisions that would cause HP loss to an object caused by a bullet

        Args:
            arbiter (pymunk.Arbiter): pymunk provided arg
            space (pymunk.Space): pymunk provided arg
            data (_type_): pymunk provided arg
        """
        damage = config.BULLET.DAMAGE

        for shape in arbiter.shapes:
            if isinstance(shape._gameobject, Bullet):
                damage = shape._gameobject.damage

        for shape in arbiter.shapes:
            self.register_replay_manager_event(shape, "HEALTH_LOSS")
            if shape._gameobject.apply_damage(damage).is_destroyed():
                if shape.collision_type == config.COLLISION_TYPE.DESTRUCTIBLE_WALL:
                    self.map.register_wall_broken(shape._wall_coords)
                space.remove(shape, shape.body)
                self.game_objects.remove(
                    shape._gameobject
                )  # remove reference to game object

                self.register_replay_manager_event(shape, "DESTRUCTION")

    def handle_client_response(self):
        message = self.comms.get_message()
        for client_id in message:
            self.game_objects.extend(  # keep the reference to any object created
                self.players[client_id].register_actions(
                    actions=message[client_id], replay_manager=self.replay_manager
                )
            )

    def tick(self):
        """called at every tick"""
        self.tick_count += 1
        self._play_turn()
        if self.tick_count % config.TICKS_PER_POWERUP == 0:
            self.spawn_powerup()
        if self._is_terminal():
            self.comms.terminate_game()
            return True
        return False

    def spawn_powerup(self) -> Powerup:
        boundary_vertices = self.closing_boundary.get_vertices()
        xrange = (
            min(map(lambda x: int(x[0]), boundary_vertices)),
            max(map(lambda x: int(x[0]), boundary_vertices)),
        )
        yrange = (
            min(map(lambda x: int(x[1]), boundary_vertices)),
            max(map(lambda x: int(x[1]), boundary_vertices)),
        )

        for _ in range(15):  # 15 retries to find position to plant powerup
            collision_detected = False
            poweup_coord = (random.randint(*xrange), random.randint(*yrange))
            powerup = Powerup(
                space=self.space,
                coord=poweup_coord,
                powerup_type=random.choice(list(PowerupType)),
            )
            for object in self.game_objects:
                if (isinstance(object, Wall) or isinstance(object, Tank)) and len(
                    object.shape.shapes_collide(powerup.shape).points
                ) > 0:
                    collision_detected = True
                    self.space.remove(powerup.shape, powerup.body)
                    del powerup
                    break
            if not collision_detected:
                powerup_type = random.choice(list(PowerupType))
                powerup = Powerup(
                    space=self.space, coord=poweup_coord, powerup_type=powerup_type
                )
                self.replay_manager.add_event(
                    Event.powerup_spawn(
                        powerup.id, powerup.body.position, powerup.powerup_type
                    )
                )
                self.game_objects.append(powerup)
                return powerup

    def _play_turn(self) -> None:
        for player in self.players.values():
            player.tick()

    def _is_terminal(self) -> bool:
        active_players = 0
        for player in self.players.values():
            if player.gameobject.hp > 0:
                active_players += 1
        if active_players > 1:
            return False
        return True

    def results(self) -> defaultdict:
        results = defaultdict(list)
        for playerId, player in self.players.items():
            if player.gameobject.hp > 0:
                results["victor"].append(playerId)
            else:
                results["vanquished"].append(playerId)
        return results
