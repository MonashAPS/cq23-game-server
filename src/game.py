import logging
from collections.abc import Callable

import pymunk

from config import config
from map import Map


class Game:
    def __init__(self, space: pymunk.Space, m: Map):
        self.space = space
        self.map = m
        self.add_collision_handlers()

    def add_collision_handlers(self):
        collision_groups: list[tuple[int, int, Callable | None]] = [
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.WALL, None),
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.DESTRUCTIBLE_WALL, None),
            (config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.TANK, None),
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
        ]

        for coltype_a, coltype_b, handler in collision_groups:
            collision_handler = self.space.add_collision_handler(coltype_a, coltype_b)
            if handler:
                collision_handler.post_solve = handler

    def damage_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        game_objects = self.map.get_game_objects()

        for go in game_objects:
            for shape in arbiter.shapes:
                if shape == go.shape:
                    if go.apply_damage(config.BULLET.DAMAGE).is_destroyed():
                        # TODO: remove the destroyed object from the map
                        if (
                            shape.collision_type
                            == config.COLLISION_TYPE.DESTRUCTIBLE_WALL
                        ):
                            self.map.register_wall_broken(shape._wall_coords)
                        self.space.remove(shape, shape.body)

    def _initialise_state(self):
        # initialise the map by either loading from a file or randomly generating one (handled by other methods)
        # select spawn location for players, etc
        pass

    def _play_turn(self):
        # request move from each player
        # check if the moves are valid in the context of the gamestate (e.g. check bot has ammo if trying to shoot)
        # play moves
        # update the gamestate for a single tick (calculate collisions, bullet movements, closing map ring, etc)
        # if the game is terminal, return the result
        pass

    def _is_terminal(self):
        # check which players still have hp
        # if both players have 0 hp, it is a draw. Else the player with 0 hp loses
        pass

    def run(self):
        # initialise state
        logging.info("Starting game between players: ... and ...")
        # while true (or number of turns is less than max turns), play_move
        pass
