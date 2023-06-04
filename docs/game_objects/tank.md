# Tank

This is the game object that you will be controlling.

## Data

The data that you will be given about each tank is as follows:

```json
"tank_id": {
    "type": 1,
    "position": [356.12, 534.39],
    "velocity": [-100.0, -100.0],
    "hp": 10
}
```

* `type`: The type refers to what type of game object this is. For example, all the tanks will have `"type": 1`.
For more information on types please refer to [Types](../game_logic/types.md).

* `position`: This refers to the position of this tank on the game map. For more information on the map, please refer
to [Map](../game_logic/map.md).

* `velocity`: This is the directional velocity of this tank (i.e. `[x_speed, y_speed]`). Refer to
[Map](../game_logic/map.md) if you're not sure how the directions work.

* `hp`: This is the health points of this tank. This would be useful for knowing the health of the enemy tanks.

* `tank-id`: The tank id shown above would be your client-id with a "tank" suffix. So if your client-id is "tanksters" then your tank id will be `tanksters-tank`.
