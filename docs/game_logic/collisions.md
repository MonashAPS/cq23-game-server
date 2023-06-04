# Collisions

The collision behaviour for different objects are quite different in this game. Each object reacts differently to
other objects. You can see a summary of these below.

## Collision Table

- Damage: damage is dealt to the objects after collision.
- None: the objects do NOT collide.
- Collide: the objects collide but nothing happens to either of them.
- Collect: special case for powerups - when they collide, they're collected by the tanks.

|                   |  Tank   | Bullet  |  Wall   | Destructible Wall | Boundary | Powerup |
|-------------------|:-------:|:-------:|:-------:|:-----------------:|:--------:|:-------:|
| Tank              | collide | damage  | collide |      collide      |  damage  | collect |
| Bullet            | damage  | damage  | damage  |      damage       | collide  |  None   |
| Wall              | collide | damage  |  None   |       None        |   None   |  None   |
| Destructible Wall | collide | damage  |  None   |       None        |   None   |  None   |
| Boundary          | damage  | collide |  None   |       None        |   None   |  None   |
| Powerup           | collect |  None   |  None   |       None        |   None   |  None   |
