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

        self.file_number = 1

        self.output_path = output_path
        self.live_replay_path = live_replay_path

        # Buffer is the list of all lines that are waiting to be written in the replay file
        self.buffer = []

        self.events = []
        self.current_info = {}
        self.new_info = {}
        self.comms_info = {}

        # The last state of all objects in the game - used for diffing
        self.replay_current_object_states = {}
        # List of objects that are updated and are waiting to be written
        self.replay_pending_object_updates = {}
        # List of object ids that were deleted and are waiting to be written
        self.replay_pending_object_deletes = []

        # This logic needs to happen twice - one for writing replay lines, one for writing client messages.
        # The objects below are used for client messages.
        self.comms_current_object_states = {}
        self.comms_pending_object_updates = {}
        self.comms_pending_object_deletes = []

    def record_deleted_object(self, deleted_object_id):
        self.replay_pending_object_deletes.append(deleted_object_id)
        self.comms_pending_object_deletes.append(deleted_object_id)

    def record_object_state(self, object_id: str, object_data: dict[str, Any]):
        self.replay_pending_object_updates[object_id] = object_data
        self.comms_pending_object_updates[object_id] = object_data

    def empty_buffer(self):
        # Add EOF to buffer before flushing it out
        self.buffer.append('"EOF"\n')

        file_names = (
            f"{self.output_path}-{self.file_number}.txt",
            f"{self.live_replay_path}-{self.file_number}.txt",
        )
        for file_name in file_names:
            with open(file_name, "w") as f:
                f.writelines(self.buffer)

        self.buffer = []
        self.file_number += 1

    def write_to_buffer(self, obj):
        serialized_obj = json.dumps(obj, cls=ReplayJSONEncoder, separators=(",", ":"))
        self.buffer.append(serialized_obj + "\n")

        # Flush buffer if it's gotten too big (more than 50 lines of each 500 characters)
        if self.is_multi_file and sum([len(x) for x in self.buffer]) >= 50 * 500:
            self.empty_buffer()

    def post_custom_replay_line(self, obj: dict) -> None:
        """
        Post a custom JSON message to replay.
        Used for initial messaging / finale
        """
        self.write_to_buffer(obj)

    def set_game_info(self, space):
        for x in space.shapes:
            self.record_object_state(
                x._gameobject.id,
                x._gameobject.info(),
            )

    def _find_object_diffs(self, current_state, new_updates):
        changed_objects = {}
        for object_id in new_updates:
            if current_state.get(object_id) != new_updates[object_id]:
                changed_objects[object_id] = new_updates[object_id]

        return changed_objects

    def _remove_pending_deletes(pending_object_deletes, object_states):
        for pending_object_delete_key in pending_object_deletes:
            try:
                del object_states[pending_object_delete_key]
            except KeyError:
                pass

    def sync_object_updates_in_replay(self):
        pending_object_updates = self._find_object_diffs(
            self.replay_current_object_states, self.replay_pending_object_updates
        )

        message = {
            "deleted_objects": self.replay_pending_object_deletes,
            "updated_objects": pending_object_updates,
        }

        self.write_to_buffer(message)

        # Update stale locations
        self.replay_current_object_states.update(pending_object_updates)
        self.replay_pending_object_updates = {}

        self._remove_pending_deletes(
            self.replay_pending_object_deletes, self.replay_current_object_states
        )
        self.replay_pending_object_deletes = []

    def sync_object_updates_in_comms(self):
        pending_object_updates = self._find_object_diffs(
            self.comms_current_object_states, self.comms_pending_object_updates
        )

        message = {
            "deleted_objects": self.comms_pending_object_deletes,
            "updated_objects": pending_object_updates,
        }

        # Clear events and update all objects' info
        self.comms_current_object_states.update(pending_object_updates)
        self.comms_pending_object_updates = {}

        self._remove_pending_deletes(
            self.comms_pending_object_deletes, self.comms_current_object_states
        )
        self.comms_pending_object_deletes = []

        return message
