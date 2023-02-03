import logging

from map import Map


class Game:
    def __init__(self, map: Map):
        # setup communication with the two(?) players
        # initialise replay and logs
        self.map = map

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
