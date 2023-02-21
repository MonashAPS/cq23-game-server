from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum, auto

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
    Each json object is either a custom message, or a tick update, containing events and updated locations.

    Be sure to execute instance.close() once you are certain no more replays will be passed through.
    """

    def __init__(self, output_path: str) -> None:
        self.output_path = output_path
        self._file = open(output_path, "w")
        self.events = []
        self.current_locations = {}
        self.new_locations = {}

    def add_event(self, e: Event) -> None:
        self.events.append(e)

    def set_location(self, key: str, position: tuple[float, float]) -> None:
        self.new_locations[key] = position

    def post_custom_replay_line(self, obj: dict) -> None:
        """
        Post a custom JSON message to replay.
        Used for initial messaging / finale
        """
        self._file.write(json.dumps(obj, cls=ReplayJSONEncoder) + "\n")

    def post_replay_line(self) -> dict:
        updated_locations = {}
        for key in self.new_locations:
            if self.current_locations.get(key, None) != self.new_locations[key]:
                updated_locations[key] = self.new_locations[key]

        obj = {
            "events": list(map(asdict, self.events)),
            "locations": updated_locations,
        }
        self._file.write(json.dumps(obj, cls=ReplayJSONEncoder) + "\n")

        # Clear events and update stale locations
        self.current_locations.update(self.new_locations)
        self.events = []
        return obj

    def close(self):
        self._file.close()
