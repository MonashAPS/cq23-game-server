# Events

Events are whatever happens in the game that's worth knowing. If a wall is destroyed, if a powerup is spawned,
if the enemy tanks fires a bullet. You want to know all of those things, so we will let you know when they happen with
an event.

## Event types

The following items are the events that you will receive as part of the json message from the game server.

You can also see the information that you will receive with each event type below.

### BULLET_SPAWN

```json
{
    "id": "bullet_id",
    "tank_id": "tank_id",
    "position": [x, y],
    "velocity": "velocity",
    "angle": "angle"
}
```

### BULLET_DESTROYED

```json
{
    "id": "bullet_id",
    "position": [x, y]
}
```

### TANK_HEALTH_LOSS

```json
{
    "id": "tank_id",
    "position": [x, y]
}
```

### TANK_DESTROYED

```json
{
    "id": "tank_id",
    "position": [x, y]
}
```

### WALL_HEALTH_LOSS

```json
{
    "id": "wall_id",
    "position": [x, y]
}
```

### WALL_DESTROYED

```json
{
    "id": "wall_id",
    "position": [x, y]
}
```

### POWERUP_SPAWN

```json
{
    "position": [x, y],
    "powerup_id": "powerup_id",
    "powerup_type": "powerup_type"
}
```

### POWERUP_COLLECTED

```json
{
    "tank_id": "tank_id",
    "position": [x, y],
    "powerup_id": "powerup_id",
    "powerup_type": "powerup_type"
}
```

## Example event message

```json
{
  "events": [
    {
      "event_type": "BULLET_SPAWN",
      "data": {
        "id": "bullet-3",
        "tank_id": "tank-1",
        "position": [
          660.90,
          839.35
        ],
        "velocity": [
          -449.71,
          -15.92
        ],
        "angle": 37
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
  "object_info": {...}
}
```
