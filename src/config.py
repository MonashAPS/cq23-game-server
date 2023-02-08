"""
Example usage:

config = get_config()
config.EXAMPLE_CONSTANT
"""
import dotenv
import pygame
from addict import Dict


def get_config():
    dotenv.load_dotenv()  # load environment variables from any local .env files

    values = defaults  # load default values
    values.update(
        dotenv.dotenv_values()
    )  # override default values from environment variables
    return Dict(
        values
    )  # using Addict Dict for convenient access of values (see example at top of file)


defaults = {
    "TANK": {"DIMS": (30, 30), "HP": 100, "COLOR": pygame.Color("blue")},
    "MAP": {"DIMS": (500, 500)},
    "COLLISION_TYPE": {"TANK": 1, "BULLET": 2, "WALL": 3},
    "BULLET": {"RADIUS": 5, "COLOR": pygame.Color("orange")},
}
config = get_config()
