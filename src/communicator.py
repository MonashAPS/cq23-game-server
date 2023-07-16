import json
import logging
from time import sleep

from config import config


class Communicator:
    def __init__(self):
        self.timeout = config.COMMUNICATION.TIMEOUT
        self.client_info = self.get_message()["clients"]

        for client in self.client_info:
            client["id"] = str(client["id"])

        self.post_client_ids()

    def post_client_ids(self):
        print(
            json.dumps(
                {
                    self.client_info[0]["id"]: {
                        "your-tank-id": f"tank-{self.client_info[0]['id']}",
                        "enemy-tank-id": f"tank-{self.client_info[1]['id']}",
                    },
                    self.client_info[1]["id"]: {
                        "your-tank-id": f"tank-{self.client_info[1]['id']}",
                        "enemy-tank-id": f"tank-{self.client_info[0]['id']}",
                    },
                },
                separators=(",", ":"),
            ),
            flush=True,
        )
        print(0.1, flush=True)
        sleep(0.1)

    def post_init_world_message(self, message):
        """
        Prints an init world message - refer to the GCS docs.
        These messages are sent to all clients.
        """
        object_info = message["updated_objects"]
        current_message = {"deleted_objects": [], "updated_objects": {}}

        for key, value in object_info.items():
            if len(current_message["updated_objects"]) == 100:
                self.post_message_with_delay(current_message)
                current_message = {"deleted_objects": [], "updated_objects": {}}
            current_message["updated_objects"][key] = value

        if len(current_message["updated_objects"]) > 0:
            self.post_message_with_delay(current_message)

    def post_message_with_delay(
        self,
        message: str,
    ):
        json_message = json.dumps({"": message}, separators=(",", ":"))
        print(json_message, flush=True)
        print(0.1, flush=True)  # GCS expects timeout time for all messages
        sleep(0.1)
        logging.info(json_message)
        logging.info(0.1)

    def terminate_init_world_sequence(self):
        print('"END_INIT"', flush=True)
        sleep(0.1)
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
        logging.info('"END"')
