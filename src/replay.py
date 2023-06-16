from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    BULLET_DESTROYED = "BULLET_DESTROYED"
    TANK_DESTROYED = "TANK_DESTROYED"
    WALL_DESTROYED = "WALL_DESTROYED"
    POWERUP_COLLECTED = "POWERUP_COLLECTED"


@dataclass
class Event:
    """
    Single use event data to be used in replays.
    Data should be a json-serializable object
    """

    event_type: EventType
    data: dict = field(default_factory=dict)

    @classmethod
    def tank_destroyed(cls, tank_id: str):
        return Event(EventType.TANK_DESTROYED, {"id": tank_id})

    @classmethod
    def wall_destroyed(cls, wall_id: str):
        return Event(EventType.WALL_DESTROYED, {"id": wall_id})

    @classmethod
    def bullet_destroyed(cls, bullet_id: str):
        return Event(
            EventType.BULLET_DESTROYED,
            {"id": bullet_id},
        )

    @classmethod
    def powerup_collected(cls, tank_id: str, powerup_id: str):
        return Event(
            EventType.POWERUP_COLLECTED,
            {
                "tank_id": tank_id,
                "powerup_id": powerup_id,
            },
        )


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

    def __init__(self, output_path: str, is_multi_file: bool) -> None:
        self.is_multi_file = is_multi_file

        # We'll use a line counter to
        self.line_counter = 1
        self.file_number = 1

        self.output_path = output_path
        self.open_file()
        self.events = []
        self.current_info = {}
        self.new_info = {}
        self.comms_info = {}

    def add_event(self, e: Event) -> None:
        self.events.append(e)

    def set_info(self, key: str, data: dict[str, Any]) -> None:
        self.new_info[key] = data

    def post_custom_replay_line(self, obj: dict) -> None:
        """
        Post a custom JSON message to replay.
        Used for initial messaging / finale
        """
        self.new_file_if_required()
        self.line_counter += 1

        self._file.write(
            json.dumps(obj, cls=ReplayJSONEncoder, separators=(",", ":")) + "\n"
        )

    def set_game_info(self, space):
        for x in space.shapes:
            self.set_info(
                x._gameobject.id,
                x._gameobject.info(),
            )

    def create_file_name(self):
        return f"{self.output_path}-{self.file_number}.txt"

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
            "deleted_objects": list(map(asdict, self.events)) if include_events else [],
            "updated_objects": updated_info,
        }
        self._file.write(
            json.dumps(obj, cls=ReplayJSONEncoder, separators=(",", ":")) + "\n"
        )

        # Update stale locations
        self.current_info.update(updated_info)
        self.new_info = {}

    def get_comms_line(self):
        comms_updated_info = {}
        for key in self.new_info:
            if self.comms_info.get(key, None) != self.new_info[key]:
                comms_updated_info[key] = self.new_info[key]
        comms_obj = {
            "deleted_objects": list(map(asdict, self.events)),
            "updated_objects": comms_updated_info,
        }

        # Clear events and update all objects' info
        self.comms_info.update(comms_updated_info)
        self.events = []
        self.new_info = {}

        return comms_obj

    def open_file(self):
        self._file = open(self.create_file_name(), "w")

    def close(self):
        self._file.close()
