from config import get_config
from gameObjects.game_object import GameObject


class Tank(GameObject):
    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)

        self.health_points = get_config().TANK_HEALTH_POINTS
