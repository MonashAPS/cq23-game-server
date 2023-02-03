"""
Example usage:

config = get_config()
config.EXAMPLE_CONSTANT
"""
import dotenv
from addict import Dict

defaults = {"TANK_HEALTH_POINTS": 100, "MAP_SIZE": (50, 50)}


def get_config():
    dotenv.load_dotenv()  # load environment variables from any local .env files

    values = defaults  # load default values
    values.update(
        dotenv.dotenv_values()
    )  # override default values from environment variables
    return Dict(
        values
    )  # using Addict Dict for convenient access of values (see example at top of file)
