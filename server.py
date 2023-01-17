class ParseError(Exception):
    def __init__(self):
        pass


class IllegalMove(Exception):
    def __init__(self):
        pass


class GameState:
    def __init__(self):
        pass


class Move:
    def __init__(self):
        # calls self._parse() and returns an exception if there is an error in the message received from the player
        pass

    def _parse(self):
        pass


class Player:
    def __init__(self):
        # setup communication channel with the player's bot
        pass

    def request_move(self):
        # supply the relevant gamestate info to the player, then await their move
        pass


class Game:
    def __init__(self):
        # setup communication with the two(?) players
        # initialise replay and logs
        pass

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
        # while true (or number of turns is less than max turns), play_move
        pass


class Result:
    def __init__(self):
        self.winning_player_id = None  # if =None, the game was a draw
