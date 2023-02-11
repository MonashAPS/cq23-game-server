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


class Result:
    def __init__(self):
        self.winning_player_id = None  # if =None, the game was a draw
