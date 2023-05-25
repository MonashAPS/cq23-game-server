# Collisions

The collision behaviour for different objects are quite different in this game. Each object reacts differently to other objects and you can see a summary of these below.

## Tank

Tanks collide with other tanks, walls, destructible walls, bullets and the boundaries.
Tanks will receive damage from colliding with bullets and the closing boundary.

## Collision Table

|                   | Tank    | Bullet   | Wall   | Destructible Wall | Boundary   | Powerup |
| ----------------- | :-----: | :------: | :----: | :---------------: | :--------: | :-----: |
| Tank              | collide | damage   | collide| collide           | damage     | collect |
| Bullet            | damage  | damage   | damage | damage            | collide    | None    |
| Wall              | collide | damage   | None   | None              | None       | None    |
| Destructible Wall | collide | damage   | None   | None              | None       | None    |
|  Boundary         | damage  | collide  | None   | None              | None       | None    |
| Powerup           | collect | None     | None   | None              | None       | None    |
