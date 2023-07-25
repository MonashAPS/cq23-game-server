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
        "HP": 10,
        "COLOR": (0, 0, 255, 255),
        "DENSITY": 100,
        "VELOCITY": 100,
        "RADIUS": 0.1,
    },
    "MAP": {"NUKETOWN": "nuketown.map", "DIR": "maps/"},
    "COLLISION_TYPE": {
        "TANK": 1,
        "BULLET": 2,
        "WALL": 3,
        "DESTRUCTIBLE_WALL": 4,
        "BOUNDARY": 5,
        "CLOSING_BOUNDARY": 6,
        "POWERUP": 7,
        "PATH": 8,
    },
    "GRID_SCALING": 20,
    "BULLET": {
        "RADIUS": 5,
        "COLOR": (255, 165, 0, 255),
        "HP": 1,
        "ELASTICITY": 1,
        "DENSITY": 1,
        "DAMAGE": 1,
        "VELOCITY": 450,
    },
    "WALL": {
        "HP": math.inf,
        "DESTRUCTIBLE_HP": 1,
        "COLOR": (0, 0, 0, 255),
        "DESTRUCTIBLE_COLOR": (255, 0, 0, 255),
        "ELASTICITY": 1,
        "DENSITY": 1,
        "RADIUS": 0.1,
        "DIM_MULT": (0.9, 0.9),
    },
    "BOUNDARY": {
        "HP": math.inf,
        "COLOR": (38, 205, 38, 0),
        "ELASTICITY": 1,
        "DENSITY": 1,
    },
    "CLOSING_BOUNDARY": {
        "COLOR": (205, 38, 38, 0),
        "DAMAGE": 1,
        "VELOCITY": 10,
    },
    "SIMULATION": {
        "PHYSICS_TIMESTEP": 1 / 6000,
        "PHYSICS_ITERATIONS_PER_COMMUNICATION": 15,
        "PYGAME_FPS": 60,
        "PYMUNK_TIMESTEP_ITERATIONS": 100,
    },
    "REPLAY": {
        "PATH": "replay/replay",
        "LIVE_PATH": "live-replay/replay",
    },
    "COMMUNICATION": {"TIMEOUT": 0.1},
    "POWERUP": {
        "RADIUS": 15,
        "COLOR": (255, 165, 255, 0),
        "HP": math.inf,
        "ELASTICITY": 1,
        "DENSITY": 1,
        "HP_BOOST": 2,
        "BULLET_BOOST": 2,
        "SPEED_BOOST": 2,
    },
    "TICKS_PER_POWERUP": 25000,
}
config = get_config()
