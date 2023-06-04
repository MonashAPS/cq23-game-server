# Actions

The game consists of some actions that the players (tanks) can take at every turn. The action space for this game is
quite simple: the players can shoot, move, or do both during their turn.

## Format

You will decide what action you'd like to take by printing a json object in the standard output. For example, if you
wanted to shoot, you would do the following in python:

```python
import json

my_action = {
    "shoot": 31
}

print(json.dumps(my_action))
```

It's important to always print your messages as JSON objects.

## Shoot

The `shoot` action takes an angle in degrees as its argument. This angle will determine the direction at which the tank
will shoot.

For example, if you wanted to shoot in the "top-right" direction, you would post `{"shoot": 45}` to the standard output.

Refer to the diagram below for more information on what the angle means visually.

![Screenshot](../img/actionShootDegrees.png)

The angles start from `0 degress` being a straight line to the right, `90 degress` being a straight line up, `180 degress`
being a straight line to the left and `270 degrees` a straight line down from where the tank is. You may use any angle
between 0 and 360. TODO: Is this checked in the game server? What happens if they say 8245 degrees?

## Path

The `path` action takes a coordinate point on the map and the game server will figure out a route for your tank to get
to that coordinate point. This action is convenient for those who want to travel to other points in the map without
having to figure out the path themselves.

You only have to specify your destination coordinate point once. For example, you should **NOT** do the following:

- tick 1: `{"path": [100,100]}`
- tick 2: `{"path": [100,100]}`
- tick 3: `{"path": [100,100]}`

Instead, you can specify your target once and the server will remember where you want to go. You can also easily change
your destination target if you decide to by calling the same action:

- tick 1: `{"path": [100,100]}`
- tick 2: `{}`
- tick 3: `{}`
- tick 4: `{"path": [250,300]}`

In the example above, the client initially chose to travel to the coordinate point `[100,100]`, then the client took no
action for 2 ticks and in the 4th tick they decided to interrupt their previous journey, change their destination and
go to `[250,300]`. This is a valid set of events.
