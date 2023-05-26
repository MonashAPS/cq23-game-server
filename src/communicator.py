import json
import logging
from time import sleep

from config import config


class Communicator:
    def __init__(self):
        self.timeout = config.COMMUNICATION.TIMEOUT
        self.client_info = self.get_message()["clients"]

    def post_init_world_message(self, message):
        """
        Prints an init world message - refer to the GCS docs.
        These messages are sent to all clients.
        """
        object_info = message["object_info"]
        current_message = {"events": [], "object_info": {}}

        for key, value in object_info.items():
            if len(current_message["object_info"]) == 10:
                json_message = json.dumps(current_message, separators=(",", ":"))
                print(json_message, flush=True)
                sleep(0.1)
                logging.info(json_message)
                current_message = {"events": [], "object_info": {}}
            current_message["object_info"][key] = value

        if len(current_message["object_info"]) > 0:
            json_message = json.dumps(current_message, separators=(",", ":"))
            print(json_message, flush=True)
            sleep(0.1)
            logging.info(json_message)

    def terminate_init_world_sequence(self):
        print('"END_INIT"', flush=True)
        logging.info('"END_INIT"')

    def post_message(
        self,
        message: str,
        client_id: str = "",
    ):
        print(json.dumps({client_id: message}, separators=(",", ":")), flush=True)
        print(self.timeout, flush=True)

        logging.info(json.dumps({client_id: message}, separators=(",", ":")))
        logging.info(self.timeout)

    def get_message(self):
        return json.loads(input())

    def terminate_game(self):
        print('"END"', flush=True)
