# Wall

A wall is always a square block with a constant height and width of 20.

## Data

The data that you will be given about each wall is as follows:

```json
"wall-id": {
    "type": 3,
    "position": [356.12, 534.39]
}
```

* type: The type refers to what type of game object this is. All the walls will have `"type": 3`.
For more information on types please refer to [Types](../game_logic/types.md).

* position: This refers to the position of this wall on the game map. This coordinate refers to the wall's centre.
For more information on the map, please refer to [Map](../game_logic/map.md).

* `wall-id` is the id of this wall.
