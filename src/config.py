"""
Example usage:

config = get_config()
config.EXAMPLE_CONSTANT
"""
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


defaults = {"TANK": {"DIMS": (30, 30), "HP": 100}, "MAP": {"DIMS": (500, 500)}}
config = get_config()
