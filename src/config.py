"""
Example usage:

config = get_config()
config.EXAMPLE_CONSTANT
"""
import math

import dotenv
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
    "TANK": {
        "DIM_MULT": (1, 1),
        "HP": 2,
        "COLOR": (0, 0, 255, 255),
        "DENSITY": 100,
        "VELOCITY": 10,
    },
    "MAP": {
        "PATH": "maps/simple.map"
    },  # TODO: change this so it is the correct path in docker container /codequest/maps/simple.map
    "COLLISION_TYPE": {"TANK": 1, "BULLET": 2, "WALL": 3, "DESTRUCTIBLE_WALL": 4},
    "GRID_SCALING": 20,
    "BULLET": {
        "RADIUS": 5,
        "COLOR": (255, 165, 0, 255),
        "HP": 1,
        "ELASTICITY": 1,
        "DENSITY": 1,
        "DAMAGE": 1,
        "VELOCITY": 30,
    },
    "WALL": {
        "HP": math.inf,
        "DESTRUCTIBLE_HP": 1,
        "COLOR": (0, 0, 0, 255),
        "DESTRUCTIBLE_COLOR": (255, 0, 0, 255),
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
    "SIMULATION": {
        "PHYSICS_TIMESTEP": 1 / 60,
        "PHYSICS_ITERATIONS_PER_COMMUNICATION": 6,
        "COMMUNICATION_POLLING_TIME": 1 / 10,
    },
    "REPLAY": {
        "PATH": "replay.txt",
    },
    "COMMUNICATION": {"TIMEOUT": 0.5},
}
config = get_config()
