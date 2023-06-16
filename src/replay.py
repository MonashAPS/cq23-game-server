from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any


class ReplayJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        elif isinstance(o, float):
            return f"{o:.4f}"
        return super().default(o)


class ReplayManager:
    """
    Manager for posting replays to a file.
    Replay format is a file where each line contains a JSON object.
    Each json object is either a custom message, or a tick update, containing events and updated information.

    Be sure to execute instance.close() once you are certain no more replays will be passed through.
    """

    def __init__(
        self, output_path: str, live_replay_path: str, is_multi_file: bool
    ) -> None:
        self.is_multi_file = is_multi_file

        # We'll use a line counter to
        self.line_counter = 1
        self.file_number = 1

        self.output_path = output_path
        self.live_replay_path = live_replay_path

        self.open_file()

        self.events = []
        self.current_info = {}
        self.new_info = {}
        self.comms_info = {}

    def add_event(self, id) -> None:
        self.events.append(id)

    def set_info(self, key: str, data: dict[str, Any]) -> None:
        self.new_info[key] = data

    def post_custom_replay_line(self, obj: dict) -> None:
        """
        Post a custom JSON message to replay.
        Used for initial messaging / finale
        """
        self.new_file_if_required()
        self.line_counter += 1

        self.write_to_file(obj)

    def set_game_info(self, space):
        for x in space.shapes:
            self.set_info(
                x._gameobject.id,
                x._gameobject.info(),
            )

    def create_file_names(self):
        return (
            f"{self.output_path}-{self.file_number}.txt",
            f"{self.live_replay_path}-{self.file_number}.txt",
        )

    def new_file_if_required(self):
        if self.is_multi_file and self.line_counter % 50 == 0:
            self.close()
            self.file_number += 1
            self.open_file()

    def post_replay_line(self, include_events=False) -> dict:
        self.new_file_if_required()
        self.line_counter += 1

        updated_info = {}
        for key in self.new_info:
            if self.current_info.get(key, None) != self.new_info[key]:
                updated_info[key] = self.new_info[key]

        obj = {
            "deleted_objects": self.events if include_events else [],
            "updated_objects": updated_info,
        }

        self.write_to_file(obj)

        # Update stale locations
        self.current_info.update(updated_info)
        self.new_info = {}

    def get_comms_line(self):
        comms_updated_info = {}
        for key in self.new_info:
            if self.comms_info.get(key, None) != self.new_info[key]:
                comms_updated_info[key] = self.new_info[key]
        comms_obj = {
            "deleted_objects": self.events,
            "updated_objects": comms_updated_info,
        }

        # Clear events and update all objects' info
        self.comms_info.update(comms_updated_info)
        self.events = []
        self.new_info = {}

        return comms_obj

    def write_to_file(self, obj):
        for file in (self._file, self._live_file):
            file.write(
                json.dumps(obj, cls=ReplayJSONEncoder, separators=(",", ":")) + "\n"
            )

    def open_file(self):
        file_names = self.create_file_names()
        self._file = open(file_names[0], "w")
        self._live_file = open(file_names[1], "w")

    def close(self):
        # print end of file before closing file
        self.write_to_file("EOF")

        self._file.close()
        self._live_file.close()
