from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum, auto
from typing import Any

class EventType(Enum):

    BULLET_SPAWN = auto()
    BULLET_DESTROYED = auto()
    TANK_HEALTH_LOSS = auto()
    TANK_DESTROYED = auto()
    POWERUP_SPAWN = auto()


@dataclass
class Event:
    """
    Single use event data to be used in replays.
    Data should be a json-serializable object
    """

    event_type: EventType
    data: dict = field(default_factory=dict)

    @classmethod
    def bullet_spawn(cls, player_index: int, position: tuple[float, float], rotation: float):
        return Event(EventType.BULLET_SPAWN, {
            "player_index": player_index,
            "position": position,
            "rotation": rotation,
        })

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

    def __init__(self, output_path: str) -> None:
        self.output_path = output_path
        self._file = open(output_path, "w")
        self.events = []
        self.current_info = {}
        self.new_info = {}

    def add_event(self, e: Event) -> None:
        self.events.append(e)

    def set_info(self, key: str, data: dict[str, Any]) -> None:
        self.new_info[key] = data

    def post_custom_replay_line(self, obj: dict) -> None:
        """
        Post a custom JSON message to replay.
        Used for initial messaging / finale
        """
        self._file.write(json.dumps(obj, cls=ReplayJSONEncoder) + "\n")

    def post_replay_line(self) -> dict:
        updated_info = {}
        for key in self.new_info:
            if self.current_info.get(key, None) != self.new_info[key]:
                updated_info[key] = self.new_info[key]

        obj = {
            "events": list(map(asdict, self.events)),
            "object_info": updated_info,
        }
        self._file.write(json.dumps(obj, cls=ReplayJSONEncoder) + "\n")

        # Clear events and update stale locations
        self.current_info.update(self.new_info)
        self.events = []
        return obj

    def close(self):
        self._file.close()
