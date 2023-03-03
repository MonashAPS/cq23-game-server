import json

from config import config


class communicator:
    def __init__(self):
        self.timeout = config.COMMUNICATION.TIMEOUT
        self.client_info = self.get_message()["clients"]

    def post_message(
        self,
        message: str,
        client_id: str = "",
    ):
        print(json.dumps({client_id: message}))
        print(self.timeout)

    def get_message(self):
        return json.loads(input())

    def terminate_game(self):
        print("END")
