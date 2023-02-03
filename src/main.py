from game import Game
from gameObjects.bullet import Bullet
from gameObjects.tank import Tank
from map import Map

if __name__ == "__main__":
    game_map = Map(map_name="some_map")
    tank = Tank((0, 0))
    bullet = Bullet((0, 0), 45.0)

    game = Game(map=game_map)
    game.run()
