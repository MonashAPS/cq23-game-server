"""
Example usage:

config = get_config()
config.EXAMPLE_CONSTANT
"""
import math

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
    "TANK": {"DIMS": (30, 30), "HP": 3, "COLOR": pygame.Color("blue"), "DENSITY": 1},
    "MAP": {"DIMS": (500, 500)},
    "COLLISION_TYPE": {"TANK": 1, "BULLET": 2, "WALL": 3, "D_WALL": 4},
    "BULLET": {
        "RADIUS": 5,
        "COLOR": pygame.Color("orange"),
        "HP": 1,
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
    "WALL": {
        "RADIUS": 5,
        "HP": math.inf,
        "COLOR": pygame.Color("black"),
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
    "D_WALL": {"RADIUS": 5, "HP": 1, "COLOR": pygame.Color("red"), "DENSITY": 1},
}
config = get_config()