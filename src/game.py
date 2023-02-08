import logging

import pymunk

from config import config


class Game:
    def __init__(self, space: pymunk.Space):
        self.space = space
        self.add_collision_handlers()

    def add_collision_handlers(self):
        # add bullet-tank collision handler
        bullet_tank_handler = self.space.add_collision_handler(
            config.COLLISION_TYPE.TANK, config.COLLISION_TYPE.BULLET
        )
        bullet_tank_handler.post_solve = self.post_solve_collision_handler
        # add bullet-wall collision handler
        bullet_wall_handler = self.space.add_collision_handler(
            config.COLLISION_TYPE.WALL, config.COLLISION_TYPE.BULLET
        )
        bullet_wall_handler.post_solve = self.post_solve_collision_handler

    def post_solve_collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data
    ):
        shape1, shape2 = arbiter.shapes
        self.space.remove(shape1, shape1.body)
        self.space.remove(shape2, shape2.body)

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
