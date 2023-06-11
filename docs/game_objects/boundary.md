# Boundary

There are two types of boundaries in the game.

* Game boundary
* Closing boundary

The **game boundary** constitutes four walls that encapsulate the map. The **closing boundary** are four walls that will
slowly close and make the map smaller. Battle Royale style!

## Data

The data that you will be given about each boundary is as follows:

```json
"boundary-id": {
    "type": 6, 
    "position": [
        [1.50, 998.5],
        [1.50, 1.50],
        [1798.5, 1.50],
        [1798.5, 998.5]
    ], 
    "velocity": [
        [10.0, 0.0],
        [0.0, 10.0],
        [-10.0, 0.0],
        [0.0, -10.0]
    ]
}
```

* `type`: The type for game boundary would be `5` and the type of closing boundary would be `6`. For more information on
types please refer to [Types](../game_logic/types.md).

* `position`: Unlike other objects in the game, the boundary will have a json array as its position value with 4
elements. Each of those 4 elements will be another json array containing the position of each of the vertex of the
boundary. For more information on the map, please refer to [Map](../game_logic/map.md).

* `velocity`: Similar to the position field, this will be a json array with 4 elements where each element is the
velocity of its corresponding wall of the boundary. (i.e. `[x_speed, y_speed]`). Please note that the velocity for game
boundary will always be zero.

* Where `boundary-id` is mentioned, this will be replace with the id of this boundary.
