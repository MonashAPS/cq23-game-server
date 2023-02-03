from gameObjects.game_object import GameObject


class Bullet(GameObject):
    def __init__(self, coord: tuple[int, int], angle: float):
        super().__init__(coord)

        self.angle = angle
