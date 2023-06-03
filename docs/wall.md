# Wall

A wall is always a square block with a constant height and width of 20.

## Data

The data that you will be given about each wall is as follows:

```json
{
    "type": 3,
    "position": [356.12, 534.39],
}
```

* type: The type refers to what type of game object this is. For example, all the tanks will have `"type": 1`. For more information on types please refer to [Types](types.md)

* position: This refers to the position of this object on the game map. In the case of walls, this coordinate refers to the wall's bottom left vertex. For more information on the map, please refer to [Map](map.md)
