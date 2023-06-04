# Powerup

Powerups can be collected by moving to their position with your tank.

## Types

There are three different types of powerups.

* **Health Boost**: increases the hp of your tank by `2` points.
* **Speed Boost**: doubles the speed of your tank.
* **Damage Boost**: doubles the damage of your bullets.

## Data

The data that you will be given about each powerup is as follows:

```json
{
    "type": 7,
    "position": [356.12, 534.39],
    "powerup_type": "HEALTH"
}
```

* type: The type refers to what type of game object this is. Powerups will always have type = `7`.
For more information on types please refer to [Types](../game_logic/types.md).

* position: This refers to the position of this powerup on the game map.
For more information on the map, please refer to [Map](../game_logic/map.md).

* hp: This is the health points of this powerup. The health points of powerups would generally be `"inf"` indicating
that you cannot destroy them by shooting at them. TODO: Should we remove the hp if it's always inf? we can just say here
you can't destroy powerups. It kinda goes without saying.

* powerup_type: This indicates the type of this powerup. This will be one of three values: `"HEALTH"`, `"SPEED"`, `"DAMAGE"`.
