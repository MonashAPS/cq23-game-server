from __future__ import annotations
import numpy as np
from typing import Generator
from yaml import safe_load

from config import config
from gameObjects.game_object import GameObject
from gameObjects import Wall, Tank

class MapLoadError(Exception):
    pass


class Map:
    # map(self, y, x, space) -> Physics object.
    CHARACTER_MAP = {
        ".": None,
        "X": lambda self, y, x, space: Wall(
            space,
            self.to_global_coords(y-0.5, x-0.5),
            self.to_global_coords(y+0.5, x+0.5),
            False
        ),
        "D": lambda self, y, x, space: Wall(
            space,
            self.to_global_coords(y-0.5, x-0.5),
            self.to_global_coords(y+0.5, x+0.5),
            True
        ),
        "S": lambda self, y, x, space: Tank(space, self.to_global_coords(y, x), (0, 0)),
    }
    SPECIAL_CHARS = "P"

    def __init__(self, map_name: str):
        """_summary_

        Args:
            map_name (str): name of the json file that holds the map information
        """
        self.map_name = map_name

        self._load_map()

    def to_global_coords(self, y, x):
        """Translates grid coordinates to pymunk space coordinates in the same visual direction."""
        return ((x+0.5) * config.GRID_SCALING, (self.map_height - y - 0.5) * config.GRID_SCALING)

    def _load_map(self):
        """
        Loads the map. Any existing information will be lost.
        Requires self.map_name to be set.
        """
        # Map format: width/height, ascii grid, yaml
        self.objects: list[tuple[int, int, function]] = []
        self.power_up_spawns: list[tuple[int, int]] = []
        with open(self.map_name, "r") as f:
            contents = list(f.readlines())
        self.map_width, self.map_height = list(map(int, contents[0].split()))
        map_ascii = contents[1:self.map_height+1]
        yaml = "\n".join(contents[self.map_height+1:]).strip()
        self.extra_config = safe_load(yaml)  # TODO: Do something with this.
        self.map = np.zeros((self.map_height, self.map_width), dtype=GameObject)
        for y in range(self.map_height):
            if len(map_ascii[y]) < self.map_width:
                raise MapLoadError(
                    f"Map given in incorrect format. "
                    f"Not enough characters to define {self.map_width} wide "
                    f"by {self.map_height} tall grid"
                )
            for x in range(self.map_width):
                self._handle_character(y, x, map_ascii[y][x])

    def _handle_character(self, y: int, x: int, character: str) -> None:
        """
        Handle actions required for a grid square in the map file.
        Either creations a physics object or has some special functionality.
        """
        if (
            character not in self.CHARACTER_MAP and
            character not in self.SPECIAL_CHARS
        ):
            raise MapLoadError(
                f"Invalid character found in map file {character} at line {y+2} column {x+1}."
            )
        if character in self.CHARACTER_MAP:
            if self.CHARACTER_MAP[character] is not None:
                self.objects.append((y, x, self.CHARACTER_MAP[character]))
        else:                         # SPECIAL
            if character == "P":      # Powerup
                self.power_up_spawns.append((y, x))

    def create_game_objects(self, space) -> Generator[GameObject]:
        for y, x, mapper in self.objects:
            yield mapper(self, y, x, space)
