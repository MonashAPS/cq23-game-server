# Wall

## Data

The data that you will be given about each wall is as follows:

```json
{
    "type": 3,
    "position": [356.12, 534.39],
    "velocity": [0.0, 0.0],
    "hp": "inf",
}
```

* type: The type refers to what type of game object this is. For example, all the tanks will have `"type": 1`. For more information on types please refer to [Types](types.md)

* position: This refers to the position of this object on the game map. For more information on the map, please refer to [Map](map.md)

* velocity: This is the directional velocity of this object. (i.e. `[x_speed, y_speed]`)

* hp: This is the health points of this object. The health points of walls would generally be `"inf"` indicating that they are NOT destructible
