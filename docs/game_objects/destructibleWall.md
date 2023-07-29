# Destructible Wall

A destructible wall is exactly like a normal wall: a square block with a constant height and width of 18. The only
difference is that you can destroy destructible walls by shooting at them.

## Data

The data that you will be given about each destructible wall is as follows:

```json
"destructibleWall-id": {
    "type": 4,
    "position": [356.12, 534.39],
    "hp": 1
}
```

* type: The type refers to what type of game object this is. This will always be `4` for destructible walls.
For more information on types please refer to [Types](../game_logic/types.md).

* position: This refers to the position of this wall block on the game map.
For more information on the map and object blocks, please refer to [Map](../game_logic/map.md).

* hp: The health points of destructible walls would generally be `1` indicating that they will be destroyed with one bullet.

* `destructibleWall-id` is the id of this wall.
