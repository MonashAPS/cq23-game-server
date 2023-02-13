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
    "TANK": {"DIM_MULT": (1, 1), "HP": 3, "COLOR": pygame.Color("blue"), "DENSITY": 1},
    "MAP": {"PATH": "maps/simple.map"},
    "COLLISION_TYPE": {"TANK": 1, "BULLET": 2, "WALL": 3, "DESTRUCTIBLE_WALL": 4},
    "GRID_SCALING": 20,
    "BULLET": {
        "RADIUS": 5,
        "COLOR": pygame.Color("orange"),
        "HP": 1,
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
    "WALL": {
        "HP": math.inf,
        "COLOR": pygame.Color("black"),
        "DESTRUCTIBLE_COLOR": pygame.Color("red"),
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
}
config = get_config()
