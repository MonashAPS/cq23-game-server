# Powerup

Powerups can be collected by moving to their position with your tank.

## Types

There are three different types of powerups.

* **Health Boost**: increases the hp of your tank by `2` points
* **Speed Boost**: doubles the speed of your tank
* **Damage Boost**: doubles the damage of your bullets

## Data

The data that you will be given about each powerup is as follows:

```json
{
    "type": 7,
    "position": [356.12, 534.39],
    "hp": "inf",
}
```

* type: The type refers to what type of game object this is. For example, all the tanks will have `"type": 1`. For more information on types please refer to [Types](types.md)

* position: This refers to the position of this object on the game map. For more information on the map, please refer to [Map](map.md)

* hp: This is the health points of this object. The health points of powerups would generally be `"inf"` indicating that you cannot destroy them by shooting at them.
