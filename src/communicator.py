import json
import logging

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
        json_message = json.dumps(message)
        print(json_message, flush=True)
        logging.info(json_message)

    def terminate_init_world_sequence(self):
        print(json.dumps("END_INIT"), flush=True)
        logging.info(json.dumps("END_INIT"))

    def post_message(
        self,
        message: str,
        client_id: str = "",
    ):
        print(json.dumps({client_id: message}), flush=True)
        print(self.timeout)
        logging.info(json.dumps({client_id: message}))
        logging.info(self.timeout)

    def get_message(self):
        return json.loads(input())

    def terminate_game(self):
        print('"END"', flush=True)
