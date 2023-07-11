# Bullet

## Data

The data that you will be given about each bullet is as follows:

```json
"bullet-id": {
    "type": 2,
    "tank_id": "tank-2",
    "position": [356.12, 534.39],
    "velocity": [-100.0, -100.0],
    "damage": 1
}
```

* `type`: The type refers to what type of game object this is. It will always be `2` for bullets.
For more information on types please refer to [Types](../game_logic/types.md).

* `tank_id`: Shows which tank has shot this bullet. If the id here is yours, this is your bullet otherwise it's your opponent's.
Note that you will still take damage from your own bullets. Avoid them!

* `position`: This refers to the position of this bullet on the game map. For more information on the map and position,
please refer to [Map](../game_logic/map.md).

* `velocity`: This is the directional velocity of this bullet (i.e. `[x_speed, y_speed]`).

* `damage`: This is how much damage this particular bullet will deal. This value can change if a tank collects a powerup.

* `bullet-id` is the id of this bullet.
