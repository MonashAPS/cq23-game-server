from __future__ import annotations

from collections.abc import Callable, Generator

from yaml import safe_load

from config import config
from exceptions import CoordinateError, MapLoadError
from gameObjects import Bullet, Tank, Wall
from gameObjects.game_object import GameObject


class Map:
    CHARACTER_MAP = {
        ".": None,
        "X": lambda self, y, x, space: Wall(
            space,
            self.to_global_coords(y - 0.5, x - 0.5),
            self.to_global_coords(y + 0.5, x + 0.5),
            False,
        ),
        "D": lambda self, y, x, space: Wall(
            space,
            self.to_global_coords(y - 0.5, x - 0.5),
            self.to_global_coords(y + 0.5, x + 0.5),
            True,
        ),
        "S": lambda self, y, x, space: Tank(space, self.to_global_coords(y, x), (0, 0)),
        "B": lambda self, y, x, space: Bullet(
            space, self.to_global_coords(y, x), (0, 0)
        ),
    }
    TRAVERSABLE = ".SP"
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
        return (
            (x + 0.5) * config.GRID_SCALING,
            (self.map_height - y - 0.5) * config.GRID_SCALING,
        )

    def from_global_coords(self, x, y):
        "From pymunk coordinates to grid coordinates"
        return (
            round(-y / config.GRID_SCALING - 0.5 + self.map_height),
            round(x / config.GRID_SCALING - 0.5),
        )

    def _load_map(self):
        """
        Loads the map. Any existing information will be lost.
        Requires self.map_name to be set.
        """
        # Map format: width/height, ascii grid, yaml
        self.objects: dict[tuple[int, int], GameObject] = {}
        self.fn_objects: dict[tuple[int, int], Callable] = {}
        self.power_up_spawns: list[tuple[int, int]] = []
        self.traversability: list[list[bool]] = []
        with open(self.map_name) as f:
            contents = list(f.readlines())
        self.map_width, self.map_height = list(map(int, contents[0].split()))
        map_ascii = contents[1 : self.map_height + 1]
        yaml = "\n".join(contents[self.map_height + 1 :]).strip()
        self.extra_config = safe_load(yaml)  # TODO: Do something with this.
        for y in range(self.map_height):
            if len(map_ascii[y]) < self.map_width:
                raise MapLoadError(
                    f"Map given in incorrect format. "
                    f"Not enough characters to define {self.map_width} wide "
                    f"by {self.map_height} tall grid"
                )
            self.traversability.append([False] * self.map_width)
            for x in range(self.map_width):
                self._handle_character(y, x, map_ascii[y][x])

        self._precomp()

    def _handle_character(self, y: int, x: int, character: str) -> None:
        """
        Handle actions required for a grid square in the map file.
        Either creations a physics object or has some special functionality.
        """
        if character not in self.CHARACTER_MAP and character not in self.SPECIAL_CHARS:
            raise MapLoadError(
                f"Invalid character found in map file {character} at line {y+2} column {x+1}."
            )
        self.traversability[y][x] = character in self.TRAVERSABLE
        if character in self.CHARACTER_MAP:
            if self.CHARACTER_MAP[character] is not None:
                self.fn_objects[(y, x)] = self.CHARACTER_MAP[character]
        else:
            if character == "P":  # SPECIAL Powerup
                self.power_up_spawns.append((y, x))

    def create_game_objects(self, space) -> Generator[GameObject, None, None]:
        for (y, x), mapper in self.fn_objects.items():
            self.objects[(y, x)] = mapper(self, y, x, space)
            yield self.objects[(y, x)]

    def get_game_objects(self) -> list[GameObject]:
        if not self.objects:
            return []
        return list(self.objects.values())

    def _is_valid_coord(self, y: int, x: int):
        return 0 <= y < self.map_height and 0 <= x < self.map_width

    # PATHFINDING UTILS

    def _precomp(self):
        from pathfinding.core.grid import Grid

        self._gen_special_points()
        self.pf_grid = Grid(matrix=self.traversability)

    def _is_special(self, y, x):
        if not self.traversability[y][x]:
            return False
        points = [
            (y, x + 1),
            (y + 1, x + 1),
            (y + 1, x),
            (y + 1, x - 1),
            (y, x - 1),
            (y - 1, x - 1),
            (y - 1, x),
            (y - 1, x + 1),
            (y, x + 1),
        ]
        for z in range(0, 7, 2):
            if (
                0 <= points[z][0] < self.map_height
                and 0 <= points[z][1] < self.map_width
                and 0 <= points[z + 2][0] < self.map_height
                and 0 <= points[z + 2][1] < self.map_width
            ):
                if (
                    self.traversability[points[z][0]][points[z][1]]
                    and not self.traversability[points[z + 1][0]][points[z + 1][1]]
                    and self.traversability[points[z + 2][0]][points[z + 2][1]]
                ):
                    return True
        return False

    def _gen_special_points(self):
        """
        A special point is one with two traversable tiles adjacent and a non-traversable tile in between.
        This ensures that the shortest path between any tiles on the map can begin with a straight line
        to a special point.
        """
        self.special_points = set()
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self._is_special(y, x):
                    self.special_points.add((y, x))

    def register_wall_broken(self, coords):
        """Call this function when a wall is broken to update pathfinding."""
        from pathfinding.core.node import Node

        av = (coords[0][0] + coords[1][0]) / 2, (coords[0][1] + coords[1][1]) / 2
        (cy, cx) = self.from_global_coords(*av)
        self.pf_grid.nodes[cy][cx] = Node(cx, cy, True)
        self.traversability[cy][cx] = True
        # Re-check if this point or those surrounding is special
        for y in range(cy - 1, cy + 2):
            for x in range(cx - 1, cx + 2):
                if self._is_special(y, x):
                    self.special_points.add((y, x))

    def path(self, c1, c2):
        """
        Finds the shortest path between two grid points,
        when constrained to the grid world (but allowed to move diagonally)
        Inefficient path chosen on large open fields.
        """
        from pathfinding.core.diagonal_movement import DiagonalMovement
        from pathfinding.finder.a_star import AStarFinder

        if not (self._is_valid_coord(*c1) and self._is_valid_coord(*c2)):
            raise CoordinateError(f"Coordinates out of map's bounds: {c1}, {c2}")

        start = self.pf_grid.node(c1[1], c1[0])
        end = self.pf_grid.node(c2[1], c2[0])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        path, runs = finder.find_path(start, end, self.pf_grid)
        self.pf_grid.cleanup()
        return list(map(lambda p: (p[1], p[0]), path))

    def path_shortcut(self, c1, c2):
        """
        Finds a pretty good path on an open gridworld by restricting the grid-path
        to some particular points.
        """
        to_remove = []
        path = self.path(c1, c2)
        for x in range(1, len(path) - 1):
            if path[x] not in self.special_points:
                to_remove.append(x)
        for x in to_remove[::-1]:
            del path[x]
        return path
