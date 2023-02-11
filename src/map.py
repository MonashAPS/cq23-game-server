import numpy as np

from config import config
from gameObjects.game_object import GameObject


class Map:
    def __init__(self, map_name: str, map_size: tuple[int, int] = None):
        """_summary_

        Args:
            map_name (str): name of the json file that holds the map information
            width (int): width of the tile map
            height (int): height of the tile map
        """
        self.map_name = map_name

        if map_size:
            self.width, self.height = map_size
        else:
            self.width, self.height = config.MAP.DIMS

        self.map = np.zeros((self.height, self.width), dtype=GameObject)

        self._load_map()

    def _load_map(self):
        # TODO: decide a format for the map files that are to be loaded.
        pass
