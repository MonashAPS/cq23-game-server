# Deleted Objects

Deleted objects is the part of the message that contains all the game objects that have been deleted.

## Deleted Object Types

The following items are the types of deleted objects that you will receive as part of the json message from the game server.

You can also see the information that you will receive with each event type below.

### BULLET_DESTROYED

```json
{
    "id": "bullet_id",
}
```

### TANK_DESTROYED

```json
{
    "id": "tank_id",
}
```

### WALL_DESTROYED

```json
{
    "id": "wall_id",
}
```

### POWERUP_COLLECTED

```json
{
    "tank_id": "tank_id",
    "powerup_id": "powerup_id",
}
```

## Example event message

```json
{
  "deleted_objects": [
    {
      "event_type": "POWERUP_COLLECTED",
      "data": {
        "id": "bullet-3",
        "tank_id": "tank-1",
      }
    },
    {
      "event_type": "WALL_DESTROYED",
      "data": {
        "id": "wall-10",
        "position": [
          640,
          780
        ]
      }
    }
  ],
  "updated_objects": {...}
}
```
