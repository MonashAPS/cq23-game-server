from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from log import log_with_time


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

        self.file_number = 1

        self.output_path = output_path
        self.live_replay_path = live_replay_path

        # Buffer is the list of all lines that are waiting to be written in the replay file
        self.buffer = []

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
        log_with_time("-> post_custom_replay_line")
        self.write_to_buffer(obj)

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

    def post_replay_line(self, include_events=False) -> dict:
        log_with_time("-> post_replay_line")
        updated_info = {}
        for key in self.new_info:
            if self.current_info.get(key, None) != self.new_info[key]:
                updated_info[key] = self.new_info[key]

        obj = {
            "deleted_objects": self.events if include_events else [],
            "updated_objects": updated_info,
        }

        self.write_to_buffer(obj)

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

    def write_to_buffer(self, obj):
        serialized_obj = json.dumps(obj, cls=ReplayJSONEncoder, separators=(",", ":"))
        self.buffer.append(serialized_obj + "\n")

        # Flush buffer if it's gotten too big (more than 50 lines of each 500 characters)
        if self.is_multi_file and sum([len(x) for x in self.buffer]) >= 50 * 500:
            self.empty_buffer()

    def empty_buffer(self):
        log_with_time("-> empty_buffer")
        # Add EOF to buffer before flushing it out
        self.buffer.append('"EOF"\n')

        file_names = self.create_file_names()
        for file_name in file_names:
            with open(file_name, "w") as f:
                f.writelines(self.buffer)

        self.buffer = []
        self.file_number += 1
        log_with_time("<- empty_buffer")
