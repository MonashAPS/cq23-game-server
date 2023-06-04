# Powerup

Powerups can be collected by moving to their position with your tank.

Note that you can only collect powerups, you cannot shoot them.

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

* powerup_type: This indicates the type of this powerup. This will be one of three values: `"HEALTH"`, `"SPEED"`, `"DAMAGE"`.
